from django.db.models import Count

from chef.models import Dish, Meal
from datetime import date, timedelta


def first_day_of_week(a_date):
    return a_date - timedelta(days=a_date.weekday())


def meals_for_week(start_date, current_user):

    # Set up a dictionary as a lookup for the days in this week
    # and which meals, if any, are on them. They key is the date (as a string)
    # and the value will be a list of one or more Meals (or empty if no Meals
    # are scheduled)

    meals_for_dates = {}
    for offset in range(7):
        # get a date object for the right date in the week
        date = start_date + timedelta(days=offset)

        # use that date as a key in our meals lookup dictionary,
        # but initially we have no actual Meals in it:

        date_as_string = date.isoformat()  # eg "2023-12-01"
        meals_for_dates[date_as_string] = []  # assume no meals on that date

    # Now let's find which Meals we can fit into the lookup we just made

    end_date = start_date + timedelta(days=6)

    meals = Meal.objects.filter(
        date__gte=start_date,
        date__lte=end_date,
        owner=current_user,
    )
    for meal in meals:
        # turn the Meal's date into the same format as the dictionary's keys
        # so that we can slot the meal into the right part of the dictionary.
        date_as_string = meal.date.isoformat()  # eg "2023-12-01"

        if date_as_string in meals_for_dates.keys():
            # add the meal to the (existing) list at that key in the dictionary
            meals_for_dates[date_as_string].append(meal)

    return meals_for_dates


def suggest_dishes(current_user, overall_suggestion_limit=10):

    rare_dishes = get_rare_dishes(current_user, suggestion_limit=5)

    suggested_dishes_from_meals = suggest_dish_from_meals(
        current_user,
        suggestion_limit=overall_suggestion_limit - len(rare_dishes),
    )

    return rare_dishes + suggested_dishes_from_meals


def get_rare_dishes(current_user, suggestion_limit):
    # Returns a list of Dishes that we consider 'rare': at most used once

    counted_dishes = (
        Dish.objects.filter(owner=current_user)
        .annotate(times_used=Count("meal"))
        .order_by("times_used")
        .exclude(exclude_from_suggestions=True)
        .filter(times_used__lte=1)
    )
    return list(counted_dishes[:suggestion_limit])


def suggest_dish_from_meals(current_user, suggestion_limit=5):
    # Returns a list of Dishes (not Meals),
    # that belong to the current_user
    # ordered by least recent,
    # limited in number

    today = date.today()
    blackout_start = today - timedelta(days=60)
    blackout_end = today + timedelta(days=7)

    # Get meals that are outside of our blackout window
    least_recent_meals = (
        Meal.objects.filter(owner=current_user)
        .exclude(dish__exclude_from_suggestions=True)
        .exclude(
            date__gte=blackout_start,
            date__lte=blackout_end,
        )
        .order_by("-date")
    )

    # then we need to be sure to prune out any meals that are in the blackout window
    recent_dish_ids = (
        Meal.objects.filter(owner=current_user)
        .exclude(dish__exclude_from_suggestions=True)
        .filter(  # ie, get INSIDE the blackout window this itme
            date__gte=blackout_start,
            date__lte=blackout_end,
        )
        .values_list(
            "dish", flat=True
        )  # values_list gives us just the ids of the relevant dishes, flat=true gets it to us as a list
    )

    # Now prune down the least_recent_meals to remove any dishes we DID have in the blackout period
    pruned_least_recent_meals = []
    for meal in least_recent_meals:
        if meal.dish.id not in recent_dish_ids:
            pruned_least_recent_meals.append(meal)

    pruned_least_recent_meals = pruned_least_recent_meals[:suggestion_limit]

    suggested_dishes = []
    for meal in pruned_least_recent_meals:
        suggested_dishes.append(meal.dish)
    return suggested_dishes

    # or return [meal.dish for meal in pruned_least_recent_meals]
