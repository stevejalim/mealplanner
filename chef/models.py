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

    def __str__(self):
        return self.title


class Meal(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    date = models.DateField()

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self):
        return f"{self.dish} on {self.date}"
