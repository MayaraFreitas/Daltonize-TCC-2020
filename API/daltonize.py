from PIL import Image
import numpy

rgbToLmsMatrix = [
    0.31399022, 0.63951294, 0.04649755,
    0.15537241, 0.75789446, 0.08670142,
    0.01775239, 0.10944209, 0.87256922,
]

lmsToRgbMatrix = [
  5.47221206, -4.6419601, 0.16963708,
  -1.1252419, 2.29317094, -0.1678952,
  0.02980165, -0.19318073, 1.16364789,
]

protanopiaMatrix = [
  0.0, 1.05118294, -0.05116099,
  0.0, 1.0, 0.0,
  0.0, 0.0, 1.0,
]

deuteranopiaMatrix = [
  1.0, 0.0, 0.0,
  0.9513092, 0.0, 0.04866992,
  0.0, 0.0, 1.0,
]

tritanopiaMatrix = [
  1.0, 0.0, 0.0,
  0.0, 1.0, 0.0,
  -0.86744736, 1.86727089, 0.0,
]

def multiplyMatrix(array1, array2):
  return [
    array1[0] * array2[0] + array1[1] * array2[1] + array1[2] * array2[2],
    array1[3] * array2[0] + array1[4] * array2[1] + array1[5] * array2[2],
    array1[6] * array2[0] + array1[7] * array2[1] + array1[8] * array2[2],
  ]

def daltonize(image, sizeX, sizeY, colorBlindnessType):

    resultMatrix = numpy.zeros((sizeX,sizeY,3), 'float')
    for i in range(0,sizeX):
        for j in range(0,sizeY):
            resultMatrix[i,j] = simulateColorBlindness(image[i,j], colorBlindnessType)

    return resultMatrix

def simulateColorBlindness(rgb, colorBlindnessType):
    #print('Convert RGB to LMS')
    lmsMatrix = convertRgbToLms(rgb)
    #print('Apply Color Blindness')
    lmsDaltonized = applyColorBlindness(lmsMatrix, colorBlindnessType)
    #print('Convert Lms To Rgb')
    newRgb = convertLmsToRgb(lmsDaltonized)
    return newRgb

def applyColorBlindness(lmsMatrix, colorBlindnessType):

    if colorBlindnessType == 1:
        #print('Convertendo para Protanopes')
        return multiplyMatrix(protanopiaMatrix, lmsMatrix)
    elif colorBlindnessType == 2:
        #print('Convertendo para Deuteranopes')
        return multiplyMatrix(deuteranopiaMatrix, lmsMatrix)
    elif colorBlindnessType == 3:
        #print('Convertendo para Tritanope')
        return multiplyMatrix(tritanopiaMatrix, lmsMatrix)
    else:
        #throw error!
        print('ERRO!!!!!')

def convertRgbToLms(rgb):

    #convert Rgb to Matrix
    rgbMatrix = [0, 0, 0]
    rgbMatrix[0] = rgb[0] / 255
    rgbMatrix[1] = rgb[1] / 255
    rgbMatrix[2] = rgb[2] / 255

    #Convert to lms
    lms = multiplyMatrix(rgbToLmsMatrix, rgbMatrix)

    return lms

def convertLmsToRgb(lms):
    rgbMatrix = multiplyMatrix(lmsToRgbMatrix, lms)

    rgb = [0, 0, 0]
    rgb[0] = normalise(rgbMatrix[0] * 255)
    rgb[1] = normalise(rgbMatrix[1] * 255)
    rgb[2] = normalise(rgbMatrix[2] * 255)

    return rgb

def normalise(value):
    if (value > 255):
        return 255
    elif (value < 0):
        return 0
    else:
        return value

def bestImage(originalImg, newImg, sizeX, sizeY):

    resultMatrix = numpy.zeros((sizeX,sizeY,3), 'float')
    for i in range(0,sizeX):
        for j in range(0,sizeY):
            resultMatrix[i,j] = bestImageItem(originalImg[i,j], newImg[i,j])
    #return normaliseValues(resultMatrix, sizeX, sizeY)
    return resultMatrix

def bestImageItem(originalRGB, newRGB):

    difR = (originalRGB[0] - newRGB[0])
    difG = (originalRGB[1] - newRGB[1])
    difB = (originalRGB[2] - newRGB[2])

    r = (0.0 * difR) + (0.0 * difG) + (0.0 * difB)
    g = (0.7 * difR) + (1.0 * difG) + (0.0 * difB)
    b = (0.7 * difR) + (0.0 * difG) + (1.0 * difB)

    newR = normalise(originalRGB[0] + r)
    newG = normalise(originalRGB[1] + g)
    newB = normalise(originalRGB[2] + b)

    return [normalise(newR), normalise(newG), normalise(newB)]

def processImage(img, typeOfColorBlindness):

    print('START')
    #return img
    # if (typeOfColorBlindness <= 0 and typeOfColorBlindness > 6):
    #     return

    #img = Image.open(dirImgBase)
    sizeX = img.size[1]
    sizeY = img.size[0]
    #print('X:' + str(sizeX) + ' | Y: ' + str(sizeY))

    # Converte a imagem para uma matriz
    imgMatrix = numpy.asarray(img)

    if (typeOfColorBlindness <= 3):
        resultImgMatrix = daltonize(imgMatrix, sizeX, sizeY, typeOfColorBlindness)
    else:
        resultDaltonize = daltonize(imgMatrix, sizeX, sizeY, (typeOfColorBlindness - 3))
        print('Best Image')
        resultImgMatrix = bestImage(imgMatrix, resultDaltonize, sizeX, sizeY)

    print('End')
    result = Image.fromarray(numpy.uint8(resultImgMatrix))
    return result
