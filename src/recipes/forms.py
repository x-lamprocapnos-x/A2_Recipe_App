from django import forms
from .models import FOOD_TYPES

CHART_CHOICES = (
    ('#1', 'Bar Chart'),
    ('#2', 'Pie Chart'),
    ('#3', 'Line Chart'),
)

class RecipeSearchForm(forms.Form):
    query = forms.CharField(label='Search Recipes', required=False)
    ingredients = forms.CharField(required=False)
    food_type = forms.ChoiceField(choices=[('', 'All')] + FOOD_TYPES, required=False)
    cooking_time = forms.IntegerField(label='Max Cooking Time', required=False)
    difficulty = forms.ChoiceField(choices=[
        ('', 'All'),
        ('Easy', 'Easy'),
        ('Intermediate', 'Intermediate'),
        ('Moderate', 'Moderate'),
        ('Hard', 'Hard'),
    ], required=False)

    chart_type = forms.ChoiceField(label='Chart Type', choices=CHART_CHOICES, required=False)
