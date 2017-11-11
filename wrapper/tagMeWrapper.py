import re
import json
import os

import wrapper.interface as interface


def get_answer_from_web(question):
    raw_answer = interface.get_json(question=question, site='TagMe')
    if raw_answer is not None:
        answer = Answer(answer=raw_answer)
    else:
        answer = Answer()

    return answer


def get_answer_from_dump(answer_id, file_name):
    directory = os.path.dirname(__file__)
    data_path = os.path.join(directory, 'dumps/' + file_name + '.json')
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
            self.dataset = ''
            self.question = None
            self.raw_result = None

            self.result = []

            for result in answer['annotations']:
                # result['spot'] chunk
                # result['title'] value
                r = Result(chunk=result['spot'], value=result['title'])
                self.result.append(r)

            self.api_status = None
        else:
            self.dataset = None
            self.question = None
            self.raw_result = None
            self.result = None
            self.api_status = 'API rate limit exceeded'

    def index_by_chunk(self, chunk):
        """
        Returns the index of the chunk

        Returns the index of the chunk of the question passed, from the results list

        Parameters
        ----------
        chunk : str
            Chunk you want the index of

        Returns
        -------
        int
            Index of the chunk, None if not found
        """
        for i, result in enumerate(self.result):
            if str(chunk).strip() == str(result.chunk).strip():
                return int(i)
        return None

    def get_dataset_index(self):
        for i, result in enumerate(self.result):
            if result.is_dataset():
                return int(i)
        return None


class Result:
    def __init__(self, chunk, value):
        self.chunk = chunk
        self.subject = None
        self.property = None
        value = re.sub(' ', '_', value)
        self.value = '<http://dbpedia.org/resource/' + value + '>'

    def is_dataset(self, dataset):
        """Returns True if the result is used as the dataset"""
        return False

    def is_identifier(self):
        """Return True if the result is an Identifier"""
        return False

    def is_type(self, type_name):
        """
        Returns True if the result is of the given type

        # >>> result.is_type('refYear')
        # True

        Parameters
        ----------
        type_name : str
            Type you want to check

        Returns
        -------
        bool
            True if the type matches, False otherwise
        """
        return False

    def get_type(self):
        """
        Returns the type of the result

        # >>> result.get_type()
        # 'refYear'

        Returns
        -------
        str
            Type of the result
        """
        return None
