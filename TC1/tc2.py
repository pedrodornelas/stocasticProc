import cv2 as cv
import sys
from os import listdir
import numpy as np
import matplotlib.pyplot as plt
import math

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

def skewness(pmf):
    central3 = centralMom(pmf,3)
    desvio3 = math.sqrt(variance(pmf))**3
    return central3/desvio3

def kurtosis(pmf):
    central4 = centralMom(pmf,4)
    desvio4 = math.sqrt(variance(pmf))**4
    return central4/desvio4

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
i = 0
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
mean = []
for pmf in pmfs:
    mean.append(average(pmf))

var = []
for pmf in pmfs:
    var.append(variance(pmf))

desv = np.sqrt(var)

skew = []
for pmf in pmfs:
    skew.append(skewness(pmf))

kurt = []
for pmf in pmfs:
    kurt.append(kurtosis(pmf))

print("Média: "+str(mean))
print("Variância: "+str(var))
print("Desvio: "+str(desv))
print("Skewness: "+str(skew))
print("Kurtosis: "+str(kurt))