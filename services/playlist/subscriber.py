from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

import json
from utils import create_playlist
from models import Group
# from . import engine
import os

# TODO(developer)
project_id = os.getenv('PROJECT_ID', "playlist-parameters")
subscription_id = os.getenv('SUBSCRIBER_PLAYLIST', "playlist-parameters-sub")
# Number of seconds the subscriber should listen for messages
timeout = 5.0

#data = Group(id=1)

pl_dict = {
    "group_id": 1,
    "id": 1,
    "playlist_name": "Test playlist",
    "num_tracks": 80
}

pl_data = json.dumps(pl_dict)

create_playlist(pl_data)

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f"Received {message.data!r}.")

     # Test the data coming in.
    data = json.loads(message.data)

    if message.attributes:
        print("Attributes:")
        for key in message.attributes:
            value = message.attributes.get(key)
            print(f"{key}: {value}")
    
    try:
        create_playlist(data)
        message.ack()
    except Exception as e:
        print("Failed to create playlist", e)


# streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
# print(f"Listening for messages on {subscription_path}..\n")

# # Wrap subscriber in a 'with' block to automatically call close() when done.
# with subscriber:
#     try:
#         # When `timeout` is not set, result() will block indefinitely,
#         # unless an exception is encountered first.
#         streaming_pull_future.result(timeout=timeout) # timeout=timeout
#     except TimeoutError:
#         streaming_pull_future.cancel()  # Trigger the shutdown.
#         streaming_pull_future.result()  # Block until the shutdown is complete.