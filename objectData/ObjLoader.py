from __future__ import annotations
import copy
import math
#IMPORTANT NOTE: In this project, I'll be using the Z-up setup, meaning, that Y will be depth and Z will be the height value

class Verticle2D:
    """
    A class used to represent a 2D verticle

    Attributes
    ----------
    X : float
        The X coordinate of the verticle
    Y : float
        The Y coordinate of the verticle
    """
    def __init__(self, x = 0, y = 0):
        self.X = x
        self.Y = y

    """
    Returns True if it equals with another verticle

    Parameters
    ----------
    other : Verticle2D
        The other verticle to check
    """
    def __eq__(self, other):
        return self.X == other.X and self.Y == other.Y

class Verticle:
    """
    A class used to represent a 3D verticle

    Attributes
    ----------
    X : float
        The X coordinate of the verticle
    Y : float
        The Y coordinate of the verticle
    Z : float
        The Z coordinate of the verticle

    Methods
    -------
    GetValue(coordinate)
        Returns with the selected coordinate
    CrossProduct(other)
        Calculates the cross product with another verticle.
        Returns a verticle representing the cross product.
    DorProduct(other)
        Calculates the cross product with another verticle.
        Returns a verticle representing the cross product.
    """
    def __init__(self, x: float, y: float, z: float):
        self.X = x
        self.Y = y
        self.Z = z

    def GetValue(self, coordinate: int) -> float:
        """
        Returns with the selected coordinate
        If the value is out of range, returns 0

        Parameters
        ----------
        coordinate : int
            The coordinate to return
        """
        if coordinate == 0: return self.X
        elif coordinate == 1: return self.Y
        elif coordinate == 2: return self.Z
        return 0

    def __eq__(self, other) -> bool:
        """
        Returns True if it equals with another verticle

        Parameters
        ----------
        other : Verticle
            The other verticle to check
        """
        return self.X == other.X and self.Y == other.Y and self.Z == other.Z

    def __sub__(self, other):
        return Verticle(self.X - other.X, self.Y - other.Y, self.Z - other.Z)

    def __add__(self, other):
        return Verticle(self.X + other.X, self.Y + other.Y, self.Z + other.Z)

    def __neg__(self):
        return Verticle(-self.X, -self.Y, -self.Z)

    
    def CrossProduct(self, other) -> Verticle:
        """
        Calculates the cross product with another verticle.
        Returns a verticle representing the cross product.

        Parameters
        ----------
        other : Verticle
            The other verticle
        """
        i = (self.Y * other.Z) - (self.Z * other.Y)
        j = (self.Z * other.X) - (self.X * other.Z)
        k = (self.X * other.Y) - (self.Y * other.X)
        return Verticle(i, j, k)

    def DotProduct(self, other) -> float:
        """
        Calculates the dot product with another verticle

        Parameters
        ----------
        other : Verticle
            The other verticle
        """
        x = self.X * other.X
        y = self.Y * other.Y
        z = self.Z * other.Z
        return x + y + z
        

