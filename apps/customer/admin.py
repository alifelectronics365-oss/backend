from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from apps.customer.models.account import User


# -------------------------
# Custom User Creation Form
# -------------------------
class UserCreationForm(forms.ModelForm):
    """
    Form used in Django Admin to create new users.
    """
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email_or_phone", "role")

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# -------------------------
# Custom User Change Form
# -------------------------
class UserChangeForm(forms.ModelForm):
    """
    Form used in Django Admin to update existing users.
    """
    class Meta:
        model = User
        fields = "__all__"


# -------------------------
# Custom User Admin
# -------------------------
class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User

    list_display = ("id", "email_or_phone", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")

    readonly_fields = ("last_login", "date_joined")

    fieldsets = (
        (None, {"fields": ("email_or_phone", "password")}),
        ("Roles", {"fields": ("role",)}),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email_or_phone",
                "role",
                "password1",
                "password2",
                "is_staff",
                "is_active",
            ),
        }),
    )

    search_fields = ("email_or_phone",)
    ordering = ("email_or_phone",)


# Register the custom user admin
admin.site.register(User, CustomUserAdmin)
