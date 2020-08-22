#!-*- conding: utf8 -*-
# coding: utf-8
# ======================================================#!-*- conding: utf8 -*-
# coding: utf-8
# ===============================================================================
# Tarefa - Blur
# -------------------------------------------------------------------------------
# Autor: Mary Camila
# ===============================================================================

import sys
import timeit
import numpy as np
import cv2

# ===============================================================================

INPUT_IMAGE = 'flores.bmp'
WINDOW_SIZE = 7

# ===============================================================================


def filtroMediaIngenuo(img):
    imgOut = np.zeros(img.shape, img.dtype)
    larguraDiv = WINDOW_SIZE//2
    alturaDiv = WINDOW_SIZE//2

    for channel in range(0, img.shape[2]):
        for row in range(0, img.shape[0]):
            for column in range(0, img.shape[1]):
                if row + alturaDiv <= (img.shape[0] - 1) and column + larguraDiv <= (img.shape[1]-1) and row - alturaDiv > 0 and column - larguraDiv > 0:
                    soma = 0
                    rowWindow = row - alturaDiv
                    colWindow = column - larguraDiv
                    for rW in range(rowWindow, rowWindow + WINDOW_SIZE):
                        for cW in range(colWindow, colWindow + WINDOW_SIZE):
                            soma += img[rW][cW][channel]

                    imgOut[row][column][channel] = soma / \
                        (WINDOW_SIZE*WINDOW_SIZE)
                else:
                    imgOut[row][column][channel] = img[row][column][channel]

    return imgOut

# ===============================================================================


def filtroMediaSeparavelComSomas(img):
    imgBlurHorizontal = np.zeros(img.shape, img.dtype)
    imgOut = np.zeros(img.shape, img.dtype)

    for channel in range(0, img.shape[2]):
        for row in range(0, img.shape[0]):
            soma = 0
            for column in range(0, img.shape[1]):
                if column == 0:
                    for colWindow in range(0, WINDOW_SIZE):
                        soma += img[row][column + colWindow][channel]

                    imgBlurHorizontal[row][column][channel] = soma / WINDOW_SIZE
                else:
                    if column + WINDOW_SIZE-1 < img.shape[1]:
                        diminuiPixel = img[row][column - 1][channel]
                        somaPixel = img[row][column + WINDOW_SIZE-1][channel]
                        soma += somaPixel - diminuiPixel
                        imgBlurHorizontal[row][column][channel] = soma / WINDOW_SIZE
                    else:
                        imgBlurHorizontal[row][column][channel] = img[row][column][channel]

    for channel in range(0, img.shape[2]):
        for column in range(0, img.shape[1]):    
            soma = 0    
            for row in range(0, img.shape[0]):
                if row == 0:
                    for rowWindow in range(0, WINDOW_SIZE):
                        soma += imgBlurHorizontal[row + rowWindow][column][channel]
                        
                    imgOut[row][column][channel] = soma / WINDOW_SIZE
                else:
                    if row + WINDOW_SIZE-1 < img.shape[0]:
                        diminuiPixel = imgBlurHorizontal[row - 1][column][channel]
                        somaPixel = imgBlurHorizontal[row + WINDOW_SIZE-1][column][channel]
                        soma += somaPixel - diminuiPixel
                        imgOut[row][column][channel] = soma / WINDOW_SIZE
                    else:
                        imgOut[row][column][channel] = img[row][column][channel]

    return imgOut

# ===============================================================================


