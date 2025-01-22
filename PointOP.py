import matplotlib.pyplot as plt
import numpy as np

def readPGM(filePath):
    """
    Read a pgm file and return their header except format type and comment 
    and return number of pixels.

    Parameter:
    filePath(str): A path to pgm file.

    Returns:
    width(int): Width of image.
    height(int): Height of image.
    maxGrayLevel(int): Max value of gray scale.
    pixels(list): 2D list of pixels that contain each pixel in pgm file.

    Raise:
    ValueError: If the file type is not a P5 format.
    """

    file = open(filePath,"rb")

    fileType = file.readline().decode().strip()
    if fileType != "P5":
        raise ValueError("not a PGM P5 format")
    
    while True:
        line = file.readline().decode().strip()
        if not line.startswith('#'):
            dimension = line
            break

    maxGrayLevel = int(file.readline().decode().strip())
    width, height = map(int, dimension.split())

    pixel_data = file.read()
    pixels = [ list(pixel_data[row * width : (row + 1) * width]) for row in range(height)]

    return width, height, maxGrayLevel, pixels

def writePGM(filePath, header, pixels):
    """
    Write binary pgm file from file path, header and pixels.
    
    Parameters:
    filePath(str): A path of output file.
    header(list): List of header of PGM file. 
    pixels(bytes): Pixels of output image.
    """
    
    file = open(filePath, "wb")
    file.write("\n".join(header).encode() + b"\n")
    file.write(pixels)

def createHistogram(pixels, maxGrayLevel):
    """
    Create histogram by counting each pixel in pixels.

    Parameters:
    pixels(list): 2D list of pixels that contain each pixel in pgm file.
    maxGrayLevel(int): Max value of gray scale.

    Return:
    histogram(list): histogram of pgm file.
    """

    histogram = [0] * (maxGrayLevel + 1)

    for rowPixel in pixels:
        for pixel in rowPixel:
            histogram[pixel] += 1
    
    return histogram

def equalize(inputHistogram, width, height, maxGrayLevel):
    """
    Histogram equalization by performing the input histogram.
    
    Parameters:
    inputHistogram(np.array): Histogram of input image.
    width(int): Width of image.
    height(int): Height of image.
    maxGrayLevel(int): Max value of gray scale.
    
    Return:
    equalization(np.array): Gray level that equalize input histogram.
    """
    
    A0 = width * height
    PDF = inputHistogram / A0
    CDF = np.cumsum(PDF)
    equalization = maxGrayLevel * CDF

    return equalization.round(0) 

def mapHistogram(inputHistogram, equalization, maxGrayLevel):
    """
    Map value between input histogram and equalization and return output histogram.
    
    Parameters:
    inputHistogram(np.array): Histogram of input image.
    equalization(np.array): Gray level that equalize input histogram.
    maxGrayLevel(int): Max value of gray scale.
    
    Return:
    outputHistogram(list): List of output histogram.
    """
    
    outputHistogram = [0] * (maxGrayLevel + 1)
    
    for i in range(maxGrayLevel):
        outputHistogram[equalization[i]] += inputHistogram[i] 

    return outputHistogram

def pointOperate(inputHistogram, width, height, maxGrayLevel):
    """
    Point operation by equalizing the input histogram and return output histogram.
    
    Parameters:
    inputHistogram(np.array): Histogram of input image.
    width(int): Width of image.
    height(int): Height of image.
    maxGrayLevel(int): Max value of gray scale.
    
    Return:
    outputHistogram(list): List of output histogram.
    equalization(np.array): Gray level that equalize input histogram.
    """
    
    equalization = equalize(inputHistogram, width, height, maxGrayLevel)
    equalization = equalization.astype('int64')
    outputHistogram = mapHistogram(inputHistogram, equalization, maxGrayLevel)
    
    return outputHistogram, equalization

