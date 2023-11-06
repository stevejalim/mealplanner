from django import forms
from .models import Meal, Dish


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = (
            "dish",
            "date",
        )
