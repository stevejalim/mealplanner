from django.test import TestCase
from chef.models import Dish, Meal
from datetime import date


class DishTest(TestCase):
    def test_str(self):
        dish = Dish.objects.create(title="chicken", text="with peppers")

        self.assertEqual(dish.__str__(), "chicken")


class MealTest(TestCase):
    def test_str(self):

        the_date = date(1974, 10, 3)

        dish = Dish.objects.create(title="pork", text="with rice")
        meal = Meal.objects.create(dish=dish, date=the_date)

        self.assertEqual(meal.__str__(), "pork on 1974-10-03")
