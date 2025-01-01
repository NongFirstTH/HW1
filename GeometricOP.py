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

#main
filePathInGrid = 'in/grid.pgm'
filePathInDistGrid = 'in/NewDistGrid_256_256PGM.pgm'

width, height, maxGrayLevel, pixelsGrid = readPGM(filePathInGrid)
width, height, maxGrayLevel, pixelsDistGrid = readPGM(filePathInDistGrid)

histGrid = createHistogram(pixelsGrid, maxGrayLevel)
histDistGrid = createHistogram(pixelsDistGrid, maxGrayLevel)

# print(histGrid)
# print(histDistGrid)
img1 = plt.imread(filePathInGrid)
img2 = plt.imread(filePathInDistGrid)
plt.subplot(1,2,1)
plt.xlabel('y')
plt.ylabel('x')
plt.axis('off')
plt.imshow(img1)
plt.subplot(1,2,2)
plt.ylabel('x')
plt.xlabel('y')
plt.axis('off')
plt.imshow(img2)
plt.show()
