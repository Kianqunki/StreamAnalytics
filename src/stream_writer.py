import json
from kafka import KafkaProducer

class StreamWriter(object):
    def __init__(self, host):
        self.__host__ = host
        self.__streamwriter__ = None

    def write(self, topic, message):
        self.__streamwriter__ = KafkaProducer(bootstrap_servers=[self.__host__],
                                              value_serializer=lambda value:json.dumps(value).encode("utf-8"),
                                              api_version=(0, 10),
                                              request_timeout_ms=30000)
        future_metadata = self.__streamwriter__.send(topic, message)
        future_metadata.get(timeout=60)

# WRITER = StreamWriter("streamanalytics.cloudapp.net:9092")
# WRITER.write("test", "first message")
