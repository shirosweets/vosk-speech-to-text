import os

from dotenv import load_dotenv

load_dotenv()


PATH_CONFIG_CHANNELS = 'speech-to-text/config/channel_config.py'

#  Channels, if you want add a channel for use this 
#  feature check his channel ID and set his name

#  NOTE Feed ID
FEED_ID = {
    632: {"channel_name": 'CNN Español', "channel_id_prod": 64, "channel_id_beta": 73},
    758: {"channel_name": 'Aristegui Noticias', "channel_id_prod": 124, "channel_id_beta": None},
    766: {"channel_name": 'Global Test', "channel_id_prod": 120, "channel_id_beta": None},
    630: {"channel_name": 'CNN US', "channel_id_prod": 73, "channel_id_beta": 84},
    631: {"channel_name": 'CNN Internacional', "channel_id_prod": None, "channel_id_beta": None}
}

#  NOTE Set ID Channel
CHANNELS = {
    73: 'CNN_ES',  # "CNN ESpañol"
    88: 'CNN_US',  # "CNN Internacional"
    227: 'ARISTEGUI_NOTICIAS'  # "Aristegui Noticias"
}

CHANNELS_ID_PROD = {
    64: 'CNN_ES',
    73: 'CNN_US',
    120: 'GLOBAL_TEST',
    124: 'ARISTEGUI_NOTICIAS'
}

#  NOTE Set Lenguages
LIST_CHANNELS_ES_PROD = [
    'CNN ES',
    'CNN Español',
    'ARISTEGUI NOTICIAS',
    'Aristegui Noticias'
]

LIST_CHANNELS_EN_PROD = [
    'GLOBAL TEST',
    'CNN US',
    'CNN INTERNACIONAL',
    'CNN Internacional'
]
