from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    ingredients = models.CharField(
        max_length=225,
        help_text="Enter the ingredients, seperated by a comma"
        )
    cooking_time = models.IntegerField(help_text='Time in minutes')

    # Author field linked to Django's User model
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


    # calculate difficulty
    def calculate_difficulty(self):
        ingredients = self.ingredients.split(', ')
        if self.cooking_time < 10 and len(ingredients) < 4:
            return 'Easy'
        elif self.cooking_time < 10 and len(ingredients) >= 4:
            return 'Intermediate'
        elif self.cooking_time < 15 and len(ingredients) >= 4:
            return 'Moderate'
        else:
            return 'Hard'

    def __str__(self):
        return self.name
   