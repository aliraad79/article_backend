from celery import shared_task
from datetime import datetime, timedelta
from main.models import Vote
from django.db.models import Avg, StdDev, Count


@shared_task
def detect_anomalies(article_id):
    votes = Vote.objects.filter(article=article_id)
    avg = votes.aggregate(Avg("score"))["score__avg"]
    stddev = votes.aggregate(StdDev("score"))["score__stddev"]
    count = votes.aggregate(Count("score"))["score__count"]

    # not a attack
    if count < 100:
        return False

    anomalies = []
    threshold = 1
    for vote in votes:
        if stddev > 0:
            z_score = (vote.score - avg) / stddev
            if abs(z_score) > threshold:
                anomalies.append(vote)

    if anomalies:
        handle_anomalies(anomalies, article_id)
        return True

    return False


def handle_anomalies(anomalies, article_id):
    print(f"FOR OPERATION. Anomalous on article {article_id} found. votes: {anomalies}")
    for vote in anomalies:
        vote.is_disable = True
        vote.disable_unitll = datetime.now() + timedelta(days=1)
        vote.save()


@shared_task
def make_votes_valid():
    votes = Vote.objects.filter(is_disable=True)
    for vote in votes:
        if vote.disable_unitll < datetime.now():
            vote.is_disable = False
            vote.save()
