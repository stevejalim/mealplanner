from django.urls import path
from . import views


urlpatterns = [
    path("", views.meal_schedule, name="meal-schedule"),
    path("dish/", views.dish_list, name="dish-list"),
    path("dish/add/", views.DishCreate.as_view(), name="dish-add"),
    path("dish/update/<int:pk>/", views.DishUpdate.as_view(), name="dish-update"),
    path("meal/", views.meal_list, name="meal-list"),
    path("meal/update/<int:pk>/", views.MealUpdate.as_view(), name="meal-update"),
]
