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

def start_broadcasting_service():
    import datastream
    datastream.start_broadcasting(5, 2)

def start_listening_service():
    import datastream
    datastream.start_listening(__messagehandler__)

SERVICES = {"broadcast-service": start_broadcasting_service,
            "listener-service": start_listening_service}

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

