from celery import shared_task
from main.models import Vote
from django.db.models import Avg, StdDev, Count


@shared_task
def detect_anomalies(article_id):
    votes = Vote.objects.filter(article=article_id)
    avg = votes.aggregate(Avg("vote"))["vote__avg"]
    stddev = votes.aggregate(StdDev("vote"))["vote__stddev"]
    count = votes.aggregate(Count("vote"))["vote__count"]

    # not a attack
    if count < 100:
        return False

    anomalies = []
    threshold = 3
    for vote in votes:
        if stddev > 0:
            z_score = (vote.vote - avg) / stddev
            if abs(z_score) > threshold:
                anomalies.append(vote)

    if anomalies:
        handle_anomalies(anomalies)
        return True

    return False


@classmethod
def handle_anomalies(anomalies):
    for anomaly in anomalies:
        print(f"Anomalous vote detected: {anomaly}")
