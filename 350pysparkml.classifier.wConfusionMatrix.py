from __future__ import print_function
#!echo $PYTHON_PATH
import os, sys
#import path
from pyspark.sql import *

from pyspark.ml.classification import MultilayerPerceptronClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# create spark sql session
spark = SparkSession\
    .builder\
    .appName("Logistic Curve classification with pySparkML") \
    .config("spark.executor.instances", 4 ) \
    .config("spark.executor.memory", "4g") \
    .config("spark.executor.cores", 2) \
    .config("spark.yarn.access.hadoopFileSystems","hdfs://gromit:8020/tmp/")\
    .getOrCreate()


# Load training data
data = spark.read.format("libsvm").load("curves.svm")
    #.load("hdfs://gromit:8020/tmp/logicurvesSVM/logicurvesSVM")
# Split the data into train and test
splits = data.randomSplit([0.6, 0.4], 1234)
train = splits[0]
train.cache()
train.count()
train.take(5)
test = splits[1]
# specify layers for the neural network:
# input layer of size 121 (features) each sample of the curve is a feature
# , two intermediate of size 121 and 121
# and output of size 7 - the random generator must have had one 0 value.
layers = [121, 60,60, 7]
# create the trainer and set its parameters
trainer = MultilayerPerceptronClassifier(maxIter=100,\
                                         layers=layers, \
                                         blockSize=32, \
                                         tol=1E-6, \
                                         seed=1234)
# train the model
model = trainer.fit(train)
# compute accuracy on the test set
result = model.transform(test)
predictionAndLabels = result.select("prediction", "label")
evaluator = MulticlassClassificationEvaluator(metricName="accuracy")
print("Accuracy: " + str(evaluator.evaluate(predictionAndLabels)))

#!pip3 install sklearn
import numpy as np
from sklearn.metrics import confusion_matrix
# confusion (ytrue, ypredicted)
confusing=confusion_matrix(  np.array(result.select("label").collect() ),np.array(result.select("prediction").collect()) ) 
## This is a confusion-matrix and yes it is confusing
# big numbers on the diagonal are good, any numbers off the
# diagonal are missed classifications in the testing data
#Confusion matrix whose i-th row and j-th column entry 
#indicates the number of samples with true label 
#being i-th class and predicted label being j-th class.
print ( confusing )