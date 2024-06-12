# Article Back-end

This repo is provided to have load resilient back-end for a simple web app that save articles and votes on it

We will use postgres for db and redis for cache
## Installation
make sure you have docker installed. Then
```bash
docker compose up
```

## documentation
### first design
![Design](./docs/design-1.png)
### Finalized data model
![Data model](./docs/final-data-model.png)

## flows
### Add / Update vote
![Add-vote](./docs/add-vote-flow.png)

### Get Articles
![Add-vote](./docs/get-articles.png)