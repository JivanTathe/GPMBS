from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp
import uuid

# Create a SparkSession
spark = SparkSession.builder.appName("CSV to Delta Job").getOrCreate()

# Define input and output paths
input_path = "path/to/csv/files/*.csv"
output_path = "path/to/output/delta/table"

# Read CSV files
csv_options = {"header": "true", "inferSchema": "true"}
csv_df = spark.read.options(**csv_options).csv(input_path)

# Add extra columns
output_df = csv_df.withColumn("ingestion_tms", current_timestamp()).withColumn("batch_id", uuid.uuid4().hex)

# Write output DataFrame to Delta table using append mode
output_df.write.format("delta").mode("append").save(output_path)

# Stop the SparkSession
spark.stop()
