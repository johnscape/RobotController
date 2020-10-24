import cv2
import numpy as np

def LoadFromDataFile(f):
    reader = open(f, 'r')
    text = reader.read()
    parsed = text.split(' ')
    img_array = np.zeros((int(parsed[0]), int(parsed[1]), 3))
    pixels = []
    for i in range(len(parsed)):
        if i <= 1:
            continue
        if parsed[i] == "":
            continue
        pixels.append(float(parsed[i]))
    for x in range(int(parsed[0])):
        for y in range(int(parsed[1])):
            for c in range(3):
                img_array[x][y] = pixels[y * int(parsed[0]) + x]
    cv2.imshow("Depth map", img_array)
    cv2.waitKey(0)