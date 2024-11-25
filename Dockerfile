# Base image for Spark
FROM bitnami/spark:3.5

# Switch to root user to run apt-get commands
USER root

# Set the working directory inside the container
WORKDIR /opt/spark

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Copy Spark job files and other resources to the container
COPY ./spark/ /opt/spark/

# Copy the requirements.txt from the root directory to the container
COPY requirements.txt /opt/spark/
COPY ml-10M100K/movies.csv /opt/spark/

# Install Python dependencies
RUN pip install --no-cache-dir -r /opt/spark/requirements.txt
