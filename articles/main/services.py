from django.db import transaction
from django.core.cache import cache
from main.models import Article, Vote
from django.db.models import Avg


class ArticleRedis:
    def __init__(self, count: int, avg: float) -> None:
        self.count = count
        self.avg = avg


class ArticleRedisService:

    @classmethod
    def update(cls, article: Article, vote: int):
        with transaction.atomic():
            redis_value = cache.get(article)
            if redis_value:
                cls.update_redis(vote, redis_value, article)

            else:
                cls.set_on_redis(
                    article,
                    article.vote_set.count(),
                    article.vote_set.aggregate(Avg("vote")),
                )

    @classmethod
    def get(cls, article: Article) -> ArticleRedis:
        with transaction.atomic():
            redis_value = cache.get(article)
            if redis_value:
                return redis_value

            else:
                avg_score = article.vote_set.aggregate(Avg("vote"))["vote__avg"]
                return cls.set_on_redis(
                    article,
                    article.vote_set.count(),
                    avg_score if avg_score else 2.5,
                )

    @classmethod
    def update_redis(cls, user_vote, last_value: ArticleRedis, article: Article):
        new_avg_score = ((last_value.count * last_value.avg) + user_vote) / (
            last_value.count + 1
        )
        cls.set_on_redis(article, last_value.count + 1, new_avg_score)

    @classmethod
    def set_on_redis(cls, article, count, avg) -> ArticleRedis:
        result = ArticleRedis(count, avg)
        cache.set(article, result, timeout=5 * 60)
        return result


class DetectAnomaly:
    @classmethod
    def detect(self, vote: Vote):
        print(vote)
        print("Anomaly not detected")
