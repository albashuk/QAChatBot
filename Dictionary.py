

class Dictionary: 

    def __init__(self, dictionary: set) -> None:
        self.__dictionary = dictionary

    def saveToFile(self, path):
        with open(path,'w') as f:
            for word in self.__dictionary:
                f.write(str(word) + "\n")

    def setFromFile(self, path):
        self.__dictionary = set(open(path).read().split())

    def autoSet(self, messages):
        pass

    def set(self, dictionary: set):
        self.__dictionary = dictionary

    def get(self):
        return self.__dictionary

    def contains(self, word) -> bool:
        return word in self.__dictionary

# debuging

d = Dictionary(None)
d.set({1, 2, 3, "13"})
d.saveToFile("tmp.txt")
d.setFromFile("tmp.txt")
print(d.get())