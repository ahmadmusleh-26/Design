from google.cloud import pubsub_v1      # pip install google-cloud-pubsub  ##to install
import glob                             # for searching for json file
import json
import os

# Search the current directory for the JSON file (including the service account key)
# to set the GOOGLE_APPLICATION_CREDENTIALS environment variable.
files = glob.glob("*.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = files[0]

# Set the project_id with your project ID
project_id = "eda-project-509219"          # <-- change to your project ID
topic_name = "Design"                      # <-- matches the Topic you created
subscription_id = "Design-sub"             # <-- matches the Subscription ID you created

# create a subscriber for the project using the subscription_id
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

print(f"Listening for messages on {subscription_path}..\n")


# A callback function for handling received messages
def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    # Deserialize: convert the received bytes back into a string, then
    # parse that JSON string back into a Python dictionary
    record = json.loads(message.data.decode('utf-8'))

    print("Consumed record:")
    for key, value in record.items():
        print(f"  {key}: {value}")
    print()

    # Report to Google Pub/Sub that the message has been successfully processed
    message.ack()


with subscriber:
    # The callback function will be called automatically for each message
    # received from the topic through the subscription.
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
