import os
import re
import json
import datetime
import src.my_pubsub as ps

from google.cloud import pubsub_v1
from src.helper_channels import (
    check_re_cnn_es,
    check_re_cnn_us,
    check_re_cnn_internacional,
    check_re_aristegui,
    check_re_global_test
)
from src.helper_vosk import (
    get_url_from_download,
    get_filepath_for_channel,
    download_me,
    get_logparse_path_from_channel
)
from src.helper_fuctions import (
    get_channel_language,
    get_model_path,
    timerme
)
from src.run_my_vosk import main_vosk_ffmpeg as local_vosk


class Process():
    """
    Receiving messages from pubsub
    """
    def __init__(self):
        self.subscriber = ps.Subscriber(self.process_message)

    def inialization_messages(self):
        self.subscriber.listen_messages()

    def process_message(self, msgobj):
        try:
            ParseMessages(msgobj)
        except Exception as e:
            print(f"Error my_messages {e}\n")


class ParseMessages():
    """
    Parsing messages from pubsub
    """
    def __init__(self, pubsubmsgobj=None, jsonmsg=None):
        try:
            # NOTE: Depende de cómo lleguen tus mensajes
            my_messages = pubsubmsgobj.data.decode("utf-8")
            my_messages = json.loads(my_messages)
            print(f"\nmy_messages: {my_messages}\n")

            channel_info = my_messages['channel']
            print(f"channel_info: {channel_info}")

            channel_name = channel_info['name']
            print(f"channel_name: {channel_name}")

            channel_feed_id = channel_info['id']
            print(f"channel_feed_id: {channel_feed_id}")

            if(channel_name == "GLOBAL TEST"):
                self.prepare_to_vosk(
                    my_messages,
                    channel_name,
                    channel_feed_id,
                    pubsubmsgobj)
            else:
                print("> No result")
                # No hacer nada, ya que no es lo que nos interesa
                pubsubmsgobj.ack()
        except Exception as e:
            print(f"Error ParseMessages :{e}")

    def get_time_from_pubsub_message(self, timestamp):
        return datetime.datetime.utcfromtimestamp(timestamp)

    @timerme
    def prepare_to_vosk(self, message, channel_name, channel_feed_id, pubsubmsgobj):  # noqa
        try:
            file_name = message['name']
            print(f"file_name: {file_name}")

            start_time = message['start_time']
            print(f"start_time: {start_time}")

            raw_info = message['raw_info']
            print(f"raw_info: {raw_info}")

            end_time = message['end_time']
            print(f"end_time: {end_time}")

            down_url = message['cloud_endpoint']
            print(f"down_url: {down_url}")
        except Exception as e:
            print(f"\nException parse pubsub message: {e}")
            print("\nSend ACK")
            pubsubmsgobj.ack()

        channel_file_path = get_filepath_for_channel(channel_name)

        if channel_file_path is not None:
            file_path_for_down = channel_file_path + '/' + file_name
            print(f"file_name: {file_path_for_down}")
            status = True
            try:
                status = download_me(down_url, file_path_for_down)
            except Exception as e:
                print(f"\nException download: {e}")
                print("\nSend ACK")
                pubsubmsgobj.ack()
            if status:
                print("\nI am ready")
                channel_language = get_channel_language(channel_name)
                model_path = get_model_path(channel_language)
                if(channel_name is not None and model_path != "None"):
                    logparsepath = get_logparse_path_from_channel(channel_name)
                    local_vosk(
                        file_path_for_down,
                        model_path, start_time,
                        end_time,
                        channel_feed_id,
                        channel_name,
                        logparsepath,
                        pubsubmsgobj)
                else:
                    print(f"\nElse, exception with configuration...")
                    print("\nSend ACK")
                    pubsubmsgobj.ack()
            else:
                print(f"\nElse, exception download...")
                print("\nSend ACK")
                pubsubmsgobj.ack()
        else:
            print(f"\nElse, exception channel_file_path...")
            print("\nSend ACK")
            pubsubmsgobj.ack()
