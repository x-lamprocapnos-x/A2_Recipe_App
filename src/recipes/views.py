from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Recipe

# Create your views here.

# Home / Welcome page
def recipes_home(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipes_home.html', {'recipes': recipes})

# to display all recipes on a page
@login_required
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
def search_recipe(request):
    form = RecipeSearchForm(request.GET or None)
    recipe = Recipe.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get('query')
        food_type = form.cleaned_data.get('food_type')

        if query:
            recipe = recipes.filter(name_icontains=query)

        if food_type:
            recipes = recipes.filter(food_type=food_type)

    context = {
        'form' : form,
        'recipes' : recipes
    }
    return render(request, 'recipes/recipe_search_html', context)
