# Milestone 1 — Data Ingestion System (Cloud Pub/Sub)

## Setup

Before running the scripts:

1. Create a Pub/Sub topic (this repo's code assumes a topic named `Design`).
2. Create a subscription on that topic (this repo's code assumes `Design-sub`).
3. Place your service account key JSON file in the same folder as the scripts
   (it is **not** included in this repo for security reasons — see `.gitignore`).
4. Set `project_id` in both `csv_producer.py` and `csv_consumer.py` to your own GCP project ID.
5. Install dependencies: `pip install google-cloud-pubsub`

## How to run

Open two terminals in this folder:

```
# Terminal 1
python csv_consumer.py

# Terminal 2
python csv_producer.py
```

## Discussion

**1. What is EDA? What are its advantages and disadvantages?**

_TODO: write your answer here._

**2. Cloud Pub/Sub has two types of subscriptions: push and pull. Describe them, showing the strengths and weaknesses of each based on potential applications.**

_TODO: write your answer here._

**3. When publishing a message into a topic, an ordering key can be specified. Using examples, describe the role and benefits of ordering keys.**

_TODO: write your answer here._

## Design

`csv_producer.py` reads `Labels.csv` row by row, converts each row into a
dictionary (via `csv.DictReader`), replaces empty values with `None`, serializes
it to JSON, and publishes it to the `Design` topic.

`csv_consumer.py` subscribes to `Design-sub`, receives each message, deserializes
it back into a dictionary with `json.loads()`, and prints its values.

_TODO: add any additional notes on your design decisions here (e.g. the
missing-value handling, or the message-ordering observation from testing)._

## Deliverables

- GitHub repo (this one): _add link once pushed_
- Smart meter demo video (~3 min): _add link_
- Design part demo video (~5 min): _add link_
