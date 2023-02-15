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
    # print("Length dataset: "+str(n))
    # print("Length trainingDataset: "+str(m))
    aux = random.sample(range(1,n), m)  # select m different numbers in range 1:n
    aux.sort()

    testData = dataset.copy()
    testData.remove(dataset[0])
    trainingData = []
    
    for i in aux:
        trainingData.append(dataset[i])
        testData.remove(dataset[i])

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
        # print(classData)
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

# -----------------------------------
# ------------- MAIN ----------------
# -----------------------------------

dataset = readCsv("Data_Iris.csv")
# dataset = readCsv("../TC4/features.csv")

# numberOfSimu = int(input("Enter qtd tests: "))
numberOfSimu = 10

arrAccuracy = []

for i in range(numberOfSimu):
    trainingData, testData = setTrainingData(0.8, dataset)
    #print(trainingData)
    #print(testData)

    classes = classQtd(trainingData)
    #print('Classes: ' +str(classes))

    nFeat = nFeatures(trainingData)
    #print('Number of Features: ' +str(nFeat))

    means, vars = getMeansVars(trainingData)
    #print("Means: "+str(means))
    #print("Vars: "+str(vars))

    probsClass = classesProbabilities(trainingData)
    #print("Classes Probabilitites: "+str(probsClass))


    pi = math.pi

    accuracy = 0
    for image in testData:

        pFeatClass = np.ones(len(probsClass))
        Pfeatures = 0
        for j in range(len(probsClass)):
            for n in range(nFeat):
                if vars[j,n] == 0:
                    vars[j,n]=0.0000000001
                    
                pFeatClass[j] *= (1/math.sqrt(2*pi*vars[j,n]))*math.exp(-((float(image[n])-means[j,n])**2/(2*vars[j,n])))
            Pfeatures += pFeatClass[j]*probsClass[j]

        #print(pFeatClass)

        pClassFeat = []
        for p in range(len(pFeatClass)):
            pClassFeat.append(round(pFeatClass[p]*probsClass[p]/Pfeatures,4))

        #print(pClassFeat)   #Probabilities of total classes
        c = classCol(trainingData)
        # print(image[c])
        if pClassFeat.index(max(pClassFeat)) == float(image[c]):
            accuracy += 1
        #     print("Acerto")
        # else:
        #     print("Error")

    accuracy = round(accuracy/len(testData),4)
    print('Acc: '+str(accuracy*100)+'%')

    arrAccuracy.append(accuracy)

meanAccuracy = np.round(np.mean(np.array(arrAccuracy)),4)*100
varAccuracy = np.round(np.var(100*np.array(arrAccuracy)),4)
stdesAccuracy = np.round(math.sqrt(varAccuracy),4)
print('Mean Accuracy: '+str(meanAccuracy)+'%')
print('Variance Accuracy: '+str(varAccuracy))
print('Stan. Deviation Accuracy: '+str(stdesAccuracy))