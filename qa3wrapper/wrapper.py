import re
import json
import os

import qa3wrapper.interface as interface


def get_answer_from_qa3(question):
    qa3_answer = interface.get_json(question=question)
    if qa3_answer is not None:
        answer = Answer(answer=qa3_answer)
    else:
        answer = Answer()

    return answer


def get_answer_from_dump(answer_id, file_name):
    directory = os.path.dirname(__file__)
    data_path = os.path.join(directory, 'dumps/'+file_name+'.json')
    with open(data_path, newline='') as data_file:
        answers = json.load(data_file)

    if answer_id in answers:
        answer = Answer(answer=answers[answer_id])
        return answer
    else:
        return None


class Answer:
    def __init__(self, answer=None):
        if answer is not None:
            self.dataset = answer['dataset']
            self.question = answer['question']
            self.raw_result = answer['result']

            rows = re.split('\n', self.raw_result)
            self.result = []
            for row in rows:
                if row.count('\t') > 1:
                    r = Result(row)
                    self.result.append(r)

            self.api_status = None
        else:
            self.dataset = None
            self.question = None
            self.raw_result = None
            self.result = None
            self.api_status = 'API rate limit exceeded'


class Result:
    def __init__(self, row):
        result = re.split('\t', row)
        self.chunk = result[0]
        self.subject = result[1]
        self.property = result[2]
        self.value = result[3]
        # self.value = re.split('"', result[3])[1]

    def is_dataset(self, dataset):
        return re.split('"', self.value)[1] == dataset or re.match('<http://linkedspending.aksw.org/instance/' + dataset
                                                                   + '>', self.subject)

    def is_identifier(self):
        return self.property == '<http://purl.org/dc/terms/identifier>'

    def is_integer(self):
        return re.search('_[0-9]+', self.value)

    def is_type(self, type_name):
        return self.property == '<http://linkedspending.aksw.org/ontology/'+type_name+'>'
