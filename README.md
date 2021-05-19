# The "Wirtemberg" Data Pipeline



## Installation

git clone https://github.com/zillyf/datapipeline.git
cd datapipeline
sudo ./start_datapipeline

Open http://localhost:8000


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
