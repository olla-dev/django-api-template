from rest_framework import generics, authentication, permissions
from users.serializers import UserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from users.serializers import AuthTokenSerializer

class CreateUserView(generics.CreateAPIView):
    """ Creates a new user """
    serializer_class = UserSerializer

class CreateAuthTokenView(ObtainAuthToken):
    """ Generate an authtoken for a user """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManagerUserView(generics.RetrieveAPIView):
    """Manage the authenticated user"""
    serializer_class= UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user