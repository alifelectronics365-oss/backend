import random
from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from apps.customer.models.account import User
from apps.kobutor.email import send_reset_password_otp_email

class ForgotPasswordRequestSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField()

    def validate(self, attrs):
        email_or_phone = attrs['email_or_phone']
        try:
            user = User.objects.get(email_or_phone=email_or_phone)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")

        attrs["user"] = user
        return attrs

    def save(self):
        user = self.validated_data["user"]
        otp = str(random.randint(100000, 999999))

        user.reset_otp = otp
        user.reset_otp_created_at = timezone.now()
        user.save()

        # TODO: Send OTP via email or SMS
        print("OTP:", otp)
        send_reset_password_otp_email(user, otp)   # for testing

        return {"message": "OTP sent successfully"}
        

class VerifyOTPSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField()
    otp = serializers.CharField(max_length=6)

    def validate(self, attrs):
        email_or_phone = attrs['email_or_phone']
        otp = attrs['otp']

        try:
            user = User.objects.get(email_or_phone=email_or_phone)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")

        # Check OTP
        if user.reset_otp != otp:
            raise serializers.ValidationError("Invalid OTP")

        # Check expiry (10 minutes)
        if user.reset_otp_created_at < timezone.now() - timedelta(minutes=10):
            raise serializers.ValidationError("OTP expired")

        attrs["user"] = user
        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True, min_length=6)

    def validate(self, attrs):
        email_or_phone = attrs['email_or_phone']
        otp = attrs['otp']

        try:
            user = User.objects.get(email_or_phone=email_or_phone)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")

        if user.reset_otp != otp:
            raise serializers.ValidationError("Invalid OTP")

        attrs["user"] = user
        return attrs

    def save(self):
        user = self.validated_data["user"]
        user.set_password(self.validated_data["new_password"])

        # clear OTP
        user.reset_otp = None
        user.reset_otp_created_at = None

        user.save()
        return {"message": "Password reset successfully"}
