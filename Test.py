import numpy as np
# header = ["P5", str(256)+" "+str(256), str(255)]
# file = open('test.pgm', "wb")
# file.write("\n".join(header).encode() + b"\n")
# file.write(bytes([255]))
def f(i):
    i[0][0] = -1

def i():
    return [[255,255,255]]

# i = [[255,255,255]]
# i[0][0] = 0
# f(i)
f(i())

print(i())