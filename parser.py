import string


def __removeVerbEnding(word: str) -> str:
    if len(word) >= 4 and word[-3] == "'":
        return word[:-3]
    elif len(word) >= 3 and word[-2] == "'":
        return word[:-2]
    else:
        return word


def __isLink(word: str) -> bool:
    word = word.strip(string.punctuation)
    return word.startswith("https://") or word.startswith("http://")


def parseOnWords(text: str) -> list:
    return [__removeVerbEnding(word.strip(string.punctuation))
            for word_ in text.split()
            if not __isLink(word_)
            for word in word_.split("/")]  # TODO: remove special characters


# debugging
# text = "Use this link https://stackoverflow.com/questions/42602004/what-does-b-for-a-in-x-for-b-in-a-if-not-b-k-mean"
# print(parseOnWords(text))
# print(text.split())
# print([word.strip(string.punctuation) for word in text.split()])