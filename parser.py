import string


def parseOnWords(text: str):
    return [word.strip(string.punctuation) for word in text.split()]  # TODO: remove special characters
