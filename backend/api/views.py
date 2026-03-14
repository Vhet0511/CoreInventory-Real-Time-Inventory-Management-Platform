from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Users
from .serializers import RegisterSerializer, LoginSerializer
import random
from datetime import timedelta
from django.utils import timezone
from .models import Users, PasswordResetOtp

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

