

class Dictionary: 

    def __init__(self, dictionary: set) -> None:
        self.__dictionary = None if dictionary == None else {w:i for i,w in enumerate(dictionary)}

    def saveToFile(self, path):
        with open(path,'w') as f:
            for word in self.__dictionary:
                f.write(str(word) + "\n")

    def setFromFile(self, path):
        dictionary = set(open(path).read().split())
        self.__dictionary = {w:i for i,w in enumerate(dictionary)}

    def autoSet(self, messages):
        pass

    def set(self, dictionary: set):
        self.__dictionary = {w:i for i,w in enumerate(dictionary)}

    def get(self):
        return self.__dictionary

    def size(self) -> int:
        return len(self.__dictionary)

    def index(self, word) -> bool:
        return self.__dictionary.get(word)

# debuging

# d = Dictionary(None)
# d.set({1, 2, 3, "13"})
# d.saveToFile("tmp.txt")
# d.setFromFile("tmp.txt")
# print(d.get())

# d = Dictionary({"1", "2", 3})
# print(d.get())
# print(d.index(3))
# print(d.index("2"))
# print(d.index(2))