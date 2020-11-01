import cv2
import numpy as np
import math

class ImageBuilder:
    def __init__(self):
        self.Parts = []
        self.Width = 512
        self.Height = 512
        self.BytesInPart = 1024
        self.Near = 0.1
        self.Far = 0.9
        self.LastImg = 1

    def CanBuildRGB(self):
        return len(self.Parts) >= math.ceil((self.Width * self.Height * 3) / self.BytesInPart)

    def BuildRGB(self, showImg = False):
        if not self.CanBuildRGB():
            print("Not enough data to build the RGB image!")
            return None
        img = np.zeros((self.Width, self.Height, 3), dtype=np.uint8)
        pos = 0
        for x in range(self.Width):
            for y in range(self.Height):
                for c in range(3):
                    img[x][y][c] = int(self.Parts[0][pos])
                    pos += 1
                    if pos >= self.BytesInPart:
                        pos = 0
                        self.Parts.pop(0)
        if showImg:
            cvimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            cvimg = cv2.flip(cvimg, 0)
            cv2.imshow("RGB image", cvimg)
            cv2.waitKey(1)
        return img

    def CanBuildDepth(self):
        return len(self.Parts) >= math.ceil((self.Width * self.Height) / self.BytesInPart)

    def BuildDepth(self, showImg = False):
        if not self.CanBuildDepth():
            print("Not enough data to build the depth image!")
            return None
        img = np.zeros((self.Width, self.Height, 3), dtype=np.uint8)
        pos = 0
        for x in range(self.Width):
            for y in range(self.Height):
                z = (float(self.Parts[0][pos]) / 255) * 2 - 1
                z = (2 * self.Far * self.Near) / (self.Far + self.Near - z * (self.Far - self.Near))
                z *= 255
                for c in range(3):
                    img[x][y][c] = int(z)
                pos += 1
                if pos >= self.BytesInPart:
                    pos = 0
                    self.Parts.pop(0)
        if showImg:
            cvimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            cvimg = cv2.flip(cvimg, 0)
            cv2.imshow("Depth image", cvimg)
            cv2.waitKey(1)
            #TODO: remove this
            cv2.imwrite("depth_" + str(self.LastImg).zfill(4) + ".png", cvimg)
            self.LastImg += 1

        return img