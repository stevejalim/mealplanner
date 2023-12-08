from chef.models import Meal
from datetime import timedelta


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
