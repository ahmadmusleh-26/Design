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

### 1. What is EDA? What are its advantages and disadvantages?

Event-Driven Architecture (EDA) is a software design pattern where different
parts of a system communicate by producing and reacting to events, instead of
calling each other directly. A component that generates data (a producer)
publishes an event, and any component that needs it (a consumer) subscribes
and reacts on its own schedule. In this milestone, the smart meter script
published random sensor readings as events, and a separate consumer script
picked them up independently, without the two programs being directly
connected.

The main advantage of EDA is decoupling. Producers and consumers do not need
to know about each other, so each part of the system can be built, deployed,
and scaled independently. This makes the system easier to extend, since a new
consumer can be added later without touching the producer's code.

The main disadvantage is complexity. Because the flow of data is no longer a
simple sequence of function calls, it becomes harder to trace what happens
step by step, which makes debugging more difficult. There is also no
guarantee of message order by default, something we observed directly while
testing the CSV producer and consumer, so systems that depend on strict
ordering need extra care.

### 2. Push vs. pull subscriptions

In a pull subscription, the consumer application connects to Pub/Sub and asks
for messages whenever it is ready to process them. This is what we used in
this milestone: the consumer script stays running and keeps requesting new
messages as they arrive. The advantage is that the application controls the
pace at which it receives messages. The disadvantage is that the application
has to stay running at all times to receive messages without delay.

In a push subscription, Pub/Sub sends each message directly to a web address
(an endpoint) chosen by the developer, instead of waiting for the application
to ask for it. This means the application does not need to run constantly,
which works well for serverless setups. The disadvantage is that the
application needs a public web address that can reliably receive these
messages, and it has less control over how fast messages arrive.

### 3. Ordering keys

Cloud Pub/Sub does not guarantee message order by default. This is confirmed
by Google's own documentation. We saw this in our testing: the producer
published CSV rows in order, but a few early messages arrived much later than
expected.

An ordering key can fix part of this problem. It is a string attached to each
message. Messages with the same key are guaranteed to arrive in order.
Messages with different keys are not guaranteed to arrive in any particular
order relative to each other.

The benefit of ordering keys is that they give ordering only where it is
actually needed. Related messages stay in order, but unrelated messages can
still be delivered and processed at the same time, in parallel. This means we
do not have to give up speed just to get ordering for the messages that need
it.

For example, we could use the profileName field (denver, boston, losang) as
the ordering key. This would keep each city's readings in order. But a denver
message and a boston message could still arrive in any order, since they use
different keys. This still allows fast, parallel processing overall.

## Design

`csv_producer.py` opens `Labels.csv` and reads it row by row using
`csv.DictReader`, which turns each row into a dictionary keyed by the CSV
header (time, profileName, temperature, humidity, pressure). Any missing
value in a row (an empty string in the CSV) is replaced with `None`, so it
becomes a proper `null` once serialized, instead of an empty string that
would be hard to distinguish from real data. Each dictionary is then
serialized with `json.dumps()` and encoded to bytes, since Pub/Sub requires
messages to be sent as bytes. The script publishes the message to the
`Design` topic and waits for `future.result()` before moving to the next row,
to confirm the message was actually published successfully.

`csv_consumer.py` subscribes to `Design-sub`. For each message it receives, it
deserializes the JSON back into a dictionary using `json.loads()` and prints
the values.

A couple of design notes from building and testing this:

- The CSV data has several missing values (for example, some rows have no
  humidity or pressure reading). These are converted from empty strings to
  `None` before publishing, so they come through as `null` in JSON instead of
  an ambiguous empty string.
- While testing, message order was not always preserved. A few of the
  earliest published rows arrived after most of the later rows had already
  been consumed. This matches the ordering behavior discussed in question 3
  above, and confirms that ordering keys would be needed if this data
  depended on strict delivery order.
