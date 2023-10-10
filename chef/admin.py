from django.contrib import admin

# Register your models here.
from .models import Dish
from .models import Meal

admin.site.register(Dish)

admin.site.register(Meal)
