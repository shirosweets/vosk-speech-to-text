from datetime import datetime
from dateutil.parser import isoparse
from elasticsearch_dsl import (
    connections,
    Date,
    Document,
    Object,
    Text,
    Keyword,
    Integer,
    Search
    )
from elasticsearch.exceptions import RequestError
from config_speech import elasticsearch_dsl_config as elastic_conf


class ElasticClient(object):
    _client = None
    _indexes = []

    @classmethod
    def get_client(cls, index):
        if not ElasticClient._client:
            print("No ElasticClient")
            hosts = elastic_conf.HOST_ELASTIC
            ElasticClient._client = connections.create_connection(hosts=hosts)

        if index not in ElasticClient._indexes:
            print("No index en ElasticClient")
            ElasticClient._client.indices.create(
                index=index,
                ignore=400
            )
            ElasticClient._indexes.append(index)
        return ElasticClient._client


class Table(Document):
    """
    first_word: Text()

    first_time: Date()

    end_time: Date()

    end_word: Text()

    channel_id: Integer()

    channel_name: Text()

    sentence: Text()
    """
    # 1er palabra de la frase
    first_word = Text(analyzer='snowball', fields={'raw': Keyword()})
    # incio de cuando se comienza a "hablar" (t de la 1ra palabra de la frase)
    first_time = Date()
    # final de cuando se termina de "hablar" (t de la n-1 palabra de la frase)
    end_time = Date()
    # n-1 palabra de la frase
    end_word = Text(analyzer='snowball', fields={'raw': Keyword()})
    channel_id = Integer()
    channel_name = Text(analyzer='snowball', fields={'raw': Keyword()})
    # "frase"
    sentence = Text(analyzer='snowball', fields={'raw': Keyword()})

    class Index:
        name = elastic_conf.INDEX_ELASTIC


class ElasticPublisher():

    def __init__(self):
        self.client = ElasticClient.get_client(elastic_conf.INDEX_ELASTIC)
        try:
            Table.init()
        except RequestError:
            print(f"Error RequestError on ElasticPublisher")
            pass

    def _save_my_t_elastic(
        self,
        first_word,
        first_time,
        end_time,
        end_word,
        channel_id,
        channel_name,
        sentence
    ):
        """
        first_word,

        first_time,

        end_time,

        end_word,

        channel_id,

        channel_name,

        sentence
        """
        table = Table(
            first_word=first_word,
            first_time=first_time,
            end_time=end_time,
            end_word=end_word,
            channel_id=channel_id,
            channel_name=channel_name,
            sentence=sentence
        )
        try:
            r = table.save()
            print(f"save() {r}")
        except Exception as e:
            print(f"Exception {e}")

    def parse_t_log(self, first_word, first_time, end_time, end_word, channel_id, channel_name, sentence):  # noqa
        """
            Reading and listening from
            pubsub -> parse -> new parse -> prepare to send to elastic -> send
        """
        self._save_my_t_elastic(
            first_word,
            first_time,
            end_time,
            end_word,
            channel_id,
            channel_name,
            sentence)
