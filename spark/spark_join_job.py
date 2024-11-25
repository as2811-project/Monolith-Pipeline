import os
from dotenv import load_dotenv
from pyspark.sql import SparkSession
from pyspark.sql.functions import expr, from_json, col
from pyspark.sql.types import StructType, StructField, IntegerType, LongType, FloatType
from traitlets import Float

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
    .config("spark.jars", "spark/spark-sql_2.12-3.5.3.jar") \
    .getOrCreate()

# Read from Kafka stream
kafka_stream = (
    spark
    .readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "user_features")
    .option("startingOffsets", "latest")
    .load()
)

# Cast Kafka value to STRING
kafka_json = kafka_stream.withColumn("value", expr("cast(value as STRING)"))

# Define the schema to match the JSON structure
schema = StructType([
    StructField("userId", IntegerType(), True),
    StructField("itemId", IntegerType(), True),
    StructField("rating", FloatType(), True),
    StructField("timestamp", LongType(), True),
])

# Parse JSON and extract fields
streaming_df = kafka_json.withColumn("values_json", from_json(col("value"), schema)).selectExpr("values_json.*")

# Write the output to the console
query = (
    streaming_df
    .writeStream
    .format("console")
    .outputMode("append")
    .start()
)

query.awaitTermination()
