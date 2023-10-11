from django.shortcuts import render
from django.urls import reverse
from .models import Dish, Meal
from django.utils import timezone
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
)


# Create your views here.


def meal_schedule(request):

    date_now = timezone.now().date()
    meals = Meal.objects.filter(date__gte=date_now).order_by("date")

    return render(request, "chef/meal_schedule.html", {"meals": meals})


def dish_list(request):
    dishes = Dish.objects.all().order_by("title")
    return render(request, "chef/dish_list.html", {"dishes": dishes})


class DishCreate(CreateView):

    # The automatic template _name_ generated for this view is dish_form.html

    model = Dish
    fields = [
        "title",
        "text",
    ]

    def get_context_data(self):

        context = super().get_context_data()
        context["title"] = "Create a new dish"

        return context


class DishUpdate(UpdateView):

    # The automatic template _name_ generated for this view is dish_form.html

    model = Dish
    fields = [
        "title",
        "text",
    ]

    def get_context_data(self):

        context = super().get_context_data()
        context["title"] = "Edit dish"
        return context

    def get_success_url(self):

        return reverse("dish-list")


class MealUpdate(UpdateView):

    # The automatic template _name_ generated for this view is meal_form.html

    model = Meal
    fields = [
        "dish",
        "date",
    ]

    def get_context_data(self):

        context = super().get_context_data()
        context["title"] = "Edit meal"
        return context

    def get_success_url(self):

        return reverse("meal-schedule")


def meal_list(request):

    meals = Meal.objects.all().order_by("date")

    return render(request, "chef/meal_list.html", {"meals": meals})
