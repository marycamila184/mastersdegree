#!-*- conding: utf8 -*-
# coding: utf-8
# ======================================================#!-*- conding: utf8 -*-
# coding: utf-8
# ===============================================================================
# Tarefa - Contar arroz em diferentes imagens
# -------------------------------------------------------------------------------
# Autor: Mary Camila
# ===============================================================================

import sys
import timeit
import numpy as np
import cv2
import glob


# ============================================================================================================================
# Metodo para a chamada de os outros metodos para processar as imagens antes da manipulacao das bordas
# ============================================================================================================================
def processingImages(imagesList):
    listImgsOut = []

    for i in range(0, len(imagesList)):
        imgBackground = np.zeros((imagesList[i].shape[0], imagesList[i].shape[1], 1), imagesList[i].dtype)

        # Usa o filtro da mediana para borrar todas as imagens
        imgBackground = medianFilter(imagesList[i], 121)
        # cv2.imwrite((str(i)+' - APMediana.png'), imgBackground * 255)

        # Removo o fundo da imagem original para ficar somente com o arroz
        img = subtractionImages(imagesList[i], imgBackground)
        # cv2.imwrite((str(i)+' - BSub.png'), img * 255)

        # Binarizacao para criar a mascara e retornar somente o arroz
        imgBin = binarizeImage(img, 0.15)
        # cv2.imwrite((str(i)+' - CMask.png'), imgBin * 255)

        # Aplico a mascara para selecionar os graos de arroz
        imgRice = applyMaskImage(img, imgBin)
        # cv2.imwrite((str(i)+' - DRice.png'), imgRice * 255)

        # Operacao de abertura para remover ruidos
        imgOpened = openImage(imgRice, 1)
        # cv2.imwrite((str(i)+' - EOp.png'), imgOpened * 255)

        # Normalizada para realcar as diferencas de contraste e ter um padrao de contraste para todas as imagens
        imgOut = normalizeImage(imgOpened)
        # cv2.imwrite((str(i)+' - Norm.png'), imgOut * 255)

        listImgsOut.append(imgOut)

    return listImgsOut


def medianFilter(img, size):
    imgOut = np.zeros((img.shape[0], img.shape[1], 1), img.dtype)

    # Filtro da mediana para remover o fundo
    imgOut = cv2.medianBlur((img*255).astype(np.uint8), size)
    imgOut = imgOut.reshape(imgOut.shape[0], imgOut.shape[1], 1)
    imgOut = imgOut.astype(np.float32) / 255

    return imgOut


def subtractionImages(img1, img2):
    imgOut = np.zeros((img1.shape[0], img1.shape[1], 1), img1.dtype)

    # Subtraindo as imagens
    imgOut = np.subtract(img1, img2)
    imgOut = np.clip(imgOut, 0, 1)  # Truncando em 1

    return imgOut


def binarizeImage(img, threshold):
    imgOut = np.zeros((img.shape[0], img.shape[1], 1), img.dtype)

    # Binarizo a imagem baseado no threshold passado por parametro
    imgOut = np.where(img > threshold, 1, 0)
    imgOut = imgOut.reshape(imgOut.shape[0], imgOut.shape[1], 1)
    imgOut = imgOut.astype(np.float32)
    # imgOut = cv2.adaptiveThreshold((img*255).astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 101, 5) #Teste com threshold adaptativo

    return imgOut


def applyMaskImage(img, mask):
    imgOut = np.zeros((img.shape[0], img.shape[1], 1), img.dtype)

    # Aplico a mascara na imagem
    imgOut = np.where(mask == 1, img, 0)
    # imgOut = cv2.bitwise_and(src1=img, src2=mask)

    return imgOut


def openImage(img, size):
    imgOut = np.zeros((img.shape[0], img.shape[1], 1), img.dtype)

    element = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (2 * size + 1, 2 * size + 1), (size, size))
    # Retiro os ruidos que estiverem fora do arroz da imagem
    imgOut = cv2.morphologyEx(img, cv2.MORPH_OPEN, element)

    return imgOut


