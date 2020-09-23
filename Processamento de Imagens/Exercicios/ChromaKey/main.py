#!-*- conding: utf8 -*-
# coding: utf-8
# ======================================================#!-*- conding: utf8 -*-
# coding: utf-8
# ===============================================================================
# Tarefa - Contar arroz em diferentes imagens
# -------------------------------------------------------------------------------
# Autor: Mary Camila
# ===============================================================================

import cv2
import glob
import numpy as np
from matplotlib import pyplot as plt

BACKGROUND_IMG = 'background.jpg'

# ============================================================================================================================
# Metodo para a chamada de os outros metodos para remocao do fundo verde
# ============================================================================================================================

def removeGreenBackground(imagesList, imagesListHsv):
    listImgsOut = []

    for i in range(0, len(imagesListHsv)):
        imgOut = np.zeros(
            (imagesListHsv[i].shape[0], imagesListHsv[i].shape[1], 3), imagesListHsv[i].dtype)

        # OBS: tentei normalizar o canal S e V so para ver o que acontecia
        # Entao nada aconteceu, nao teve nenhuma mudanca significativa entao decidi tirar.

        # OBS: tentei usar o HSL porem nao consegui acertar certinho o tom entao tentei com o HSV deu mais boa.
        # H - Hue - Pego somente o tom de verde que vai de aprox de 75 a 120 graus - Convertendo para 0...255 Fica em 53 ate 77
        # S - Saturation - Comeco em 0.25 para retirar os pixels mais brancos e defino o limite da saturacao em 1 para pegar o verde mais puro.
        # V - Value/Brightness - Comeco em 0.35 para retirar os pixels mais escuros e defino o limite em 1 para pegar o verde sem tom preto.
        lowerGreen = np.array([0.2, 0.25, 0.35])
        upperGreen = np.array([0.3, 1, 1])

        # Crio minha mascara para aplicar o background
        imgOut = createMaskColor(lowerGreen, upperGreen, imagesListHsv[i])

        # OBS: Tinha usado fechamento so para corrigir buracos (Testei com o kernel tamanho 1 e 3) mas distorceu as letras
        # e perdi algumas informacoes importantes entao decidi borrar a mascara para evitar o serrilhado
        # Porem borrando aqui nao me ajudou muito entao decidi aplicar a dilataco para afinar os contornos e poder
        # colocar o background de maneira mais assertiva sobre o verde porem acabou influenciando na aplicacao do background,
        # acabei perdendo informacao das figuras como cabelos e dos contornos das coisas entao decidi usar uma erosao para
        # aumentar um pouco o tamanho da borda e mais para frente corrigir o balanco do verde nas bordas
        # imgOut = erodeImage(masked, 1)
        # cv2.imwrite(str(i+10)+" - Final.bmp", imgOut * 255)

        # Tentei fazer uma segunda mascara para pegar os tons mais escuros do heroi,
        # Nao deu certo, entao decidi continuar e ver depois
        # lowerGreen = np.array([0.2, 0, 0])
        # upperGreen = np.array([0.4, 1, 1])

        # maskGU = np.logical_not(imgOutUp)
        # imgG = applyMask(imagesList[i], maskGU.astype(np.uint8))

        # imgGHSV = cv2.cvtColor(imgG, cv2.COLOR_BGR2HSV)
        # imgGHSV = imgGHSV.astype(np.float32) / 255

        # imgOutL = createMaskColor(lowerGreen, upperGreen, imgGHSV)
        # mask2 = np.logical_not(imgOutL)

        # cv2.imwrite(str(i+10)+" - Final2.bmp", mask2 * 255)

        listImgsOut.append(imgOut)

    return listImgsOut


def createMaskColor(lowColor, upColor, img):
    imgOut = cv2.inRange(img, lowColor, upColor)   # Gero a mascara invertida
    # Seto a mascara como float para padronizar
    imgOut = imgOut.astype(np.float32)
    imgOut = imgOut / 255

    return imgOut


def binarizeImage(img, threshold):
    imgOut = np.zeros((img.shape[0], img.shape[1], 1), img.dtype)

    # Binarizo a imagem baseado no threshold passado por parametro
    imgOut = np.where(img > threshold, 1, 0)
    imgOut = imgOut.reshape(imgOut.shape[0], imgOut.shape[1], 1)
    imgOut = imgOut.astype(np.float32)

    return imgOut


