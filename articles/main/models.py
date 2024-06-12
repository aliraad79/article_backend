from django.db import models
from django.db.models import Avg
from django.core.validators import MaxValueValidator, MinValueValidator


class User(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=256)
    number_of_scores = models.PositiveBigIntegerField(default=0)
    avg_scores = models.FloatField(default=2.5)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_statics(self):
        self.number_of_scores = self.vote_set.count()
        self.avg_scores = self.vote_set.aggregate(Avg("score"))["score__avg"]
        self.save()

    def __str__(self):
        return f"Article_{self.id}"


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=False, blank=False
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
