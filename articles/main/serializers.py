from rest_framework import serializers
from main.models import Article, Vote
from main.services import ArticleRedisService


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ["user", "vote", "article"]


class ArticleSerializer(serializers.ModelSerializer):
    number_of_votes = serializers.SerializerMethodField()
    avarage_vote_score = serializers.SerializerMethodField()

    def get_number_of_votes(self, obj: Article):
        return ArticleRedisService.get(obj).count

    def get_avarage_vote_score(self, obj: Article):
        return ArticleRedisService.get(obj).avg

    class Meta:
        model = Article
        fields = ["id", "title", "number_of_votes", "avarage_vote_score"]