def dilateImage(img, size):
    imgOut = np.zeros((img.shape[0], img.shape[1], 1), img.dtype)

    element = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (2 * size + 1, 2 * size + 1), (size, size))
    # Retiro os ruidos que estiverem fora do arroz da imagem
    imgOut = cv2.dilate(img, element, iterations=1)

    return imgOut


def erodeImage(img, size):
    imgOut = np.zeros((img.shape[0], img.shape[1], 1), img.dtype)

    element = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (2 * size + 1, 2 * size + 1), (size, size))
    # Retiro os ruidos que estiverem fora do arroz da imagem
    imgOut = cv2.erode(img, element, iterations=1)

    return imgOut


def openImage(img, size):
    imgOut = np.zeros((img.shape[0], img.shape[1], 1), img.dtype)

    element = cv2.getStructuringElement(
        cv2.MORPH_RECT, (2 * size + 1, 2 * size + 1), (size, size))
    # Retiro os ruidos que estiverem fora do arroz da imagem
    imgOut = cv2.morphologyEx(img, cv2.MORPH_OPEN, element)

    return imgOut

def blurImage(img, size):
    imgOut = np.zeros((img.shape[0], img.shape[1]), img.dtype)

    # Borro a imagem usando o metodo gaussiano para ter mais controle
    imgOut = cv2.blur(img, (size, size), 0)
    # imgOut = imgOut.reshape(imgOut.shape[0], imgOut.shape[1])

    return imgOut

def gaussBlurImage(img, size):
    imgOut = np.zeros((img.shape[0], img.shape[1]), img.dtype)

    # Borro a imagem usando o metodo gaussiano para ter mais controle
    imgOut = cv2.GaussianBlur(img, (size, size), 0)
    # imgOut = imgOut.reshape(imgOut.shape[0], imgOut.shape[1])

    return imgOut

# ============================================================================================================================
# Metodo para a chamada de os outros metodos para colocar a imagem no chroma key
# ============================================================================================================================

