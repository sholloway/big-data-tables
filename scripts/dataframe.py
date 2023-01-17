from datetime import datetime, date
from pyspark.sql import Row, SparkSession

spark = SparkSession.builder.getOrCreate()
df = spark.createDataFrame([
    (1, 2., 'string1', date(2000, 1, 1), datetime(2000, 1, 1, 12, 0)),
    (2, 3., 'string2', date(2000, 2, 1), datetime(2000, 1, 2, 12, 0)),
    (3, 4., 'string3', date(2000, 3, 1), datetime(2000, 1, 3, 12, 0))
], schema='a long, b double, c string, d date, e timestamp')

# Write some rows to STDOUT.
df.show(5)

# show a record vertically
df.show(1, vertical=True)

# Print the column names
print(df.columns)

# Print the dataframe's schema.
df.printSchema()

# Show the summary of the dataframe (count, mean, stddev, min, max)
df.select("a", "b", "c").describe().show()

# Run SQL against a dataframe.
df.createOrReplaceTempView("tableA")
spark.sql("SELECT count(*) from tableA").show()