def blurImage(img, size):
    imgOut = np.zeros((img.shape[0], img.shape[1], 1), img.dtype)

    # Borro a imagem usando o metodo gaussiano para ter mais controle
    imgOut = cv2.GaussianBlur(img, (size, size), 0)
    imgOut = imgOut.reshape(imgOut.shape[0], imgOut.shape[1], 1)

    return imgOut


def normalizeImage(img):
    imgOut = np.zeros((img.shape[0], img.shape[1], 1), img.dtype)
    # Estico mais os tons de brancos e pretos da imagem
    cv2.normalize(img, imgOut, 0, 1, cv2.NORM_MINMAX)

    return imgOut


# ============================================================================================================================
# Metodo para chamada de os outros metodos para manipulacao e subtracao das bordas
# ============================================================================================================================
def extractEdgesImages(imagesList):

    listImgsOut = []

    for i in range(0, len(imagesList)):
        imgBlur = np.zeros((imagesList[i].shape[0], imagesList[i].shape[1], 1), imagesList[i].dtype)

        imgBlur = blurImage(imagesList[i], 3)    # Aplico gauss antes das operacoes nas bordas
        # cv2.imwrite((str(i)+' - EBlur.png'), imgBlur * 255)

        # Tentei usar sobel de 1 a 7
        # Quanto mais alto, mais gorda a borda ficava e acabava conectando os elementos
        # No caso do tamanho 1, ficou muito fino e os proximmos passos nao ficaram bons
        imgSobel = applySobel(imgBlur, 3) #  Aplico Sobel para pegar o gradiente da imagem dos contornos
        # cv2.imwrite((str(i)+' - Sobel.png'), imgSobel * 255)

        # Tentei passar o filtro de gauss, erosao, abertura e fechamento aqui, ambos nao ficaram bons (Abertura quase ficou legal)
        # entao decidi usar a mediana para deixar o branco do contorno um pouco menor
        # Com relacao ao tamanho, tentei de 1 a 5 - 1 nao fez quase nada e 5 eu perdi informacao entao decidi usar o 3
        imgMedian = medianFilter(imgSobel, 3) # Alguns contornos ainda fica conectados entao tento fazer alguma operacao aqui para desconecta-los
        # cv2.imwrite((str(i)+' - Median.png'), imgMedian * 255)

        #OBS: Apos o passo da mediana tentei aplicar Gauss para tirar um pouco do ruido 
        # porem perdia informacao do arroz entao decidi limiarizar direto

        # Aqui num primeiro momento tentei subtrair da imagem original e nao ficou bom
        # Mas dai decidi limiarizar direto
        imgOut = binarizeImage(imgMedian, 0.46) # Binarizacao para contagem
        # cv2.imwrite((str(i)+' - ZBinarizada.png'), imgOut * 255)

        listImgsOut.append(imgOut)

    return listImgsOut


def applySobel(img, size):
    imgOut = np.zeros((img.shape[0], img.shape[1], 1), img.dtype)

    # Aplicando sobel no eixo X
    sobelX = cv2.Sobel(img, cv2.CV_32F, 1, 0, ksize=size)
    # Aplicando sobel no eixo y
    sobelY = cv2.Sobel(img, cv2.CV_32F, 0, 1, ksize=size)
    # Somando gradiente  de dx e dy
    imgOut = cv2.addWeighted(sobelX, 0.5, sobelY, 0.5, 0)
    imgOut = imgOut.reshape(imgOut.shape[0], imgOut.shape[1], 1)
    imgOut = np.clip(imgOut, 0, 1)  # Truncando em 1

    return imgOut

# ============================================================================================================================
# Metodos para contagem de arroz
# ============================================================================================================================


def countingRiceImages(imagesList, imagesOut):

    for i in range(0, len(imagesList)):
        components = labelingComponentsImages(imagesList[i])
        n_componentes = len(components)

        # Mostra os objetos encontrados.
        for c in components:
            cv2.rectangle(imagesOut[i], (c['L'], c['T']),
                          (c['R'], c['B']), (0, 0, 1), 2)

        cv2.imwrite((str(n_componentes) + ' - out.bmp'), imagesOut[i] * 255)


