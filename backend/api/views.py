from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Users
from .serializers import RegisterSerializer, LoginSerializer
import random
from datetime import timedelta
from django.utils import timezone
from .models import Users, PasswordResetOtp
from django.db.models import Count
from .models import Receipts, Deliveries
from .models import Products, Receipts, ReceiptItems, Deliveries, DeliveryItems, InventoryStock, StockLedger
from django.db import connection, transaction

@api_view(['POST'])
def register(request):

    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():

        serializer.save()

        return Response({"message":"user created"})


    return Response(serializer.errors)


@api_view(['POST'])
def login(request):

    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:

            user = Users.objects.get(email=email)

            if user.password_hash == password:

                return Response({
                    "message":"login success",
                    "user_id":user.id,
                    "role":user.role
                })

            else:
                return Response({"error":"invalid password"})

        except Users.DoesNotExist:

            return Response({"error":"user not found"})

    return Response(serializer.errors)

@api_view(['POST'])
def request_password_reset(request):

    email = request.data.get("email")

    try:
        user = Users.objects.get(email=email)

        otp = str(random.randint(100000, 999999))

        PasswordResetOtp.objects.create(
            user=user,
            otp_code=otp,
            expires_at=timezone.now() + timedelta(minutes=5)
        )

        return Response({
            "message": "OTP generated",
            "otp": otp
        })

    except Users.DoesNotExist:
        return Response({"error": "user not found"})


@api_view(['POST'])
def confirm_password_reset(request):

    email = request.data.get("email")
    otp = request.data.get("otp")
    new_password = request.data.get("new_password")

    try:
        user = Users.objects.get(email=email)

        record = PasswordResetOtp.objects.get(user=user, otp_code=otp)

        if record.expires_at < timezone.now().replace(tzinfo=None):
            return Response({"error": "OTP expired"})

        user.password_hash = new_password
        user.save()

        record.delete()

        return Response({"message": "password updated"})

    except PasswordResetOtp.DoesNotExist:
        return Response({"error": "invalid OTP"})

@api_view(['GET'])
def dashboard_summary(request):

    receipts_to_receive = Receipts.objects.filter(status="pending").count()

    total_receipts = Receipts.objects.count()

    deliveries_to_deliver = Deliveries.objects.filter(status="pending").count()

    total_deliveries = Deliveries.objects.count()

    return Response({
        "receipts": {
            "to_receive": receipts_to_receive,
            "total_operations": total_receipts
        },
        "deliveries": {
            "to_deliver": deliveries_to_deliver,
            "total_operations": total_deliveries
        }
    })

@api_view(['POST'])
def create_product(request):

    category_id = request.data.get("category_id")
    unit_id = request.data.get("unit_id")

    from django.db import connection

    with connection.cursor() as cursor:

        cursor.execute(
            "INSERT INTO product_categories (id,name,description) VALUES (%s,'Default','Auto') ON CONFLICT DO NOTHING",
            [category_id]
        )

        cursor.execute(
            "INSERT INTO units_of_measure (id,name,symbol) VALUES (%s,'Piece','pc') ON CONFLICT DO NOTHING",
            [unit_id]
        )

    product = Products.objects.create(
        name=request.data.get("name"),
        sku=request.data.get("sku"),
        category_id=category_id,
        unit_id=unit_id,
        reorder_level=request.data.get("reorder_level")
    )

    return Response({
        "message": "product created",
        "product_id": product.id
    })

