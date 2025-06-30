from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Recipe
from .forms import RecipeSearchForm
from .utils import get_chart
import pandas as pd

# Create your views here.

# Home / Welcome page
def recipes_home(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipes_home.html', {'recipes': recipes})

# to display all recipes on a page
def recipe_list(request): 
    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})

# to show one recipes' details
@login_required
def recipe_details(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    difficulty = recipe.calculate_difficulty()
    return render(request, 'recipes/recipe_details.html', {'recipe': recipe, 'difficulty': difficulty})

# Log out success 
def logout_success(request):
    return render(request, 'recipes/success.html')

# log in success
def login_success(request):
    return render(request, 'recipes/success.html')

# search recipes
def recipe_search(request):
    form = RecipeSearchForm(request.GET or None)
    recipes = Recipe.objects.all()
    no_results = False
    chart = None
    table = None

    if form.is_valid():
        name = form.cleaned_data.get('query')
        ingredients = form.cleaned_data.get('ingredients')
        food_type = form.cleaned_data.get('food_type')
        cooking_time = form.cleaned_data.get('cooking_time')
        difficulty = form.cleaned_data.get('difficulty')
        chart_type = form.cleaned_data.get('chart_type')
        
        recipes = Recipe.objects.all()

        if name:
            recipes = recipes.filter(name__icontains=name)

        if ingredients:
            recipes = recipes.filter(ingredients__icontains=ingredients)

        if food_type:
            recipes = recipes.filter(food_type=food_type)

        if cooking_time:
            recipes = recipes.filter(cooking_time__lte=cooking_time)

        if difficulty:
            recipes = recipes.filter(difficulty=difficulty)

        if not recipes.exists(): 
            no_results = True
        else:
            df = pd.DataFrame(recipes.values('name', 'ingredients', 'food_type', 'cooking_time', 'difficulty'))
            table = df.to_html()
            chart = get_chart(chart_type, df)

    context = {
        'form' : form,
        'recipes' : recipes,
        'no_results' : no_results,
        'chart': chart,
        'table': table if not no_results else None
    }
    return render(request, 'recipes/recipe_search.html', context)
