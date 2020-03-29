#!-*- conding: utf8 -*-
# coding: utf-8

# ======================================================#!-*- conding: utf8 -*-
# coding: utf-8

# ===============================================================================
# Exemplo: segmentacaoo de uma imagem em escala de cinza.
# -------------------------------------------------------------------------------
# Autor: Bogdan T. Nassu
# Universidade Tecnológica Federal do Paraná
# ===============================================================================

import sys
import timeit
import numpy as np
import cv2

# ===============================================================================

INPUT_IMAGE = 'arroz.bmp'

# TODO: ajuste estes parâmetros!
NEGATIVO = False
THRESHOLD = 0.8  # Utilizo 0.8 pois como vimos em sala de aula e o valor que mostra corretamente os graos
ALTURA_MIN = 15
LARGURA_MIN = 15
N_PIXELS_MIN = 400

# ===============================================================================

def binariza(img, threshold):
    ''' Binarização simples por limiarização.

Parâmetros: img: imagem de entrada. Se tiver mais que 1 canal, binariza cada
              canal independentemente.
            threshold: limiar.

Valor de retorno: versão binarizada da img_in.'''
    img = np.where(img > threshold, 1, 0)
    img = img.astype(np.float32)
    return img


# -------------------------------------------------------------------------------
def rotula(img, largura_min, altura_min, n_pixels_min):
    '''Rotulagem usando flood fill. Marca os objetos da imagem com os valores
[0.1,0.2,etc].

Parâmetros: img: imagem de entrada E saída.
            largura_min: descarta componentes com largura menor que esta.
            altura_min: descarta componentes com altura menor que esta.
            n_pixels_min: descarta componentes com menos pixels que isso.

Valor de retorno: uma lista, onde cada item é um vetor associativo (dictionary)
com os seguintes campos:

'label': rótulo do componente.
'n_pixels': número de pixels do componente.
'T': coordenadas do retângulo envolvente de um componente conexo - top
'L': coordenadas do retângulo envolvente de um componente conexo - left
'B': coordenadas do retângulo envolvente de um componente conexo - bottom
'R': coordenadas do retângulo envolvente de um componente conexo - right '''

    # TODO: escreva esta função.
    # Use a abordagem com flood fill recursivo.
    lst = []
    label = 0.001
    rice_dictionary = {}
    for row in range(0, img.shape[0]):
        for column in range(0, img.shape[1]):
            if img[row][column][0] == 1:
                topPixel = row
                bottomPixel = row
                leftPixel = column
                rightPixel = column

                floodDictionary = floodfill(label, img, row, column, 0, row, column, column)
                riceDictionary = dict(label=label, n_pixels=floodDictionary[0], T=row, L=floodDictionary[2], B=floodDictionary[1], R=floodDictionary[3])
                height = riceDictionary['B'] - riceDictionary['T']
                width = riceDictionary['R'] - riceDictionary['L']
                if riceDictionary['n_pixels'] > N_PIXELS_MIN and height > ALTURA_MIN and width > LARGURA_MIN:
                    lst.append(riceDictionary)
                    label = label + 0.001

    return lst


# ==============================================================================

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

# ===============================================================================

def main():
    # Abre a imagem em escala de cinza.
    img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print('Erro abrindo a imagem.\n')
        sys.exit()

    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não. Também já convertemos para float32.
    img = img.reshape((img.shape[0], img.shape[1], 1))
    img = img.astype(np.float32) / 255

    # Mantém uma cópia colorida para desenhar a saída.
    img_out = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # Segmenta a imagem.
    if NEGATIVO:
        img = 1 - img
    img = binariza(img, THRESHOLD)
    cv2.imshow ('01 - binarizada', img)
    cv2.imwrite('01 - binarizada.png', img * 255)

    start_time = timeit.default_timer()
    componentes = rotula(img, LARGURA_MIN, ALTURA_MIN, N_PIXELS_MIN)
    cv2.imwrite('teste - binarizada.png', img)
    n_componentes = len(componentes)
    print('Tempo: %f' % (timeit.default_timer() - start_time))
    print('%d componentes detectados.' % n_componentes)

    # Mostra os objetos encontrados.
    for c in componentes:
        cv2.rectangle(img_out, (c['L'], c['T']), (c['R'], c['B']), (0, 0, 1), 2)

    cv2.imshow ('02 - out', img_out)
    cv2.imwrite('02 - out.png', img_out * 255)
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()