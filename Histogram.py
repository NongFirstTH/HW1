def readPGM(filepath):
    """
    Read a pgm file and return their header except format type and comment 
    and return number of pixels.

    Parameter:
    filepath(str): A path to pgm file.

    Returns:
    width(int): Width of image.
    height(int): Height of image.
    maxGrayLevel(int): Max value of gray scale.
    pixels(list): 2D list of pixels that contain each pixel in pgm file.

    Raise:
    ValueError: If the file type is not a P5 format.
    """

    file = open(filepath,"rb")

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

# main
filepath = "in/scaled_shapes.pgm"
width, height, maxGrayLevel, pixels = readPGM(filepath)

histogram = createHistogram(pixels, maxGrayLevel)
print(histogram)
print(histogram.index(4969))
print(histogram.index(4956))
print(histogram.index(7529))
print(histogram.index(3460))
print(histogram.index(4955))
# 4969, 4956, 7529, 3460, 4955