import cv2 as cv
from os import listdir
import numpy as np
import math
import time
import csv

#read images
def readImg(imgs, path):
    imgRead = []
    for img in imgs:
        imgRead.append(cv.imread(path+img))
    return imgRead

def showImg(imgs):
    for img in imgs:
        cv.namedWindow('img', cv.WINDOW_NORMAL)
        cv.resizeWindow('img', 400, 400)
        cv.imshow('img', img)
        k = cv.waitKey(0)

# função para requantização
def requantiza(bits,imgs):
    newImgs = []
    # 4 bits: 0 - 15
    # Precisamos dividir de 0 a 255 em 16 valores, ou seja, 256/16 = 16, então devemos fazer pixel/16 para requantizar
    # 2 bits: 0 - 3
    # 0 a 255 em 4 valores, ou seja, 256/4 = 64, então devemos fazer pixel/64 para requantizar
    # 1 bit: 0 - 1
    # 256/2 = 128 -> pixel/128
    orig = pow(2,8)
    valores = pow(2,bits)
    razao = int(orig/valores)
    for img in imgs:
        # Para requantizar, devemos fazer o pixel divido pela razão e aproximar a um inteiro
        # Após, devemos multiplicar de volta pela razão para termos novamente 8 bits
        newImgs.append(np.uint8(img / razao) * razao)
    return newImgs
    
def histogram(img):
    rows = len(img)
    col = len(img[0])

    hist = [0]*16
    for i in range(rows):
        for j in range(col):
            hist[int(img[i,j]/16)] += 1
    return hist

def pmfunction(img):
    rows = len(img)
    col = len(img[0])
    n = rows*col
    hist = histogram(img)
    return np.array(hist)/n

def highOrdMom(pmf,pot):
    sum = 0
    for i in range(len(pmf)):
        sum += pow(i*16,pot)*pmf[i]
        # print(sum)
    return sum

def centralMom(pmf,pot):
    mean = highOrdMom(pmf,1)
    sum = 0
    for i in range(len(pmf)):
        sum += pow(i*16-mean,pot)*pmf[i]
    return sum

def average(pmf):
    return highOrdMom(pmf,1)

def variance(pmf):
    sec = highOrdMom(pmf,2)
    media = highOrdMom(pmf,1)
    return sec-pow(media,2)

def deviation(pmf):
    return math.sqrt(variance(pmf))

def skewness(pmf):
    central3 = centralMom(pmf,3)
    desvio3 = math.sqrt(variance(pmf))**3
    return central3/desvio3

def kurtosis(pmf):
    central4 = centralMom(pmf,4)
    desvio4 = math.sqrt(variance(pmf))**4
    return central4/desvio4

def min_and_max(img):
    min = np.min(img)
    max = np.max(img)
    return min, max

def SDR(img):
    min, max = min_and_max(img)
    sdr = (max - min)**2
    return sdr

def shannon_entropy1(pmf):
    sum = 0
    for i in range(len(pmf)):
        if pmf[i] == 0:
            sum += 0
        else:
            #print("p= "+str(pmf[i])+"------- log2= "+str(math.log2(pmf[i])))
            sum += math.log2(pmf[i])*pmf[i]
    entropy = sum*(-1)
    return entropy

# def shannon_entropy2(img):
#     shannon = skimage.measure.shannon_entropy(img)
#     return shannon

def percentile(img, p):
    perc = np.percentile(img, p)
    return perc

def interquartile(img):
    p75 = percentile(img, 75)
    p25 = percentile(img, 25)
    inter = p75 - p25
    return inter

def mediann(pmf):
    cont = 0
    for i in range(len(pmf)):
        if cont+pmf[i]<0.5:
            cont += pmf[i]
        else:
            med = i*16
            break
    return med

def RMS(pmf):
    ave = average(pmf)
    var = variance(pmf)
    rms = math.sqrt(ave**2 + var)
    return rms

def norm_energy(pmf):
    rms = RMS(pmf)
    energy = rms**2
    return energy

def bins_entropy(pmf):
    epsilon = 2.2e-16
    entropy = 0
    for i in range(len(pmf)):
        entropy -= pmf[i]*math.log2(pmf[i]+epsilon)
    return entropy

