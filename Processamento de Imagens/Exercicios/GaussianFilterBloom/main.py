#!-*- conding: utf8 -*-
# coding: utf-8
# ======================================================#!-*- conding: utf8 -*-
# coding: utf-8
# ===============================================================================
# Tarefa - Bloom
# -------------------------------------------------------------------------------
# Autor: Mary Camila
# ===============================================================================

import sys
import timeit
import numpy as np
import cv2

# ===============================================================================

INPUT_IMAGE = 'jogo.png'


# METODO GAUSSIANO
def gaussian(y, x, sigma):
    # Calculo para geracao do kernel
    return np.exp(-(y**2 + x**2) / (2*(sigma**2)))

# ===============================================================================


def metodoGaussiano(img, imgMask):
    const = 1
    sigma = 15
    listImgSoma = []

    for i in range(0, 3):
        # Defino o intervalo (-intervalo*sigma ate +intervalo*sigma)
        intervalo = round(const)*round(sigma)
        # Ponto central para saber a distancia futuramente
        centroRow, centroCol = intervalo, intervalo
        # Multiplico por dois para saber o tamanho do kernel e adiciono mais um para ser impar
        kernelSize = intervalo * 2 + 1
        kernel = np.zeros((kernelSize, kernelSize))  # Inicio o kernel
        somaNormaliza = 0

        for row in range(0, kernel.shape[0]):
            for col in range(0, kernel.shape[1]):
                # Faco a diferenca entro o ponto central e o ponto atual e passo para a funcao que calcula o valor da posicao do kernel
                kernel[row, col] = gaussian(
                    row - centroRow, col - centroCol, sigma)
                # Encontro o valor para divisao futura - Para normalizacao apos a multiplicacao
                somaNormaliza += kernel[row, col]

        kernel = kernel / somaNormaliza  # Normalizando o kernel

        # Aplica o efeito bloom usando o filtro gaussiano.
        imgList = np.zeros(img.shape, img.dtype)
        imgList = borraGaussiano(imgMask, kernel, intervalo)
        listImgSoma.append(imgList)
        sigma = sigma * 2 + 1 # adiciono mais um para ser impar
        cv2.imwrite('Bloom - Gauss' + str(i) + '.bmp', imgList * 255)

    imgBloom = sumImages(img, listImgSoma)

    return imgBloom

# ===============================================================================


def borraGaussiano(img, kernel, intervalo):
    imgOut = np.zeros(img.shape, img.dtype)

    for channel in range(0, img.shape[2]):
        for row in range(0, img.shape[0]):
            for col in range(0, img.shape[1]):
                # Pego os pontos da lminha janela
                alturaIni = row-intervalo
                larguraIni = col-intervalo
                alturaLim = row + intervalo + 1
                larguraLim = col + intervalo + 1

                # Checo para ver se nao esta estourando a borda
                if alturaIni < 0:
                    alturaIni = 0

                if alturaLim >= img.shape[0]:
                    alturaLim = img.shape[0]

                if larguraIni < 0:
                    larguraIni = 0

                if larguraLim >= img.shape[1]:
                    larguraLim = img.shape[1]

                # Pego somente o quadrante da minha janela
                gaussianFilter = img[alturaIni:alturaLim,
                                     larguraIni:larguraLim, channel]

                # Acho os indices de um kernel menor com os limites da janela
                rowKernelIni = 0
                colKernelIni = 0
                rowKernelLim = kernel.shape[0]
                colKernelLim = kernel.shape[1]

                if row - intervalo < 0:
                    rowKernelIni = abs(row - intervalo)

                if intervalo + row >= img.shape[0]:
                    # Acho a diferenca da linha atual para a ult linha da matriz e adiciono o intervalo para achar o limite do kernel menor
                    rowKernelLim = img.shape[0] - row + intervalo

                if col - intervalo < 0:
                    colKernelIni = abs(col - intervalo)

                if intervalo + col >= img.shape[1]:
                    # Acho a diferenca da coluna atual para a ult coluna da matriz e adiciono o intervalo para achar o limite do kernel menor
                    colKernelLim = img.shape[1] - col + intervalo

                # Pego somente o kernel da minha janela - se ela estiver na borda o kernel reduz
                kernelFinal = kernel[rowKernelIni:rowKernelLim,
                                     colKernelIni:colKernelLim]

                # Transformo para vetor para efetuar a multiplicacao com o kernel
                gaussianFilter = gaussianFilter.flatten()*kernelFinal.flatten()

                # Somo os valor e encontro o valor finak
                imgOut[row][col][channel] = gaussianFilter.sum()

    return imgOut

# ===============================================================================

