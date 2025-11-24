from rest_framework import generics, permissions
from .serializers import RegisterSerializer, UserSerializer
from .models import CustomUser

class RegisterAPIView(generics.CreateAPIView):
    """
    API endpoint for new user registration.
    
    Handles POST requests to create a new CustomUser instance.
    Uses RegisterSerializer for input validation and user creation.
    """
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny] # Anyone can register
    serializer_class = RegisterSerializer

class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for viewing and updating the authenticated user's profile.
    
    Handles GET (view) and PUT/PATCH (update) requests.
    Requires authentication (IsAuthenticated).
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        """
        Overrides get_object to return the currently authenticated user.
        """
        return self.request.user