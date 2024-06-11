from rest_framework import serializers
from main.models import Article, Vote, User


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ["user", "vote", "article"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name"]


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["id", "title", "number_of_scores", "avg_scores"]