class Face:
    """
    A class used to represent an face created by 3 vertices

    Attributes
    ----------
    Verticle1 : Verticle
        The first verticle which creates the face
    Verticle1 : Verticle
        The second verticle which creates the face
    Verticle1 : Verticle
        The third verticle which creates the face

    Methods
    -------
    CollisionCheck(line_start, line_end)
        Returns a True if the 3D line intersects/collides with the face, False otherwise.
    GenerateNormal()
        Returns a verticle representing the face's normal vector.
    CalculateAverage()
        Returns a verticle made from the other verticles avarage value.
    """
    def __init__(self, v1: Verticle, v2: Verticle, v3: Verticle):
        self.Verticle1 = v1
        self.Verticle2 = v2
        self.Verticle3 = v3

    def CollisionCheck(self, line_start: Verticle, line_end: Verticle) -> bool:
        """
        Returns a True if the 3D line intersects/collides with the face, False otherwise.
        
        Parameters
        ----------
        line_start : Verticle
            The starting point of the 3D line
        line_end : Verticle
            The ending point of the 3D line
        """
        front = self.__PartCheck(line_start, line_end, 0, 2)
        side = self.__PartCheck(line_start, line_end, 1, 2)
        top = self.__PartCheck(line_start, line_end, 0, 1)

        return (front and side) or (side and top) or (front and top)

    def GenerateNormal(self) -> Verticle:
        """
        Returns a verticle representing the face's normal vector.
        """
        v1 = self.Verticle2 - self.Verticle1
        v2 = self.Verticle3 - self.Verticle1
        return v1.CrossProduct(v2)

    def CalculateAverage(self) -> Verticle:
        """
        Returns a verticle made from the other verticles avarage value.
        """
        x = (self.Verticle1.X + self.Verticle2.X + self.Verticle3.X) / 3
        y = (self.Verticle1.Y + self.Verticle2.Y + self.Verticle3.Y) / 3
        z = (self.Verticle1.Z + self.Verticle2.Z + self.Verticle3.Z) / 3
        return Verticle(x, y, z)

    def __PartCheck(self, line_start: Verticle, line_end: Verticle, x_dimension: int, y_dimension: int) -> bool:
        """
        Returns a True if the 3D line intersects/collides with the face from a specific view, False otherwise.
        
        Parameters
        ----------
        line_start : Verticle
            The starting point of the 3D line
        line_end : Verticle
            The ending point of the 3D line
        x_dimension : int
            Selects a dimension from 3D to use in 2D as X (i.e. 1 means that the 3D Y value will be used as the 2D X)
        y_dimension : int
            Selects a dimension from 3D to use in 2D as Y (i.e. 2 means that the 3D Z value will be used as the 2D Y)
        """
        line_start_view = Verticle2D(line_start.GetValue(x_dimension), line_start.GetValue(y_dimension))
        line_end_view = Verticle2D(line_end.GetValue(x_dimension), line_end.GetValue(y_dimension))

        #v1 and v2
        collider_start = Verticle2D(self.Verticle1.GetValue(x_dimension), self.Verticle1.GetValue(y_dimension))
        collider_end = Verticle2D(self.Verticle2.GetValue(x_dimension), self.Verticle2.GetValue(y_dimension))
        if LineCollision(line_start_view, line_end_view, collider_start, collider_end):
            return True
        # v2 and v3
        collider_start = Verticle2D(self.Verticle2.GetValue(x_dimension), self.Verticle2.GetValue(y_dimension))
        collider_end = Verticle2D(self.Verticle3.GetValue(x_dimension), self.Verticle3.GetValue(y_dimension))
        if LineCollision(line_start_view, line_end_view, collider_start, collider_end):
            return True

        # v3 and v1
        collider_start = Verticle2D(self.Verticle3.GetValue(x_dimension), self.Verticle3.GetValue(y_dimension))
        collider_end = Verticle2D(self.Verticle1.GetValue(x_dimension), self.Verticle1.GetValue(y_dimension))
        return LineCollision(line_start_view, line_end_view, collider_start, collider_end)
        

class ObjFile:
    def __init__(self, file = None):
        self.FileName = file
        self.Vertices = []
        self.Faces = []

        if file is not None:
            self.LoadFile(self.FileName)

    def LoadFile(self, file):
        if self.FileName is None:
            self.FileName = file
        self.__ReadFile()
        

    def __ReadFile(self):
        with open(self.FileName, 'r') as reader:
            line = reader.readline()
            current_line = 1
            while line:
                if line[0] != '#':
                    splits = line.split(' ')
                    if splits[0] == 'v':
                        self.Vertices.append(Verticle(float(splits[1]), float(splits[2]), float([3])))
                    elif splits[0] == 'f':
                        v1 = self.Vertices[int(splits[1])]
                        v2 = self.Vertices[int(splits[2])]
                        v3 = self.Vertices[int(splits[3])]
                        self.Faces.append(Face(v1, v2, v3))
                    else:
                        print("Unknown data: " + line + "\n at line: " + str(current_line))
                        break
                line = reader.readline()
                current_line = 1


def LineCollision(line_a_start: Verticle2D, line_a_end: Verticle2D, line_b_start: Verticle2D, line_b_end: Verticle2D) -> bool:
        """
        Returns a True if the two 2D line intersects/collides, False otherwise.

        Parameters
        ----------
        line_a_start : Verticle2D
            The starting point of the first 2D line
        line_a_end : Verticle2D
            The ending point of the first 2D line
        line_b_start : Verticle2D
            The starting point of the second 2D line
        line_b_end : Verticle2D
            The ending point of the second 2D line
        """
        if line_a_start == line_a_end or line_b_start == line_b_end: # if line a or b is just a point
            if (line_a_start == line_a_end and line_b_end == line_b_start): # if line a and b is just a point
                return line_a_start == line_b_start
            if line_a_start == line_a_end: # if line a is just a point
                return (line_b_start.X - line_b_end.X) * (line_b_start.Y - line_b_end.Y) == (line_b_end.X - line_a_end.X) * (line_b_end.Y - line_a_end.Y)
            if line_b_end == line_b_start: # if line b is just a point
                return (line_a_start.X - line_a_end.X) * (line_a_start.Y - line_a_end.Y) == (line_a_end.X - line_b_end.X) * (line_a_end.Y - line_b_end.Y)

        aXDist = line_a_end.X-line_a_start.X
        aYDist = line_a_end.Y-line_a_start.Y
        bXDist = line_b_end.X-line_b_start.X
        bYDist = line_b_end.Y-line_b_start.Y
        dividor = ((bYDist)*(aXDist) - (bXDist)*(aYDist))
        if dividor == 0: # this means, that the two lines are in the same dimension (booth have the same x or y component)
            if aXDist == 0 and bXDist == 0:
                return (line_a_start.Y <= line_b_start.Y <= line_a_end.Y or line_a_start.Y <= line_b_end.Y <= line_a_end.Y) or \
                    (line_a_end.Y <= line_b_start.Y <= line_a_start.Y or line_a_end.Y <= line_b_end.Y <= line_a_start.Y)
            # since the two cannot be points (we already checked that), the two must share the same Y value
            return (line_a_start.X <= line_b_start.X <= line_a_end.X or line_a_start.X <= line_b_end.X <= line_a_end.X) or \
                (line_a_end.X <= line_b_start.X <= line_a_start.X or line_a_end.X <= line_b_end.X <= line_a_start.X)
        uA = ((line_b_end.X-line_b_start.X)*(line_a_start.Y-line_b_start.Y) - (line_b_end.Y-line_b_start.Y)*(line_a_start.X-line_b_start.X)) / dividor
        uB = ((line_a_end.X-line_a_start.X)*(line_a_start.Y-line_b_start.Y) - (line_a_end.Y-line_a_start.Y)*(line_a_start.X-line_b_start.X)) / dividor
        return (uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1)

def VerticleDistance(a: Verticle, b: Verticle) -> float:
    """
    Returns the Euclidan distance of two vertices

    Parameters
    ----------
    a : Verticle
        The first verticle
    b : Verticle
        The second verticle
    """
    return math.sqrt(pow(a.X - b.X, 2) + pow(a.Y - b.Y, 2) + pow(a.Z - b.Z, 2))

def NormalizeLine(start_point: Verticle, end_point: Verticle) -> Verticle:
    """
    Takes two vertices, representing a segment, then returns the normalised end point, so the segments lenght will be 1

    Parameters
    ----------
    a : Verticle
        The first verticle
    b : Verticle
        The second verticle
    """
    new_end = end_point - start_point
    dist = VerticleDistance(Verticle(0, 0, 0), new_end)
    if dist == 0 or dist == 1:
        return new_end + start_point
    return Verticle(new_end.X / dist, new_end.Y / dist, new_end.Z / dist) + start_point

def LineFaceCollision(face: Face, line_start: Verticle, line_end: Verticle) -> Verticle:
    """
    Calculates the position of the line-face collision. Returns the point of the collision

    Parameters
    ----------
    face : Face
        The colliding face
    line_start : Verticle
        The starting point of the ray
    line_end: Verticle
        A point on the ray. Used to calculate the ray's trajectory.
    """
    # algorithm based on: http://geomalgorithms.com/a05-_intersect-1.html
    n = face.GenerateNormal()
    P0 = copy.deepcopy(line_start)
    u = line_end - line_start
    P1 = P0 + u
    V0 = face.CalculateAverage()
    dotp = n.DotProduct(u)
    if dotp == 0:
        return Verticle(0, 0, 0)
    w = P0 - V0
    sI = (w.DotProduct(-n)) / dotp
    return Verticle(u.X * sI + w.X + V0.X, u.Y * sI + w.Y + V0.Y, u.Z * sI + w.Z + V0.Z)


