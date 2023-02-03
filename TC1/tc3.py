import cv2 as cv
import sys
from os import listdir
import numpy as np
import matplotlib.pyplot as plt
import math
import skimage
from tabulate import tabulate

#ler imagens
def readImg(imgs):
    imgRead = []
    for img in imgs:
        imgRead.append(cv.imread("8/"+img))
    return imgRead

def showImg(imgs):
    for img in imgs:
        cv.namedWindow('img', cv.WINDOW_NORMAL)
        cv.resizeWindow('img', 400, 400)
        cv.imshow('img', img)
        k = cv.waitKey(0)

#mostrar imagens
# def showImg(imgs,pmfs):
#     i = 0
#     x = np.linspace(0,240,16)
#     for img in imgs:
#         cv.namedWindow('img', cv.WINDOW_NORMAL)
#         #cv.resizeWindow('img', 400, 400)
#         plt.stem(x,pmfs[i])
#         plt.show()
#         # plt.pause(1) # <-------
#         input("<Hit Enter To Close>")
#         plt.close()
#         #plt.pause(0.01)
#         cv.imshow('img', img)
#         k = cv.waitKey(0)
#         i += 1

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

def min_and_max(pmfs):
    min = []
    min.append("Minimum")
    max = []
    max.append("Maximum")
    for pmf in pmfs:
        # print(pmf)
        min.append(np.min(pmf))
        max.append(np.max(pmf))
    return min, max

def SDR(pmfs):
    sdr = []
    sdr.append("Squared Dynamic Range")
    min, max = min_and_max(pmfs)
    for i in range(len(pmfs)):
        aux = (max[i+1] - min[i+1])**2
        sdr.append(aux)
    return sdr

def shannon_entropy(pmfs):
    entropy = []
    entropy.append("Shannon Entropy (1)")
    for pmf in pmfs:
        sum = 0
        for i in range(len(pmf)):
            if pmf[i] == 0:
                sum += 0
            else:
                #print("p= "+str(pmf[i])+"------- log2= "+str(math.log2(pmf[i])))
                sum += math.log2(pmf[i])*pmf[i]
        entropy.append(sum*(-1))
    return entropy

def shannon_entropy1(imgs):
    shannon = []
    shannon.append("Shannon Entropy (2)")
    for img in imgs:
        shannon.append(skimage.measure.shannon_entropy(img))
    return shannon

def percentile(imgs, p):
    '''aux = 240*(p/100)
    perc = []
    perc.append("Percentile "+str(p))
    for img in imgs:
        rows = len(img)
        col = len(img[0])
        n = rows*col
        cont = 0
        for i in range(rows):
            for j in range(col):
                if img[i,j]>=aux:
                    cont += 1
        perc.append(cont/n)'''
    perc = []
    perc.append("Percentile "+str(p))
    for img in imgs:
        perc.append(np.percentile(img, p))
    return perc

def interquartile(imgs):
    inter = []
    inter.append("Interquartile Range")
    p75 = percentile(imgs, 75)
    p25 = percentile(imgs, 25)
    for i in range(len(p75)-1):
        aux = p75[i+1]-p25[i+1]
        inter.append(aux)
    return inter

def mediann(pmfs):
    med = []
    med.append("Median")
    for pmf in pmfs:
        cont = 0
        for i in range(len(pmf)):
            if cont+pmf[i]<0.5:
                cont += pmf[i]
            else:
                med.append(i*16)
                break
    return med

def rms1(pmfs):
    rm = []
    rm.append("Root Mean Square(1)")
    for pmf in pmfs:
        ave = average(pmf)
        var = variance(pmf)
        rm.append(math.sqrt(ave**2 + var))
    return rm

def norm_energy(pmfs):
    energy = []
    energy.append("Normalized Energy")
    rms = rms1(pmfs)
    for i in range(len(pmfs)):
        energy.append(rms[i+1]**2)
    return energy

def rms2(imgs):
    rm1 = []
    rm1.append("Root Mean Square(2)")
    for img in imgs:
        rows = len(img)
        col = len(img[0])
        n = rows*col
        sum = 0
        for i in range(rows):
            for j in range(col):
                sum += (img[i,j]**2)/n
        rm1.append(math.sqrt(sum))
    return rm1

