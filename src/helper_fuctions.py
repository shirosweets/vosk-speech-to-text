import os
import sys
import errno
import shutil
import pathlib
import requests
import subprocess
import config_speech.constants
import config_speech.config as conf
import config_speech.channel_config as ch_conf

from time import time
from shutil import rmtree
from zipfile import ZipFile
from .my_logs import Logger as logger
from datetime import datetime, timezone
from tempfile import NamedTemporaryFile
from timeit import default_timer as timer


# NOTE Time

def timing_ms(f):
    def wrap(*args):
        time1 = time()
        ret = f(*args)
        time2 = time()
        print(
            '{:s} function took {:.3f} ms'
            .format(f.__name__, (time2 - time1) * 1000.0))
        try:
            [f.__name__] = round(time2 - time1, 4)
        except Exception as e:
            pass
        return ret
    return wrap


def timerme(func):
    def wrapper(*arg, **kwargs):
        st = time()
        res = func(*arg, **kwargs)
        ed = time()
        print(f"function took: {func.__name__} took {ed-st}")
        return res
    return wrapper


def utc_datetime(dateobj: datetime):
    return datetime.fromtimestamp(dateobj.timestamp(), timezone.utc)


# NOTE Files

def does_file_exist(fullpath):
    try:
        with open(fullpath):
            it_exists = True
    except FileNotFoundError as e:
        print(e)
        it_exists = False
    return it_exists


def append_file_create_folders(fullpath, msg):
    if not os.path.exists(os.path.dirname(fullpath)):
        try:
            os.makedirs(os.path.dirname(fullpath))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    with open(fullpath, 'a') as f:
        f.write(msg)
        f.write('\n')


def convert_size(size, unit):
    if unit == 'KB':
        size = size >> 10
    elif unit == 'MB':
        size = size >> 20
    elif unit == 'GB':
        size = size >> 30
    return size


def create_file_from_string(string, filetype):
    local_file = NamedTemporaryFile(suffix="."+filetype).name
    with open(local_file, 'w') as fd:
        string.seek(0)
        shutil.copyfileobj(string, fd)
    return local_file


def upload_from_filename(self, source_file, destination_name):
    local_filename = source_file
    filename = destination_name
    self.filename = filename
    path = pathlib.Path(filename)
    self.__check_dir(path)
    tempfile = "/tmp/{}".format(path.name)
    sftp = self.client.open_sftp()
    sftp.put(local_filename, tempfile)
    self.client.exec_command(
        "mv {} {}/{}".format(
            tempfile,
            self.config['dir'],
            filename)
        )
    url = self._build_url()
    if 'backup' in self.config and self.config['backup']:
        self._backup_from_filename(local_filename, destination_name)
    return url


def remove_local_file(file):
    subprocess.call(["rm", file])


def update_string(self, url, string):
    filetype = url.split('.')[-1]
    parts = url.split('/')
    local_filename = create_file_from_string(string, filetype)
    remote_output_file = '/'.join(parts[4:])
    filename = self.config['bucket'] + "/" + remote_output_file
    self.filename = filename
    path = pathlib.Path(filename)
    self.__check_dir(path)
    tempfile = "/tmp/{}".format(path.name)
    sftp = self.client.open_sftp()
    sftp.put(local_filename, tempfile)
    self.client.exec_command(
        "mv {} {}/{}".format(
            tempfile,
            self.config['dir'],
            filename)
        )
    url = self._build_url()
    remove_local_file(local_filename)
    # logger.info("ovh update string:{0}".format(url))
    return url


def __check_dir(self, path):
    self.client.exec_command(
        "mkdir -p {}/{}".format(
            self.config['dir'],
            path.parents[0])
        )


# NOTE Lenguage

def check_language(str):
    """
    input: str

    return [bool, dict]

    bool: soported from feature

    dict: [str1, str2] -> str1: name of languague on Spanish,
    str2: name of languague on English
    """
    if(str == config_speech.constants.EN):
        return [True, config_speech.constants.EN]
    elif(str == config_speech.constants.ES):
        return
    else:
        return [False, str]


def get_channel_language(channel_name):
    """
    return languaguee as iso format

    return "None" if don't have
    """
    for channel in ch_conf.LIST_CHANNELS_EN_PROD:
        if(channel_name == channel):
            return "EN"
    for channel in ch_conf.LIST_CHANNELS_ES_PROD:
        if(channel_name == channel):
            return "ES"
    return "None"


