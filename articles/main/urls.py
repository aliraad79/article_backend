from django.urls import path
from main.views import VoteApiView

urlpatterns = [
    path("v1/articles/", VoteApiView.as_view())
    # path("v1/articles/<int:article_id>/", admin.site.urls)
]
