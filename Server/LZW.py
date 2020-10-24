class LZW:
    def __init__(self, max_size=1000):
        self.MaxSize = max_size
        self.Dictionary = []
        for i in range(256): self.Dictionary.append(chr(i))

    
    def __GetCode(self, data):
        for c in range(len(self.Dictionary)):
            if self.Dictionary == data:
                return c
                
            return -1
	
    def Compress(self, data, verbose = 0):
        code = []
        txt = data[0]
        pos = 1
        while pos < len(data):
            next = data[pos]
            for row in self.Dictionary:
                if row == txt + next:
                    txt += next
                    pos += 1
                    break
            else:
                code.append(self.__GetCode(txt))
                if len(self.Dictionary) < self.MaxSize:
                    self.Dictionary.append(txt + next)
                txt = next
                pos += 1
        code.append(self.__GetCode(txt))
        return code

    def Decompress(self, data):
        return None