def filtroMediaIntegral(img):
    intgralImg = np.zeros(img.shape, img.dtype)
    imgOut = np.zeros(img.shape, img.dtype)

    # Somando a matriz manual
    # for channel in range(0, img.shape[2]):
    #     for row in range(0, img.shape[0]):
    #         intgralImg[row][0][channel] = img[row][0][channel]
    #         for column in range(0, img.shape[1]):
    #             if column > 0:
    #                 intgralImg[row][column][channel] = img[row][column][channel] + intgralImg[row][column - 1][channel]

    # for channel in range(0, img.shape[2]):
    #     for row in range(0, img.shape[0]):
    #         for column in range(0, img.shape[1]):
    #             if row > 0:
    #                 intgralImg[row][column][channel] = intgralImg[row][column][channel] + intgralImg[row - 1][column][channel]

    # Somando a matriz usando numpy
    for channel in range(0, img.shape[2]):
        for row in range(0, img.shape[0]):
            for column in range(0, img.shape[1]):
                somaArray = img[0:row+1, 0:column+1, channel]      
                teste = somaArray.sum()              
                intgralImg[row][column][channel] = somaArray.sum()

    for channel in range(0, img.shape[2]):
        for row in range(0, img.shape[0]):
            for column in range(0, img.shape[1]):
                if row + WINDOW_SIZE//2 < img.shape[0] and column + WINDOW_SIZE//2 < img.shape[1] and row - WINDOW_SIZE//2 > 0 and column - WINDOW_SIZE//2 > 0:
                    # Canto superior esquerdo
                    intImgA = intgralImg[row -
                                         WINDOW_SIZE//2-1][column-WINDOW_SIZE//2-1][channel]
                    # Canto superior direito
                    intImgB = intgralImg[row-WINDOW_SIZE//2 -
                                         1][column+WINDOW_SIZE//2][channel]
                    # Canto inferior esquerdo
                    intImgC = intgralImg[row +
                                         WINDOW_SIZE//2][column-WINDOW_SIZE//2-1][channel]
                    # Canto inferior direito
                    intImgD = intgralImg[row +
                                         WINDOW_SIZE//2][column+WINDOW_SIZE//2][channel]

                    calcIntegral = intImgD - intImgB - intImgC + intImgA
                    teste = calcIntegral / (WINDOW_SIZE*WINDOW_SIZE)
                    imgOut[row][column][channel] = calcIntegral / (WINDOW_SIZE*WINDOW_SIZE)                 
                else:
                    bordaLimRow = row + WINDOW_SIZE//2
                    bordaIniRow = row - WINDOW_SIZE//2 - 1
                    bordaLimCol = column + WINDOW_SIZE//2
                    bordaIniCol = column - WINDOW_SIZE//2 - 1

                    #Checo para ver se nao estoura os limites da imagem 
                    if bordaIniRow < 0:
                        bordaIniRow = 0
                    
                    if bordaIniCol < 0:
                        bordaIniCol = 0

                    if bordaLimRow >= intgralImg.shape[0]:
                        bordaLimRow = intgralImg.shape[0] - 1

                    if bordaLimCol >= intgralImg.shape[1]:
                        bordaLimCol = intgralImg.shape[1] - 1

                    intImgA = intgralImg[bordaIniRow][bordaIniCol][channel]
                    # Canto superior direito
                    intImgB = intgralImg[bordaIniRow][bordaLimCol][channel]
                    # Canto inferior esquerdo
                    intImgC = intgralImg[bordaLimRow][bordaIniCol][channel]
                    # Canto inferior direito
                    intImgD = intgralImg[bordaLimRow][bordaLimCol][channel]

                    calcIntegral = intImgD - intImgB - intImgC + intImgA
                    sizeRow = bordaLimRow - bordaIniRow + 1 # Adiciono mais um para compensar a posicao atual
                    sizeCol = bordaLimCol - bordaIniCol + 1 # Adiciono mais um para compensar a posicao atual
                    imgOut[row][column][channel] = calcIntegral / (sizeRow*sizeCol) 
    return imgOut

# ===============================================================================


def main():
    # Abre a imagem em escala de cinza.
    img = cv2.imread(INPUT_IMAGE)
    if img is None:
        print('Erro abrindo a imagem.\n')
        sys.exit()

    img = img.astype(np.float32) / 255

    # Aplica o filtro da média ingenuo.
    # img_out = filtroMediaIngenuo(img)
    # cv2.imshow('Filtro Media - Ingenuo', img_out)
    # cv2.imwrite('Filtro Media - Ingenuo.bmp', img_out * 255)

    # Aplica o filtro da média separável.
    # img_outMS = filtroMediaSeparavelComSomas(img)
    # cv2.imshow('Filtro Media - Separavel com Somas', img_outMS)
    # cv2.imwrite('Filtro Media - Separavel com Somas.bmp', img_outMS * 255)

    # Aplica o filtro da média com imagens integrais.
    img_outMI = filtroMediaIntegral(img)
    cv2.imshow('Filtro Media - Imagem Integral', img_outMI)
    cv2.imwrite('Filtro Media - Imagem Integral.bmp', img_outMI * 255)

    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
