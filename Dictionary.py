from parser import parseOnWords
from properties import properties


class Dictionary:
    def __init__(self,
                 dictionary: set = None,
                 update_enabled: bool = False,
                 configure_default_general_words_usage: bool = False) -> None:
        self.__dictionary = None if dictionary is None else {w: i for i, w in enumerate(dictionary)}
        self.__dictionary_version = 0
        self.__update_enabled = update_enabled
        self.__words_currency = {}
        self.__words_count = 0
        self.__general_words_usage = {}
        if configure_default_general_words_usage:
            self.configGeneralWordsUsage()

    def __str__(self):
        return str(self.__dictionary) + "\n" + str(self.__words_currency) + "\n"

    def saveToFile(self, path):
        with open(path ,'w') as f:
            for word in self.__dictionary:
                f.write(str(word) + "\n")

    def setFromFile(self, path, update_enabled: bool = False):
        dictionary = set(parseOnWords(open(path).read()))
        self.__dictionary = {w: i for i, w in enumerate(dictionary)}
        self.__update_enabled = update_enabled
        self.__dictionary_version += 1

    def set(self, dictionary: set, update_enabled: bool = False):
        self.__dictionary = {w :i for i ,w in enumerate(dictionary)}
        self.__update_enabled = update_enabled
        self.__dictionary_version += 1

    def getVersion(self) -> int:
        return self.__dictionary_version

    def size(self) -> int:
        return len(self.__dictionary)

    def index(self, word: str) -> bool:
        word = word.lower()
        return self.__dictionary.get(word)

    def setUpdateMode(self, update_enabled: bool):
        self.__update_enabled = update_enabled

    def increaseWordCurrency(self, word: str):
        word = word.lower()
        if self.__update_enabled:
            if self.__words_currency.get(word) is None:
                self.__words_currency[word] = 0
            self.__words_currency[word] += 1
            self.__words_count += 1

    def cleanCurrency(self, threshold: int = properties.dictionary.default_clean_threshold):
        if self.__update_enabled:
            for word in list(self.__words_currency):
                if self.__words_currency[word] <= threshold:
                    self.__words_count -= self.__words_currency[word]
                    self.__words_currency.pop(word)

    def update(self,
               max_size: int = properties.dictionary.default_size,
               threshold: float = properties.dictionary.default_update_threshold):
        if self.__update_enabled:
            if len(self.__general_words_usage) != 0:
                words_usage = []
                for word in self.__words_currency:
                    general_words_usage = self.__general_words_usage[word] \
                        if self.__general_words_usage.get(word) is not None \
                        else 0
                    word_usage = self.__words_currency[word] / self.__words_count - general_words_usage
                    if word_usage > threshold:
                        words_usage.append((word_usage, word))
                if len(words_usage) > 0:
                    words_usage.sort(reverse=True)
                    self.__dictionary = {w[1] :i for i ,w in enumerate(words_usage[:max_size])}
                    self.__dictionary_version += 1

    def configGeneralWordsUsage(self, path="long-text.txt"):  # TODO: test
        self.__dictionary_version += 1
        self.__general_words_usage = {}

        words = parseOnWords(open(path).read())
        for word in words:
            if self.__general_words_usage.get(word) is None:
                self.__general_words_usage[word] = 0
            self.__general_words_usage[word] += 1

        for word in self.__general_words_usage:
            self.__general_words_usage[word] /= len(words)



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

d = Dictionary()
print(d)
d.setUpdateMode(True)
d.increaseWordCurrency("one")
d.increaseWordCurrency("one")
d.increaseWordCurrency("one")
d.increaseWordCurrency("one")
d.increaseWordCurrency("two")
d.increaseWordCurrency("two")
d.increaseWordCurrency("two")
d.increaseWordCurrency("three")
d.increaseWordCurrency("three")
d.increaseWordCurrency("four")
print(d)
d.cleanCurrency(1)
print(d)
d.update(2)
print(d)

