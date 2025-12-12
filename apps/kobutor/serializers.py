from rest_framework import serializers
from apps.kobutor.models.forgot_password_otp import ForgotPasswordOTP

from rest_framework import serializers
from django.contrib.auth import get_user_model

from django.utils import timezone
import random
from apps.kobutor.email import send_reset_password_otp_email
User = get_user_model()

class ForgotPasswordRequestSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField(max_length=100)

    def validate_email_or_phone(self, value):
        if not User.objects.filter(email_or_phone=value).exists():
            raise serializers.ValidationError("User not found.")
        return value

    def save(self):
        email_or_phone = self.validated_data['email_or_phone']
        user = User.objects.get(email_or_phone=email_or_phone)

        otp_code = str(random.randint(100000, 999999))

        otp_obj, created = ForgotPasswordOTP.objects.update_or_create(
            user=user,
            defaults={
                'reset_otp': otp_code,
                'reset_otp_created_at': timezone.now()
            }
        )
        # Add sending OTP logic here if needed
        send_reset_password_otp_email(user, otp_code)
        return otp_obj

from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.kobutor.models.forgot_password_otp import ForgotPasswordOTP

User = get_user_model()

class VerifyForgotPasswordOTPSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField(max_length=100)
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        email_or_phone = data['email_or_phone']
        otp = data['otp']

        # Validate user
        try:
            user = User.objects.get(email_or_phone=email_or_phone)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        # Validate OTP record
        try:
            otp_record = ForgotPasswordOTP.objects.get(user=user)
        except ForgotPasswordOTP.DoesNotExist:
            raise serializers.ValidationError("OTP not found. Please request again.")

        # Check OTP code
        if otp_record.reset_otp != otp:
            raise serializers.ValidationError("Incorrect OTP.")

        # Check OTP validity
        if not otp_record.otp_is_valid():
            raise serializers.ValidationError("OTP expired. Please request again.")

        data['user'] = user
        data['otp_record'] = otp_record
        return data

    def save(self):
        otp_record = self.validated_data['otp_record']
        # Mark OTP as used by clearing it (optional)
        otp_record.reset_otp = None
        otp_record.save()
        return self.validated_data['user']

import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.customer.validators import strong_password_validator

User = get_user_model()

class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        write_only=True,
        validators=[strong_password_validator]
    )

    def save(self):
        user = self.context.get('user')
        new_password = self.validated_data['new_password']

        user.set_password(new_password)
        user.save()
        return user
