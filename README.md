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

Event-Driven Architecture (EDA) is a software design pattern where different parts of a system communicate by producing and reacting to events, instead of calling each other directly. A component that generates data (a producer) publishes an event, and any component that needs it (a consumer) subscribes and reacts on its own schedule. In this milestone, the smart meter script published random sensor readings as events, and a separate consumer script picked them up independently, without the two programs being directly connected.

The main advantage of EDA is decoupling. Producers and consumers do not need to know about each other, so each part of the system can be built, deployed, and scaled independently. This makes the system easier to extend, since a new consumer can be added later without touching the producer's code.

The main disadvantage is complexity. Because the flow of data is no longer a simple sequence of function calls, it becomes harder to trace what happens step by step, which makes debugging more difficult. There is also no guarantee of message order by default, something we observed directly while testing the CSV producer and consumer, so systems that depend on strict ordering need extra care.

**2. Cloud Pub/Sub has two types of subscriptions: push and pull. Describe them, showing the strengths and weaknesses of each based on potential applications.**

In a pull subscription, the consumer application connects to Pub/Sub and asks for messages whenever it is ready to process them. This is what we used in this milestone: the consumer script stays running and keeps requesting new messages as they arrive. The advantage is that the application controls the pace at which it receives messages. The disadvantage is that the application has to stay running at all times to receive messages without delay.

In a push subscription, Pub/Sub sends each message directly to a web address (an endpoint) chosen by the developer, instead of waiting for the application to ask for it. This means the application does not need to run constantly, which works well for serverless setups. The disadvantage is that the application needs a public web address that can reliably receive these messages, and it has less control over how fast messages arrive.

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
