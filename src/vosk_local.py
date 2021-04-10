import os
import sys
import wave
import subprocess

from time import time
from my_logs import Log
from vosk import Model, KaldiRecognizer, SetLogLevel


def timerme(func):
    def wrapper(*arg, **kwargs):
        st = time()
        res = func(*arg, **kwargs)
        ed = time()
        print(f"function took: {func.__name__} took {ed-st}")
        return res
    return wrapper


@timerme
def main_vosk_ffmpeg(file_path, model_path, logparse_path=None):
    """
    main_vosk_ffmpeg(file_path, model_path)
    """
    SetLogLevel(0)
    print(f"model_path usado: {model_path}\n")

    if not os.path.exists("config") and not os.path.exists(model_path):
        print("Please configure VOSK Model")
        exit(1)

    sample_rate = 16000
    model = Model(model_path)
    rec = KaldiRecognizer(model, sample_rate)

    process = subprocess.Popen(['ffmpeg', '-loglevel', 'quiet', '-i', file_path, '-ar', str(sample_rate), '-ac', '1', '-f', 's16le', '-'], stdout=subprocess.PIPE)  # noqa

    while True:
        data = process.stdout.read(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            # Acá se imprime con tiempos las palabras
            print(f"rec.AcceptWaveform(data): {rec.AcceptWaveform(data)}")

            # my_log = Log(logparse_path, "parcial")
            # my_log.save_message_on_log(rec.AcceptWaveform(data))

            print(rec.Result())
        else:
            # Acá se imprimen sin tiempo las palabras (partes parciales)
            print(rec.PartialResult())

    print(f"rec.FinalResult():\n")
    print(rec.FinalResult())


main_vosk_ffmpeg("files/global_test/global-test_20210328_231450_a31c8b05.ts", 'config_speech/vosk_config/model_EN/model', 'logs/parse_logs/log_global_test')  # noqa
