from rest_framework import mixins
from rest_framework import generics
from main.models import Article, Vote
from main.serializers import ArticleSerializer, VoteSerializer


class VoteApiView(
    generics.ListCreateAPIView,
):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
