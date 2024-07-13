# Fetch Data Engineer Take-Home Exercise

## Project Setup

### Prerequisites

1. Install Docker: Follow the instructions for your operating system on the [Docker official website](https://docs.docker.com/get-docker/).
2. Install Docker Compose: Docker Compose is included with Docker Desktop for Windows and macOS. For Linux, follow the instructions on the [Docker Compose installation page](https://docs.docker.com/compose/install/).

### Steps

1. Clone the Repository:
   git clone <repository-url>
   cd fetch-data-pipeline
2. Create docker-compose.yml File: Ensure the docker-compose.yml file is in the root of your project directory.
3. Start Docker Containers

Data Flow
1.Data Ingestion:

Data is ingested into Kafka from a data generator producing messages to the user-login topic.

2.Data Processing:

A Kafka consumer written in Python consumes messages from the user-login topic.
The consumer processes the messages by:
Filtering by device_type (only "android" devices).
Transforming the timestamp from UNIX format to human-readable format.
Aggregating message counts by locale.

3.Data Output:

The processed data is produced to a new Kafka topic named processed-data-topic
