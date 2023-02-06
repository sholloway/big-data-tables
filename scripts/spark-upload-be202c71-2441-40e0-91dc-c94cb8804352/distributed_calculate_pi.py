'''
A very simple Spark job designed to be a hello world for working with a Cluster.

To Run (Via Kubernetes Scheduler)
# Run on a Kubernetes cluster in cluster deploy mode

# WIP
spark-submit \
  --master k8s://http://localhost:8001/ \
  --deploy-mode cluster \
  --executor-memory 1G \
  --num-executors 5 \
  --conf spark.kubernetes.driverEnv.SPARK_MASTER_URL=spark://spark-cluster-master-0.spark-cluster-headless.default.svc.cluster.local:7077 \
  --conf spark.kubernetes.container.image=bitnami/spark:3 \
  --conf spark.kubernetes.file.upload.path=./scripts \
  ./scripts/distributed_calculate_pi.py

# Other examples. TODO: DELETE these.
./bin/spark-submit \
  --class org.apache.spark.examples.SparkPi \
  --master spark://spark-release-master-0.spark-release-headless.default.svc.cluster.local:7077 \
  --num-executors 3 \
  --driver-memory 512m \
  --executor-memory 512m \
  --executor-cores 1 examples/jars/spark-examples_2.12-3.3.1.jar 10

./bin/spark-submit \
  --conf spark.kubernetes.container.image=bitnami/spark:3 \
  --master k8s://https://k8s-apiserver-host:k8s-apiserver-port \
  --conf spark.kubernetes.driverEnv.SPARK_MASTER_URL=spark://spark-master-svc:spark-master-port \
  --deploy-mode cluster \
  ./examples/jars/spark-examples_2.12-3.2.0.jar 1000
'''


import random
from pyspark import SparkContext

def inside(p):
  x, y = random.random(), random.random()
  return x*x + y*y < 1

def main() -> None:    
  sc = SparkContext(appName="EstimatePi")
  NUM_SAMPLES = 1000000
  count = sc.parallelize(range(0, NUM_SAMPLES)).filter(inside).count()
  print("Pi is roughly %f" % (4.0 * count / NUM_SAMPLES))
  sc.stop()

if __name__ == '__main__':
  main()