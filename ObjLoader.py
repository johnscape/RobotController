import copy

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
        if self.LineCollision(line_start_view, line_end_view, collider_start, collider_end):
            return True
        # v2 and v3
        collider_start = Verticle2D(self.Verticle2.GetValue(x_dimension), self.Verticle2.GetValue(y_dimension))
        collider_end = Verticle2D(self.Verticle3.GetValue(x_dimension), self.Verticle3.GetValue(y_dimension))
        if self.LineCollision(line_start_view, line_end_view, collider_start, collider_end):
            return True

        # v3 and v1
        collider_start = Verticle2D(self.Verticle3.GetValue(x_dimension), self.Verticle3.GetValue(y_dimension))
        collider_end = Verticle2D(self.Verticle1.GetValue(x_dimension), self.Verticle1.GetValue(y_dimension))
        return self.LineCollision(line_start_view, line_end_view, collider_start, collider_end)
        


    @staticmethod
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
        uA = ((line_b_end.x-line_b_start.x)*(line_a_start.y-line_b_start.y) - (line_b_end.y-line_b_start.y)*(line_a_start.x-line_b_start.x)) / ((line_b_end.y-line_b_start.y)*(line_a_end.x-line_a_start.x) - (line_b_end.x-line_b_start.x)*(line_a_end.y-line_a_start.y))
        uB = ((line_a_end.x-line_a_start.x)*(line_a_start.y-line_b_start.y) - (line_a_end.y-line_a_start.y)*(line_a_start.x-line_b_start.x)) / ((line_b_end.y-line_b_start.y)*(line_a_end.x-line_a_start.x) - (line_b_end.x-line_b_start.x)*(line_a_end.y-line_a_start.y))
        return (uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1)
        

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
