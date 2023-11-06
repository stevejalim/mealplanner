from django import forms
from .models import Meal, Dish


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = (
            "dish",
            "date",
        )

    def __init__(self, *args, **kwargs):
        owner = kwargs.pop("owner")
        super().__init__(*args, **kwargs)
        self.fields["dish"] = forms.ModelChoiceField(
            queryset=Dish.objects.filter(owner=owner),
        )
