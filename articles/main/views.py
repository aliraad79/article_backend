from rest_framework import generics
from main.models import Article, Vote, User
from main.serializers import ArticleSerializer, VoteSerializer, UserSerializer
from main.services import ArticleRedisService, DetectAnomaly
from django.db.models import Avg


class ArticleApiView(generics.ListCreateAPIView):
    """
    API endpoint that allows users to see articles
    """

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class UserApiView(generics.ListCreateAPIView):
    """
    API endpoint that allows creating user
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class VoteApiView(generics.CreateAPIView, generics.UpdateAPIView):
    """
    API endpoint allows user to vote and update vote
    """

    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    lookup_field = "article"

    def perform_create(self, serializer: VoteSerializer):
        new_vote = serializer.save()
        article = serializer.validated_data["article"]
        article.number_of_scores = article.vote_set.count()
        article.avg_scores = article.vote_set.aggregate(Avg("vote"))["vote__avg"]
        DetectAnomaly().detect(new_vote)

    def get_object(self):
        user = self.request.data["user"]
        article = self.request.data["article"]
        vote = self.filter_queryset(self.get_queryset()).get(user=user, article=article)
        DetectAnomaly().detect(vote)
        return vote
