## Challenge: What is all this stuff?
Need to read: https://www.thoughtworks.com/en-us/insights/blog/architecture/the-evolution-of-data-lake-table

## Challenge: Bootstrapping
It looks like Iceberg isn't a standalone solution, but rather extends other 
platforms to provide a table structure for big data.
According to the docs, Apache Spark is the most mature implementation and
it is recommended people use that first so that's what I'll do.

## Challenge: Get going locally with Apache Spark


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
