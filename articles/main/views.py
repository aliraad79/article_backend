from rest_framework import generics
from main.models import Article, Vote, User
from main.serializers import ArticleSerializer, VoteSerializer, UserSerializer
from main.services import ArticleRedisService, DetectAnomaly


class ArticleApiView(generics.ListCreateAPIView):
    """
    API endpoint that allows users to see articles
    """

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def post(self, request, *args, **kwargs):
        ArticleRedisService.evict_articles()
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        cached_articles = ArticleRedisService.get_all()
        if cached_articles:
            return cached_articles
        result = super().get_queryset()
        ArticleRedisService.set_all_articles(result)
        return result


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
        serializer.validated_data["article"].update_statics()
        ArticleRedisService.evict_articles()
        DetectAnomaly().detect(new_vote)

    def get_object(self):
        user = self.request.data["user"]
        article = self.request.data["article"]
        article.update_statics()
        ArticleRedisService.evict_articles()
        vote = self.filter_queryset(self.get_queryset()).get(user=user, article=article)
        DetectAnomaly().detect(vote)
        return vote