def mapColor(pixels, width, height, equalization):
    """
    Map color between input image and equalization.
    
    Parameters:
    pixels(list): 2D list of pixels that contain each pixel in pgm file.
    width(int): Width of image.
    height(int): Height of image.
    equalization(np.array): Gray level that equalize input histogram.
    """
    
    for x in range(height):
        for y in range(width):
            pixels[x][y] = equalization[pixels[x][y]]

def writePixelsToPGM(filePathOutput , width, height, maxGrayLevel, pixels):
    """
    Write pixels to PGM file.
    
    Parameters:
    filePathOutput(str): A path of output file.
    width(int): Width of image.
    height(int): Height of image.
    maxGrayLevel(int): Max value of gray scale of image.
    pixels(list): 2D list of pixels that contain each pixel in pgm file.
    """
    
    header = ["P5", str(width)+" "+str(height), str(maxGrayLevel)]
    pixels2Dto1D = bytes(sum(pixels, []))
    pixels = pixels2Dto1D
    writePGM(filePathOutput, header, pixels)
    
def showHistogram(filePath, inputHistogram, equalization, outputHistogram):
    """
    Show histogram of input histogram, equalization and output histogram.
    
    Parameters:
    filePath(str): A path to pgm file.
    inputHistogram(np.array): Histogram of input image.
    equalization(np.array): Gray level that equalize input histogram.
    outputHistogram(list): List of output histogram.
    """
    
    plt.subplot(1, 3, 1)
    plt.title(f'Input of histogram of {filePath}')
    plt.xlabel('Gray Level(D)')
    plt.ylabel('frequency (H(D))')
    plt.plot(inputHistogram)

    plt.subplot(1, 3, 2)
    plt.title('Equalization')
    plt.xlabel('DA')
    plt.ylabel('DB')
    plt.plot(equalization)

    plt.subplot(1, 3, 3)
    plt.title(f'Output of histogram of {filePath}')
    plt.xlabel('Gray Level(D)')
    plt.ylabel('frequency (H(D))')
    plt.plot(outputHistogram)
    plt.show()

# # main
# filePathIn1 = "in/Cameraman.pgm"
# filePathOut1 = "out/CameramanOut.pgm"

# # read pgm file
# width1, height1, maxGrayLevel1, pixels1 = readPGM(filePathIn1)

# # perform histogram equalization
# inputHistogram1 = np.array(createHistogram(pixels1, maxGrayLevel1))
# outputHistogram1, equalization1 = pointOperate(inputHistogram1,  width1, height1, maxGrayLevel1)
# mapColor(pixels1, width1, height1, equalization1)

# # write pgm file
# writePixelsToPGM(filePathOut1 , width1, height1, maxGrayLevel1, pixels1)

# showHistogram(filePathIn1, inputHistogram1, equalization1, outputHistogram1)

# # perform second image
# filePathIn2 = "in/SEM256_256.pgm"
# filePathOut2 = "out/SEM256_256Out.pgm"

# width2, height2, maxGrayLevel2, pixels2 = readPGM(filePathIn2)

# inputHistogram2 = np.array(createHistogram(pixels2, maxGrayLevel2))
# outputHistogram2, equalization2 = pointOperate(inputHistogram2, width2, height2, maxGrayLevel2)
# mapColor(pixels2, width2, height2, equalization2)

# writePixelsToPGM(filePathOut2, width2, height2, maxGrayLevel2, pixels2)
# showHistogram(filePathIn2, inputHistogram2, equalization2, outputHistogram2)

# perform second image
filePathIn3 = "in/62877.pgm"
filePathOut3 = "out/62865Out.pgm"

width3, height3, maxGrayLevel3, pixels3 = readPGM(filePathIn3)

inputHistogram3 = np.array(createHistogram(pixels3, maxGrayLevel3))
outputHistogram3, equalization3 = pointOperate(inputHistogram3, width3, height3, maxGrayLevel3)
mapColor(pixels3, width3, height3, equalization3)

writePixelsToPGM(filePathOut3, width3, height3, maxGrayLevel3, pixels3)
showHistogram(filePathIn3, inputHistogram3, equalization3, outputHistogram3)