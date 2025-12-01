from django.urls import path
from apps.ponno.views.home import HomeView

# Import other views similarly if needed


app_name = "ponno"  # Namespace for URL names

urlpatterns = [
    path('', HomeView, name='home'),
  
]
