from django.db import models


class Users(models.Model):

    name = models.CharField(max_length=100)

    email = models.CharField(max_length=150, unique=True)

    password_hash = models.TextField()

    role = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = "users"

class PasswordResetOtp(models.Model):

    user = models.ForeignKey('Users', on_delete=models.CASCADE)

    otp_code = models.CharField(max_length=6)

    created_at = models.DateTimeField(auto_now_add=True)

    expires_at = models.DateTimeField()

    class Meta:
        db_table = "password_reset_otp"

class Receipts(models.Model):

    supplier_name = models.CharField(max_length=150)

    warehouse_id = models.IntegerField()

    status = models.CharField(max_length=50)

    created_by = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "receipts"


class Deliveries(models.Model):

    customer_name = models.CharField(max_length=150)

    warehouse_id = models.IntegerField()

    status = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "deliveries"

class Products(models.Model):

    name = models.CharField(max_length=150)

    sku = models.CharField(max_length=100, unique=True)

    category_id = models.IntegerField()

    unit_id = models.IntegerField()

    reorder_level = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "products"


class InventoryStock(models.Model):

    product_id = models.IntegerField()

    location_id = models.IntegerField()

    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "inventory_stock"


class Receipts(models.Model):

    supplier_name = models.CharField(max_length=150)

    warehouse_id = models.IntegerField()

    status = models.CharField(max_length=50)

    created_by = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "receipts"


class ReceiptItems(models.Model):

    receipt_id = models.IntegerField()

    product_id = models.IntegerField()

    location_id = models.IntegerField()

    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "receipt_items"


class Deliveries(models.Model):

    customer_name = models.CharField(max_length=150)

    warehouse_id = models.IntegerField()

    status = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "deliveries"


class DeliveryItems(models.Model):

    delivery_id = models.IntegerField()

    product_id = models.IntegerField()

    location_id = models.IntegerField()

    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "delivery_items"


class StockLedger(models.Model):

    product_id = models.IntegerField()

    location_id = models.IntegerField()

    change_qty = models.DecimalField(max_digits=10, decimal_places=2)

    operation_type = models.CharField(max_length=50)

    reference_id = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "stock_ledger"