import json
import os
import re


def get_test_data(file_name):
    directory = os.path.dirname(__file__)
    data_path = os.path.join(directory, 'datasets/'+file_name+'.json')
    with open(data_path, newline='') as data_file:
        data = json.load(data_file)
        return data


class Dataset:
    def __init__(self, file_name):
        test_data = get_test_data(file_name)
        self.questions = []

        for raw_question in test_data['questions']:
            question = DCQuestion(raw_question=raw_question)
            self.questions.append(question)


class DCQuestion:
    def __init__(self, raw_question):
        self.id = raw_question['id']
        self.question = raw_question['question'][0]['string']
        self.query = raw_question['query']['sparql']
        self.aggregation = raw_question['aggregation']

        dataset = None
        if re.search(' from <([a-z]|[0-9]|-|_|\.|/|:)*> ', self.query) is not None:
            dataset = re.search(' from <([a-z]|[0-9]|-|_|\.|/|:)*> ', self.query).group(0)
            dataset = re.sub(' from <http://linkedspending.aksw.org/', '', dataset)
            dataset = re.sub('>', '', dataset)
        self.dataset = str(dataset)

        # self.vars = []
        # for var in raw_question['answers'][0]['head']['vars']:
        #     self.vars.append(var)
        #
        # self.answers = []
        # for binding in raw_question['answers'][0]['results']['bindings']:
        #     for var in self.vars:
        #         answer = Answer(var, binding[var])
        #         self.answers.append(answer)


class Answer:
    def __init__(self, var, answer):
        self.var = var
        self.type = answer['type']
        self.value = answer['value']
