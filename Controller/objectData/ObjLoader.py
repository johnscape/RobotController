from objectData.objectView import Face, Verticle
from settings import Verbose

class ObjFile:
    def __init__(self, file = None):
        self.FileName = file
        self.Vertices = []
        self.Faces = []
        self.VerboseSetting = Verbose.FULL

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
                line = line[:-1]
                if len(line) <= 1:
                    line = reader.readline()
                    current_line += 1
                    continue
                if line[0] != '#':
                    splits = line.split(' ')
                    if splits[0] == 'v':
                        self.Vertices.append(Verticle(float(splits[1]), float(splits[2]), float(splits[3])))
                    elif splits[0] == 'f':
                        if '//' in splits[1]:
                            v1 = self.Vertices[int(splits[1].split('//')[0]) - 1]
                            v2 = self.Vertices[int(splits[2].split('//')[0]) - 1]
                            v3 = self.Vertices[int(splits[3].split('//')[0]) - 1]
                            self.Faces.append(Face(v1, v2, v3))
                        else:
                            v1 = self.Vertices[int(splits[1]) - 1]
                            v2 = self.Vertices[int(splits[2]) - 1]
                            v3 = self.Vertices[int(splits[3]) - 1]
                            self.Faces.append(Face(v1, v2, v3))
                    elif self.VerboseSetting.value == 0:
                        print("Unknown data: " + line + "\nat line: " + str(current_line))
                line = reader.readline()
                current_line += 1
        if self.VerboseSetting.value[0] <= 1:
            print("Obj loading finished!")

    def SwapZY(self):
        for face in self.Faces:
            face.SwapUp()


