from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
# B will be the value, So this is what we'll store in the db
# Breakfast is the user friendly view, so what you see when you use a dropdown
MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

class Toy(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('toys_detail', kwargs={'pk': self.id})

class Finch(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    toys = models.ManyToManyField(Toy)
    # finch = Finch.objects.get(id=1) -> finch.user_id
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'finch_id': self.id})

    def fed_for_today(self):
        return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)

class Photo(models.Model):
    url = models.CharField(max_length=200)
    finch = models.ForeignKey(Finch, on_delete=models.CASCADE)

    def __str__(self):
        return f'Photo for finch_id: {self.finch_id} @{self.url}'

class Feeding(models.Model): 
    date = models.DateField('feeding date')
    meal = models.CharField(
        max_length=1,
            choices=MEALS,
            default=MEALS[0][0]
    )

	# the foregin key always goes on the many side
	# internally it will be cat_id the _id automatically gets added
    finch = models.ForeignKey(Finch, on_delete=models.CASCADE)

    def __str__(self):
        # this method will gives us the friendly meal choices value, so like Breakfast instead of B
        return f'{self.get_meal_display()} on {self.date}'

    class Meta:
        ordering = ['-date']
