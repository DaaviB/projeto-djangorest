from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from tag.models import Tag

from ..models import Recipe
from ..serializers import RecipeSerializer, TagSerializer


# ClassBasedViews
class RcipeApiV2Pagination(PageNumberPagination):
    page_size = 10


class RecipeApiV2List(ListCreateAPIView):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RcipeApiV2Pagination


class RecipeApiV2Detail(RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer


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
