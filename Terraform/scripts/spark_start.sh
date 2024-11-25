#!/bin/bash
sudo yum update -y
cd /home/ec2-user
wget https://downloads.apache.org/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz
tar -xvf spark-3.5.0-bin-hadoop3.tgz
sudo mv spark-3.5.0-bin-hadoop3 /opt/spark
sudo yum install java-1.8.0-amazon-corretto-devel -y