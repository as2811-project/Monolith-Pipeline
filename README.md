### Scale Replica of TikTok's Monolith Recommender System's Pipeline

I recently started reading TikTok's Monolith research paper and thought I'd replicate the ETL pipeline they built for the system. In this repo, you will find Terraform files to create an EC2 instance
and install the necessary dependencies (i.e., Kafka, Java) on launch. But you can ignore these as I've shelved IaC and AWS as a whole temporarily as I highly doubt I'll stay within the free tier limits.

You will find a notebook with some code to periodically send a row of data from the 'ratings.dat' file to the Kafka
topic. A separate Spark job runs to join the ratings data with the movies metadata (movies.dat) which is preloaded into memory.

To try this out:
* Clone the repo
* Create a `.env` file in the `spark` directory and add your Redshift credentials
* Run `docker compose up`
* Once everything's up and running, run the `payload.ipynb` notebook
* If there are no errors, you will be able to see `MicroBatchExecution` logs on your terminal

Data Source:
https://grouplens.org/datasets/movielens/10m/

Monolith:
https://arxiv.org/pdf/2209.07663

I might figure out a way to deploy this on AWS whilst remaining within the free tier limits later.