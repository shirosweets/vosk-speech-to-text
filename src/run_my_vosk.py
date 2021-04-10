import os
import sys
import time
import wave
import json
import subprocess

from src.my_logs import Log
from src.helper_fuctions import timerme
from vosk import Model, KaldiRecognizer, SetLogLevel
from src.my_elasticsearch_dsl import ElasticPublisher


@timerme
def main_vosk_ffmpeg(
        file_path,
        model_path,
        startime,
        endtime,
        channel_feed_id,
        channel_name,
        logparse_path=None,
        pubsubmsgobj=None):
    """
    Pubsub -> Vosk -> Elastic
    """
    result = []
    partial = []
    final = []
    wave = []
    SetLogLevel(0)
    print(f"model_path usado: {model_path}\n")

    if not os.path.exists("config") and not os.path.exists(model_path):
        print("Please configure VOSK Model")
        send_ack(pubsubmsgobj)
        exit(1)

    sample_rate = 16000
    model = Model(model_path)
    rec = KaldiRecognizer(model, sample_rate)

    process = get_process(file_path, sample_rate)

    while True:
        data = process.stdout.read(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            # Acá se imprime con tiempos las palabras
            print(f"rec.AcceptWaveform(data): {rec.AcceptWaveform(data)}")
            wave.insert(len(wave), (rec.AcceptWaveform(data)))
            if data == str:
                print("str")
                wave.insert(len(wave), data)

            # my_log = Log(logparse_path, "parcial")
            # my_log.save_message_on_log(rec.AcceptWaveform(data))

            print(rec.Result())
            result.insert(len(result), json.loads(rec.Result()))
        else:
            # Acá se imprimen sin tiempo las palabras (partes parciales)
            print(rec.PartialResult())
            partial.insert(len(partial), json.loads(rec.PartialResult()))
    final.insert(len(final), json.loads(rec.FinalResult()))

    wave.insert(len(wave), (rec.AcceptWaveform(data)))

    remove_file(file_path)
    prepare_to_elastic(
        result,
        partial,
        final,
        wave,
        pubsubmsgobj,
        startime,
        endtime,
        channel_feed_id,
        channel_name)


def get_process(file_path, sample_rate):
    process = subprocess.Popen(['ffmpeg', '-loglevel', 'quiet', '-i', file_path, '-ar', str(sample_rate), '-ac', '1', '-f', 's16le', '-'], stdout=subprocess.PIPE)  # noqa
    return process


def prepare_to_elastic(
        result,
        partial,
        final,
        wave,
        pubsubmsgobj,
        startime,
        endtime,
        channel_feed_id,
        channel_name):
    print("> Send to elastic\n")
    print(f"result: {result}\n")
    print(f"partial: {partial}\n")
    print(f"final: {final}\n")
    print(f"wave: {wave}\n")
    if(len(partial) != 0):
        elastic_client = ElasticPublisher()
        text = partial[-1]  # dict
        sentence = text['partial']
        if(len(sentence) != 0):
            list_words = sentence.split()
            first_word = list_words[0]
            end_word = list_words[-1]
            print(f"first_word: {first_word} - end_word: {end_word}\n")
            # def parse_t_log(
            #   first_word,
            #   first_time,
            #   end_time,
            #   end_word,
            #   channel_feedid,
            #   channel_name,
            #   sentence)
            elastic_client.parse_t_log(
                first_word,
                startime,
                endtime,
                end_word,
                channel_feed_id,
                channel_name,
                sentence)
            print("> Ok\n")
    send_ack(pubsubmsgobj)


def remove_file(file_path):
    while os.path.exists(file_path):
        os.remove(file_path)


def send_ack(pubsubmsgobj):
    print("\n> Send ACK")
    pubsubmsgobj.ack()
    time.sleep(1)
