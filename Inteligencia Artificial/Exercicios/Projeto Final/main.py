#!-*- conding: utf8 -*-
# coding: utf-8
# ======================================================#!-*- conding: utf8 -*-
# coding: utf-8

import sys
import timeit
import numpy as np
import cv2
import glob

def greenRoi(imagesList, imagesListHsv):
    listImgsOut = []

    for i in range(0, len(imagesListHsv)):
        imgOut = np.zeros(
            (imagesListHsv[i].shape[0], imagesListHsv[i].shape[1], 3), imagesListHsv[i].dtype)

        h, s, v = imagesListHsv[i][:, :, 0], imagesListHsv[i][:, :, 1], imagesListHsv[i][:, :, 2]
        remainGreenMask = np.where(np.logical_and(h >= 0.05, h <= 0.4), 1, 0)
        remainGreen = applyMask(imagesList[i], remainGreenMask.astype(np.uint8))
       
        sGreen = np.zeros((s.shape[0], s.shape[1]), s.dtype)
        np.putmask(sGreen, remainGreenMask, s)
        sGreen = np.where(sGreen >= 0.1, 1, 0)
       
        maskGreenLeaf = closeImage(sGreen.astype(np.uint8), 3)
        imgOut = applyMask(imagesList[i], maskGreenLeaf)
        cv2.imwrite(str(i+10)+" - TomatoLeaf.bmp", imgOut * 255)

        listImgsOut.append(imgOut)

    return listImgsOut


def applyMask(img, mask):
    imgOut = np.zeros((img.shape[0], img.shape[1], 3), img.dtype)

    imgOut = cv2.bitwise_and(img, img, mask=mask)

    return imgOut


def closeImage(img, size):
    imgOut = np.zeros((img.shape[0], img.shape[1]), img.dtype)

    element = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (2 * size + 1, 2 * size + 1), (size, size))
    imgOut = cv2.morphologyEx(img, cv2.MORPH_CLOSE, element)

    return imgOut


# ============================================================================================================================
# Metodo principal
# ============================================================================================================================
def main():

    listImages = []
    listImagesHsv = []

    for img in glob.glob("*.JPG"):
        imgG = cv2.imread(img)
        if imgG is None:
            print('Erro abrindo a '+str(i + 1)+' imagem .\n')
        imgG = cv2.cvtColor(imgG, cv2.COLOR_BGR2HSV)
        imgG = imgG.reshape(imgG.shape[0], imgG.shape[1], 3)
        imgG = imgG.astype(np.float32) / 255
        listImagesHsv.append(imgG)
        imgOriginal = cv2.imread(img)
        imgOriginal = imgOriginal.astype(np.float32) / 255
        listImages.append(imgOriginal)

    listImgGreen = greenRoi(listImages, listImagesHsv)


if __name__ == '__main__':
    main()
