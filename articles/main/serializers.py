from rest_framework import serializers
from main.models import Article, Vote
from django.db.models import Avg


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ["id", "user", "vote"]


class ArticleSerializer(serializers.ModelSerializer):
    number_of_votes = serializers.SerializerMethodField()
    avarage_vote_score = serializers.SerializerMethodField()

    def get_number_of_votes(self, obj):
        return obj.vote_set.count()

    def get_avarage_vote_score(self, obj):
        return obj.vote_set.aggregate(Avg("vote", default=3))['vote__avg']

    class Meta:
        model = Article
        fields = ["id", "title", "text", "number_of_votes", "avarage_vote_score"]
