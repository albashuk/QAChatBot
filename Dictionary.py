from parser import parseOnWords
from properties import properties


class Dictionary:
    def __init__(self,
                 dictionary: set = None,
                 update_enabled: bool = False,
                 configure_default_common_words_usage: bool = False) -> None:
        self.__dictionary = None if dictionary is None else {w: i for i, w in enumerate(dictionary)}
        self.__dictionary_version = 0
        self.__update_enabled = update_enabled
        self.__words_currency = {}
        self.__words_count = 0
        self.__common_words_usage = {}
        if configure_default_common_words_usage:
            self.configCommonWordsUsage()

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
        self.__dictionary = {w: i for i, w in enumerate(dictionary)}
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
               common_words_weight: float = properties.dictionary.default_common_words_weight,
               threshold: float = properties.dictionary.default_update_threshold):
        if self.__update_enabled:
            if len(self.__common_words_usage) != 0:
                words_usage = []
                for word in self.__words_currency:
                    common_words_usage = self.__common_words_usage[word] \
                        if self.__common_words_usage.get(word) is not None \
                        else 0
                    word_usage = self.__words_currency[word] / self.__words_count \
                                 - common_words_usage * common_words_weight
                    if word_usage > threshold:
                        words_usage.append((word_usage, word))
                if len(words_usage) > 0:
                    words_usage.sort(reverse=True)
                    self.__dictionary = {w[1]: i for i, w in enumerate(words_usage[:max_size])}
                    self.__dictionary_version += 1

    def configCommonWordsUsage(self, path="long-text.txt"):
        self.__dictionary_version += 1
        self.__common_words_usage = {}

        words = parseOnWords(open(path, "r", encoding="utf-8").read())
        for word in words:
            word = word.lower()
            if self.__common_words_usage.get(word) is None:
                self.__common_words_usage[word] = 0
            self.__common_words_usage[word] += 1

        for word in self.__common_words_usage:
            self.__common_words_usage[word] /= len(words)



# debugging

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

# d = Dictionary(configure_default_common_words_usage=True)
# print(d)
# d.setUpdateMode(True)
# d.increaseWordCurrency("one")
# d.increaseWordCurrency("one")
# d.increaseWordCurrency("one")
# d.increaseWordCurrency("one")
# d.increaseWordCurrency("two")
# d.increaseWordCurrency("two")
# d.increaseWordCurrency("two")
# d.increaseWordCurrency("three")
# d.increaseWordCurrency("three")
# d.increaseWordCurrency("four")
# print(d)
# d.cleanCurrency(1)
# print(d)
# d.update(2)
# print(d)

# d = Dictionary(configure_default_common_words_usage=True)
# d.setUpdateMode(True)
# words = parseOnWords("Kublai's government faced financial difficulties after 1279. Wars and construction projects had drained the Mongol treasury. Efforts to raise and collect tax revenues were plagued by corruption and political scandals. Mishandled military expeditions followed the financial problems. Kublai's second invasion of Japan in 1281 failed because of an inauspicious typhoon. Kublai botched his campaigns against Annam, Champa, and Java, but won a Pyrrhic victory against Burma. The expeditions were hampered by disease, an inhospitable climate, and a tropical terrain unsuitable for the mounted warfare of the Mongols. The Tran dynasty which ruled Annam (Dai Viet) crushed and defeated the Mongols at the Battle of B\u1ea1ch \u0110\u1eb1ng (1288). The Chinese region of Fujian was the original home of the Chinese Tran (Chen) clan before they migrated under Tr\u1ea7n Kinh (\u9673\u4eac, Ch\u00e9n J\u012bng) to Dai Viet and whose descendants established the Tr\u1ea7n dynasty which ruled Vietnam \u0110\u1ea1i Vi\u1ec7t, and certain members of the clan could still speak Chinese such as when a Yuan dynasty envoy had a meeting with the Chinese-speaking Tr\u1ea7n prince Tr\u1ea7n Qu\u1ed1c Tu\u1ea5n (later King Tr\u1ea7n H\u01b0ng \u0110\u1ea1o) in 1282. Professor Liam Kelley noted that people from Song dynasty China like Zhao Zhong and Xu Zongdao fled to Tran dynasty ruled Vietnam after the Mongol invasion of the Song and they helped the Tran fight against the Mongol invasion. The Tran dynasty originated from the Fujian region of China as did the Daoist cleric Xu Zongdao who recorded the Mongol invasion and referred to them as \"Northern bandits\". Annam, Burma, and Champa recognized Mongol hegemony and established tributary relations with the Yuan dynasty.")
# for word in words:
#     d.increaseWordCurrency(word)
# # print(d)
# d.update(100)
# print(d)


