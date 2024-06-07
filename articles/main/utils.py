def get_article_avg_redis_key(article_id):
    return f"AVG_{article_id}"

def get_article_count_redis_key(article_id):
    return f"COUNT_{article_id}"