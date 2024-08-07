from django.contrib import admin

# Register your models here.
from .models import Dish
from .models import Meal

admin.site.register(Dish)


class MealAdminConfig(admin.ModelAdmin):
    list_display = ["dish_title", "date"]


admin.site.register(Meal, MealAdminConfig)
