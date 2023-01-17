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

## Challenge: Monitoring

- There is a Web UI and REST API for monitoring metrics.
  https://spark.apache.org/docs/latest/monitoring.html
- Grafana & Prometheus

## Challenge: Learning PySpark

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