def prepareImage(imagesList, maskList):
    listImgsOut = []
    imgback = cv2.imread(BACKGROUND_IMG)
    imgback = imgback.reshape(imgback.shape[0], imgback.shape[1], 3)
    imgback = imgback.astype(np.float32) / 255

    for i in range(0, len(imagesList)):
        imgOut = np.zeros(
            (imagesList[i].shape[0], imagesList[i].shape[1], 3), imagesList[i].dtype)

        # Inverte Mascara
        mask = cv2.bitwise_not(maskList[i].astype(np.uint8))
        mask = mask.astype(np.float32) / 255
        imgRoi = applyMask(imagesList[i], mask.astype(np.uint8))
        # cv2.imwrite(str(i+10)+" - imgRoi.bmp", imgRoi * 255)   
        
        # Green balance
        # OBS: Demorei bastante, tentei varias coisas aqui:
        # Mudei a imagem para RGB e trabalhei com o canal verde buscando um verde vivo sobel e com isso
        # via aonde estao meus pixels verdes q restaram da primeira limiarizacao.
        # Porem somente para teste peguei uma imagem verde de mar e praia na internet e nao funcinou :(
        # Tentei aplicar o metodo seguinte na mascara com a minha regiao de interesse mas tambem
        # nao ficou bom pois dentro das pessoas, objetos, tenho magnitudes altas tambem entao se
        # eu contruisse uma mascara baseado nisso iria perder informacao

        # Ainda tinha ficado um resquicio de verde entao tentei tento fazer mais manualmente,
        # tento achar os tons de verde e tento deixar eles menos verde

        # OBS: Tinha feito esse passo na primeira parte, mas perdia muita informacao do fundo
        # entao decidi fazer aqui, ja que nao tenho q me preocupar com a maior parte do fundo

        imgG = cv2.cvtColor(imgRoi, cv2.COLOR_BGR2HSV)
        imgG = imgG.astype(np.float32)

        h, s, v = imgG[:, :, 0], imgG[:, :, 1], imgG[:, :, 2]
        remainGreenMask = np.where(np.logical_and(h/255 >= 0.35, h/255 <= 0.5), 1, 0)
        remainGreen = applyMask(imgRoi, remainGreenMask.astype(np.uint8))
        # cv2.imwrite(str(i+10)+" - RemainGreen.bmp", remainGreen * 255)   
        
        # Gerei uma mascara com os tons de verdes remanescentes para equilibrar eles nos proximos passos
        # Aplico a mascara nos dois canais S 
        sGreen = np.zeros((s.shape[0], s.shape[1]), s.dtype)
        np.putmask(sGreen, remainGreenMask, s)
        sGreen = np.where(sGreen >= 0.5, 1, 0)

        # Olhando os resultados vejo que os lugares com saturacao mais baixa e indo ate 1 e com o brilho mais escuro 
        # Sao os lugares com o verde remanescente que quero equilibrar entao faco mais um corte para pegar somente esse lugares 

        # Fiz uns testes com o canal V mas nao deu mt boa entao decidi usar somente o canal S para encontrar os tons de verde
        # que eu quero
        # vGreen = np.zeros((v.shape[0], v.shape[1]), v.dtype)
        # np.putmask(vGreen, remainGreenMask, v)
        # vGreen = np.where(vGreen <= 0.6, vGreen, 0)
        # cv2.imwrite(str(i+10)+" - V.bmp", vGreen* 255)

        newMaskNG = maskList[i] + sGreen
        newMaskNG = np.logical_not(newMaskNG)
        # cv2.imwrite(str(i+10)+" - MaskRemove.bmp", newMaskNG * 255)    

        greenRemoved = applyMask(imagesList[i], newMaskNG.astype(np.uint8))
        # cv2.imwrite(str(i+10)+" - greenRemoved.bmp", greenRemoved * 255)     

        # Agora que removi o green preciso preencher os espacos vazios e comisso
        # borro a imagem para preecher os espacos da mascara principal  

        blurImg = blurImage(greenRemoved, 159)
        # cv2.imwrite(str(i+10)+" - blurImg.bmp", blurImg * 255) 

        sGreen = sGreen.reshape(mask.shape[0], sGreen.shape[1], 1)
        smoothEdges = np.where(sGreen == 1, blurImg, greenRemoved)
        # cv2.imwrite(str(i+10)+" - smoothEdges.bmp", smoothEdges * 255) 

        # Ainda ha alguns tons de verde na imagem
        # Tento corrigilos para um cinza
        # OBS: Nao pude zerar totalmente o S e o V pois irei zerar regioes com informacoes como cabelo, roupa, etc
        # Fiz alguns testes e com as mascaras acima e tentei baleancear um pouco o verde restante deixando ele mais escuro
        # ou mais amarelado, nao deu boa, as mudancas nao ficaram tao legais entao decidi deixar deixar o verde do jeito q esta

        imgGB = cv2.cvtColor(smoothEdges, cv2.COLOR_BGR2HSV)
        imgGB = imgGB.astype(np.float32)

        hG, sG, vG = imgGB[:, :, 0], imgGB[:, :, 1], imgGB[:, :, 2]
        greenToGray = np.where(np.logical_and(hG/255 >= 0.38, hG/255 <= 0.47), 1, 0)
        # cv2.imwrite(str(i+10)+" - greenToGray.bmp", greenToGray * 255) 

        # Gerei uma mascara com os tons de verdes remanescentes para acinzentar eles nos proximos passos
        # Aplico a mascara nos dois canais S 
        imgSGreen = np.zeros((sG.shape[0], sG.shape[1]), sG.dtype)
        np.putmask(imgSGreen, greenToGray, sG)
        imgSGreen = np.where(imgSGreen > 0.2, 1, 0) 
        # maskGreenToG = applyMask(smoothEdges, imgSGreen.astype(np.uint8)) 
        # cv2.imwrite(str(i+10)+" - imgSGreen.bmp", imgSGreen * 255) 

        sG = np.where(imgSGreen == 1, sG*0.1, sG)

        balanced = cv2.merge((hG, sG, vG))
        balanced = cv2.cvtColor(balanced, cv2.COLOR_HSV2BGR)
        # cv2.imwrite(str(i+10)+" - Balanced.bmp", balanced * 255)     

        imgEdNG = np.where(balanced > 0, balanced, smoothEdges)
        # cv2.imwrite(str(i+10)+" - imgEdNG.bmp", imgEdNG * 255)    

        ### Operacoes com o background
        # Uso interpolacao cubica para redimensionar a imagem
        backResized = cv2.resize(imgback, (imagesList[i].shape[1], imagesList[i].shape[0]), interpolation=cv2.INTER_CUBIC)
        # Truncando em 1 pois apareceram valores negativos e valores acima de 1
        backResized = np.clip(backResized, 0, 1)
        
        # Mascara com o novo backgroundx
        newMaskNG = np.logical_not(newMaskNG)
        # cv2.imwrite(str(i+10)+" - newMaskNG.bmp", newMaskNG * 255)
        imgBackground = applyMask(backResized, newMaskNG.astype(np.uint8))
        # cv2.imwrite(str(i+10)+" - imgBackground.bmp", imgBackground * 255)

        # Juntando as duas imagens
        imgOut = np.where(balanced > 0, balanced, imgBackground)
        # cv2.imwrite(str(i+10)+" - imgOut.bmp", imgOut * 255)

        listImgsOut.append(imgOut)

    return listImgsOut


