from rest_framework import generics
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