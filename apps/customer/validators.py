import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import EmailValidator
import phonenumbers

# -------------------------------------------------------
# EMAIL VALIDATOR (Using Django built-in)
# -------------------------------------------------------
validate_email = EmailValidator(message=_("Invalid email address."))


# -------------------------------------------------------
# PHONE VALIDATOR (International using phonenumbers lib)
# -------------------------------------------------------
def validate_phone(value):
    """
    Validate international phone number.
    Accepts:
    - 017XXXXXXXX
    - +88017XXXXXXXX
    - +8801XXXXXXXXX
    """
    try:
        # If starts with 0 → assume Bangladesh
        if value.startswith("0"):
            value = "+88" + value

        # If starts with 880 → add +
        if value.startswith("880"):
            value = "+" + value

        phone = phonenumbers.parse(value, "BD")  # default region BD

        if not phonenumbers.is_valid_number(phone):
            raise ValidationError(_("Invalid phone number."))

    except phonenumbers.NumberParseException:
        raise ValidationError(_("Invalid phone number."))

    return value


# -------------------------------------------------------
# EMAIL OR PHONE VALIDATOR
# -------------------------------------------------------
def email_or_phone_validator(value):
    """
    Detect whether input is email or phone and validate accordingly.
    """
    if "@" in value:
        return validate_email(value)
    # Strict phone number pattern: optional '+' at start, then digits only
    if re.fullmatch(r"\+?\d+", value):
        return validate_phone(value)
    raise ValidationError(_("Enter a valid email or phone number."))


# -------------------------------------------------------
# STRONG PASSWORD VALIDATOR
# -------------------------------------------------------
PASS_REGEX = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
)

def strong_password_validator(value):
    """
    Password must contain at least:
    - 8 characters
    - One uppercase letter
    - One lowercase letter
    - One number
    - One special character (@$!%*?&)
    """
    if not PASS_REGEX.match(value):
        raise ValidationError(_(
            "Password must contain at least 8 characters, "
            "one uppercase letter, one lowercase letter, "
            "one number, and one special character."
        ))
    return value


# -------------------------------------------------------
# NAME VALIDATOR (Letters + spaces + . ' -)
# -------------------------------------------------------
NAME_REGEX = re.compile(r"^[A-Za-z\s.\'\-]+$")

def name_validator(value):
    if not NAME_REGEX.match(value):
        raise ValidationError(_("Name may only contain letters, spaces, and characters . ' -"))
    return value


# -------------------------------------------------------
# ONLY PHONE AND ONLY EMAIL VALIDATORS (optional)
# -------------------------------------------------------
def only_phone(value):
    return validate_phone(value)

def only_email(value):
    return validate_email(value)
