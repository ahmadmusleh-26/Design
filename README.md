# Milestone 1 - Data Ingestion System (Cloud Pub/Sub)

## Setup

1. Create a Pub/Sub topic. This code assumes a topic named `Design`.
2. Create a subscription on that topic. This code assumes `Design-sub`.
3. Place your service account key JSON file in the same folder as the scripts.
   It is not included in this repo for security reasons, see `.gitignore`.
4. Set `project_id` in both `csv_producer.py` and `csv_consumer.py` to your own
   GCP project ID.
5. Install the required package:

```
pip install google-cloud-pubsub
```

## How to run

Open two terminals in this folder.

Terminal 1:
```
python csv_consumer.py
```

Terminal 2:
```
python csv_producer.py
```

The consumer needs to be running first so it can pick up the messages as soon
as the producer starts publishing them.

## Discussion

**1. What is EDA? What are its advantages and disadvantages?**

TODO: write your answer here.

**2. Cloud Pub/Sub has two types of subscriptions: push and pull. Describe them, showing the strengths and weaknesses of each based on potential applications.**

TODO: write your answer here.

**3. When publishing a message into a topic, an ordering key can be specified. Using examples, describe the role and benefits of ordering keys.**

TODO: write your answer here.

## Design

`csv_producer.py` reads `Labels.csv` row by row. Each row is converted into a
dictionary using `csv.DictReader`, missing values are replaced with `None`,
the dictionary is serialized to JSON, and the message is published to the
`Design` topic.

`csv_consumer.py` subscribes to `Design-sub`. For each message it receives, it
deserializes the JSON back into a dictionary using `json.loads()` and prints
the values.

TODO: add any additional notes on your own design decisions here, for example
the missing value handling or the message ordering behavior observed while
testing.
