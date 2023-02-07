'''
A very simple Spark job designed to be a hello world for working with a Cluster.

To Run (Via Kubernetes Scheduler)
# Run on a Kubernetes cluster in cluster deploy mode

# WIP: This is starting the container but then running longer than I think it probably should.
# Need to look at what the proper design for an executor program is. 

# Cluster Mode
spark-submit \
  --master k8s://http://localhost:8001/ \
  --deploy-mode cluster \
  --executor-memory 1G \
  --num-executors 5 \
  --conf spark.kubernetes.driverEnv.SPARK_MASTER_URL=spark://spark-cluster-master-0.spark-cluster-headless.default.svc.cluster.local:7077 \
  --conf spark.kubernetes.container.image=bitnami/spark:3 \
  --conf spark.kubernetes.file.upload.path=/tmp/distributed_pi \
  scripts/distributed_calculate_pi.py

# Client Mode
spark-submit \
  --master k8s://http://localhost:8001/ \
  --deploy-mode client \
  --conf spark.kubernetes.driverEnv.SPARK_MASTER_URL=spark://spark-cluster-master-0.spark-cluster-headless.default.svc.cluster.local:7077 \
  --conf spark.kubernetes.container.image=bitnami/spark:3 \
  scripts/distributed_calculate_pi.py

A few things to note:
- deploy-mode: Whether to deploy your driver on the worker nodes (cluster) or 
  locally as an external client (client) 
- spark.kubernetes.file.upload.path determines where the file will be uploaded to on the pod.

When this connects it starts the SparkUI on port 4040.
localhost:4040
'''


import random
from pyspark import SparkContext

def inside(p):
  x, y = random.random(), random.random()
  return x*x + y*y < 1
 
sc = SparkContext(
  appName="EstimatePi", 
  master="spark://spark-cluster-master-0.spark-cluster-headless.default.svc.cluster.local:7077"
)
NUM_SAMPLES = 1000000
count = sc.parallelize(range(0, NUM_SAMPLES)).filter(inside).count()
print("Pi is roughly %f" % (4.0 * count / NUM_SAMPLES))
sc.stop()