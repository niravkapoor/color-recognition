# import json
from time import sleep
from kafka import KafkaConsumer, KafkaProducer
from kafka.structs import OffsetAndMetadata, TopicPartition
from .init import InitDetect
from django.conf import settings

class KafkaConsProd:
    consumer = None
    def __init__(self):
        print('Running Consumer..')
        self.topic_name = 'image_url'
        self.initDetect = InitDetect()
        
        self.producer = self.connect_kafka_producer()

        # self.consumer.subscribe([self.topic_name])

        
        # while True:
        #     msg = self.consumer.poll(timeout_ms=50000.0)
        #     if msg is None:
        #         continue
        #     else:
        #         print ('msg in consumer', msg)

        # print ('msg in>>>>>>', msg)
        # for msg in self.consumer:
        #     print ('msg in consumer', msg)
            # self.consumer.commit(offsets=[msg.offset], message=["try"])
            # self.consumer.close()
            # self.initDetect.start(settings.MEDIA_ROOT + '/' + msg.value.decode("utf-8"))

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
            _producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(0, 10))
        except Exception as ex:
            print('Exception while connecting Kafka')
            print(str(ex))
        finally:
            return _producer
    
    def check_consumer(self):
        self.consumer = KafkaConsumer(self.topic_name, auto_offset_reset='earliest',
                                bootstrap_servers=['localhost:9092'], api_version=(0, 10), consumer_timeout_ms=1000, enable_auto_commit=True, group_id="my-group")
        lastOffset = None
        for msg in self.consumer:
            lastOffset = msg.offset
            print ('msg in publisher', msg, lastOffset)
        
        self.consumer.close(autocommit=True)
