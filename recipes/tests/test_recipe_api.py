from unittest.mock import patch

from django.urls import reverse
from recipes.tests.test_recipe_base import RecipeMixin
from rest_framework.test import APITestCase


class RecipeApiV2Test(APITestCase, RecipeMixin):
    def get_recipe_reverse_url(self, reverse_result=None):
        api_url = reverse_result or reverse('recipes:recipes-api-list')
        return api_url

    def get_recipe_api_list(self, reverse_result=None):
        api_url = self.get_recipe_reverse_url(reverse_result=None)
        response = self.client.get(api_url)
        return response

    def make_user(self):
        userdata = {
            'username': 'user_tester',
            'password': 'abc1234//',
        }
        self.make_author(**userdata)
        return userdata

    def make_jwt_request(self):
        userdata = self.make_user()
        jwt_url = reverse('recipes:token_obtain_pair')
        return self.client.post(jwt_url, data=userdata)

    def get_jwt_acces_token(self):
        token_response = self.make_jwt_request()
        access_token = token_response.data.get('access')
        return access_token

    def get_recipe_raw_data(self):
        data = {
            'title': 'my_test_title',
            'description': 'my_test_description',
            'preparation_time': 3,
            'preparation_time_unit': 'my_test_preparation_time_unit',
            'servings': 3,
            'servings_unit': 'my_test_sevings_unit',
            'preparation_steps': 'my_test_preparation_steps'
        }
        return data

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

    def test_recipe_api_list_load_recipes_by_category_id(self):
        # Creates 10 recipes
        recipes = self.make_recipe_in_batch(qtd=10)
        # Creates categories
        wanted_category = self.make_category(name='WANTED_CATEGORY')
        not_wanted_category = self.make_category(name='NOT_WANTED_CATEGORY')
        # Change all recipes to the wanted category
        for recipe in recipes:
            recipe.category = wanted_category
            recipe.save()
        # change one recipe to the NOT wanted category
        # As a result, this recipe should NOT show in the page
        recipes[0].category = not_wanted_category
        recipes[0].save()
        # Action: get the recipes by wanted category id
        api_url = reverse('recipes:recipes-api-list') + \
            f'?category_id={wanted_category.id}'
        response = self.client.get(api_url)

        recipes_with_wanted_category = len(response.data.get('results'))
        # We should only see recipes from wanted category
        print(response.data)
        print(wanted_category.id)
        self.assertEqual(recipes_with_wanted_category, 9)

    def test_recipe_api_list_user_must_send_jwt_token_to_create_recipe(self):
        api_url = self.get_recipe_reverse_url()
        response = self.client.post(api_url)
        self.assertEqual(response.status_code, 401)

    def test_recipe_api_list_logged_user_can_create_a_recipe(self):
        token = self.get_jwt_acces_token()
        data = self.get_recipe_raw_data()
        response = self.client.post(
            self.get_recipe_reverse_url(), data=data,
            HTTP_AUTHORIZATION=F'Bearer {token}'
        )
        self.assertEqual(response.status_code, 201)
