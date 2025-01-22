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
    
def spatialTranform(grid, distGrid, refPoint):
    # grid x
    xy = np.array([
        [grid[refPoint[0]]['x'], grid[refPoint[0]]['y'], grid[refPoint[0]]['x']*grid[refPoint[0]]['y'], 1],
        [grid[refPoint[1]]['x'], grid[refPoint[1]]['y'], grid[refPoint[1]]['x']*grid[refPoint[1]]['y'], 1],
        [grid[refPoint[2]]['x'], grid[refPoint[2]]['y'], grid[refPoint[2]]['x']*grid[refPoint[2]]['y'], 1],
        [grid[refPoint[3]]['x'], grid[refPoint[3]]['y'], grid[refPoint[3]]['x']*grid[refPoint[3]]['y'], 1]    
        ])
    
    # Distgrid x'
    x_ = np.array([
                distGrid[refPoint[0]]['x'], 
                distGrid[refPoint[1]]['x'], 
                distGrid[refPoint[2]]['x'], 
                distGrid[refPoint[3]]['x']
                ])
    coeX = np.linalg.solve(xy, x_)

    # Distgrid y'
    y_ = np.array([
                distGrid[refPoint[0]]['y'], 
                distGrid[refPoint[1]]['y'], 
                distGrid[refPoint[2]]['y'], 
                distGrid[refPoint[3]]['y']
                ])
    coeY = np.linalg.solve(xy, y_)
    
    inputCoor = []
    xUpLeft = grid[refPoint[0]]['x']
    xDownLeft = grid[refPoint[2]]['x']
    yUpLeft = grid[refPoint[0]]['y']
    yUpRight = grid[refPoint[1]]['y']
    
    for x in range(xUpLeft, xDownLeft+1):
        result = []
        for y in range(yUpLeft, yUpRight+1):
            x_i = coeX[0]*x + coeX[1]*y + coeX[2]*x*y + coeX[3]
            y_i = coeY[0]*x + coeY[1]*y + coeY[2]*x*y + coeY[3]
            result.append({"x'": x_i, "y'": y_i})
        inputCoor.append(result)
    inputCoor = np.array(inputCoor)
    
    return inputCoor

def bilearInterpolate(inputCoor, pixelsDistGrid):
    res = []
    height = 256
    width = 256
    for blockI in range(len(inputCoor)):
        for blockJ in range(len(inputCoor[0])):
            for row in range(len(inputCoor[blockI][blockJ])):
                for col in range(len(inputCoor[blockI][blockJ][0])):
                    x = inputCoor[blockI][blockJ][row][col]["x'"]
                    y = inputCoor[blockI][blockJ][row][col]["y'"]
                    xPoint = int(x); yPoint = int(y)
                    
                    if 0 <= xPoint < height and 0 <= yPoint < width:
                        x0 = xPoint
                        y0 = yPoint
                        x1 = min(x0 + 1, height - 1)
                        y1 = min(y0 + 1, width - 1)
                    
                        #real (x,y)
                        x = x%1; y = y%1
                        #calculate color
                        a = pixelsDistGrid[x1][y0] - pixelsDistGrid[x0][y0]
                        b = pixelsDistGrid[x0][y1] - pixelsDistGrid[x0][y0]
                        c = pixelsDistGrid[x1][y1] + pixelsDistGrid[x0][y0] - pixelsDistGrid[x0][y1] - pixelsDistGrid[x1][y0]
                        d = pixelsDistGrid[x0][y0]
                        result = round(a*x + b*y + c*x*y + d)
                        res.append(result)
    return res

#main
filePathInGrid = 'in/grid.pgm'
filePathInDistGrid = 'in/NewDistGrid_256_256PGM.pgm'
filePathInOpera = 'in/DistOperaHouse_256_256PGM_Gray.pgm'

width, height, maxGrayLevel, pixelsGrid = readPGM(filePathInGrid)
width, height, maxGrayLevel, pixelsDistGrid = readPGM(filePathInDistGrid)
width, height, maxGrayLevelOp, pixelsOpera = readPGM(filePathInOpera)

