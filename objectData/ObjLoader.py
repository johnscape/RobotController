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





