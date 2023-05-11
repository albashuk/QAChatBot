import string
import nltk

nltk.download('punkt')
stemmer = nltk.PorterStemmer()


def wordToStem(word: str) -> str:
    if len(word) >= 4 and word[-3] == "'":
        word = word[:-3]
    elif len(word) >= 3 and word[-2] == "'":
        word = word[:-2]
    else:
        word = word
    return stemmer.stem(word)


def __isLink(word: str) -> bool:
    word = word.strip(string.punctuation)
    return word.startswith("https://") or word.startswith("http://")


def parseOnWords(text: str) -> list:
    return [wordToStem(word.strip(string.punctuation))
            for word_ in text.split()
            if not __isLink(word_)
            for word in word_.split("/")
            if len(wordToStem(word.strip(string.punctuation))) > 0]  # TODO: remove special characters


def parseOnSentences(text: str) -> list:
    return nltk.tokenize.sent_tokenize(text)


# debugging

# text = "Use this link https://stackoverflow.com/questions/42602004/what-does-b-for-a-in-x-for-b-in-a-if-not-b-k-mean"
# print(parseOnWords(text))
# print(text.split())
# print([word.strip(string.punctuation) for word in text.split()])

# text = 'Some sentence. Mr.Holmes... This is a new sentence! And is this another one? Hi!'
# print(parseOnWords(text))
# print(parseOnSentences(text))
# text = 'The U.S. Drug Enforcement Administration (DEA) says hello. And have a nice day.'
# print(parseOnWords(text))
# print(parseOnSentences(text))

