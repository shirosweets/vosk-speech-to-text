import os
import datetime

from json import dumps
from google.cloud import pubsub_v1
from config_speech import config as conf
from google.api_core.exceptions import AlreadyExists


class Pubsub():
    def __init__(self):
        PROJECT_PATH = "projects/project_name"
        TOPIC_NAME = 'topic_name'
        self.TOPIC_PATH = f"{PROJECT_PATH}/topics/"+TOPIC_NAME
        self.SUBSCRIPTION_PATH = f"{PROJECT_PATH}/subscriptions/"+'topic_name'
        self._set_google_credentials()

    def _set_google_credentials(self):
        print("Pubsub _set_google...")
        credentials_path = conf.FILE_PATH_GOOGLE_CREDENTIALS
        gkey = "GOOGLE_APPLICATION_CREDENTIALS"
        if os.getenv(gkey, default=None) is None:
            try:
                CRED_DIR = os.getcwd() + credentials_path
                os.environ[gkey] = CRED_DIR
            except Exception as e:
                print(f"Error : {e}\n")
                print(f"I can't use {credentials_path}")
                raise(e)


class Subscriber(Pubsub):
    def __init__(self, callback):
        Pubsub.__init__(self)
        self.callback = callback

    def _subscribe(self):
        self.subscriber = pubsub_v1.SubscriberClient()
        self.flow_control = pubsub_v1.types.FlowControl(max_messages=6)
        try:
            self.subscriber.create_subscription(
                name=self.SUBSCRIPTION_PATH,
                topic=self.TOPIC_PATH)
        except AlreadyExists:
            print(f"Already Exists")
        except Exception as e:
            print(f"Error: {e}")
        # Wrap subscriber
        self.f = self.subscriber.subscribe(
            self.SUBSCRIPTION_PATH,
            callback=self.callback,
            flow_control=self.flow_control)

    def listen_messages(self):
        # Wrap subscriber
        self._subscribe()
        with self.subscriber:
            try:
                print("Listening messages...")
                self.f.result()
                print(self.f.result())
            except KeyboardInterrupt:
                self.f.cancel()
                print("\nInterrumpted listening messages...")
            except Exception as e:
                print(f"Error listening messages: {e}")
