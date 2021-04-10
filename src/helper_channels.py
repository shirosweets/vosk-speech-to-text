import re
import json
import config_speech.channel_config as config_channel


# NOTE feedId channels

# NOTE id channels

def exist_channel_by_ID(id):
    exist = config_channel.CHANNELS.get(id)
    if exist is not None:
        return True
    else:
        return False


def get_channel_name_by_ID(id):
    if exist_channel_by_ID(id):
        channel_name = config_channel.CHANNELS[id]
        return channel_name
    else:
        return None


def get_lenguage_channel_by_FeedID(feedId):
    """
    return srt

    return None if don't have lenguage
    """
    for c_id in config_channel.LIST_CHANNELS_ES:
        if(c_id == id):
            return "ES"
    for c_id in config_channel.LIST_CHANNELS_EN:
        if(c_id == id):
            return "EN"
    return "None"


def add_new_channel(id, name):
    if not exist_channel_by_ID(id):
        config_channel.CHANNELS[str(name)] = id
    else:
        print(f"You can't add this channel because already exists")


def change_channel_name(id, newname):
    if exist_channel_by_ID(id):
        config_channel.CHANNELS[id] = str(newname)
        print(f"New name set for id: {id} -> {config_channel.CHANNELS[id]}")
    else:
        print(f"You can't rename a channel that does not exist with id: {id}")


def delete_channel_by_ID(id):
    """
    return bool

    True: removed, False: no removed
    """
    if exist_channel_by_ID(id):
        return True
    else:
        return None


# NOTE re channels
def check_re_cnn_us(message):
    if(re.search("(CNN US)", message)):
        return True
    else:
        return False


def check_re_cnn_es(message):
    if(re.search("(cnn-espanol)", message)):
        return True
    else:
        return False


def check_re_cnn_internacional(message):
    if(re.search("(CNN Internacional)", message)):
        return True
    else:
        return False


def check_re_aristegui(message):
    if(re.search("(Aristegui Noticias)", message)):
        return True
    else:
        return False


def check_re_global_test(message):
    if(re.search("(Global Test)", message)):
        return True
    else:
        return False
