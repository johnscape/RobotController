from objectData.objectView import Verticle, Face, LineFaceCollision, VerticleDistance
from objectData.ObjLoader import ObjFile
import numpy as np
import copy
import math

UP = Verticle(0, 0, 1)

class DepthCamera:
    def __init__(self):
        self.ViewPoint = Verticle(0, 0, 0)
        self.ViewDirection = Verticle(0, -1, 0)

        self.ViewPlaneDistance = 0
        self.ViewPlaneSize = [32, 32]
        self.PixelDistance = 0.01
        self.ViewDegree = 90

        self.__MinDistance = 1
        self.__MaxDistance = 100

        self.Object = ObjFile()

    def Render(self):
        image = np.zeros((self.ViewPlaneSize[0], self.ViewPlaneSize[1]))
        if self.Object is None:
            print("Render object is not set!")
            return image
        if self.ViewDirection.Y == 0:
            print("The camera has no view direction!")
            return image
        possible_faces = []
        for face in self.Object.Faces:
            if face.DistanceFromVerticle(self.ViewPoint) < self.__MaxDistance:
                possible_faces.append(face)
                # TODO: remove faces that are back


        bottom_point, shift_x, shift_y = self.CalculateVectors()

        for x in range(self.ViewPlaneSize[0]):
            for y in range(self.ViewPlaneSize[1]):
                current_point = bottom_point + (shift_x * x) + (shift_y * (self.ViewPlaneSize[1] - y - 1))
                current_point.Normalize()
                current_point *= self.__MaxDistance

                collider_faces = []
                for face in possible_faces:
                    if face.CollisionCheck(self.ViewPoint, current_point):
                        collider_faces.append(face)

        color_img = np.zeros((self.ViewPlaneSize[0], self.ViewPlaneSize[1], 3))
        for x in range(self.ViewPlaneSize[0]):
            for y in range(self.ViewPlaneSize[1]):
                for c in range(3):
                    color_img[x][y][c] = math.floor(255 * image[x][y])
        return color_img
                
                    

    def CalculateVectors(self):
        # RAYTRACING
        t = (self.ViewDirection * self.__MaxDistance) # forward pointing vector
        b = UP.CrossProduct(t)
        tn = copy.deepcopy(t)
        tn.Normalize()
        bn = copy.deepcopy(b)
        bn.Normalize()
        vn = tn.CrossProduct(bn)
        
        C = self.ViewPoint + tn

        hx = self.ViewPlaneSize[0] / 2
        hy = self.ViewPlaneSize[1] / 2

        gx = math.tan(np.radians(self.ViewDegree) / 2)
        gy = gx * (self.ViewPlaneSize[0] / self.ViewPlaneSize[1])

        shift_x = ((2*gx) / (self.ViewPlaneSize[1] - 1)) * bn
        shift_y = ((2*gy) / (self.ViewPlaneSize[0] - 1)) * vn

        bottom_point = tn - gx * bn - gy * vn

        return bottom_point, shift_x, shift_y