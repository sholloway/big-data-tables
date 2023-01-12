## Challenge: What is all this stuff?
Need to read: https://www.thoughtworks.com/en-us/insights/blog/architecture/the-evolution-of-data-lake-table

## Challenge: Bootstrapping
It looks like Iceberg isn't a standalone solution, but rather extends other 
platforms to provide a table structure for big data.
According to the docs, Apache Spark is the most mature implementation and
it is recommended people use that first so that's what I'll do.

## Challenge: Get going locally with Apache Spark
- Spark runs on Java 8/11/17, Scala 2.12/2.13, Python 3.7+ and R 3.5+.
- 

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
