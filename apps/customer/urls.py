from django.urls import path
from apps.customer.views.signup import SignUpView
from apps.customer.views.signin import SignInView
from apps.customer.views.profile import ProfileView
from apps.customer.views.logout import LogoutView
from apps.customer.views.profile_edit import EditProfileView
from apps.customer.views.profile_settings import ProfileSettingsView
from apps.customer.views.forgot_password import ForgotPasswordView

app_name = "customer"

from django.urls import path

urlpatterns = [
    path('signup/', SignUpView, name='signup'),

    path('signin/', SignInView, name='signin'),
    path("forgot-password/", ForgotPasswordView, name="forgot-password"),
    
     # Logout URL
    path('logout/', LogoutView, name='logout'),

    path('profile/', ProfileView, name='profile'),  # <-- Add this line
    path("edit_profile/", EditProfileView, name="edit_profile"),
    path("profile_settings/", ProfileSettingsView, name="profile_settings"),

    
]
