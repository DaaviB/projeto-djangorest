from recipes.tests.test_recipe_base import RecipeMixin
from rest_framework.test import APITestCase


class RecipeApiV2Test(APITestCase, RecipeMixin):
    def test_the_test(self):
        assert 1 == 1
