from django.urls import path
from . import views


urlpatterns = [
    path("", views.meal_schedule, name="meal-schedule"),
    path("dishes/", views.dish_list, name="dish-list"),
    path("dish/add/", views.DishCreate.as_view(), name="dish-add"),
    path("dish/update/<int:pk>/", views.DishUpdate.as_view(), name="dish-update"),
    path("dish/delete/<int:pk>/", views.DishDelete.as_view(), name="dish-delete"),
    path("meals/", views.meal_list, name="meal-list"),
    path("meal/add/", views.MealCreate.as_view(), name="meal-add"),
    path("meal/update/<int:pk>/", views.MealUpdate.as_view(), name="meal-update"),
    path("meal/delete/<int:pk>/", views.MealDelete.as_view(), name="meal-delete"),
]