@api_view(['POST'])
def create_receipt(request):
    """
    Demo-safe receipt creation:
    - auto-creates minimal master rows if missing
    - creates a receipts header + receipt_items
    - updates/creates inventory_stock (increases)
    - appends a stock_ledger entry
    """

    # pull request data with safe defaults for a fast demo
    supplier_name = request.data.get("supplier_name", "Demo Supplier")
    product_id = int(request.data.get("product_id") or 1)
    quantity = float(request.data.get("quantity") or 1)
    warehouse_id = int(request.data.get("warehouse_id") or 1)
    location_id = int(request.data.get("location_id") or 1)
    created_by = int(request.data.get("user_id") or 1)

    try:
        with transaction.atomic():
            with connection.cursor() as cursor:
                # ensure a demo manager user exists
                cursor.execute("""
                    INSERT INTO users (id,name,email,password_hash,role,created_at)
                    VALUES (1,'DemoAdmin','admin@demo.local','demo','manager',NOW())
                    ON CONFLICT (id) DO NOTHING;
                """)

                # ensure category & unit exist for product creation fallback
                cursor.execute("""
                    INSERT INTO product_categories (id,name,description)
                    VALUES (1,'Default','Auto created for demo')
                    ON CONFLICT (id) DO NOTHING;
                """)
                cursor.execute("""
                    INSERT INTO units_of_measure (id,name,symbol)
                    VALUES (1,'Piece','pc')
                    ON CONFLICT (id) DO NOTHING;
                """)

                # ensure product exists (if product_id not present create a demo product)
                cursor.execute("SELECT id FROM products WHERE id=%s;", [product_id])
                if cursor.fetchone() is None:
                    cursor.execute("""
                        INSERT INTO products (id,name,sku,category_id,unit_id,reorder_level,created_at)
                        VALUES (%s, 'Demo Product', 'DEMO-%s', 1, 1, 0, NOW())
                        ON CONFLICT (id) DO NOTHING;
                    """, [product_id, product_id])

                # ensure warehouse exists and has manager (manager_id NOT NULL)
                cursor.execute("""
                    INSERT INTO warehouses (id,name,address,manager_id,created_at)
                    VALUES (%s,'Main Warehouse','Demo Address',1,NOW())
                    ON CONFLICT (id) DO NOTHING;
                """, [warehouse_id])

                # ensure location exists
                cursor.execute("""
                    INSERT INTO locations (id,warehouse_id,name,type)
                    VALUES (%s,%s,'Shelf A1','storage')
                    ON CONFLICT (id) DO NOTHING;
                """, [location_id, warehouse_id])

                # create receipt header and get its id
                cursor.execute("""
                    INSERT INTO receipts (supplier_name,warehouse_id,status,created_by,created_at)
                    VALUES (%s,%s,'completed',%s,NOW())
                    RETURNING id;
                """, [supplier_name, warehouse_id, created_by])
                receipt_id = cursor.fetchone()[0]

                # create receipt item
                cursor.execute("""
                    INSERT INTO receipt_items (receipt_id,product_id,location_id,quantity)
                    VALUES (%s,%s,%s,%s)
                    RETURNING id;
                """, [receipt_id, product_id, location_id, quantity])
                # update or create inventory_stock safely (select for update)
                cursor.execute("""
                    SELECT id, quantity FROM inventory_stock
                    WHERE product_id=%s AND location_id=%s
                    FOR UPDATE;
                """, [product_id, location_id])
                row = cursor.fetchone()
                if row:
                    stock_id, current_qty = row
                    new_qty = float(current_qty) + quantity
                    cursor.execute("""
                        UPDATE inventory_stock SET quantity=%s, updated_at=NOW()
                        WHERE id=%s;
                    """, [new_qty, stock_id])
                else:
                    cursor.execute("""
                        INSERT INTO inventory_stock (product_id, location_id, quantity, updated_at)
                        VALUES (%s,%s,%s,NOW())
                        RETURNING id;
                    """, [product_id, location_id, quantity])

                # append ledger entry
                cursor.execute("""
                    INSERT INTO stock_ledger (product_id, location_id, change_qty, operation_type, reference_id, created_at)
                    VALUES (%s,%s,%s,'receipt',%s,NOW());
                """, [product_id, location_id, quantity, receipt_id])

        return Response({"message": "receipt created", "receipt_id": receipt_id})

    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['POST'])
