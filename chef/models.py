from django.db import models
from django.contrib.auth.models import User


class Dish(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
    )

    exclude_from_suggestions = models.BooleanField(
        default=False,
        help_text="Meals marked with this, such as away days or dinner out will not be automatically suggested.",
    )

    class Meta:
        verbose_name_plural = "dishes"
        constraints = [
            models.UniqueConstraint(
                fields=["title", "owner"], name="unique_dish_title_per_owner"
            )
        ]

    def __str__(self):
        return self.title

    def get_latest_meal(self):
        return self.meal_set.order_by("date").first()


class Meal(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    date = models.DateField()
    text = models.TextField(
        blank=True,
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self):
        return f"{self.dish.title} on {self.date}"

    def dish_title(self):
        return self.dish.title
