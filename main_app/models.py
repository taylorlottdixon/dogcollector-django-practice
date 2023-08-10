from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

MEALS = (
    ('B', 'Breakfast'),
    ('D', 'Dinner')
)

# Create your models here.

class Dog(models.Model):
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    # loves = models.ForeignKey(Love, on_delete=models.CASCADE)
    # hates = models.ForeignKey(Hate, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.id})'
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'dog_id': self.id})
    
    def fed_for_today(self):
        return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)
    
    class Meta:
        ordering = ['name']

class Walk(models.Model):
    date = models.DateField('Walk Date')
    time_start = models.TimeField('Walk Start')
    time_end = models.TimeField('Walk End')
    length = models.IntegerField('Miles')
    dogs = models.ManyToManyField(Dog, related_name='walks')

    def __str__(self):
        # Nice method for obtaining the friendly value of a Field.choice
        return f"{self.length} miles on {self.date}"
    
    def get_absolute_url(self):
        return reverse('walks_detail', kwargs={'pk': self.id, 'walk_id': self.id})

    class Meta:
        ordering = ['-date']
    
class Feeding(models.Model):
    date = models.DateField('Feeding Date')
    meal = models.CharField(
        max_length=1,
        choices=MEALS,
        default=MEALS[0][0]
    )
      # Create a dog_id FK
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    def __str__(self):
        # Nice method for obtaining the friendly value of a Field.choice
        return f"{self.get_meal_display()} on {self.date}"

    # change the default sort
    class Meta:
        ordering = ['-date']


    def __str__(self):
    # Nice method for obtaining the friendly value of a Field.choice
        return f"{self.get_meal_display()} on {self.date}"
    
class Photo(models.Model):
    url = models.CharField(max_length=200)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for dog_id: {self.dog_id} @{self.url}"