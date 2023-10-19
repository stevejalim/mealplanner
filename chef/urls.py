from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    path("", views.meal_schedule, name="meal-schedule"),
    path("dishes/", login_required(views.dish_list), name="dish-list"),
    path("dish/add/", login_required(views.DishCreate.as_view()), name="dish-add"),
    path(
        "dish/update/<int:pk>/",
        login_required(views.DishUpdate.as_view()),
        name="dish-update",
    ),
    path(
        "dish/delete/<int:pk>/",
        login_required(views.DishDelete.as_view()),
        name="dish-delete",
    ),
    path("meals/", login_required(views.meal_list), name="meal-list"),
    path("meal/add/", login_required(views.MealCreate.as_view()), name="meal-add"),
    path(
        "meal/update/<int:pk>/",
        login_required(views.MealUpdate.as_view()),
        name="meal-update",
    ),
    path(
        "meal/delete/<int:pk>/",
        login_required(views.MealDelete.as_view()),
        name="meal-delete",
    ),
]
