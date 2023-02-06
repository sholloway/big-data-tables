'''
A very simple Spark job designed to be a hello world for working with a Cluster.

To Run (Via Kubernetes Scheduler)
# Run on a Kubernetes cluster in cluster deploy mode

# WIP: This is starting the container but then running longer than I think it probably should.
# Need to look at what the proper design for an executor program is. 

spark-submit \
  --master k8s://http://localhost:8001/ \
  --deploy-mode cluster \
  --executor-memory 1G \
  --num-executors 5 \
  --conf spark.kubernetes.driverEnv.SPARK_MASTER_URL=spark://spark-cluster-master-0.spark-cluster-headless.default.svc.cluster.local:7077 \
  --conf spark.kubernetes.container.image=bitnami/spark:3 \
  --conf spark.kubernetes.file.upload.path=./scripts \
  ./scripts/distributed_calculate_pi.py
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