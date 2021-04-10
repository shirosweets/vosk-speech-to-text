import os
import sys
import wave
import time
import subprocess

from config_speech import config as conf
from src.my_logs import Log
from src.helper_fuctions import timing_ms, timerme
from vosk import Model, KaldiRecognizer, SetLogLevel


result = []
partial = []
final = []


@timerme
def main_vosk_ffmpeg(
        file_path,
        model_path,
        logparse_path,
        pubsubmsgobj):
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
            my_log = Log(logparse_path, "total")
            my_log.save_message_on_log(rec.Result())

            print(rec.Result())
            result.insert(len(result), rec.Result())
            print(f"type rec.Result(): {type(rec.Result())}")
        else:
            # Acá se imprimen sin tiempo las palabras (partes parciales)
            my_log = Log(logparse_path, "parcial")
            my_log.save_message_on_log(rec.PartialResult())

            print(rec.PartialResult())
            print(f"type rec.PartialResult(): {type(rec.PartialResult())}")
            partial.insert(len(partial), rec.PartialResult())

    print(f"rec.FinalResult():\n")
    print(rec.FinalResult())
    final.insert(len(final), rec.FinalResult())

    my_log = Log(logparse_path, "final")
    my_log.save_message_on_log(rec.FinalResult())
    remove_file(file_path)
    prepare_to_elastic(result, partial, final)
    send_ack(pubsubmsgobj)


def prepare_to_elastic(result, partial, final):
    print("\n> Send to elastic")
    print(f"result: {result}\n")
    print(f"partial: {partial}\n")
    print(f"final: {final}\n")


def remove_file(file_path):
    while os.path.exists(file_path):
        os.remove(file_path)


def send_ack(pubsubmsgobj):
    print("\n> Send ACK")
    pubsubmsgobj.ack()
    time.sleep(1)