# NOTE Models

def get_model_path(iso_lenguage):
    """
    return language path model

    return "None" if don't have
    """
    if(iso_lenguage == "EN"):
        return conf.PATH_VOSK_MODEL_EN
    elif(iso_lenguage == "ES"):
        return conf.PATH_VOSK_MODEL_ES
    else:
        return "None"


def rename_to_model(old_file, model_path):
    print("in process")


def remove_old_zip_model(zip_path, model_path):
    while os.path.exists(zip_path) and os.path.exists(model_path):
        os.remove(zip_path)


def check_model_en():
    """
    return [bool, model_path]

    bool: exist
    """
    if os.path.exists(conf.PATH_VOSK_MODEL_EN):
        return [True, conf.PATH_VOSK_MODEL_EN]
    else:
        return [False, conf.PATH_VOSK_MODEL_EN]


def download_model_en(model_path):
    """
    return zip_path
    """
    if not os.path.exists(model_path):
        print("\n...")
        try:
            url = 'https://alphacephei.com/vosk/models/vosk-model-en-us-aspire-0.2.zip'  # noqa
            r = requests.get(url, allow_redirects=True)
            open(
                'config_speech/vosk_config/model_EN/vosk-model-en-us-aspire-0.2.zip',  # noqa
                'wb').write(r.content)
            zip_path = 'config_speech/vosk_config/model_EN/model.zip'
            os.rename(
                'config_speech/vosk_config/model_EN/vosk-model-en-us-aspire-0.2.zip',  # noqa
                zip_path)
            return zip_path
        except Exception as e:
            print(f"Exception download_model_en: {e}")


def extract_model_en(zip_path, model_path):
    while not os.path.exists(model_path):
        print("Waiting for extract model...")
        with ZipFile(zip_path, 'r') as zipObj:
            # Extrae todo el conteneido del archivo
            # zip en un directorio diferente
            zipObj.extractall(model_path[0:35])  # Acá va el directorio destino
            # print(model_path[0:35])
            print("File is unzipped in temp folder")
            try:
                os.rename(
                    'config_speech/vosk_config/model_EN/vosk-model-en-us-aspire-0.2.zip',  # noqa
                    model_path)
            except Exception as e:
                print(f"{e}")
            zipObj.close()


def check_model_es():
    """
    return [bool, model_path]

    bool: exist
    """
    if os.path.exists(conf.PATH_VOSK_MODEL_ES):
        return [True, conf.PATH_VOSK_MODEL_ES]
    else:
        return [False, conf.PATH_VOSK_MODEL_ES]


def download_model_es(model_path):
    """
    return zip_path
    """
    if not os.path.exists(model_path):
        print("\n...")
        try:
            url = 'https://alphacephei.com/vosk/models/vosk-model-small-es-0.3.zip'  # noqa
            r = requests.get(url, allow_redirects=True)
            open('config_speech/vosk_config/model_ES/vosk-model-small-es-0.3.zip', 'wb').write(r.content)  # noqa
            zip_path = 'config_speech/vosk_config/model_ES/model.zip'
            os.rename(
                'config_speech/vosk_config/model_ES/vosk-model-small-es-0.3.zip',  # noqa
                zip_path)
            return zip_path
        except Exception as e:
            print(f"Exception download_model_en: {e}")


def extract_model_es(zip_path, model_path):
    while not os.path.exists(model_path):
        print("Waiting for extract model...")
        with ZipFile(zip_path, 'r') as zipObj:
            # Extrae todo el conteneido del archivo
            # zip en un directorio diferente
            zipObj.extractall(model_path[0:35])  # Acá va el directorio destino
            # print(model_path[0:35])
            print("File is unzipped in temp folder")
            try:
                os.rename(
                    'config_speech/vosk_config/model_ES/vosk-model-small-es-0.3',  # noqa
                    model_path)
            except Exception as e:
                print(f"{e}")
            zipObj.close()


def clear_all_models():
    """
    Remove all files vosk models
    """
    print("¿Do you want to remove all models?\nType 'yes (y)' or 'no (n)'")
    option = input()
    if("yes" == option or "y" == option):
        try:
            rmtree(conf.PATH_VOSK_MODEL_ES+"/")
            rmtree(conf.PATH_VOSK_MODEL_EN+"/")
        except Exception:
            pass
        print("All models removed :)")
    else:
        exit(1)


def clear_files_channel():
    """
    Remove all files from channel_file
    """
    print("Wait")
