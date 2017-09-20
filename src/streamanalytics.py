import getopt
from os import sys
from utils import Directory

def add_modules():
    MODULE_PATHS = []
    MODULE_PATHS.append(Directory.current().moveup().path)
    for module_path in MODULE_PATHS:
        sys.path.append(module_path)

def __messagehandler__(message):
    print message

def start_dispatcher_service():
    import datastream
    datastream.start_dispatching(5, 2)

def start_listener_service():
    import datastream
    datastream.start_listening(__messagehandler__)

SERVICES = {"dispatcher": start_dispatcher_service,
            "listener": start_listener_service}

def main(argv):
    srv = None
    try:
        opts, args = getopt.getopt(argv,"hs:",["srv="])
    except getopt.GetoptError:
        print "No such option found!"
        print "main_service.py -s <serviceid>"
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print "main_service.py -s <serviceid>"
            sys.exit()
        elif opt in ("-s", "--srv"):
            srv = arg
    if srv in SERVICES:
        print "Initiating service: ", srv
        SERVICES[srv]()
    else:
        print "No such service has been found!"

if __name__ == "__main__":
    add_modules()
    main(sys.argv[1:])

