from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from tag.models import Tag

from ..models import Recipe
from ..serializers import RecipeSerializer, TagSerializer


# ClassBasedViews
class RcipeApiV2Pagination(PageNumberPagination):
    page_size = 10


class RecipeApiV2ViewSet(ModelViewSet):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RcipeApiV2Pagination

    def get_queryset(self):
        qs = super().get_queryset()
        category_id = self.request.query_params.get('category_id', None)

        if category_id and category_id.isnumeric():
            qs = qs.filter(category_id=category_id)

        return qs


@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(
        Tag.objects.all(),
        pk=pk
    )
    serializer = TagSerializer(
        instance=tag,
        many=False,
        context={'request': request},
    )
    return Response(serializer.data)
