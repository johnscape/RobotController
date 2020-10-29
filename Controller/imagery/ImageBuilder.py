import cv2
import numpy as np
import math

class ImageBuilder:
    def __init__(self):
        self.Parts = []
        self.Width = 512
        self.Height = 512
        self.BytesInPart = 1024

    def BuildRGB(self):
        if len(self.Parts) < math.ceil((self.Width * self.Height * 3) / self.BytesInPart):
            print("Not enough data to build the RGB image!")
            return None
        img = np.zeros((self.Width, self.Height, 3))
        pos = 0
        for x in range(self.Width):
            for y in range(self.Height):
                for c in range(3):
                    img[x][y][c] = self.Parts[0][pos]
                    pos += 1
                    if pos >= self.BytesInPart:
                        pos = 0
                        self.Parts.pop(0)
        cv2.imshow("Test", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
