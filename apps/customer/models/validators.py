import re
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError


# -----------------------------
#  Email Validator
# -----------------------------
email_validator = EmailValidator(
    message="Enter a valid email address."
)


# -----------------------------
#  Phone Validator
#  Accepts 7–15 digits only
# -----------------------------
phone_validator = RegexValidator(
    regex=r'^[0-9]{7,15}$',
    message="Enter a valid phone number (7–15 digits, numbers only)."
)


# -----------------------------
#  Combined Email OR Phone Validator
# -----------------------------
def email_or_phone_validator(value):
    """
    Validates that the input is either a valid email or a phone number.
    """
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    phone_regex = r"^[0-9]{7,15}$"

    if re.match(email_regex, value):  # valid email
        return value

    if re.match(phone_regex, value):  # valid phone number
        return value

    raise ValidationError(
        "Enter a valid email or phone number."
    )
