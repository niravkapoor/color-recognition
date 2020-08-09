import json
from time import sleep
from kafka import KafkaConsumer, KafkaProducer
from kafka.structs import OffsetAndMetadata, TopicPartition
from .init import InitDetect
from django.conf import settings
from .db import DataBase

hostNamePort = 'localhost:9092'

class KafkaConsProd:
    consumer = None
    def __init__(self):
        print('Running Consumer..')
        self.topic_name = 'image_url'
        self.initDetect = InitDetect()
        self.db = DataBase()
        self.producer = self.connect_kafka_producer()

    def publish_message(self, topic_name, key, value):
        try:
            key_bytes = bytes(key, encoding='utf-8')
            value_bytes = bytes(value, encoding='utf-8')
            self.producer.send(topic_name, key=key_bytes, value=value_bytes)
            self.producer.flush()
            print('Message published successfully.')
        except Exception as ex:
            print('Exception in publishing message')
            print(str(ex))


    def connect_kafka_producer(self):
        _producer = None
        try:
            _producer = KafkaProducer(bootstrap_servers=[hostNamePort], api_version=(0, 10))
        except Exception as ex:
            print('Exception while connecting Kafka')
            print(str(ex))
        finally:
            return _producer
    
    def check_consumer(self):
        self.consumer = KafkaConsumer(self.topic_name, auto_offset_reset='earliest',
                                bootstrap_servers=[hostNamePort], api_version=(0, 10), consumer_timeout_ms=1000, enable_auto_commit=True, group_id="my-group")
        lastOffset = None
        for msg in self.consumer:
            lastOffset = msg.offset
            data = json.loads(msg.value.decode("utf-8"))
            print ('msg in publisher', data, lastOffset)
            color = self.initDetect.start(settings.MEDIA_ROOT + '/' + data["url"], data["url"], settings.MEDIA_ROOT)
            print(color)
            self.db.update("update uploads set fruit_name = '{color}' where id = {upload_id} RETURNING id".format(upload_id = data["id"], color = color))
        self.consumer.close(autocommit=True)
