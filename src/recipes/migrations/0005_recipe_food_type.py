# Generated by Django 4.2.20 on 2025-06-19 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_alter_recipe_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='food_type',
            field=models.CharField(choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner'), ('Drink', 'Drink'), ('Appetizer', 'Appetizer')], default='Lunch', max_length=20),
        ),
    ]