# METODO IMAGEM INTEGRAL
def metodoMedia(img, imgMask):
    intgralImg = np.zeros(img.shape, img.dtype)

    # Somando a matriz usando numpy
    # Para poder fazer a imagem integral
    for channel in range(0, img.shape[2]):
        for row in range(0, img.shape[0]):
            for column in range(0, img.shape[1]):
                somaArray = imgMask[0:row+1, 0:column+1, channel]
                intgralImg[row][column][channel] = somaArray.sum()

    janela = 13
    listImgSoma = []

    for i in range(0, 4):
        imgList = np.zeros(img.shape, img.dtype)
        imgList = borraMediaIntegral(imgMask, intgralImg, janela)
        listImgSoma.append(imgList)
        janela = janela * 2  + 1 # Dobro o tamanho da janela e adiciono mais um para ficar impar
        cv2.imwrite('Bloom - Media ' + str(i) + '.bmp', imgList * 255)

    imgBloom = sumImages(img, listImgSoma)

    return imgBloom

# ===============================================================================

def borraMediaIntegral(mascara, intImg, jan):
    imgOut = np.zeros(mascara.shape, mascara.dtype)
    # Estrategia com janelas menores
    # janelaBorda = -1

    for channel in range(0, mascara.shape[2]):
        for row in range(0, mascara.shape[0]):
            for column in range(0, mascara.shape[1]):
                janela = jan // 2

                limRow = row + janela
                iniRow = row - janela - 1
                limCol = column + janela
                iniCol = column - janela - 1
                # Checo para ver se nao estoura os limites da imagem
                if iniRow < 0:
                    iniRow = 0
                if iniCol < 0:
                    iniCol = 0

                if limRow >= intImg.shape[0]:
                    limRow = intImg.shape[0] - 1

                if limCol >= intImg.shape[1]:
                    limCol = intImg.shape[1] - 1

                # Canto superior esquerdo
                intImgA = intImg[iniRow][iniCol][channel]
                # Canto superior direito
                intImgB = intImg[iniRow][limCol][channel]
                # Canto inferior esquerdo
                intImgC = intImg[limRow][iniCol][channel]
                # Canto intImg direito
                intImgD = intImg[limRow][limCol][channel]

                calcIntegral = intImgD - intImgB - intImgC + intImgA
                sizeRow = limRow - iniRow + 1  # Adiciono mais um para compensar a posicao atual
                sizeCol = limCol - iniCol + 1  # Adiciono mais um para compensar a posicao atual
                imgOut[row][column][channel] = calcIntegral / \
                    (sizeRow * sizeCol)
    return imgOut

# ===============================================================================

# METODO PARA SOMAR AS IMAGENS - RETORNA A IMAGEM FINAL

def sumImages(img, listaImagens):
    bloomImg = np.zeros(img.shape, img.dtype)
    imgOut = np.zeros(img.shape, img.dtype)

    # Somando as imagens bo
    for channel in range(0, img.shape[2]):
        for row in range(0, img.shape[0]):
            for column in range(0, img.shape[1]):
                soma = 0

                for i in range(0, len(listaImagens)):
                    imgSoma = listaImagens[i]
                    if soma + imgSoma[row][column][channel] < 1:
                        soma += imgSoma[row][column][channel]
                    else:
                        break

                bloomImg[row][column][channel] = soma

    for channel in range(0, img.shape[2]):
        for row in range(0, img.shape[0]):
            for column in range(0, img.shape[1]):
                # Multiplico por um valor menor para nao estourar a imagem
                soma = bloomImg[row][column][channel] * 0.2
                valorImg = img[row][column][channel] * 0.9
                if soma + valorImg < 1:
                    imgOut[row][column][channel] = soma + valorImg
                else:
                    imgOut[row][column][channel] = 1

    return imgOut

# ===============================================================================

# METODO PARA GERAR A MASCARA COM OS FOCOS DE LUZ


def geraMascara(img):
    mascara = np.zeros(img.shape, img.dtype)

    for channel in range(0, img.shape[2]):
        for row in range(0, img.shape[0]):
            for col in range(0, img.shape[1]):
                if img[row][col][channel] >= 0.65: # Testei com varios valores, este e o que ficou melhor
                    mascara[row][col][channel] = img[row][col][channel]
                else:  # Caso esteja na borda
                    mascara[row][col][channel] = 0

    return mascara

# ===============================================================================


def main():
    # Abre a imagem em escala de cinza.
    img = cv2.imread(INPUT_IMAGE)
    if img is None:
        print('Erro abrindo a imagem.\n')
        sys.exit()

    img = img.astype(np.float32) / 255

    imgMascara = geraMascara(img)

    # Bloom com gauss
    imgGauss = metodoGaussiano(img, imgMascara)
    cv2.imshow('Bloom - Gauss', imgGauss)
    cv2.imwrite('Bloom - Gauss.bmp', imgGauss * 255)

    # # Bloom com imagem integral
    imgMedia = metodoMedia(img, imgMascara)
    cv2.imshow('Bloom - Media', imgMedia)
    cv2.imwrite('Bloom - Media.bmp', imgMedia * 255)

    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
