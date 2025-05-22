from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.recipes_home, name='recipes_home'), # Landing page
    path('recipes/', views.recipe_list, name='recipe_list'), # Full List
    path('recipes/<int:pk>/', views.recipe_details, name='recipe_details'), # Singular recipe details
    path('logout-success/', views.logout_success, name='logout_success'), # Successful logout message
]