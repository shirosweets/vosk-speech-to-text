import src.parse_messages as pm

from time import sleep
from src import helper_channels as hc
from src.my_elasticsearch_dsl import ElasticClient
from config_speech import channel_config as ch_config
from config_speech import config as conf
from src.helper_fuctions import (
    check_model_en,
    check_model_es,
    download_model_en,
    download_model_es
)


class RunSpeech():
    def run(self):
        try:
            check_en = check_model_en()
            check_es = check_model_es()
            if not check_en[0]:
                print("Downloading model path EN\nPlease wait...")
                download_model_en(conf.PATH_VOSK_MODEL_EN)
            if not check_es[0]:
                print("Downloading model path ES\nPlease wait...")
                download_model_es(conf.PATH_VOSK_MODEL_ES)
            my_process = pm.Process()
            my_process.inialization_messages()
        except KeyboardInterrupt:
            print(f"\n Stopping...")
            raise(e)
        except Exception as e:
            print(f"Have a error {e}")
            raise(e)
