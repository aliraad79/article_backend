from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(5)])


class Article(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField()
    number_of_votes = models.IntegerField()
    votes = models.ForeignKey(Vote, on_delete=models.CASCADE)


