import requests

BASE_URL = "http://localhost:8000/api/v1"

# create a target article
article_id = requests.post(BASE_URL + "/articles/", data={"title": "TARGET"}).json()[
    "id"
]

# create 100 users
for user_name in range(1000):
    requests.post(BASE_URL + "/users/", data={"name": str(user_name)})
    # each user vote target article a bad review
    requests.post(
        BASE_URL + "/articles/vote/",
        data={"user": user_name, "article": article_id, "vote": 1},
    )
