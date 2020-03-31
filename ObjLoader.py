import copy

class Verticle2D:
    def __init__(self, x = 0, y = 0):
        self.X = x
        self.Y = y

class Verticle:
    def __init__(self, x: float, y: float, z: float):
        self.X = x
        self.Y = y
        self.Z = z

class Face:
    def __init__(self, v1: Verticle, v2: Verticle, v3: Verticle):
        self.Verticle1 = v1
        self.Verticle2 = v2
        self.Verticle3 = v3

class FaceObject:
    def __init__(self, face: Face):
        self.Point1 = copy.deepcopy(face.Verticle1)
        self.Point2 = copy.deepcopy(face.Verticle2)
        self.Point3 = copy.deepcopy(face.Verticle3)

        # now we create a box, which surround the face for faster collision detection
        self.BoxPoints = []
        self.__Temp = []

        # find limits of x, y and z
        self.__FindLimitValues()

        # setting bounding box points
        self.BoxPoints.append(Verticle(self.__Temp[3], self.__Temp[1], self.__Temp[2])) # top front left - smallest x, largest y, largest z
        self.BoxPoints.append(Verticle(self.__Temp[0], self.__Temp[1], self.__Temp[2])) # top front right - largest x, largest y, largest z
        self.BoxPoints.append(Verticle(self.__Temp[3], self.__Temp[4], self.__Temp[2])) # top back left - smallest x, smallest y, largest z
        self.BoxPoints.append(Verticle(self.__Temp[0], self.__Temp[4], self.__Temp[2])) # top back right - largest x, smallest y, largest z

        self.BoxPoints.append(Verticle(self.__Temp[3], self.__Temp[1], self.__Temp[2])) # bottom front left - smallest x, largest y, smallest z
        self.BoxPoints.append(Verticle(self.__Temp[0], self.__Temp[1], self.__Temp[2])) # bottom front right - largest x, largest y, smallest z
        self.BoxPoints.append(Verticle(self.__Temp[3], self.__Temp[4], self.__Temp[2])) # bottom back left - smallest x, smallest y, smallest z
        self.BoxPoints.append(Verticle(self.__Temp[0], self.__Temp[4], self.__Temp[2])) # bottom back right - largest x, smallest y, smallest z
    
    def __FindLimitValues(self):
        lx = self.Point1.X
        if self.Point2.X > lx:
            lx = self.Point2.X
        if self.Point3.X > lx:
            self.Point3.X
        
        sx = self.Point1.X
        if self.Point2.X < sx:
            sx = self.Point2.X
        if self.Point3.X < sx:
            sx = self.Point3.X

        ly = self.Point1.Y
        if self.Point2.Y > ly:
            ly = self.Point2.Y
        if self.Point3.Y > ly:
            self.Point3.Y

        sy = self.Point1.Y
        if self.Point2.Y < sy:
            sy = self.Point2.Y
        if self.Point3.Y < sy:
            sy = self.Point3.Y

        lz = self.Point1.Z
        if self.Point2.Z > lz:
            lz = self.Point2.Z
        if self.Point3.Z > lz:
            self.Point3.Z

        sz = self.Point1.Z
        if self.Point2.Z < sz:
            sz = self.Point2.Z
        if self.Point3.Z < sz:
            sz = self.Point3.Z
        
        self.__Temp.append(lx, ly, lz, sx, sy, sz)

    def BoxCollision(self, line_start: Verticle, line_end: Verticle):
        # front view
        start = Verticle2D(line_start.X, line_start.Z)
        end = Verticle2D(line_end.X, line_end.Z)
        p1 = Verticle2D(self.BoxPoints[0].X, self.BoxPoints[0].Z)
        p2 = Verticle2D(self.BoxPoints[1].X, self.BoxPoints[1].Z)
        p3 = Verticle2D(self.BoxPoints[4].X, self.BoxPoints[4].Z)
        p4 = Verticle2D(self.BoxPoints[5].X, self.BoxPoints[5].Z)
        front = self.RectCollision(start, end, p1, p2, p3, p4)
        # side view
        start = Verticle2D(line_start.Y, line_start.Z)
        end = Verticle2D(line_end.Y, line_end.Z)
        p1 = Verticle2D(self.BoxPoints[0].Y, self.BoxPoints[0].Z)
        p2 = Verticle2D(self.BoxPoints[2].Y, self.BoxPoints[2].Z)
        p3 = Verticle2D(self.BoxPoints[4].Y, self.BoxPoints[4].Z)
        p4 = Verticle2D(self.BoxPoints[6].Y, self.BoxPoints[6].Z)
        side = self.RectCollision(start, end, p1, p2, p3, p4)
        # top view
        start = Verticle2D(line_start.X, line_start.Y)
        end = Verticle2D(line_end.X, line_end.Y)
        p1 = Verticle2D(self.BoxPoints[2].X, self.BoxPoints[2].Y)
        p2 = Verticle2D(self.BoxPoints[4].X, self.BoxPoints[4].Y)
        p3 = Verticle2D(self.BoxPoints[0].X, self.BoxPoints[0].Y)
        p4 = Verticle2D(self.BoxPoints[3].X, self.BoxPoints[3].Y)
        top = self.RectCollision(start, end, p1, p2, p3, p4)

        return (front or side or top)
    
    def RectCollision(self, line_start: Verticle2D, line_end: Verticle2D, point1: Verticle2D, point2: Verticle2D, point3: Verticle2D, point4: Verticle2D):
        left = self.LineCollision(line_start, line_end, point1, point3)
        right = self.LineCollision(line_start, line_end, point2, point4)
        top = self.LineCollision(line_start, line_end, point1, point2)
        bottom = self.LineCollision(line_start, line_end, point3, point4)
        return (left or right or top or bottom)

    @staticmethod
    def LineCollision(line_a_start: Verticle2D, line_a_end: Verticle2D, line_b_start: Verticle2D, line_b_end: Verticle2D):
        uA = ((line_b_end.x-line_b_start.x)*(line_a_start.y-line_b_start.y) - (line_b_end.y-line_b_start.y)*(line_a_start.x-line_b_start.x)) / ((line_b_end.y-line_b_start.y)*(line_a_end.x-line_a_start.x) - (line_b_end.x-line_b_start.x)*(line_a_end.y-line_a_start.y))
        uB = ((line_a_end.x-line_a_start.x)*(line_a_start.y-line_b_start.y) - (line_a_end.y-line_a_start.y)*(line_a_start.x-line_b_start.x)) / ((line_b_end.y-line_b_start.y)*(line_a_end.x-line_a_start.x) - (line_b_end.x-line_b_start.x)*(line_a_end.y-line_a_start.y))
        return (uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1)
        

class ObjFile:
    def __init__(self, file = None):
        self.FileName = file
        self.Vertices = []
        self.Faces = []
        self.GeneratedFaces = []

        if file is not None:
            self.LoadFile(self.FileName)

    def LoadFile(self, file):
        if self.FileName is None:
            self.FileName = file
        self.__ReadFile()
        self.__GenerateData()
        

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
    
    def __GenerateData(self):
        for f in self.Faces:
            self.GeneratedFaces.append(FaceObject(f))
        self.Faces = []
        self.Vertices = []
