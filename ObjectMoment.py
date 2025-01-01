def readPGM(filepath):
    """
    Read a pgm file and return their header except format type and comment 
    and return number of pixels.

    Rarameter:
    filepath(str): A path to pgm file.

    Return:
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
    width, height = dimension.split()
    width = int(width); height = int(height)

    pixel_data = file.read()
    pixels = [ list(pixel_data[row * width : (row + 1) * width]) for row in range(height)]

    return width, height, maxGrayLevel, pixels

def pqMoment(pixels, p, q, width, height):
    moment = 0

    for x in range(height):
        for y in range(width):
            moment += x**p * y**q * pixels[x][y]

    return moment

def centralMoments(pixels, p, q, width, height):
    moment = 0
    m10 = pqMoment(pixels, 1, 0, width, height)
    m01 = pqMoment(pixels, 0, 1, width, height)
    m00 = pqMoment(pixels, 0, 0, width, height)
    xQuantity = m10 / m00
    yQuantity = m01 / m00
    
    for x in range(height):
        for y in range(width):
            moment += (x - xQuantity)**p * (y - yQuantity)**q * pixels[x][y]

    return moment

def normalizedMoments(pixels, p, q, width, height):
    moment = 0
    MUpq = centralMoments(pixels, p, q, width, height)
    MU00 = centralMoments(pixels, 0, 0, width, height)
    moment = MUpq / (MU00**((p+q)/2 + 1))

    return moment

def quantity(centralMoment20, centralMoment02):
    return centralMoment20 + centralMoment02

# main
filepath = "in/scaled_shapes.pgm"
width, height, maxGrayLevel, pixels = readPGM(filepath)

centralMoment20 = centralMoments(pixels, 2, 0, width, height)
centralMoment02 = centralMoments(pixels, 0, 2, width, height)

print(quantity(centralMoment20, centralMoment02))
