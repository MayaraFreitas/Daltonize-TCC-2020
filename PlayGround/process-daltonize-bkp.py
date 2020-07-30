import cv2
from PIL import Image
import numpy as np
import numpy
import argparse
import sys
import colorsys

typeOfColorBlindness = 2
#imgName = "frutas-2.JPG"
imgName = "teste-daltonismo2.JPG"
#imgName = "red.JPG"
#imgName = "RGB.JPG"
dirImgBase = "img/test/" + imgName
dirImgResult = "img/result/" + "T" + str(typeOfColorBlindness) + "-" + imgName

# Reestruturação da imagem invertida 
def OLDnormaliseImage(editablePhoto,sizeX,sizeY):

	normalPhoto =  np.zeros((sizeX,sizeY,3),'float')
	x=sizeX-1
	y=sizeY
	for i in range(0,sizeX):
		for j in range(0,sizeY):
			for k in range(0,3):
				normalPhoto[x,j,k]=editablePhoto[i,j,k]
		x=x-1
	return normalPhoto

# Realiza a multiplicação entre matrizes
def multiplyMatrix(matrix1, matrix2, sizeX, sizeY):
	
	resultMatrix = np.zeros((sizeX,sizeY,3),'float')
	for i in range(0,sizeX):
		for j in range(0,sizeY):
			currMatrix = np.array((0,0,0),dtype=float)
			for k in range(0,3):
				currMatrix[k] = matrix2[i,j,k]
			newMatrix = np.dot(matrix1, currMatrix)
			for k in range(0,3):
				resultMatrix[i,j,k] = newMatrix[k]
	return resultMatrix

# Converte imagem passada como parâmetro de RGB para LMS
def convertToLMS(imgArray,sizeX,sizeY):

	resultMatrix = np.zeros((sizeX,sizeY,3), 'float')
	for i in range(0,sizeX):
		for j in range(0,sizeY):
			r = imgArray[i,j,0]
			g = imgArray[i,j,1]
			b = imgArray[i,j,2]
			resultMatrix[i,j,0] = (17.8824 * r) + (43.5161 * g) + (4.11935 * b)
			resultMatrix[i,j,1] = (3.45565 * r) + (27.1554 * g) + (3.86714 * b)
			resultMatrix[i,j,2] = (0.0299566 * r) + (0.184309 * g) + (1.46709 * b)
			
	return resultMatrix

#Converte imagem passada como parâmetro de LMS para RGB
def convertToRGB(imgArray,sizeX,sizeY):

	resultMatrix = np.zeros((sizeX,sizeY,3),'float')
	for i in range(0,sizeX):
		for j in range(0,sizeY):
			l = imgArray[i,j,0]
			m = imgArray[i,j,1]
			s = imgArray[i,j,2]
			resultMatrix[i,j,0] = (0.0809444479 * l) + (-0.130504409 * m) + (0.116721066 * s)
			resultMatrix[i,j,1] = (-0.0102485335 * l) + (0.0540193266 * m) + (0.113614708 * s)
			resultMatrix[i,j,2] = (-0.000365296938  * l) + (-0.00412161469 * m) + (0.693511405 * s)

	return normaliseValues(resultMatrix,sizeX,sizeY)

def normaliseValues(imgArray,sizeX,sizeY):

	min = [999999.0, 999999.0, 999999.0]
	max = [-999999.0, -999999.0, -999999.0]
	for i in range(0,sizeX):
		for j in range(0,sizeY):
			for k in range(0,3):
				min[k] = imgArray[i,j,k] if imgArray[i,j,k] < min[k] else min[k]
				max[k] = imgArray[i,j,k] if imgArray[i,j,k] > max[k] else max[k]

	resultMatrix = np.zeros((sizeX,sizeY,3),'float')
	for i in range(0,sizeX):
		for j in range(0,sizeY):
			for k in range(0,3):
				resultMatrix[i,j,k] = normaliseValue(imgArray[i,j,k], min[k], max[k])

			# if(j == 250 and i == 100):
			# 	print('normalizado RGB: ' + str(resultMatrix[i,j,0]) + ', ' + str(resultMatrix[i,j,1]) + ', ' + str(resultMatrix[i,j,2]))

	return resultMatrix

