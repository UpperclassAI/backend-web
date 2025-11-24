from django.urls import path
from .views import RegisterAPIView, UserProfileAPIView

urlpatterns = [
    # User Registration Endpoint
    path('register/', RegisterAPIView.as_view(), name='register'),
    
    # Authenticated User Profile (GET/PUT/PATCH)
    path('user/profile/', UserProfileAPIView.as_view(), name='user-profile'),
    
    # NOTE: Login/Token generation is typically handled by a dedicated
    # package (like simplejwt) and will be added later in the project's root urls.py.
]