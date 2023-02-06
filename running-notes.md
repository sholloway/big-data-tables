## Challenge: What is all this stuff?

Need to read: https://www.thoughtworks.com/en-us/insights/blog/architecture/the-evolution-of-data-lake-table

## Challenge: Bootstrapping

It looks like Iceberg isn't a standalone solution, but rather extends other
platforms to provide a table structure for big data.
According to the docs, Apache Spark is the most mature implementation and
it is recommended people use that first so that's what I'll do.

## Challenge: Get going locally with Apache Spark

- Spark runs on Java 8/11/17, Scala 2.12/2.13, Python 3.7+ and R 3.5+.
- Need to install a specific version of Java
  With Nix 2.0 there is fetchTarball and fetchGit.
  Can download the Zulu derivation and override it
- After lots of monkeying around I realized that python 3.11 isn't supported
  with Spark 3.3.1. There is a [PR](https://github.com/apache/spark/pull/38987) that adds support that has been merged
  by the Spark team for Spark 3.4. Unfortunately, I don't know when 3.4 will
  be done.

## Challenge: Trying to get Apache Iceberg installed locally.

I've been trying to get this going using Nix. However there isn't
a binary on Nix repo.
After trying to install Iceberg from the GitHub release I realized that
Iceberg is a Java Jar based application. My options are:

- Build the Jars from source.
- Find built jars on a repo such as Maven Central
  https://mvnrepository.com/artifact/org.apache.iceberg
- Use a Docker image.

## Challenge: Can I work with Python in this space or do I need to use Java?

- https://pypi.org/project/pyspark/

## Challenge: Running a Standalone Spark Cluster

- Architecture: https://spark.apache.org/docs/latest/cluster-overview.html
- https://spark.apache.org/docs/latest/spark-standalone.html

## Challenge: Spark Cluster running on K8

https://spark.apache.org/docs/latest/running-on-kubernetes.html

## Considerations for Production Clusters

- Leverage Zookeeper for managing standby master nodes.
- https://spark.apache.org/docs/latest/security.html
- Log rotation
- Scaling the number of nodes vs scaling the number of pods.
- AWS EKS Scaling Guide: https://aws.github.io/aws-eks-best-practices/

## Challenge: Monitoring

- There is a Web UI and REST API for monitoring metrics.
  https://spark.apache.org/docs/latest/monitoring.html
- Kubernetes ships with a dashboard.
- Grafana & Prometheus

## Challenge: Learning Spark RDD

Key Modules:

- Spark RDDs
- Spark DataFrame
- Spark Streaming and Structured
- Spark MLlib
- Spark ML
- Graph Frames

Common Use Cases

-

- Use the SparkContext class to generate a SparkSession object that acts as a
  proxy with the cluster.

```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName(‘rev’).getOrCreate()
``
- After building the session, use Catalog to see what data is used in the cluster.
  spark.catalog.listTables()
```

### Key Data Structure: RDD
- RDD stands for resilient distributed dataset.
- RDDs can recover from node failure.
- _Shared variables_ can be used to pass data to functions across multiple cluster nodes.
  Shared variables can be a _broadcast variable_, which are used as a cache across
  the cluster, or _accumulators_ which are used to implement counters and sums.
- There are two ways to create RDDs: parallelizing an existing collection in your driver program, or referencing a dataset in an external storage system, such as a shared filesystem, HDFS, HBase, or any data source offering a Hadoop InputFormat.
  
**Creating an RDD from a Collection**
```python
from pyspark import SparkContext, SparkConf
conf = SparkConf().setAppName(appName).setMaster(master)
sc = SparkContext(conf=conf)

# Create an RDD (i.e. a data set that can be worked on in parallel from a collection.)
data = [1, 2, 3, 4, 5]
distData = sc.parallelize(data)
```

- One important parameter for parallel collections is the number of partitions to 
cut the dataset into. Spark will run one task for each partition of the cluster. 
- Typically you want 2-4 partitions for each CPU in your cluster. 
- Spark tries to set the number of partitions automatically based on your cluster. 
  However, you can also set it manually by passing it as a second parameter to 
  parallelize (e.g. sc.parallelize(data, 10)).

**Creating an RDD from an external data source**
```python
from pyspark import SparkContext, SparkConf
conf = SparkConf().setAppName(appName).setMaster(master)
sc = SparkContext(conf=conf)
# create the RDD from a text file.
distFile = sc.textFile("data.txt")
```
- If using a path on the local filesystem, the file must also be accessible at 
  the same path on worker nodes. Either copy the file to all workers or use a 
  network-mounted shared file system.
- All of Spark’s file-based input methods, including textFile, support running 
  on directories, compressed files, and wildcards as well. For example, you can 
  use textFile("/my/directory"), textFile("/my/directory/*.txt"), and 
  textFile("/my/directory/*.gz").

**RDD Operations**
- _Transformations_: Creates a new dataset from an operation. Transformations are 
  lazily computed. By default transformations are computed each time an action 
  is run on it. However, transformations may be saved using the _persist_ method
  or _cache_.
- _Actions_: Returns a value to the driver program after running a computation on a dataset.

**Example of Lazy Computation**
```python
# An RDD is created from a text file.
# This dataset is not loaded in memory or otherwise acted on: lines is merely a pointer to the file.
lines = sc.textFile("data.txt")

# Define lineLengths as the result of a map transformation. LineLengths is not 
# immediately computed, due to laziness.
lineLengths = lines.map(lambda s: len(s))

# Run the reduce action. At this point Spark breaks the computation into tasks 
# to run on separate machines, and each machine runs both its part of the map 
# and a local reduction, returning only its answer to the driver program.
totalLength = lineLengths.reduce(lambda a, b: a + b)

# If we also wanted to use lineLengths again later, we could run 
# lineLengths.persist() before running reduce.
```

### Shared Variables

Broadcast variables a way to create a read-only copy of data for all the executors.
This is done by calling the `SparkContext.broadcast(v)`.
```python
# Create the shared variable.
broadcastVar = sc.broadcast([1, 2, 3])

# Access it's value
broadcastVar.value
# outputs [1, 2, 3]

# To clear the variable from the cache.  If the broadcast is used again 
# afterwards, it will be re-broadcast.
broadcastVar.unpersist()

# To permanently remove the variable.
broadcastVar.destroy()
```

Leverage [accumulators](https://spark.apache.org/docs/latest/rdd-programming-guide.html#accumulators)
for collecting counters or sums across distributed workers. 
An accumulator is created from an initial value v by calling `SparkContext.accumulator(v)`.

```python
# Create a accumulator.
accum = sc.accumulator(0)

# Increment the accumulator across the executors.
sc.parallelize([1, 2, 3, 4]).foreach(lambda x: accum.add(x))

# Access the value of the accumulator.
# The value should be 10.
```

The default accumulator data type is an integer. We can create custom accumulators
by subclassing AccumulatorParam.

## Challenge: Learning Spark SQL, DataFrames, and Datasets
- The same execution engine is used for the various Spark APIs (RDD, SQL, DataFrames, etc)
  so you can switch between then in a single program.
- Spark SQL can run SQL commands but also be used to query a Hive database.
- The various shells (spark-shell, pyspark shell, etc) can be used to run Spark SQL
  queries.

**Datasets and Data Frames**
- A _Dataset_ is a distributed collection of data. It is newer than RDD. It provides 
  the strengths of RDDs with the flexibility of Spark SQL's optimized execution engine.
- The Dataset API is available in Scala and Java. Python does not have the 
  support for the Dataset API. But due to Python’s dynamic nature, many of the 
  benefits of the Dataset API are already available (i.e. you can access the 
  field of a row by name naturally row.columnName). The case for R is similar.
- A DataFrame is a Dataset organized into named columns.
- DataFrames can be constructed from a wide array of sources such as: structured
  data files, tables in Hive, external databases, or existing RDDs. 
- The DataFrame API is available in Scala, Java, Python, and R.

DataFrames are powerful. They enable running SQL on them by defining a temporary view.
```python
# Register the DataFrame as a SQL temporary view
df.createOrReplaceTempView("people")

# The query result is a new dataframe
sqlDF = spark.sql("SELECT * FROM people")

# Dump the dataframe to STDOUT.
sqlDF.show()
```


## Challenge: Learning Stream Processing with Spark
Spark Streaming has been deprecated. The replacement is the Structured Streaming engine.

By default, Structured Streaming queries are processed using a micro-batch 
processing engine, which processes data streams as a series of small batch jobs 
thereby achieving end-to-end latencies as low as 100 milliseconds and exactly-once 
fault-tolerance guarantees. The newer _Continuous Processing_ engine can achieve
end-to-end latencies as low as 1 millisecond. The continuous processing engine
is still in experimental status.


## Challenge: Learning Spark ML
TODO

## Challenge: Understand the Hive Use Cases
TODO

## Challenge: Apache Presto
PrestoDB or just Presto is a query engine.

## Challenge: Finding Data to work with

- [Netflix Daily Top 10 Movie/TV Show in the United States from 2020 - Mar 2022](https://www.kaggle.com/datasets/prasertk/netflix-daily-top-10-in-us)
- NYTimes Data Sets?
- [Global Warming Data](https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data)
- [Climate Data](https://www.globalchange.gov/browse/datasets)
- [UCI Machine Learning Repository by the University of California Irvine](https://archive.ics.uci.edu/ml/index.php)
- [Awesome Public Datasets](https://github.com/awesomedata/awesome-public-datasets)
- [Pew Research Center](https://www.pewresearch.org/internet/datasets/)
- [Buzzfeed Datasets](https://github.com/orgs/BuzzFeedNews/repositories?type=all)
- [Data Set Search](https://data.world/search)
- [StackOverflow Developer Survey](https://insights.stackoverflow.com/survey)
  I choose to use StackOverflow's Annual Developer Survey data. I picked this
  because:

1. I've been following the survey for years so I'm familiar with the results and
   I find it interesting.
2. The dataset is large enough that it makes sense to use Spark and will present
   challenges with working with the data.
3. The dataset spans from 2011 to 2022 enabling some trend analysis.

## Challenge: Working with the StackOverflow Data
I need to:
- Try processing the files as CSV.
- Try converting the files to Parquet and then do the same processing.
- Create Iceberg tables on top of Parquet.
- Linear Regression forecast of the popularity of Python.

Process
1. Create a table for each year's worth of data. 
2. Create a table that maps each year's columns to their question.
3. Convert 2011 - 2016 data so it can be used with the other years.
4. Track the popularity of Python vs Java over time from 2011 to 2022.


# Challenge: Leverage a Python Ray cluster to attempt the same use cases.
Spark is the go to solution for distributed data processing. Try leveraging 
Python's Ray to handle the same use cases.
- [Ray Tutorial](https://towardsdatascience.com/modern-parallel-and-distributed-python-a-quick-tutorial-on-ray-99f8d70369b8)
- [Ray Docs](https://docs.ray.io/en/latest/)

# Challenge: How would one use Spark to process requests from a web application?
This use case should leverage the replicated storage levels for fast fault recovery. 
All the storage levels provide full fault tolerance by recomputing lost data, 
but the replicated ones let you continue running tasks on the RDD without waiting 
to recompute a lost partition.

# Challenge: How does one benchmark and profile Spark jobs?
I want to be able to understand the performance trade offs of using CSV vs Parquet
vs ORC. What are the ways of doing this?

# Challenge: Interact with a Spark cluster with the PySpark REPL
TODO