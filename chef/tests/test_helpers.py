from datetime import date

from django.test import TestCase
from django.contrib.auth.models import User

from chef.models import Dish, Meal
from chef.helpers import suggest_dish


class MealSuggestionTests(TestCase):
    def setUp(self):
        # Create a test user with a password we know so we can log them in
        self.user = User.objects.create(username="testuser")
        self.user.set_password("test")  # create a properly hashed password in the DB
        self.user.save()

        the_date_1 = date(1976, 3, 5)
        the_date_2 = date(1976, 3, 6)
        the_date_3 = date(1976, 3, 7)
        the_date_4 = date(1976, 3, 8)
        the_date_5 = date(1976, 3, 9)
        the_date_6 = date(1976, 3, 10)

        self.dish_1 = Dish.objects.create(
            title="squash risotto",
            text="in the pressure cooker",
            owner=self.user,
        )
        self.dish_2 = Dish.objects.create(
            title="chicken risotto",
            text="on the hob",
            owner=self.user,
        )
        self.dish_3 = Dish.objects.create(
            title="baked beans on toast",
            text="in the pressure cooker!",
            owner=self.user,
        )
        self.dish_4 = Dish.objects.create(
            title="scrambled eggs",
            text="cooked with butter",
            owner=self.user,
        )
        self.dish_5 = Dish.objects.create(
            title="waffles",
            text="in the new waffle iron!",
            owner=self.user,
        )
        self.dish_6 = Dish.objects.create(
            title="tacos",
            text="with beans and chicken",
            owner=self.user,
        )

        self.meal_1 = Meal.objects.create(
            dish=self.dish_1,
            date=the_date_1,
            owner=self.user,
        )
        self.meal_2 = Meal.objects.create(
            dish=self.dish_2,
            date=the_date_2,
            owner=self.user,
        )
        self.meal_3 = Meal.objects.create(
            dish=self.dish_3,
            date=the_date_3,
            owner=self.user,
        )
        self.meal_4 = Meal.objects.create(
            dish=self.dish_4,
            date=the_date_4,
            owner=self.user,
        )
        self.meal_5 = Meal.objects.create(
            dish=self.dish_5,
            date=the_date_5,
            owner=self.user,
        )
        self.meal_6 = Meal.objects.create(
            dish=self.dish_6,
            date=the_date_6,
            owner=self.user,
        )

    def test_suggest_dish_with_at_least_five_meals_in_history(self):
        suggestions = suggest_dish(current_user=self.user)
        expected = [self.dish_1, self.dish_2, self.dish_3, self.dish_4, self.dish_5]
        self.assertEqual(suggestions, expected)

    def test_suggest_dish_has_variable_suggestion_limit(self):
        suggestions = suggest_dish(current_user=self.user, suggestion_limit=2)
        expected = [self.dish_1, self.dish_2]
        self.assertEqual(suggestions, expected)

    def test_suggest_dish_with_less_than_five_meals_in_history(self):

        self.meal_2.delete()
        self.meal_4.delete()

        suggestions = suggest_dish(current_user=self.user)
        expected = [self.dish_1, self.dish_3, self.dish_5, self.dish_6]
        self.assertEqual(suggestions, expected)

    def test_suggest_dish_no_meals_available_for_user(self):
        # Make a different user, who has no Meals or Dishes, so we expect
        # no suggestions for them

        another_user = User.objects.create(username="another_user")

        suggestions = suggest_dish(current_user=another_user)
        expected = []

        self.assertEqual(suggestions, expected)

    def test_suggest_dish_no_meals_at_all(self):
        Meal.objects.all().delete()
        assert Meal.objects.count() == 0
        suggestions = suggest_dish(current_user=self.user)
        expected = []
        self.assertEqual(suggestions, expected)
