from django.shortcuts import render
from .models import Dish, Meal
from django.utils import timezone
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
)


# Create your views here.


def show_schedule(request):

    date_now = timezone.now().date()
    meals = Meal.objects.filter(date__gte=date_now).order_by("date")

    return render(request, "chef/meal_list.html", {"meals": meals})


def dish_list(request):
    dishes = Dish.objects.all().order_by("title")
    return render(request, "chef/dish_list.html", {"dishes": dishes})


class DishCreate(CreateView):

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

        return reverse("show-schedule")
