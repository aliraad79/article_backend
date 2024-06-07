from django.contrib import admin
from main.models import Article, User, Vote


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    pass


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
