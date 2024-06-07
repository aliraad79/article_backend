from rest_framework import mixins
from rest_framework import generics
from main.models import Article, Vote
from main.serializers import ArticleSerializer, VoteSerializer


class ArticleApiView(generics.ListCreateAPIView):
    """
    API endpoint that allows users to see articles
    """

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class VoteApiView(
    mixins.UpdateModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    """
    API endpoint allows user to vote and update vote
    """

    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
