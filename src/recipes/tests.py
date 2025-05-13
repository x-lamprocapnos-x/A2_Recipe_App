from django.test import TestCase
from django.urls import reverse
from django.http import HttpResponse
from .models import Recipe

# Create your tests here.

# Recipe model tests
class RecipeModelTest(TestCase):

    # Test data
    def setUp(self):
        self.recipe = Recipe.objects.create(
            name='Tea',
            description='Herbal',
            ingredients='Tea Leaves, Sugar, Water',
            cooking_time='5'
        )

    # Name test
    def test_recipe_name(self):
        # get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # get metadata for name and query 
        field_label = recipe._meta.get_field('name').verbose_name

        # compare the value to the expected result
        self.assertEqual(field_label, 'name')
    
    def test_calculate_difficulty_easy(self):
        recipe = Recipe(name='Tea', description='Herbal', ingredients='Tea Leaves, Sugar, Water', cooking_time=5)
        self.assertEqual(recipe.calculate_difficulty(), 'Easy')

    def test_calculate_difficulty_intermediate(self):
        recipe = Recipe(name='Salad', description='Fresh', ingredients='Lettuce, Cucumber, Tomato, Carrots', cooking_time=5)
        self.assertEqual(recipe.calculate_difficulty(), 'Intermediate')

    def test_calculate_difficulty_moderate(self):
        recipe = Recipe(name='Cheese Pizza', description='Gooey', ingredients='Flour, Water, Tomato Sauce, Cheese', cooking_time=10)
        self.assertEqual(recipe.calculate_difficulty(), 'Moderate')

    def test_calculate_difficulty_hard(self):
        recipe = Recipe(name='Ramen', description='Fancy Soup', ingredients='Noodles, Water, Eggs, Corn, Shrimp, Chili Crisps ', cooking_time=20)
        self.assertEqual(recipe.calculate_difficulty(), 'Hard')

# Recipe view/url tests
class RecipeViewTests(TestCase):

    # Test data
    def setUp(self):
        seld.recipe = Recipe.objects.create(
            name='Tea',
            description='Herbal',
            ingredients='Tea Leaves, Sugar, Water',
            cooking_time='5'
        )
    
    def test_recipe_list_url_exists(self):
        response = self.client.get(reverse('recipe:recipe_list'))
        self.assertEqual(response.status_code, 200)

    def test_recipes_details_url_exists(self):
        response = self.client.get(reverse('recipe:recipe_details', args=[self.recipe.id]))
        self.assertEqual(response.status_code, 200)

    def test_recipe_list_template_used(self):
        response = self.client.get(reverse('recipe_list'))
        self.assertTemplateUsed(response, 'recipes/recipe_list.html')

    def test_recipe_details_template_used(self):
        response = self.client.get(reverse('recipe_details', args=[self.recipe.id]))
        self.assertTemplateUsed(response, 'recipes/recipe_details.html')

    def test_recipe_list_contains_recipe(self):
        response = self.client.get(reverse('recipe_list'))
        self.assertContains(response, "Tea")

    def test_recipe_details_contains_recipe_info(self):
        response = self.client.get(reverse('recipe_details', args=[self.recipe.id]))
        self.assertContains(response, 'Tea')
        self.assertContains(response, 'Tea Leaves')


