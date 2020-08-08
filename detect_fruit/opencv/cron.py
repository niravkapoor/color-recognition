from .helper.producer_consumer_kafka import KafkaConsProd
kf = KafkaConsProd()

def cron_job():
    kf.check_consumer()