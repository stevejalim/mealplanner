from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from chef.models import Dish, Meal
from datetime import date


class HomepageTest(TestCase):
    def test_page_loads(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)

    def test_page_content(self):
        resp = self.client.get("/")
        self.assertContains(
            resp, '<a class="button" href="/accounts/login/">Log in</a>'
        )
        self.assertNotContains(resp, "Log out")
        self.assertContains(
            resp, '<a href="/dishes/">Browse your library of dishes</a>'
        )
        self.assertContains(resp, '<a href="/meals/">View all meals</a>')


class TestDishList(TestCase):
    def setUp(self):
        # Create a test user with a password we know so we can log them in
        self.user = User.objects.create(username="testuser")
        self.user.set_password("test")  # create a properly hashed password in the DB
        self.user.save()

        Dish.objects.create(
            title="squash risotto",
            text="in the pressure cooker",
            owner=self.user,
        )
        Dish.objects.create(
            title="chicken risotto",
            text="on the hob",
            owner=self.user,
        )
        Dish.objects.create(
            title="baked beans on toast",
            text="in the pressure cooker!",
            owner=self.user,
        )
        Dish.objects.create(
            title="scrambled eggs",
            text="cooked with butter",
            owner=self.user,
        )

    def test_page_access__unauthenticated_user(self):
        dest = reverse("dish-list")
        resp = self.client.get(dest)
        self.assertRedirects(resp, f"/accounts/login/?next={dest}", status_code=302)

    def test_page_access__authenticated_user(self):
        dest = reverse("dish-list")

        # Log in our test user
        self.client.login(username="testuser", password="test")

        resp = self.client.get(dest, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "chef/dish_list.html")

    def test_list_page_shows_dishes(self):
        # Log in our test user
        self.client.login(username="testuser", password="test")

        # Load the page
        dest = reverse("dish-list")
        resp = self.client.get(dest, follow=True)

        # Focus only on the `dishes` data in the context, not the dish_suggestions data
        dish_results_in_context = resp.context["dishes"]

        # turn the list of Dish objects into title strings, just for easier checking
        dish_names = [x.title for x in dish_results_in_context]

        self.assertTrue("squash risotto" in dish_names)
        self.assertTrue("chicken risotto" in dish_names)
        self.assertTrue("baked beans on toast" in dish_names)
        self.assertTrue("scrambled eggs" in dish_names)

    def test_search_dish_by_title(self):
        # Log in our test user
        self.client.login(username="testuser", password="test")

        # Load the page
        dest = reverse("dish-list")

        # Update the URL to include the search term as a querystring
        dest = dest + "?q=risotto"

        resp = self.client.get(dest, follow=True)

        # Focus only on the `dishes` data in the context, not the dish_suggestions data
        dish_results_in_context = resp.context["dishes"]

        # turn the list of Dish objects into title strings, just for easier checking
        dish_names = [x.title for x in dish_results_in_context]

        self.assertTrue("squash risotto" in dish_names)
        self.assertTrue("chicken risotto" in dish_names)

        self.assertFalse("baked beans on toast" in dish_names)
        self.assertFalse("scrambled eggs" in dish_names)

    def test_search_dish_by_text(self):
        # Log in our test user
        self.client.login(username="testuser", password="test")

        # Load the page
        dest = reverse("dish-list")

        # Update the URL to include the search term as a querystring
        dest = dest + "?q=pressure cooker"
        resp = self.client.get(dest, follow=True)

        # Look for the content we expect to be there

        # Focus only on the `dishes` data in the context, not the dish_suggestions data
        dish_results_in_context = resp.context["dishes"]

        # turn the list of Dish objects into title strings, just for easier checking
        dish_names = [x.title for x in dish_results_in_context]

        self.assertTrue("squash risotto" in dish_names)
        self.assertTrue("baked beans on toast" in dish_names)

        self.assertFalse("chicken risotto" in dish_names)
        self.assertFalse("scrambled eggs" in dish_names)

    def test_search_dish_no_results(self):
        # Log in our test user
        self.client.login(username="testuser", password="test")

        # Load the page
        dest = reverse("dish-list")

        # Update the URL to include the search term as a querystring
        dest = dest + "?q=numberwang"
        resp = self.client.get(dest, follow=True)

        # Focus only on the `dishes` data in the context, not the dish_suggestions data
        dish_results_in_context = resp.context["dishes"]

        # turn the list of Dish objects into title strings, just for easier checking
        dish_names = [x.title for x in dish_results_in_context]

        self.assertFalse("squash risotto" in dish_names)
        self.assertFalse("baked beans on toast" in dish_names)
        self.assertFalse("chicken risotto" in dish_names)
        self.assertFalse("scrambled eggs" in dish_names)


class TestMealList(TestCase):
    def setUp(self):
        # Create a test user with a password we know so we can log them in
        self.user = User.objects.create(username="testuser")
        self.user.set_password("test")  # create a properly hashed password in the DB
        self.user.save()

        self.user2 = User.objects.create(username="testuser2")
        self.user2.set_password("test")  # create a properly hashed password in the DB
        self.user2.save()

        the_date_1 = date(1976, 3, 5)
        the_date_2 = date(1976, 3, 6)
        the_date_3 = date(1976, 3, 7)
        the_date_4 = date(1976, 3, 8)

        dish_1 = Dish.objects.create(
            title="squash risotto",
            text="in the pressure cooker",
            owner=self.user,
        )
        dish_2 = Dish.objects.create(
            title="chicken risotto",
            text="on the hob",
            owner=self.user,
        )
        dish_3 = Dish.objects.create(
            title="baked beans on toast",
            text="in the pressure cooker!",
            owner=self.user2,  # Note the owner
        )
        dish_4 = Dish.objects.create(
            title="scrambled eggs",
            text="cooked with butter",
            owner=self.user,
        )

        meal_1 = Meal.objects.create(dish=dish_1, date=the_date_1, owner=self.user)
        meal_2 = Meal.objects.create(dish=dish_2, date=the_date_2, owner=self.user)
        meal_3 = Meal.objects.create(
            dish=dish_3, date=the_date_3, owner=self.user2
        )  # Note the owner
        meal_4 = Meal.objects.create(dish=dish_4, date=the_date_4, owner=self.user)

    def test_page_access__unauthenticated_user(self):
        dest = reverse("meal-list")
        resp = self.client.get(dest)
        self.assertRedirects(resp, f"/accounts/login/?next={dest}", status_code=302)

    def test_page_access__authenticated_user(self):
        dest = reverse("meal-list")

        # Log in our test user
        self.client.login(username="testuser", password="test")

        resp = self.client.get(dest, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "chef/meal_list.html")

    def test_list_page_shows_meals(self):
        # Log in our test user
        self.client.login(username="testuser", password="test")

        # Load the page
        dest = reverse("meal-list")
        resp = self.client.get(dest, follow=True)

        # Look for the content we expect to be there
        self.assertContains(resp, "squash risotto")
        self.assertContains(resp, "chicken risotto")
        self.assertNotContains(
            resp, "baked beans on toast"
        )  # belongs to user2, not the logged in user
        self.assertContains(resp, "scrambled eggs")
