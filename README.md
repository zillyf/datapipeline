# The "Wirtemberg" Data Pipeline



## Installation

Clone the repository
```
git clone https://github.com/zillyf/datapipeline.git
cd datapipeline
```

If you have a fresh ubuntu installation, install docker & docker-compose

```
sudo ./install_dependencies
```

You can now build the required docker images

```
sudo ./build_datapipeline
```

Now, start the datapipeline

```
sudo ./start_datapipeline
```

Open http://localhost (or the URL of your server)

To stop the data pipeline (from inside ```datapipeline``` directory)
```
sudo ./stop_datapipeline
```


To checkout a specific version

```
git pull
git checkout Datapipe_v1.7b
```

## Add Datasets
Enter datapipeline directory:

```
python3 nodes/app/dummySender.py
```



## Modules of the Data Pipeline and Basic Architecture

### Search Engine
Web-based user interface.
Backend  on *FastAPI*

### MongoDB
The Data Pipeline uses *mongoDB* as database to store metadata

### Kafka
Message Broker for the communication between the modules

### Docker Compose
Each module is realized as Docker containers. For orchestration Docker Compose is used

## Known Bugs
### Timeout during startup
During first start, it can take long time to download all required docker images, which might lead to time-outs of different modules
How to solve:
Change the environment parameter ```KAFKA_WAIT_TIME``` in the file ```docker-compose.yml``` and restart the pipeline:
```
sudo ./stop_datapipeline
sudo ./start_datapipeline
```

