from django.db import transaction
from django.core.cache import cache
from main.models import Article, Vote
from django.db.models import Avg


class ArticleRedis:
    def __init__(self, count: int, avg: float) -> None:
        self.count = count
        self.avg = avg


class ArticleRedisService(object):
    def __init__(self) -> None:
        pass

    def update(self, article: Article, vote: int):
        with transaction.atomic():
            redis_value = cache.get(article)
            if redis_value:
                self.update_redis(vote, redis_value, article)

            else:
                self.set_on_redis(
                    article,
                    article.vote_set.count(),
                    article.vote_set.aggregate(Avg("vote")),
                )

    def get(self, article: Article) -> ArticleRedis:
        with transaction.atomic():
            redis_value = cache.get(article)
            if redis_value:
                return redis_value

            else:
                avg_score = article.vote_set.aggregate(Avg("vote"))["vote__avg"]
                return self.set_on_redis(
                    article,
                    article.vote_set.count(),
                    avg_score if avg_score else 2.5,
                )

    def update_redis(self, user_vote, last_value: ArticleRedis, article: Article):
        new_avg_score = ((last_value.count * last_value.avg) + user_vote) / (
            last_value.count + 1
        )
        self.set_on_redis(article, last_value.count + 1, new_avg_score)

    def set_on_redis(self, article, count, avg) -> ArticleRedis:
        result = ArticleRedis(count, avg)
        cache.set(article, result, timeout=5 * 60)
        return result


class DetectAnomaly:
    def __init__(self) -> None:
        pass

    def detect(self, vote: Vote):
        print(vote)
        print("Anomaly not detected")
