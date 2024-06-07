from rest_framework import serializers
from main.models import Article, Vote

from django_redis import get_redis_connection
from .utils import get_article_avg_redis_key, get_article_count_redis_key


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ["id", "user", "vote", "article"]


class ArticleSerializer(serializers.ModelSerializer):
    number_of_votes = serializers.SerializerMethodField()
    avarage_vote_score = serializers.SerializerMethodField()

    def get_number_of_votes(self, obj: Article):
        redis_score = get_redis_connection().get(get_article_avg_redis_key(obj.id))
        if redis_score is not None:
            return redis_score
        return 3

    def get_avarage_vote_score(self, obj: Article):
        redis_score = get_redis_connection().get(get_article_count_redis_key(obj.id))
        if redis_score is not None:
            return redis_score
        return 0

    class Meta:
        model = Article
        fields = ["id", "title", "text", "number_of_votes", "avarage_vote_score"]
