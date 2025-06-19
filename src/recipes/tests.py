from django.test import TestCase
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Recipe
from .forms import RecipeSearchForm

# Create your tests here.

# Recipe model tests
class RecipeModelTest(TestCase):

    # Test data
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='password')
        self.recipe = Recipe.objects.create(
            name='Tea',
            description='Herbal',
            ingredients='Tea Leaves, Sugar, Water',
            cooking_time=5,
            author=self.user
        )

    # Name test
    def test_recipe_name(self):
        # get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # get metadata for name and query 
        field_label = recipe._meta.get_field('name').verbose_name

        # compare the value to the expected result
        self.assertEqual(field_label, 'name')

    def test_recipe_has_instructions_field(self):
        field = self.recipe._meta.get_field('instructions')
        self.assertEqual(field.verbose_name, 'instructions')

    def test_recipe_has_image_field(self):
        field = self.recipe._meta.get_field('image')
        self.assertEqual(field.verbose_name, 'image')
    
    def test_recipe_has_difficulty_field(self):
        field = self.recipe._meta.get_field('difficulty')
        self.assertEqual(field.verbose_name, 'difficulty')

    def test_recipe_has_author(self):
        field = self.recipe._meta.get_field('author')
        self.assertEqual(field.related_model.__name__, 'User')
    
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

    def test_save_sets_difficulty(self):
        recipe = Recipe(
            name='Tea',
            description='Hot Beverage',
            ingredients='Tea Leaves, Sugar, Water',
            cooking_time=5,
            author=self.user
        )
        recipe.save()
        self.assertEqual(recipe.difficulty, 'Easy')

# Recipe view/url tests
class RecipeViewTests(TestCase):

    # Test data
    def setUp(self):
        self.user = User.objects.create_user(username='user2', password='password')
        self.recipe = Recipe.objects.create(
            name='Tea',
            description='Herbal',
            ingredients='Tea Leaves, Sugar, Water',
            cooking_time=5,
            author=self.user
        )
    
    def test_recipe_list_url_exists(self):
        response = self.client.get(reverse('recipes:recipe_list'))
        self.assertEqual(response.status_code, 200)

    def test_recipes_details_url_exists(self):
        response = self.client.get(reverse('recipes:recipe_details', args=[self.recipe.id]))
        self.assertEqual(response.status_code, 200)

    def test_recipe_list_template_used(self):
        response = self.client.get(reverse('recipes:recipe_list'))
        self.assertTemplateUsed(response, 'recipes/recipe_list.html')

    def test_recipe_details_template_used(self):
        response = self.client.get(reverse('recipes:recipe_details', args=[self.recipe.id]))
        self.assertTemplateUsed(response, 'recipes/recipe_details.html')

    def test_recipe_list_contains_recipe(self):
        response = self.client.get(reverse('recipes:recipe_list'))
        self.assertContains(response, "Tea")

    def test_recipe_details_contains_recipe_info(self):
        response = self.client.get(reverse('recipes:recipe_details', args=[self.recipe.id]))
        self.assertContains(response, 'Tea')
        self.assertContains(response, 'Tea Leaves')

# Recipe Search Tests
class RecipeSearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user3', password='password')
        Recipe.objects.create(
            name='Avocado Toast',
            description='Simple Breakfast',
            ingredients='Avocado, Bread, Salt, Lemon',
            cooking_time=5,
            author=self.user
        )
        Recipe.object.create(
            name='Pizza Dough',
            description='Easy no yeast dough'
            ingredients='Water, Flour, Oil, Baking Powder'
            cooking_time=15
            author=self.user
        )

        def test_search_form_fields_exist(self):
            form = RecipeSearchForm()
            self.assertIn('query', form.fields)

        def test_search_by_recipe_name_returns_result(self):
            response = self.client.get(reverse('recipes:search') + '?query=Pizza Dough')
            self.assertContains(response, 'Pizza Dough')

        def test_partial_search_returns_result(self):
            response = self.client.get(reverse('recipes:search') + '?query=Avocado')
            self.assertContains(response, 'Avocado Toast')

        def test_search_result_links_to_detail_page(self):
            recipe = Recipe.objects.get(name='Avocado Toast')
            detail_url = reverse('recipes:recipe_datails', args=[recipe.id])
            response = self.client.get(reverse('recipes:search') + '?query=Avocado')
            self.assertContains(response, detail_url)