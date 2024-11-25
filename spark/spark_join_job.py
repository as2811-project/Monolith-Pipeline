import os
from dotenv import load_dotenv
from pyspark.sql import SparkSession
from pyspark.sql.functions import expr, from_json, col
from pyspark.sql.types import StructType, StructField, IntegerType, LongType, FloatType, StringType

load_dotenv()

# Redshift connection details
redshift_url = os.getenv("REDSHIFT_URL")
redshift_user = os.getenv("REDSHIFT_USER")
redshift_password = os.getenv("REDSHIFT_PASSWORD")
redshift_table = os.getenv("REDSHIFT_TABLE")

# Initialize Spark session
spark = SparkSession.builder \
    .appName("RedshiftTest") \
    .config("spark.jars", "spark/redshift-jdbc42-2.1.0.31.jar") \
    .getOrCreate()

# Read from Kafka stream
kafka_stream = (
    spark
    .readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", os.getenv("SPARK_KAFKA_BROKER", "monolith-kafka:29092"))
    .option("subscribe", "user_features")
    .option("startingOffsets", "latest")
    .load()
)

# Cast Kafka value to STRING
kafka_json = kafka_stream.withColumn("value", expr("cast(value as STRING)"))

# Define schemas
schema = StructType([
    StructField("userId", IntegerType(), True),
    StructField("itemId", IntegerType(), True),
    StructField("rating", FloatType(), True),
    StructField("timestamp", LongType(), True),
])

metadata_schema = StructType([
    StructField("itemId", IntegerType(), True),
    StructField("title", StringType(), True),
    StructField("genre", StringType(), True),
])

metadata_df = spark.read.csv("movies.csv", schema=metadata_schema, header=True)

streaming_df = kafka_json.withColumn("values_json", from_json(col("value"), schema)).selectExpr("values_json.*")
enriched_user_data = streaming_df.join(metadata_df, on="itemId", how="left")

# Write enriched user data to Redshift
def write_to_redshift(batch_df, batch_id):
    """Function to write each batch of the streaming DataFrame to Redshift."""
    batch_df.write \
        .format("jdbc") \
        .option("url", redshift_url) \
        .option("dbtable", redshift_table) \
        .option("user", redshift_user) \
        .option("password", redshift_password) \
        .option("driver", "com.amazon.redshift.jdbc42.Driver") \
        .mode("append") \
        .save()

# Add the foreachBatch function to the streaming query
query = (
    enriched_user_data
    .writeStream
    .foreachBatch(write_to_redshift)
    .outputMode("append")
    .start()
)

query.awaitTermination()
