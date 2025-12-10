from django.db import models
from django.contrib.auth.models import User

FOOD_TYPES = [
    ('Breakfast', 'Breakfast'),
    ('Lunch', 'Lunch'),
    ('Dinner', 'Dinner'),
    ('Drink', 'Drink'),
    ('Appetizer', 'Appetizer'),
]

class Recipe(models.Model):
    food_type = models.CharField(max_length=20, choices=FOOD_TYPES, default='Lunch')
    name = models.CharField(max_length=50)
    description = models.TextField()
    ingredients = models.CharField(
        max_length=225,
        help_text="Enter the ingredients, seperated by a comma"
        )
    cooking_time = models.IntegerField(help_text='Time in minutes')
    instructions = models.TextField(null=True) # Detailed steps
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True, default='recipe_images/default_img.jpg') # Visual enhancement
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    difficulty = models.CharField(max_length=20, blank=True) # Store difficulty


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

    def save(self, *args, **kwargs):
        self.difficulty = self.calculate_difficulty()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
   