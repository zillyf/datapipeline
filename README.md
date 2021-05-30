# The "Wirtemberg" Data Pipeline



## Installation

Clone the repository
```
git clone https://github.com/zillyf/datapipeline.git
cd datapipeline
git checkout Datapipe_v1.7b
sudo ./start_datapipeline
```


Open http://localhost:8000

## Add Datasets
Enter datapipeline directory:

```
python3 nodes/app/dummySender.py
```



## Modules of the Data Pipeline and Basic Architecture

### Search Engine
Web-based user interface.
Backeend  on *FastAPI*

### MongoDB
The Data Pipeline uses *mongoDB* as database to store metadata

### Kafka
Message Broker for the communication between the modules

### Docker Compose
Each module is realized as Docker containers. For orchestration Docker Compose is used
