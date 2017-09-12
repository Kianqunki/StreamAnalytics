# TEST ENVIRONMENT
## Host Environment
* Hostname      : streamanalytics.cloudapp.net
* SSH           : username@streamanalytics.cloudapp.net:22

## Messaging Component
Kafka, a distributed streaming platform, constitutes the messaging infrastructure of this project. A single node Kafka cluster has been utilized on an Ubuntu Server on Azure. 
Producer & consumer applications will broadcast/receive messages over this server. 

* Kafka Server  : streamanalytics.cloudapp.net:9092
* Zookeeper     : streamanalytics.cloudapp.net:2181