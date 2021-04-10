import os
import re
import wget
import urllib3
import requests

from hashlib import md5

# TODO TEST
LOGPATH = 'logs'
NOLOGPATH = 'no/'

FILESPATH = 'files'
FILEPATH_CNN_ES = FILESPATH + '/cnn_es'
FILEPATH_CNN_US = FILESPATH + '/cnn_us'
FILEPATH_ARISTEGUI = FILESPATH + '/aristegui'
FILEPATH_CNN_INTER = FILESPATH + '/cnn_inter'
FILEPATH_GLOBAL_TEST = FILESPATH + '/global_test'

# TODO Move to config
LOGPARSEPATH = '/parse_logs'
LOGPARSEPATH_CNN_ES = LOGPARSEPATH + '/log_cnn_es/'
LOGPARSEPATH_CNN_US = LOGPARSEPATH + '/log_cnn_us/'
LOGPARSEPATH_CNN_INTER = LOGPARSEPATH + '/log_cnn_inter/'
LOGPARSEPATH_ARISTEGUI = LOGPARSEPATH + '/log_aristegui/'
LOGPARSEPATH_GLOBAL_TEST = LOGPARSEPATH + '/log_global_test/'


# NOTE Files for VOSK
def get_url_from_download(message):
    print("get_url_from_download()")
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"  # noqa
    search_url = re.findall(regex, message)
    urls = [x[0] for x in search_url]
    return urls[0]


def get_filepath_for_channel(channel_name):
    if(channel_name == "CNN INTERNACIONAL"):
        return FILEPATH_CNN_INTER
    elif(channel_name == "CNN US"):
        return FILEPATH_CNN_US
    elif(channel_name == "CNN ES"):
        return FILEPATH_CNN_ES
    elif(channel_name == "ARISTEGUI"):
        return FILEPATH_ARISTEGUI
    elif(channel_name == "GLOBAL TEST"):
        return FILEPATH_GLOBAL_TEST
    else:
        return None


def download_me(url, filepathchannel):
    print(f"*** url: {url}, filepathchannel: {filepathchannel} ***")
    try:
        status = wget.download(url, filepathchannel)
        print("\n")
        if status:
            return True
    except Exception as e:
        print(f"Exception: {e}")
        return False


def get_logparse_path_from_channel(channel_name):
    if(channel_name == "CNN INTERNACIONAL"):
        return LOGPARSEPATH_CNN_INTER
    elif(channel_name == "CNN US"):
        return LOGPARSEPATH_CNN_US
    elif(channel_name == "CNN ES"):
        return LOGPARSEPATH_CNN_ES
    elif(channel_name == "ARISTEGUI"):
        return LOGPARSEPATH_ARISTEGUI
    elif(channel_name == "GLOBAL TEST"):
        return LOGPARSEPATH_GLOBAL_TEST
    else:
        return None


def get_key(dictionary):
    iv = dictionary['key']['iv']
    uri = dictionary['key']['uri']

    if iv is not None:
        key_file = f"/tmp/{iv}.key"
    else:
        key_file = f"/tmp/{md5(uri.encode()).hexdigest()}.key"

    try:
        with open(key_file, 'rb') as f:
            key = f.read()
        return key
    except FileNotFoundError:
        r = requests.get(
            uri,
            headers=dictionary['download']['headers'],
            stream=True,
            verify=False
        )

        if r.status_code == requests.codes.ok:
            with open(key_file, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
    with open(key_file, 'rb') as f:
        key = f.read()
    return key


def decrypt_file(filepath, dictionary):
    if dictionary['key']:
        key = get_key(dictionary)
        iv = bytes.fromhex(dictionary['key']['iv'][2:])
        decryptor = AES.new(key, AES.MODE_CBC, IV=iv)

        with open(filepath, "rb") as f:
            data = f.read()

        with open(filepath, 'wb') as f:
            dec_data = decryptor.decrypt(data)
            f.write(dec_data)