#Robust Mean Absolute Deviation
def rMAD(img):
    p90 = percentile(img, 90)
    p10 = percentile(img, 10)
    rows = len(img)
    col = len(img[0])
    n = 0
    sum = 0
    for i in range(rows):
        for j in range(col):
            if((img[i,j]>=p10) and (img[i,j]<=p90)):
                n += 1
                sum += abs(img[i,j]-mean)
    rmad = sum/n
    return rmad

def meanAbsDev(img, mean):
    rows = len(img)
    col = len(img[0])
    n = rows*col
    sum = 0
    for i in range(rows):
        for j in range(col):
            sum += abs(img[i,j]-mean)
    mad = sum/n
    return mad

def featuresImgPixels(img, mean):
    p90 = percentile(img, 90)
    p10 = percentile(img, 10)

    rows = len(img)
    col = len(img[0])
    n = rows*col

    mad = 0
    rmad = 0
    cont = 0

    for i in range(rows):
        for j in range(col):
            mad += abs(img[i,j]-mean)
            if((img[i,j]>=p10) and (img[i,j]<=p90)):
                cont += 1
                rmad += abs(img[i,j]-mean)

    mad = mad/n
    rmad = rmad/cont
    return mad, rmad

# --------------------------------------------------------
# MAIN
# --------------------------------------------------------

start = time.time()

file = open('features.csv', 'w', newline='')
writer = csv.writer(file)
header = ['Image', 'Minimum', 'Maximum', 'Squared Dynamic Range', 'Mean', 'Standard Deviation',
          'Variance', 'Skewness', 'Kurtosis', '92.5 Percentile', '85 Percentile', '15 Percentile',
          '7.5 Percentile', 'Interquartile Range', 'Median', 'Shannon Entropy', 'Bins Entropy',
          'Normalized Energy', 'Root Mean Square', 'Mean Absolute Deviation', 'Robust Mean Absolute Deviaton', 'label']

writer.writerow(header)

path = "img_dataset/"
folders = listdir(path)
label = 0
cont = 0

for folder in folders:
    start_folder = time.time()
    cont_folder = 0

    new_path = path+str(folder)+"/"
    images = listdir(new_path)
    imgs = readImg(images, new_path)
    print(folder)
    #showImg(imgs)

    imgsGray = []
    for img in imgs:
        imgsGray.append(cv.cvtColor(img, cv.COLOR_BGR2GRAY))
    #showImg(imgsGray)

    imgs4bits = requantiza(4,imgsGray)
    #showImg(imgs4bits)

    #if folder == "Brazilian_Leaves":
    #    showImg([imgs4bits[3],imgs4bits[4]])

    # FEATURES
    for img in imgs4bits:
        cont += 1
        cont_folder += 1
        #print("Image: "+str(cont))
        index = "Img"+str(cont)
        pmf = pmfunction(img)

        min, max = min_and_max(img)
        squared_dyn_range = SDR(img)
        mean = average(pmf)
        standart_deviation = deviation(pmf)
        var = variance(pmf)
        skew = skewness(pmf)
        kurt = kurtosis(pmf)
        percentile92_5 = percentile(img, 92.5)
        percentile85   = percentile(img, 85)
        percentile15   = percentile(img, 15)
        percentile7_5  = percentile(img, 7.5)
        interquartilerange = interquartile(img)
        median = mediann(pmf)
        shannon = shannon_entropy1(pmf)
        bins = bins_entropy(pmf)
        energy = norm_energy(pmf)
        rms = RMS(pmf)
        mad, rmad = featuresImgPixels(img, mean)

        row = [index, min, max, squared_dyn_range, mean, standart_deviation, var, skew,
               kurt, percentile92_5, percentile85, percentile15, percentile7_5, interquartilerange,
               median, shannon, bins, energy, rms, mad, rmad, label]
        writer.writerow(row)

    label += 1
    end_folder = time.time()
    execution_folder = round(end_folder - start_folder, 2)
    print("The running time for "+ str(cont_folder) +" images was: " + str(execution_folder) + " seconds")

file.close()

end = time.time()
execution_time = round(end - start, 2)
print("The total running time for "+ str(cont) +" images was: " + str(execution_time) + " seconds")
