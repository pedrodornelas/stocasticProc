import csv
import random
import numpy as np
import math

def readCsv(file):
    f = open(file, 'r')
    csvreader = csv.reader(f)
    aux = []
    for row in csvreader:
        aux.append(row)
    f.close
    return aux

def setTrainingData(trainingRate, dataset):
    n = len(dataset)-1 # delete line 1
    m = round(n*trainingRate)
    print("Length dataset: "+str(n))
    print("Length trainingDataset: "+str(m))
    aux = random.sample(range(1,n), m)  # select m different numbers in range 1:n
    aux.sort()

    trainingData = []
    testData = dataset
    for i in aux:
        print("i: "+str(i))
        print("len: "+str(len(testData)))
        print(dataset[i])
        trainingData.append(dataset[i])
        testData.remove(testData[i])

    return trainingData, testData

def nFeatures(dataset):
    return len(dataset[0])-1

def classCol(dataset):
    return len(dataset[0])-1

def classQtd(dataset):
    n = len(dataset[0])-1
    data = np.array(dataset)
    colClass = data[: , n] # select classes column
    return np.unique(colClass)

def getMeansVars(dataset):
    nFeat = nFeatures(dataset)
    classes = classQtd(dataset)

    means = []
    vars = []
    for i in classes:
        classData = np.array(classDataset(i, dataset))
        #print(classData)
        meansFeatures = []
        varsFeatures = []
        for i in range(nFeat):
            feat = np.single(classData[: ,i])
            meanFeat = np.round(np.mean(feat),4)
            varFeat = np.round(np.var(feat),4)
            meansFeatures.append(meanFeat)
            varsFeatures.append(varFeat)
        means.append(meansFeatures)
        vars.append(varsFeatures)
    return np.array(means), np.array(vars)

def classesProbabilities(dataset):
    classes = classQtd(dataset)
    n = len(dataset)
    col = classCol(dataset)
    data = np.array(dataset)[: ,col]
    p = []
    for cl in classes:
        sum = np.count_nonzero(data == cl)
        p.append(round(sum/n,4))
    return np.array(p)

def classDataset(c, dataset):
    cDataset = []
    col = classCol(dataset)
    for row in dataset:
        if row[col] == c:
            cDataset.append(row)
    return cDataset

def pClass(c, dataset):
    cont = 0
    n = len(dataset)
    colClass = len(dataset[0])-1
    nFeatures = colClass
    means = np.zeros(nFeatures)
    for row in dataset:
        if row[colClass] == str(c):
            cont += 1
            for i in range(nFeatures):
                means[i] += float(row[i])

    return round(cont/n,4), np.round(means/cont,4)

# -----------------------------------
# ------------- MAIN ----------------
# -----------------------------------

dataset = readCsv("Data_Iris.csv")
# dataset = readCsv("../TC4/features.csv")

trainingData, testData = setTrainingData(0.8, dataset)
#print(trainingData)
#print(testData)

classes = classQtd(trainingData)
print('Classes: ' +str(classes))

nFeat = nFeatures(trainingData)
print('Number of Features: ' +str(nFeat))

means, vars = getMeansVars(trainingData)
print("Means: "+str(means))
print("Vars: "+str(vars))

probs = classesProbabilities(trainingData)
print("Classes Probabilitites: "+str(probs))



pi = math.pi
# pFeatClass = (1/math.sqrt(2*pi*vars[0,0]))*math.exp(-(()/()))


# p0, means0 = pClass(0, trainingData)
# p1, means1 = pClass(1, trainingData)
# p2, means2 = pClass(2, trainingData)

# p = [p0,p1,p2]

# print(np.array([means0,means1, means2]))

# print(p)