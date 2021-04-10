import os

from dotenv import load_dotenv

load_dotenv()


# Google Credentials
FILE_PATH_GOOGLE_CREDENTIALS = '/config_speech/service_account.json'

# VOSK CONFIG
# Config Languages
FOLDER_PATH_VOSK_MODELS_LANGUAGES = 'config_speech/vosk_config/'
PATH_VOSK_MODEL_ES = FOLDER_PATH_VOSK_MODELS_LANGUAGES + 'model_ES/model'
PATH_VOSK_MODEL_EN = FOLDER_PATH_VOSK_MODELS_LANGUAGES + 'model_EN/model'
PATH_VOSK_MODEL_ALL = FOLDER_PATH_VOSK_MODELS_LANGUAGES + 'model_ALL/model'
PATH_VOSK_MODEL_PT = FOLDER_PATH_VOSK_MODELS_LANGUAGES + 'model_PT/model'
PATH_VOSK_MODEL_FR = FOLDER_PATH_VOSK_MODELS_LANGUAGES + 'model_FR/model'

# FILES PATH
FILESPATH = 'files'
FILEPATH_GLOBAL_TEST = FILESPATH + '/global_test'

# PARSE LOGS PATH
LOGPARSEPATH = '/parse_logs'
LOGPARSEPATH_GLOBAL_TEST = LOGPARSEPATH + '/log_global_test/'
