from rest_framework import serializers
from .models import Users


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ['name','email','password','role']


    def create(self, validated_data):

        password = validated_data.pop('password')

        user = Users.objects.create(
            password_hash=password,
            **validated_data
        )

        return user


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField()

class RequestOtpSerializer(serializers.Serializer):

    email = serializers.EmailField()


class ConfirmOtpSerializer(serializers.Serializer):

    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField()