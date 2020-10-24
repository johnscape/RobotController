from objectData.rayTracer import DepthCamera
from objectData.objectView import Verticle
import math

def test_vectorCalc1():
    d = DepthCamera()
    d.ViewPlaneSize = [640, 480]
    d.ViewDegree = 90
    d.ViewDirection = Verticle(0, 1, 0)
    b, x, y = d.CalculateVectors()
    errors = []
    if abs(x.Sum() - Verticle(-(2/479), 0, 0).Sum()) > 0.001:
        errors.append("X shift value is not expected! {0}, {1}, {2}".format(x.X, x.Y, x.Z))
    if abs(y.Sum() - Verticle(0, 0, 0.004).Sum()) > 0.001:
        errors.append("Y shift value is not expected! {0}, {1}, {2}".format(y.X, y.Y, y.Z))
    if abs(b.Sum() - Verticle(1, 1, -(640/480)).Sum()) > 0.001:
        errors.append("Bottom value is not expected! {0}, {1}, {2}".format(b.X, b.Y, b.Z))
    
    assert errors == []

def test_rectangleCenter():
    d = DepthCamera()
    d.ViewPlaneSize = [5, 5]
    d.ViewDegree = 60
    d.ViewDirection = Verticle(0, -1, 0)
    d.Object.LoadFile("F:\\Prog\\GIT\\RobotController\\rectangle.obj")

    img = d.Render()

    assert img[3][3][0] != img[0][3][0]
