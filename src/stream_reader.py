from threading import Thread
from kafka import KafkaConsumer

class StreamReader(object):
    def __init__(self, topic, host):
        self.__topic__ = topic
        self.__host__ = host
        self.__streamreader__ = None
        self.__stopping__ = False

    def __start__(self, message_handler):
        self.__streamreader__ = KafkaConsumer(self.__topic__,
                                              bootstrap_servers=[self.__host__],
                                              api_version=(0, 10), group_id=None)
        for message in self.__streamreader__:
            message_handler(message.value)
            if self.__stopping__:
                self.__streamreader__.close()
                break

    def start(self, message_handler):
        # thread = Thread(target=self.__start__, args=[message_handler])
        # thread.start()
        self.__start__(message_handler)

    def stop(self):
        pass
