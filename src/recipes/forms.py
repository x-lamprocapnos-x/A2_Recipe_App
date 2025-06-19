from django import forms
from .models import FOOD_TYPES

class RecipeSearchForm(forms.Form):
    query = forms.CharField(label='Search Recipes', required=False)
    food_type = forms.ChoiceField(choices=[('', 'All')] + FOOD_TYPES, required=False)