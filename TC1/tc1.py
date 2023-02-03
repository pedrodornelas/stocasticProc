import cv2 as cv
import sys
from os import listdir
import numpy as np

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


# main

images = listdir("8/")
imgs = readImg(images)
#showImg(imgs)

imgsGray = []
for img in imgs:
    imgsGray.append(cv.cvtColor(img, cv.COLOR_BGR2GRAY))

#showImg(imgsGray)

imgs4bits = requantiza(4,imgsGray)
showImg(imgs4bits)
# print(imgs4bits[3])
# print('\n-------------------------------\n')

imgs2bits = requantiza(2,imgs)
showImg(imgs2bits)
# print(imgs2bits[3])
# print('\n-------------------------------\n')

imgs1bit = requantiza(1,imgs)
showImg(imgs1bit)
# print(imgs1bit[3])
# print('\n-------------------------------\n')
