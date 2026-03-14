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