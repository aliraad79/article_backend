from django.urls import path
from main.views import ArticleApiView, VoteApiView

urlpatterns = [
    path("v1/articles/", ArticleApiView.as_view()),
    path("v1/articles/vote", VoteApiView.as_view()),
]