def meanAbsDev1(imgs, pmfs):
    mad = []
    mad.append("Mean Absolute Deviation")
    mean = []
    for pmf in pmfs:
        mean.append(average(pmf))

    x=0
    for img in imgs:
        rows = len(img)
        col = len(img[0])
        n = rows*col
        sum = 0
        for i in range(rows):
            for j in range(col):
                sum += abs(img[i,j]-mean[x])
        mad.append(sum/n)
        x+=1
    return mad

def bins_entropy(pmfs):
    bins = []
    bins.append("Bins Entropy")
    epsilon = 2.2e-16
    for pmf in pmfs:
        entropy = 0
        for i in range(len(pmf)):
            entropy -= pmf[i]*math.log2(pmf[i]+epsilon)
        bins.append(entropy)
    return bins

#Robust Mean Absolute Deviation
def rMAD(imgs):
    rmad = []
    rmad.append("rMAD")
    p90 = percentile(imgs, 90)
    p10 = percentile(imgs, 10)
    cont = 1
    for img in imgs:
        rows = len(img)
        col = len(img[0])
        n = 0
        sum = 0
        for i in range(rows):
            for j in range(col):
                if((img[i,j]>=p10[cont]) and (img[i,j]<=p90[cont])):
                    n += 1
                    sum += abs(img[i,j])
        rmad.append(sum/n)
        cont += 1
    return rmad

# main

images = listdir("8/")
imgs = readImg(images)
#showImg(imgs)

imgsGray = []
for img in imgs:
    imgsGray.append(cv.cvtColor(img, cv.COLOR_BGR2GRAY))
#showImg(imgsGray)

imgs4bits = requantiza(4,imgsGray)
#showImg(imgs4bits)

#calculando pmfs das imagens
pmfs = []
i = 1
for img in imgs4bits:
    print("PMF "+str(i))
    pmfs.append(pmfunction(img))
    i += 1

# showImg(imgs4bits)

# x = np.linspace(0,240,16)
# for pmf in pmfs:
#     plt.stem(x, pmf)
#     plt.xticks(x)
#     plt.show()
#     plt.waitforbuttonpress(1)
#     plt.close()

#calculando metricas

min, max = min_and_max(imgs4bits)

squared_dyn_range = SDR(imgs4bits)

percentile92_5 = percentile(imgs4bits, 92.5)
percentile85   = percentile(imgs4bits, 85)
percentile15   = percentile(imgs4bits, 15)
percentile7_5  = percentile(imgs4bits, 7.5)

interquartilerange = interquartile(imgs4bits)

mean = []
mean.append("Mean")
for pmf in pmfs:
    mean.append(average(pmf))

var = []
var.append("Variance")
for pmf in pmfs:
    var.append(variance(pmf))

desv = []
desv.append("Standart Deviation")
for pmf in pmfs:
    desv.append(deviation(pmf))

skew = []
skew.append("Skewness")
for pmf in pmfs:
    skew.append(skewness(pmf))

kurt = []
kurt.append("Kurtosis")
for pmf in pmfs:
    kurt.append(kurtosis(pmf))

shannon = shannon_entropy(pmfs)
shannon1 = shannon_entropy1(imgs4bits)

bins = bins_entropy(pmfs)

median = mediann(pmfs)

energy = norm_energy(pmfs)

rm1 = rms1(pmfs)
rm2 = rms2(imgs4bits)

mad1 = meanAbsDev1(imgs4bits, pmfs)

rmad = rMAD(imgs4bits)

col_names = ["Features","Img1","Img2","Img3","Img4","Img5"]

data = [min,
        max,
        squared_dyn_range,
        mean,
        var,
        desv,
        skew,
        kurt,
        percentile92_5,
        percentile85,
        percentile15,
        percentile7_5,
        interquartilerange,
        median,
        shannon,
        shannon1,
        bins,
        energy,
        rm1,
        rm2,
        mad1,
        rmad]

print(tabulate(data, headers=col_names, tablefmt="grid"))