def create_delivery(request):
    """
    Demo-safe delivery creation:
    - auto-creates minimal master rows if missing
    - creates a deliveries header + delivery_items
    - updates inventory_stock (decreases)
    - appends a stock_ledger entry
    """

    customer_name = request.data.get("customer_name", "Demo Customer")
    product_id = int(request.data.get("product_id") or 1)
    quantity = float(request.data.get("quantity") or 1)
    warehouse_id = int(request.data.get("warehouse_id") or 1)
    location_id = int(request.data.get("location_id") or 1)
    try:
        with transaction.atomic():
            with connection.cursor() as cursor:
                # ensure demo master rows exist
                cursor.execute("""
                    INSERT INTO users (id,name,email,password_hash,role,created_at)
                    VALUES (1,'DemoAdmin','admin@demo.local','demo','manager',NOW())
                    ON CONFLICT (id) DO NOTHING;
                """)
                cursor.execute("""
                    INSERT INTO warehouses (id,name,address,manager_id,created_at)
                    VALUES (%s,'Main Warehouse','Demo Address',1,NOW())
                    ON CONFLICT (id) DO NOTHING;
                """, [warehouse_id])
                cursor.execute("""
                    INSERT INTO locations (id,warehouse_id,name,type)
                    VALUES (%s,%s,'Shelf A1','storage')
                    ON CONFLICT (id) DO NOTHING;
                """, [location_id, warehouse_id])

                # ensure product exists
                cursor.execute("SELECT id FROM products WHERE id=%s;", [product_id])
                if cursor.fetchone() is None:
                    cursor.execute("""
                        INSERT INTO product_categories (id,name,description)
                        VALUES (1,'Default','Auto created for demo')
                        ON CONFLICT (id) DO NOTHING;
                    """)
                    cursor.execute("""
                        INSERT INTO units_of_measure (id,name,symbol)
                        VALUES (1,'Piece','pc')
                        ON CONFLICT (id) DO NOTHING;
                    """)
                    cursor.execute("""
                        INSERT INTO products (id,name,sku,category_id,unit_id,reorder_level,created_at)
                        VALUES (%s, 'Demo Product', 'DEMO-%s', 1, 1, 0, NOW())
                        ON CONFLICT (id) DO NOTHING;
                    """, [product_id, product_id])

                # create delivery header
                cursor.execute("""
                    INSERT INTO deliveries (customer_name,warehouse_id,status,created_at)
                    VALUES (%s,%s,'completed',NOW())
                    RETURNING id;
                """, [customer_name, warehouse_id])
                delivery_id = cursor.fetchone()[0]

                # create delivery item
                cursor.execute("""
                    INSERT INTO delivery_items (delivery_id,product_id,location_id,quantity)
                    VALUES (%s,%s,%s,%s);
                """, [delivery_id, product_id, location_id, quantity])

                # update inventory_stock (decrease). Use SELECT FOR UPDATE to avoid race
                cursor.execute("""
                    SELECT id, quantity FROM inventory_stock
                    WHERE product_id=%s AND location_id=%s
                    FOR UPDATE;
                """, [product_id, location_id])
                row = cursor.fetchone()
                if row:
                    stock_id, current_qty = row
                    new_qty = float(current_qty) - quantity
                    cursor.execute("""
                        UPDATE inventory_stock SET quantity=%s, updated_at=NOW()
                        WHERE id=%s;
                    """, [new_qty, stock_id])
                else:
                    # No stock record exists — create a negative/zero-safe record (for demo)
                    cursor.execute("""
                        INSERT INTO inventory_stock (product_id, location_id, quantity, updated_at)
                        VALUES (%s,%s,%s,NOW());
                    """, [product_id, location_id, -quantity])

                # append ledger entry
                cursor.execute("""
                    INSERT INTO stock_ledger (product_id, location_id, change_qty, operation_type, reference_id, created_at)
                    VALUES (%s,%s,%s,'delivery',%s,NOW());
                """, [product_id, location_id, -quantity, delivery_id])

        return Response({"message": "delivery created", "delivery_id": delivery_id})

    except Exception as e:
        return Response({"error": str(e)}, status=500)