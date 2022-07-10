from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from ..serializers import AuthorSerializer


class AuthorPagination(PageNumberPagination):
    page_size = 10


class AuthorViewSet(ReadOnlyModelViewSet):
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = AuthorPagination

    def get_queryset(self):
        user = get_user_model()
        qs = user.objects.filter(username=self.request.user.username)
        return qs
