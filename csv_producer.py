from google.cloud import pubsub_v1      # pip install google-cloud-pubsub  ##to install
import glob                             # for searching for json file
import json
import csv
import os

# Search the current directory for the JSON file (including the service account key)
# to set the GOOGLE_APPLICATION_CREDENTIALS environment variable.
files = glob.glob("*.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = files[0]

# Set the project_id with your project ID
project_id = "eda-project-509219"   # <-- change to your project ID
topic_name = "Design"               # <-- matches the Topic you created
csv_file = "Labels.csv"

# create a publisher and get the topic path for the publisher
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_name)
print(f"Publishing records from {csv_file} to {topic_path}.\n")

# Open and read the CSV file
with open(csv_file, newline='') as f:
    reader = csv.DictReader(f)   # each row becomes a dictionary, keyed by the header row

    for row in reader:
        # row is already a dictionary here, e.g.:
        # {'time': '1768708698.49', 'profileName': 'denver', 'temperature': '31.11', ...}

        # Replace empty strings (missing values in the CSV) with None,
        # so they are serialized as JSON null instead of an empty string.
        row = {k: (v if v != '' else None) for k, v in row.items()}

        # Serialize the dictionary into a JSON string, then encode it to bytes
        # (Pub/Sub messages must be sent as bytes, not as a Python object or plain JSON string)
        message = json.dumps(row).encode('utf-8')

        print("Producing a record:", message)
        future = publisher.publish(topic_path, message)

        # ensure that the publishing has been completed successfully
        future.result()

print("\nAll records have been published.")
