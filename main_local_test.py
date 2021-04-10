import os
import time
import requests

from zipfile import ZipFile
from src import run_speech as rsp
from config_speech import config as conf
from src.vosk_local import main_vosk_ffmpeg as vff
from src.helper_fuctions import (
    rename_to_model,
    check_model_es,
    download_model_es,
    check_model_en,
    download_model_en,
    extract_model_en,
    extract_model_es,
    remove_old_zip_model
)

if __name__ == "__main__":
    print(f"1 -> pub\n2 -> ffmpeg\n5 -> stop")
    print(f"100 -> test model es\n101 test model en")
    option = int(input("Please select your option: "))
    if(option == 1):
        initial = rsp.RunSpeech(73, 3)
        initial.run()
    elif(option == 2):
        file = input("Please type your relative path file (you can type 1min_en, 1min_es, 6min1_en or 6min_es): ")  # noqa
        if(file == "1min_en"):
            file = 'src/test/1min_EN.mp4'
            model = conf.PATH_VOSK_MODEL_EN
        elif(file == "1min_es"):
            file = 'src/test/1min_ES.mp4'
            model = conf.PATH_VOSK_MODEL_ES
        elif(file == "6min1_en"):
            file = 'src/test/6min1_EN.mp4'
            model = conf.PATH_VOSK_MODEL_EN
        elif(file == "6min2_en"):
            file = 'src/test/6min2_EN.mp4'
            model = conf.PATH_VOSK_MODEL_EN
        elif(file == "6min2_en.flv"):
            file = 'src/test/6min2_EN.flv'
            model = conf.PATH_VOSK_MODEL_EN
        elif(file == "6min_es"):
            file = 'src/test/6min_ES.flv'
            model = conf.PATH_VOSK_MODEL_ES
        else:
            model = input("Please type your model path or language (es, en): ")
            if(model == "es"):
                model = conf.PATH_VOSK_MODEL_ES
            elif(model == "en"):
                model = conf.PATH_VOSK_MODEL_EN
            else:
                model = conf.PATH_VOSK_MODEL_ALL
        vff(file, model)
    elif(option == 100):
        print(f"Option 100\n")
        file_path = "src/test/1min_ES.mp4"

        check = check_model_es()
        if not check[0]:
            print("Downloading...")
            zip_path = download_model_es(conf.PATH_VOSK_MODEL_ES)
            print("Extrating...")
            extract_model_es(zip_path, conf.PATH_VOSK_MODEL_ES)
            remove_old_zip_model(zip_path, conf.PATH_VOSK_MODEL_ES)
        else:
            print("Already exist")
            model_path = conf.PATH_VOSK_MODEL_ES
            vff(file_path, model_path)

        print("Waiting...")
        model_path = conf.PATH_VOSK_MODEL_ES
        vff(file_path, model_path)

    elif(option == 101):
        print(f"Option 101\n")
        file_path = "src/test/1min_EN.mp4"

        check = check_model_en()
        if not check[0]:
            print("Downloading...")
            zip_path = download_model_en(conf.PATH_VOSK_MODEL_EN)
            print("Extrating...")
            extract_model_en(zip_path, conf.PATH_VOSK_MODEL_EN)
            remove_old_zip_model(zip_path, conf.PATH_VOSK_MODEL_EN)
        else:
            print("Already exist")
            model_path = conf.PATH_VOSK_MODEL_EN
            vff(file_path, model_path)

        print("Waiting...")
        model_path = conf.PATH_VOSK_MODEL_EN
        vff(file_path, model_path)
    else:
        print("No option selected")