def labelingComponentsImages(img):
    # Quando tentei controlar a contagem pela janela perdi informacao entao
    # Decidi ter uma janela minima de 1 X 1 e controlar a contagem pelo numero de pixels 
    width_min = 1
    height_min = 1
    n_pixels_min = 7

    lst = []
    label = 0.001

    for row in range(0, img.shape[0]):
        for column in range(0, img.shape[1]):
            if img[row][column][0] == 1:
                topPixel = row
                bottomPixel = row
                leftPixel = column
                rightPixel = column

                floodDictionary = floodfill(
                    label, img, row, column, 0, row, column, column)
                riceDictionary = dict(
                    label=label, n_pixels=floodDictionary[0], T=row, L=floodDictionary[2], B=floodDictionary[1], R=floodDictionary[3])
                height = riceDictionary['B'] - riceDictionary['T']
                width = riceDictionary['R'] - riceDictionary['L']
                if riceDictionary['n_pixels'] > n_pixels_min and height > height_min and width > width_min:
                    lst.append(riceDictionary)
                    label = label + 0.001

    return lst


def floodfill(label, img, row, column, nPixels=0, bottomPixel=0, leftPixel=0, rightPixel=0):
    if img[row][column][0] != 1:
        return (nPixels, bottomPixel, leftPixel, rightPixel)

    img[row][column][0] = label
    nPixels += 1

    if bottomPixel < row:
        bottomPixel = row

    if rightPixel < column:
        rightPixel = column

    if leftPixel > column:
        leftPixel = column

    if row > 0:
        (nPixels, bottomPixel, leftPixel, rightPixel) = floodfill(label,
                                                                  img,
                                                                  row - 1,
                                                                  column,
                                                                  nPixels=nPixels,
                                                                  bottomPixel=bottomPixel,
                                                                  leftPixel=leftPixel,
                                                                  rightPixel=rightPixel)

    if row < (img.shape[0] - 1):
        (nPixels, bottomPixel, leftPixel, rightPixel) = floodfill(label,
                                                                  img,
                                                                  row + 1,
                                                                  column,
                                                                  nPixels=nPixels,
                                                                  bottomPixel=bottomPixel,
                                                                  leftPixel=leftPixel,
                                                                  rightPixel=rightPixel)

    if column > 0:
        (nPixels, bottomPixel, leftPixel, rightPixel) = floodfill(label,
                                                                  img,
                                                                  row,
                                                                  column - 1,
                                                                  nPixels=nPixels,
                                                                  bottomPixel=bottomPixel,
                                                                  leftPixel=leftPixel,
                                                                  rightPixel=rightPixel)

    if column < (img.shape[1]-1):
        (nPixels, bottomPixel, leftPixel, rightPixel) = floodfill(label,
                                                                  img,
                                                                  row,
                                                                  column + 1,
                                                                  nPixels=nPixels,
                                                                  bottomPixel=bottomPixel,
                                                                  leftPixel=leftPixel,
                                                                  rightPixel=rightPixel)

    return (nPixels, bottomPixel, leftPixel, rightPixel)


# ============================================================================================================================
# Metodo principal
# ============================================================================================================================
def main():

    listImages = []
    listImagesOut = []
    listImagesProcessed = []
    listImagesNoEdges = []

    for img in glob.glob("*.bmp"):
        imgGray = []
        imgGray = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
        if imgGray is None:
            print('Erro abrindo a '+str(i + 1)+' imagem .\n')
        imgGray = imgGray.reshape((imgGray.shape[0], imgGray.shape[1], 1))
        imgGray = imgGray.astype(np.float32) / 255
        listImages.append(imgGray)
        imgOut = cv2.cvtColor(imgGray, cv2.COLOR_GRAY2RGB)
        listImagesOut.append(imgOut)

    listImagesProcessed = processingImages(listImages)
    listImagesNoEdges = extractEdgesImages(listImagesProcessed)
    countingRiceImages(listImagesNoEdges, listImagesOut)


if __name__ == '__main__':
    main()
