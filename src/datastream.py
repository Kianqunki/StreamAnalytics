import time
from datasets.edgar import edgar
from stream_writer import StreamWriter
from stream_reader import StreamReader

TOPIC = "test"
HOST = "streamanalytics.cloudapp.net:9092"

def start_broadcasting(num_of_messages, interval):
    DATASET = edgar.DATASET.head(num_of_messages)
    WRITER = StreamWriter(HOST)

    for row in DATASET.iterrows():
        message = row[1].to_dict()
        time.sleep(interval)
        WRITER.write(TOPIC, message)
        print "Message with ID=" + str(row[0]) + " has been dispatched..."
    
    print "All messages have been dispatched!"

def start_listening(message_handler):
    READER = StreamReader(TOPIC, HOST)
    READER.start(message_handler)
