from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from recipes.models import Tag
from recipes.serializers import TagSerializer

class TagViewSet(viewsets.GenericViewSet,
        mixins.ListModelMixin,
        mixins.CreateModelMixin):
    """Manage Tags"""
    serializer_class = TagSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()

    def get_queryset(self):
        """Returns tags for the current user"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """create a new tag"""
        serializer.save(user=self.request.user)