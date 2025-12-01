from django.urls import path
from apps.customer.views.signup import signup_view

# Import other views similarly if needed


app_name = "customer"  # Namespace for URL names

urlpatterns = [
    path('signup/', signup_view, name='signup'),
   # path('signin/', views.signin_view, name='signin'),
   # path('profile/', views.profile_view, name='profile'),
   # path('logout/', views.logout_view, name='logout'),
]
