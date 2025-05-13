from django.shortcuts import render, get_object_or_404
from .models import Recipe

# Create your views here.

# Home / Welcome page
def recipes_home(request):
    return render(request, 'recipes/recipes_home.html')

# to display all recipes on a page
def recipe_list(request): 
    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})

# to show one recipes' details
def recipe_details(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    difficulty = recipe.calculate_difficulty()
    return render(request, 'recipes/recipe_details.html', {'recipe': recipe, 'difficulty': difficulty})


