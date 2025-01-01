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

def combineLists(pixelsA, operator, pixelsB):
    """
    Combine pixels a and b according to operator.
    
    Parameters:
    pixelA(list): 2D list of first pixels.
    operator(str): Arithmatic operator e.g. '+', '-'.
    pixelB(list): 2D list of second pixels.
    
    Return:
    outputPixels(list): 2D list of result from combine two lists.
    """
    
    width = len(pixelsA[0])
    height = len(pixelsA)
    outputPixels = [[0]*width for x in range(height)]
    
    op = {'+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y,
            '**': lambda x, y: x ** y}
    operator = op[operator]
    if not operator:
        raise ValueError("Invalid operator")
    
    for x in range(height):
        for y in range(width):
            result = operator (pixelsA[x][y], pixelsB[x][y])
            if result > 255:
                outputPixels[x][y] = 255
            elif result < 0:
                outputPixels[x][y] = 0
            else:
                outputPixels[x][y] = result
                    
    return outputPixels

def combineNumAndList(num, operator, pixels):
    """
    Combine pixels and number according to operator.
    
    Parameters:
    num(int or float): Number.
    operator(str): Arithmatic operator e.g. '+', '-'.
    pixels(list): 2D list of pixels.
    
    Return:
    outputPixels(list): 2D list of result from combine list and number.
    """
    
    width = len(pixels[0])
    height = len(pixels)
    outputPixels = [[0]*width for x in range(height)]
    
    op = {'+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y,
            '**': lambda x, y: x ** y}
    operator = op[operator]
    if not operator:
        raise ValueError("Invalid operator")
    
    for x in range(height):
        for y in range(width):
            result = operator (num, pixels[x][y])
            if result > 255:
                outputPixels[x][y] = 255
            elif result < 0:
                outputPixels[x][y] = 0
            else:
                outputPixels[x][y] = result
                        
    return outputPixels

def excessGreen(num, channels):
    """
    Excess green channel of image by using num*g-r-b to combine images.
    
    Parameters:
    num(int or float): Number.
    channels(dict): Three color channels(rgb) of image.
    
    Return:
    excessGreen(list): Excess green channel image. 
    """
    
    r = channels['r']
    g = channels['g']
    b = channels['b']
    multiG = combineNumAndList(num, '*', g)
    rbDiff = combineLists(r,'-', b)
    excessGreen = combineLists(multiG, '-' , rbDiff)
    
    return excessGreen

def excessBlue(num, channels):
    """
    Excess blue channel of image by using num*b-g-r to combine images.
    
    Parameters:
    num(int or float): Number.
    channels(dict): Three color channels(rgb) of image.
    
    Return:
    excessBlue(list): Excess blue channel image. 
    """
    
    r = channels['r']
    g = channels['g']
    b = channels['b']
    multiB = combineNumAndList(num, '*', b)
    grDiff = combineLists(g,'-', r)
    excessBlue = combineLists(multiB, '-' , grDiff)
    
    return excessBlue

def excessRed(num, channels):
    """
    Excess red channel of image by using num*r-b-g to combine images.
    
    Parameters:
    num(int or float): Number.
    channels(dict): Three color channels(rgb) of image.
    
    Return:
    excessRed(list): Excess red channel image. 
    """
    
    r = channels['r']
    g = channels['g']
    b = channels['b']
    multiR = combineNumAndList(num, '*', r)
    bgDiff = combineLists(b,'-', g)
    excessRed = combineLists(multiR, '-' , bgDiff)
    
    return excessRed

def intensity(num, channels):
    """
    Intensity image by using num*(r+b+g) to combine images.
    
    Parameters:
    num(int or float): Number
    channels(dict): Three color channels(rgb) of image.
    
    Return:
    intensity(list): Intensity image. 
    """
    
    r = channels['r']
    g = channels['g']
    b = channels['b']
    rbAdd = combineLists(r, '+', b)
    rbAddg = combineLists(rbAdd, '+', g)
    intensity = combineNumAndList(num, '*', rbAddg)
    
    return intensity

# def showImages(titles, images):
    plt.subplot(2, 3, 1)
    plt.title("SanFranPeak_red")
    plt.imshow(r, cmap='gray')
    plt.axis('off')
    plt.subplot(2, 3, 2)
    plt.title("SanFranPeak_green")
    plt.imshow(g, cmap='gray')
    plt.axis('off')
    plt.subplot(2, 3, 3)
    plt.title("SanFranPeak_blue")
    plt.imshow(b, cmap='gray')
    plt.axis('off')
    
    plt.subplot(2, 3, 4)
    plt.title(titles[0])
    plt.imshow(images[0], cmap='gray')
    plt.axis('off')
    plt.subplot(2, 3, 5)
    plt.title(titles[1])
    plt.imshow(images[1], cmap='gray')
    plt.axis('off')
    plt.subplot(2, 3, 6)
    plt.title(titles[2])
    plt.imshow(images[2], cmap='gray')
    plt.axis('off')
    plt.show()

# main
filePathInR = "in/SanFranPeak_red.pgm"
filePathInG = "in/SanFranPeak_green.pgm"
filePathInB = "in/SanFranPeak_blue.pgm"

width, height, maxGrayLevel, r = readPGM(filePathInR)
width, height, maxGrayLevel, g = readPGM(filePathInG)
width, height, maxGrayLevel, b = readPGM(filePathInB)
channels = {'r': r, 'g': g, 'b': b}

# combine images
excessGreen2 = excessGreen(2, channels)
excessGreen3 = excessGreen(3, channels)
excessGreen5 = excessGreen(5, channels)
excessBlue2 = excessBlue(2, channels)
excessBlue3 = excessBlue(3, channels)
excessBlue5 = excessBlue(5, channels)
excessRed2 = excessRed(2, channels)
excessRed3 = excessRed(3, channels)
excessRed5 = excessRed(5, channels)
rbDiff = combineLists(combineLists(r,'-', b), '-', g)
intensityChannel = intensity(1/3, channels)
rgAdd = combineLists(r, '+', g)
gbAdd = combineLists(g, '+', b)
addAll = combineLists(rgAdd, '+', b)

# write PGM file
filePathsOut = ["excessGreen2.pgm", "excessGreen3.pgm", "excessGreen5.pgm",
               "excessBlue2.pgm", "excessBlue3.pgm", "excessBlue5.pgm",
               "excessRed2.pgm", "excessRed3.pgm", "excessRed5.pgm",
               "rgAdd.pgm", "addAll.pgm", "gbAdd.pgm"
               ]
pixelsImages = [excessGreen2, excessGreen3, excessGreen5,
                excessBlue2, excessBlue3, excessBlue5,
                excessRed2, excessRed3, excessRed5,
                rgAdd, addAll, gbAdd
                ]
for i in range(len(filePathsOut)):
    writePixelsToPGM("out/"+filePathsOut[i], width, height, maxGrayLevel, pixelsImages[i])

# titles = ["2*g-r-b", "r-b", "(r+b+g)/3"]
# images = [excessGreen2, rbDiff, intensityChannel]
# titles = ["2*g-r-b", "3*g-r-b", "5*g-r-b"]
# images = [excessGreen2, excessGreen3, excessGreen5]
# titles = ["2*b-g-r", "3*b-g-r", "5*b-g-r"]
# images = [excessBlue2, excessBlue3, excessBlue5]
# titles = ["2*r-g-b", "3*r-g-b", "5*r-g-b"]
# images = [excessRed2, excessRed3, excessRed5]
# titles = ['r+g', 'r+g+b', 'g+b']
# images = [rgAdd, addAll, gbAdd]
# showImages(titles, images)
