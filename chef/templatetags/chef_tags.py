import datetime
from django import template


register = template.Library()


@register.filter
def friendly_date(date_string):
    the_date = datetime.date.fromisoformat(date_string)

    return the_date.strftime("%a %d")
