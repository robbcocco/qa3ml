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


def get_answer_from_dump(answer_id):
    directory = os.path.dirname(__file__)
    data_path = os.path.join(directory, 'dumps/test.json')
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
        self.subject = result[1]
        self.property = result[2]
        self.value = result[3]
        # self.value = re.split('"', result[3])[1]
