from objectData.rayTracer import DepthCamera
from PIL import Image


d = DepthCamera()
d.Object.LoadFile("F:\\Prog\\GIT\\RobotController\\rectangle.obj")
d.Object.SwapZY()
img_data = d.Render()
img = Image.fromarray(img_data, mode="RGB")
img.show()