from unittest.mock import patch

from django.urls import reverse
from recipes.tests.test_recipe_base import RecipeMixin
from rest_framework.test import APITestCase


class RecipeApiV2Test(APITestCase, RecipeMixin):
    def get_recipe_api_list(self):
        api_url = reverse('recipes:recipes-api-list')
        response = self.client.get(api_url)
        return response

    def test_recipe_api_list_returns_status_code_200(self):
        response = self.get_recipe_api_list()
        self.assertEqual(response.status_code, 200)

    @patch('recipes.views.api.RcipeApiV2Pagination.page_size', new=7)
    def test_recipe_api_list_loads_correct_number_of_recipes(self):
        wanted_number_of_recipes = 7
        self.make_recipe_in_batch(wanted_number_of_recipes)

        response = self.get_recipe_api_list()
        qtd_of_loaded_recipes = len(response.data.get('results'))

        self.assertEqual(wanted_number_of_recipes, qtd_of_loaded_recipes)

    def test_recipe_api_list_dont_show_not_published_recipes(self):
        self.make_recipe(is_published=False, title='I am NOT PUBLISHED')

        response = self.get_recipe_api_list()
        recipes = response.data.get('results')

        self.assertEqual(len(recipes), 0)