def normaliseValue(x, min, max):
    return (x - min) / (max - min) * 255

def daltonizeImage(colorBlindnessType, lsmMatrix, sizeX, sizeY):

    if colorBlindnessType == 1:
        print('Convertendo para Protanopes')
        baseMatrix = numpy.array([[0, 2.02344, -2.52581],[0, 1, 0],[0 ,0 ,1]])
    elif colorBlindnessType == 2:
        print('Convertendo para Deuteranopes')
        baseMatrix = numpy.array([[1,0,0],[0.494207,0,1.24827],[0,0,1]])
    elif colorBlindnessType == 3:
        print('Convertendo para Tritanope')
        baseMatrix = numpy.array([[1.0, 0.0 , 0.0],[0.0, 1.0 , 0.0],[-0.395913, 0.801109, 0.0]])

    # Multiplicar a matriz base com a LMS
    resultMatrix = multiplyMatrix(baseMatrix, lsmMatrix, sizeX, sizeY)
    return resultMatrix

def calculareErrorImage(imgBase, daltonizeImg, sizeX, sizeY):
	
	resultMatrix = np.zeros((sizeX,sizeY,3),'float')
	for i in range(0,sizeX):
		for j in range(0,sizeY):
			for k in range(0,3):
				resultMatrix[i,j,k] = imgBase[i,j,k] - daltonizeImg[i,j,k]
				if resultMatrix[i,j,k] < 0 :
					resultMatrix[i,j,k] = 0
				elif resultMatrix[i,j,k] > 255:
					resultMatrix[i,j,k] = 255
	return resultMatrix

def gerenateBestImage(imgBase, errorImg, sizeX, sizeY):
    
    resultMatrix = np.zeros((sizeX,sizeY,3),'float')
    baseMatrix = numpy.array([[0.0, 0.0, 0.0],[0.7, 0.1, 0.0],[0.7 , 0.0 , 1.0]])
    newMatrix = multiplyMatrix(baseMatrix, errorImg, sizeX, sizeY)
    
    for i in range(0,sizeX):
        for j in range(0,sizeY):
            for k in range(0,3):
                resultMatrix[i,j,k] = imgBase[i,j,k] + newMatrix[i,j,k]
                if resultMatrix[i,j,k] < 0:
                    resultMatrix[i,j,k] = 0
                elif resultMatrix[i,j,k] > 255:
                    resultMatrix[i,j,k] = 255
    return resultMatrix


img = Image.open(dirImgBase)
sizeX = img.size[1]
sizeY = img.size[0]
print('X:' + str(sizeX) + ' | Y: ' + str(sizeY))

if typeOfColorBlindness != 4:
    
    # Converte a imagem para uma matriz
    imgMatrix = numpy.asarray(img)
	#teste = cv2.imread(img) #colorida

    # Primeiro, converter imagem para LSM
    print('Primeiro, converter imagem para LSM')
    lsmMatrix = convertToLMS(imgMatrix, sizeX, sizeY)

    # Segundo, converter para o tipo de daltonismo
    print('Segundo, converter para o tipo de daltonismo')
    daltonizeMatrix = daltonizeImage(typeOfColorBlindness, lsmMatrix, sizeX, sizeY)

    # Terceiro, converter de volta para RGB
    print('Terceiro, converter de volta para RGB')
    rgbPhoto = convertToRGB(daltonizeMatrix,sizeX,sizeY)

	# Quarto, calcular perda
    print('Quarto, calular perda')
    errorImg = calculareErrorImage(imgMatrix, rgbPhoto,sizeX,sizeY)
 
	# Quinto, gerar imagem melhor
    print('Quinto, gerar imagem melhor')
    bestImg = gerenateBestImage(imgMatrix, errorImg, sizeX, sizeY)
 
    result = Image.fromarray(numpy.uint8(bestImg))
    result.show()