def applyMask(img, mask):
    imgOut = np.zeros((img.shape[0], img.shape[1], 3), img.dtype)

    imgOut = cv2.bitwise_and(img, img, mask=mask)

    return imgOut

# ============================================================================================================================
# Metodo para a chamada de os outros metodos para suavizar contornos do chroma key
# ============================================================================================================================


def smoothEdges(imagesList, maskList):
    listImgsOut = []
    imgback = cv2.imread(BACKGROUND_IMG)
    imgback = imgback.reshape(imgback.shape[0], imgback.shape[1], 3)
    imgback = imgback.astype(np.float32) / 255

    for i in range(0, len(imagesList)):
        imgOut = np.zeros(
            (imagesList[i].shape[0], imagesList[i].shape[1], 3), imagesList[i].dtype)

        # OBS: Tentei usar o resize do opencv mas nao deu certo
        # Entao decidi usar sobel para pegar a magnitude e borrar 

        ### Operacoes com o background
        # Uso interpolacao cubica para redimensionar a imagem
        backResized = cv2.resize(imgback, (imagesList[i].shape[1], imagesList[i].shape[0]), interpolation=cv2.INTER_CUBIC)
        # Truncando em 1 pois apareceram valores negativos e valores acima de 1
        backResized = np.clip(backResized, 0, 1)

        # Tento corrigir os pixels da sobreposicao do background       

        imgBlurBorder = blurImage(imagesList[i], 3)
        
        imgSobelNG = applySobel(maskList[i], 7)
        # cv2.imwrite(str(i+10)+" - imgSobelNG.bmp", imgSobelNG * 255)

        maskSobelNG = applyMask(imgBlurBorder, imgSobelNG.astype(np.uint8))
        # cv2.imwrite(str(i+10)+" - maskFinal.bmp", maskSobelNG * 255)
        
        imgOut = np.where(maskSobelNG != 0, maskSobelNG, imagesList[i])
        cv2.imwrite(str(i+10)+" - imgOut.bmp", imgOut * 255)

        # Alguns tons de cinza e verde ainda ficam salientes, nao tive tempo de terminar de arrumar essa parte
        listImgsOut.append(imgOut)

    return listImgsOut

def applySobel(img, size):
    imgOut = np.zeros((img.shape[0], img.shape[1], 1), img.dtype)

    # Aplicando sobel no eixo X
    sobelX = cv2.Sobel(img, cv2.CV_32F, 1, 0, ksize=size)
    # Aplicando sobel no eixo y
    sobelY = cv2.Sobel(img, cv2.CV_32F, 0, 1, ksize=size)
    # Vendo a magnitude - sqrt(dx^2 + dy^2)
    # Arrumei aqui conforme o professor tinha apontado no outro trabalho
    imgOut = cv2.magnitude(sobelX, sobelY)
    imgOut = imgOut.reshape(imgOut.shape[0], imgOut.shape[1], 1)
    imgOut = np.clip(imgOut, 0, 1)  # Truncando em 1

    return imgOut
# ============================================================================================================================
# Metodo principal
# ============================================================================================================================


def main():

    listImages = []
    listImagesHsv = []

    for img in glob.glob("*.bmp"):
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

    listImgNoGreen = removeGreenBackground(listImages, listImagesHsv)
    listImgBackGround = prepareImage(listImages, listImgNoGreen)
    listImsSmoothEdges = smoothEdges(listImgBackGround, listImgNoGreen)


if __name__ == '__main__':
    main()
