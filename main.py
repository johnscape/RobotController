from objectData.rayTracer import DepthCamera
import cv2
import numpy as np
import math


d = DepthCamera()
d.Object.LoadFile("F:\\Prog\\GIT\\RobotController\\rectangle.obj")
d.Object.SwapZY()
d.ViewPlaneSize = [512, 512]
d.ViewDegree = 90
img_data = d.Render()
cv2.imshow("Depth map", img_data)
cv2.waitKey(0)
cv2.destroyAllWindows()
save_data = np.zeros((img_data.shape[0], img_data.shape[1], 3))
for x in range(img_data.shape[0]):
    for y in range(img_data.shape[1]):
        for c in range(3):
            save_data[x][y][c] = round(img_data[x][y] * 255)
save_data = np.clip(save_data, 0, 255)
save_data = save_data.astype(np.uint8)
cv2.imwrite("data.png", save_data)