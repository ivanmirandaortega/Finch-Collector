from django.db import models
from django.urls import reverse
from datetime import date

# Create your models here.
class Finch(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'finch_id': self.id})

    def fed_for_today(self):
        return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)

# B will be the value, So this is what we'll store in the db
# Breakfast is the user friendly view, so what you see when you use a dropdown
MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

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