grid = []
for x in range(-1, 256, 16):
    result = []
    for y in range(-1, 256, 16):
        if x == -1:
            x = 0
        if y == -1:
            y = 0
        result.append({'x': x, 'y': y})
    grid.append(result)

distGrid = [
    [{'x': 0, 'y': 0}, {'x': 0, 'y': 15}, {'x': 0, 'y': 31}, {'x': 0, 'y': 47}, {'x': 0, 'y': 63}, {'x': 0, 'y': 79}, {'x': 0, 'y': 95}, {'x': 0, 'y': 111}, {'x': 0, 'y': 127}, {'x': 0, 'y': 143}, {'x': 0, 'y': 159}, {'x': 0, 'y': 175}, {'x': 0, 'y': 191}, {'x': 0, 'y': 207}, {'x': 0, 'y': 223}, {'x': 0, 'y': 239}, {'x': 0, 'y': 255}], 
    [{'x': 15, 'y': 0}, {'x': 15, 'y': 15}, {'x': 15, 'y': 31}, {'x': 15, 'y': 47}, {'x': 15, 'y': 63}, {'x': 15, 'y': 79}, {'x': 15, 'y': 97}, {'x': 15, 'y': 115}, {'x': 15, 'y': 131}, {'x': 15, 'y': 146}, {'x': 15, 'y': 162}, {'x': 15, 'y': 175}, {'x': 15, 'y': 191}, {'x': 15, 'y': 207}, {'x': 15, 'y': 223}, {'x': 15, 'y': 239}, {'x': 15, 'y': 255}], 
    [{'x': 31, 'y': 0}, {'x': 31, 'y': 15}, {'x': 31, 'y': 31}, {'x': 31, 'y': 47}, {'x': 30, 'y': 65}, {'x': 28, 'y': 85}, {'x': 28, 'y': 105}, {'x': 29, 'y': 123}, {'x': 32, 'y': 141}, {'x': 34, 'y': 156}, {'x': 34, 'y': 168}, {'x': 34, 'y': 180}, {'x': 32, 'y': 193}, {'x': 31, 'y': 207}, {'x': 31, 'y': 223}, {'x': 31, 'y': 239}, {'x': 31, 'y': 255}], 
    [{'x': 47, 'y': 0}, {'x': 47, 'y': 15}, {'x': 47, 'y': 31}, {'x': 44, 'y': 50}, {'x': 41, 'y': 71}, {'x': 40, 'y': 94}, {'x': 41, 'y': 116}, {'x': 46, 'y': 136}, {'x': 51, 'y': 153}, {'x': 56, 'y': 167}, {'x': 57, 'y': 178}, {'x': 56, 'y': 188}, {'x': 53, 'y': 198}, {'x': 49, 'y': 209}, {'x': 47, 'y': 223}, {'x': 47, 'y': 239}, {'x': 47, 'y': 255}], 
    [{'x': 63, 'y': 0}, {'x': 63, 'y': 15}, {'x': 61, 'y': 33}, {'x': 55, 'y': 53}, {'x': 51, 'y': 78}, {'x': 51, 'y': 104}, {'x': 56, 'y': 127}, {'x': 64, 'y': 148}, {'x': 74, 'y': 163}, {'x': 82, 'y': 176}, {'x': 84, 'y': 185}, {'x': 82, 'y': 193}, {'x': 78, 'y': 203}, {'x': 70, 'y': 213}, {'x': 65, 'y': 224}, {'x': 63, 'y': 239}, {'x': 63, 'y': 255}], 
    [{'x': 79, 'y': 0}, {'x': 78, 'y': 15}, {'x': 73, 'y': 35}, {'x': 65, 'y': 57}, {'x': 60, 'y': 83}, {'x': 62, 'y': 111}, {'x': 70, 'y': 136}, {'x': 85, 'y': 155}, {'x': 100, 'y': 167}, {'x': 109, 'y': 175}, {'x': 113, 'y': 183}, {'x': 110, 'y': 193}, {'x': 104, 'y': 204}, {'x': 94, 'y': 214}, {'x': 85, 'y': 226}, {'x': 80, 'y': 239}, {'x': 79, 'y': 255}], 
    [{'x': 95, 'y': 0}, {'x': 93, 'y': 16}, {'x': 85, 'y': 35}, {'x': 75, 'y': 58}, {'x': 69, 'y': 85}, {'x': 71, 'y': 113}, {'x': 83, 'y': 138}, {'x': 103, 'y': 153}, {'x': 121, 'y': 159}, {'x': 133, 'y': 163}, {'x': 137, 'y': 172}, {'x': 135, 'y': 185}, {'x': 127, 'y': 199}, {'x': 116, 'y': 213}, {'x': 105, 'y': 226}, {'x': 97, 'y': 240}, {'x': 95, 'y': 255}], 
    [{'x': 111, 'y': 0}, {'x': 107, 'y': 16}, {'x': 98, 'y': 34}, {'x': 86, 'y': 57}, {'x': 79, 'y': 83}, {'x': 80, 'y': 110}, {'x': 93, 'y': 133}, {'x': 114, 'y': 145}, {'x': 133, 'y': 143}, {'x': 145, 'y': 143}, {'x': 154, 'y': 153}, {'x': 155, 'y': 170}, {'x': 149, 'y': 190}, {'x': 138, 'y': 208}, {'x': 124, 'y': 224}, {'x': 115, 'y': 239}, {'x': 111, 'y': 255}], 
    [{'x': 127, 'y': 0}, {'x': 122, 'y': 15}, {'x': 112, 'y': 32}, {'x': 100, 'y': 52}, {'x': 91, 'y': 75}, {'x': 88, 'y': 101}, {'x': 96, 'y': 122}, {'x': 113, 'y': 133}, {'x': 129, 'y': 127}, {'x': 144, 'y': 123}, {'x': 159, 'y': 134}, {'x': 167, 'y': 155}, {'x': 165, 'y': 179}, {'x': 154, 'y': 203}, {'x': 141, 'y': 222}, {'x': 132, 'y': 238}, {'x': 127, 'y': 255}], 
    [{'x': 143, 'y': 0}, {'x': 139, 'y': 15}, {'x': 129, 'y': 30}, {'x': 117, 'y': 46}, {'x': 106, 'y': 65}, {'x': 99, 'y': 86}, {'x': 101, 'y': 104}, {'x': 110, 'y': 114}, {'x': 123, 'y': 112}, {'x': 142, 'y': 110}, {'x': 163, 'y': 121}, {'x': 175, 'y': 144}, {'x': 176, 'y': 172}, {'x': 168, 'y': 198}, {'x': 157, 'y': 219}, {'x': 147, 'y': 238}, {'x': 143, 'y': 255}], 
    [{'x': 159, 'y': 0}, {'x': 156, 'y': 15}, {'x': 148, 'y': 28}, {'x': 137, 'y': 41}, {'x': 126, 'y': 56}, {'x': 118, 'y': 70}, {'x': 116, 'y': 84}, {'x': 121, 'y': 93}, {'x': 133, 'y': 96}, {'x': 152, 'y': 101}, {'x': 171, 'y': 116}, {'x': 183, 'y': 141}, {'x': 185, 'y': 169}, {'x': 179, 'y': 196}, {'x': 170, 'y': 219}, {'x': 161, 'y': 238}, {'x': 159, 'y': 255}], 
    [{'x': 175, 'y': 0}, {'x': 174, 'y': 15}, {'x': 168, 'y': 28}, {'x': 159, 'y': 40}, {'x': 150, 'y': 50}, {'x': 143, 'y': 61}, {'x': 140, 'y': 71}, {'x': 144, 'y': 80}, {'x': 154, 'y': 88}, {'x': 170, 'y': 99}, {'x': 184, 'y': 117}, {'x': 194, 'y': 143}, {'x': 194, 'y': 171}, {'x': 189, 'y': 197}, {'x': 182, 'y': 219}, {'x': 176, 'y': 239}, {'x': 175, 'y': 255}], 
    [{'x': 191, 'y': 0}, {'x': 191, 'y': 15}, {'x': 188, 'y': 30}, {'x': 182, 'y': 41}, {'x': 175, 'y': 51}, {'x': 170, 'y': 60}, {'x': 168, 'y': 69}, {'x': 171, 'y': 78}, {'x': 178, 'y': 90}, {'x': 189, 'y': 105}, {'x': 198, 'y': 125}, {'x': 204, 'y': 150}, {'x': 203, 'y': 176}, {'x': 199, 'y': 200}, {'x': 194, 'y': 221}, {'x': 191, 'y': 239}, {'x': 191, 'y': 255}], 
    [{'x': 207, 'y': 0}, {'x': 207, 'y': 15}, {'x': 207, 'y': 31}, {'x': 204, 'y': 44}, {'x': 200, 'y': 55}, {'x': 196, 'y': 65}, {'x': 195, 'y': 75}, {'x': 198, 'y': 86}, {'x': 202, 'y': 99}, {'x': 208, 'y': 115}, {'x': 213, 'y': 137}, {'x': 215, 'y': 159}, {'x': 213, 'y': 182}, {'x': 210, 'y': 205}, {'x': 208, 'y': 224}, {'x': 207, 'y': 239}, {'x': 207, 'y': 255}], 
    [{'x': 223, 'y': 0}, {'x': 223, 'y': 15}, {'x': 223, 'y': 31}, {'x': 223, 'y': 47}, {'x': 221, 'y': 60}, {'x': 219, 'y': 72}, {'x': 219, 'y': 84}, {'x': 220, 'y': 97}, {'x': 221, 'y': 111}, {'x': 224, 'y': 128}, {'x': 226, 'y': 148}, {'x': 226, 'y': 169}, {'x': 225, 'y': 188}, {'x': 223, 'y': 207}, {'x': 223, 'y': 223}, {'x': 223, 'y': 239}, {'x': 223, 'y': 255}], 
    [{'x': 239, 'y': 0}, {'x': 239, 'y': 15}, {'x': 239, 'y': 31}, {'x': 239, 'y': 47}, {'x': 239, 'y': 63}, {'x': 239, 'y': 79}, {'x': 239, 'y': 93}, {'x': 239, 'y': 107}, {'x': 239, 'y': 123}, {'x': 239, 'y': 139}, {'x': 239, 'y': 156}, {'x': 239, 'y': 174}, {'x': 239, 'y': 191}, {'x': 239, 'y': 207}, {'x': 239, 'y': 223}, {'x': 239, 'y': 239}, {'x': 239, 'y': 255}], 
    [{'x': 255, 'y': 0}, {'x': 255, 'y': 15}, {'x': 255, 'y': 31}, {'x': 255, 'y': 47}, {'x': 255, 'y': 63}, {'x': 255, 'y': 79}, {'x': 255, 'y': 95}, {'x': 255, 'y': 111}, {'x': 255, 'y': 127}, {'x': 255, 'y': 143}, {'x': 255, 'y': 159}, {'x': 255, 'y': 175}, {'x': 255, 'y': 191}, {'x': 255, 'y': 207}, {'x': 255, 'y': 223}, {'x': 255, 'y': 239}, {'x': 255, 'y': 255}]
]

grid = np.array(grid)
distGrid = np.array(distGrid)

inputCoor = []
for x in range(16):
    result = []
    
    for y in range(16):
        p1 = (x, y)
        p2 = (x, y+1)
        p3 = (x+1, y)
        p4 = (x+1, y+1)
        refPoint = [p1, p2, p3, p4]
        result.append(spatialTranform(grid, distGrid, refPoint))
        
    inputCoor.append(result)

res = bilearInterpolate(inputCoor, pixelsOpera)

# writePixelsToPGM('out/Opera.pgm', width, height, maxGrayLevelOp, res)

header = ["P5", str(256)+" "+str(256), str(255)]
file = open('out/Opera.pgm', "wb")
file.write("\n".join(header).encode() + b"\n")
file.write(bytes(res))