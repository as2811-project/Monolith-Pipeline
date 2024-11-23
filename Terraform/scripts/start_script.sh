#!/bin/bash
sudo yum update -y
cd /home/ec2-user
wget https://downloads.apache.org/kafka/3.9.0/kafka_2.12-3.9.0.tgz
tar -xvf kafka_2.12-3.9.0.tgz
sudo yum install java-1.8.0-amazon-corretto-devel -y
