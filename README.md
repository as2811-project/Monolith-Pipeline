### Scale Replica of TikTok's Monolith Recommender System's Pipeline

I recently started reading TikTok's Monolith research paper and thought I'd replicate the pipeline they built on AWS. In this repo, you will find Terraform files to create an EC2 instance
and install the necessary dependencies (i.e., Kafka, Java) on launch. You will also find a notebook with some code to periodically send a row of data from the 'ratings.dat' file to the Kafka
topic. 

Steps to setup Kafka:

* Once you've created all the resources after executing `terraform apply`, ssh into the instance. The script would have attached a security group allowing any IP address, this is obviously not safe but this was done to avoid issues with my IP getting updated every hour and consequently, causing ssh connections to fail.
* After connecting to the instance, run `cd kafka_2.12-3.9.0` > `bin/zookeeper-server-start.sh config/zookeeper.properties` to start zookeeper.
* Duplicate the session in a new terminal, run `cd kafka_2.12-3.9.0` > `sudo nano config/server.properties`. Here, alter `advertised_listeners` by adding the EC2 instance's public IP
* Duplicate the session again. Now, run `export KAFKA_HEAP_OPTS="-Xmx256M -Xms128M"` followed by `cd kafka_2.12-3.9.0` > `bin/kafka-server-start.sh config/server.properties` to start the Kafka server
* SSH into the instance again, and run `cd kafka_2.12-3.9.0` > `bin/kafka-topics.sh --create --topic user_features --bootstrap-server {ec2-public-ip-add}:9092 --replication-factor 1 --partitions 1` 
* Replicate the session again and start kafka producer and consumer by running `bin/kafka-console-producer.sh --topic user_features --bootstrap-server {ec2-public-ip-add}:9092` and `bin/kafka-console-consumer.sh --topic user_features --bootstrap-server {ec2-public-ip-add}:9092` respectively.
* Run the python notebook to start sending each row of data to the topic. You should be able to see each row on the consumer terminal now.
* Configure a Glue job to join the data being streamed with the movies.dat file on the 'itemId' attribute and write to Redshift.

Data Source:
https://grouplens.org/datasets/movielens/10m/

Monolith:
https://arxiv.org/pdf/2209.07663