import json
import random
from torch.utils.data import Dataset

class QuestionDetDataset:
    class Data(Dataset):
        def __init__(self, sentences) -> None:
            self.sentences = sentences

        def __len__(self):
            return len(self.sentences)

        def __getitem__(self, index):
            return self.sentences[index]

    def getDataset(name) -> Data:
        match name:
            case "SQuAD":
                return QuestionDetDataset.__SQuAD('train-v2.0.json'), QuestionDetDataset.__SQuAD('dev-v2.0.json')
            case _:
                print("No dataset selected")
                return None

    def buildDataset(sentences):
        return QuestionDetDataset.Data(sentences)

    def __SQuAD(path):
        with open(path, 'r') as file:
            data = json.load(file)

            questions = []
            answers = []
            for block in data["data"]:
                for paragraph in block["paragraphs"]:
                    for qa in paragraph["qas"]:
                        questions.append([qa["question"], 1])
                        if qa["is_impossible"] == False:
                            answers.append([qa["answers"][0]["text"], 0])

            sentences = questions + answers
            random.shuffle(sentences)

            return QuestionDetDataset.Data(sentences)

            # print(data["data"][0]["paragraphs"][0]["qas"][0]["question"])
            # print(len(questions))
            # print(len(answers))


# t,d = QuestionDetDataset.getDataset("SQuAD")
# print(t[0],d[0])
# x,y = t[0]
# print(x, y)