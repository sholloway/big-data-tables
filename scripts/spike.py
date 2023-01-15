import findspark
findspark.init()

import random
from pyspark import SparkContext

def inside(p):
  x, y = random.random(), random.random()
  return x*x + y*y < 1

sc = SparkContext(appName="EstimatePi")
NUM_SAMPLES = 1000000
count = sc.parallelize(range(0, NUM_SAMPLES)).filter(inside).count()
print("Pi is roughly %f" % (4.0 * count / NUM_SAMPLES))
sc.stop()

# def main() -> None:    
  

# if __name__ == '__main__':
#   main()