from rest_framework import generics
from main.models import Article, Vote
from main.serializers import ArticleSerializer, VoteSerializer
from django_redis import get_redis_connection
from .utils import get_article_avg_redis_key, get_article_count_redis_key


class ArticleApiView(generics.ListCreateAPIView):
    """
    API endpoint that allows users to see articles
    """

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class VoteApiView(
    generics.UpdateAPIView, generics.CreateAPIView, generics.GenericAPIView
):
    """
    API endpoint allows user to vote and update vote
    """

    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def update_redis_value(self, article_id, vote):
        article_avg_key = get_article_avg_redis_key(article_id)
        article_count_key = get_article_count_redis_key(article_id)

        redis_connection = get_redis_connection()

        number_of_votes = redis_connection.get(article_count_key)
        if number_of_votes:
            number_of_votes = int(number_of_votes)
            redis_connection.set(article_count_key, number_of_votes + 1)
            self.update_avarage_score(
                vote, article_avg_key, redis_connection, number_of_votes
            )

        else:
            redis_connection.set(article_count_key, 1)
            redis_connection.set(article_avg_key, vote)

    def update_avarage_score(
        self, vote, article_avg_key, redis_connection, number_of_votes
    ):
        avg_score = redis_connection.get(article_avg_key)
        if avg_score:
            avg_score = int(avg_score)
            avg_score = ((number_of_votes * avg_score) + vote) / (number_of_votes + 1)
            redis_connection.set(article_avg_key, avg_score)

    def perform_create(self, serializer: VoteSerializer):
        super().perform_create(serializer)
        related_article_id = serializer.validated_data["article"].id
        vote = serializer.validated_data["vote"]
        self.update_redis_value(related_article_id, vote)
