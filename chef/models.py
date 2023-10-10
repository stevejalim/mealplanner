from django.db import models


class Dish(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()

    def __str__(self):
        return self.title


class Meal(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"{self.dish} on {self.date}"
