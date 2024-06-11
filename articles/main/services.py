from django.core.cache import cache
from main.models import Vote


class ArticleRedisService:
    CACHE_NAME = "Articles"

    @classmethod
    def get_all(cls):
        return cache.get(cls.CACHE_NAME)

    @classmethod
    def set_all_articles(cls, value, ttl=60 * 60):
        return cache.set(cls.CACHE_NAME, value, timeout=ttl)

    @classmethod
    def evict_articles(cls):
        return cache.delete(cls.CACHE_NAME)


class DetectAnomaly:
    @classmethod
    def detect(self, vote: Vote):
        print(vote)
        print("Anomaly not detected")
