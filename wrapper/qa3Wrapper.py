import re
import json
import os

import wrapper.interface as interface


def get_answer_from_web(question):
    """
    Returns the answer from qa3.link's step1

    Parameters
    ----------
    question : str
        Question to ask to qa3

    Returns
    -------
    Answer
        Result from http://swipe.unica.it/apps/qa3/?q=question
    """
    raw_answer = interface.get_json(question=question)
    if raw_answer is not None:
        answer = Answer(answer=raw_answer)
    else:
        answer = Answer()

    return answer


def get_answer_from_dump(answer_id, file_name):
    """
    Returns the answer from a previously dumped result

    Parameters
    ----------
    answer_id : str
        Id of the question
    file_name : str
        Name of the file, without the extension

    Returns
    -------
    Answer
        Dumped result from http://swipe.unica.it/apps/qa3/?q=question
    """
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
    def __init__(self, row):
        result = re.split('\t', row)
        self.chunk = result[0]
        self.subject = result[1]
        self.property = result[2]
        self.value = result[3]
        # self.value = re.split('"', result[3])[1]

    def is_dataset(self, dataset):
        """Returns True if the result is used as the dataset"""
        return re.split('"', self.value)[1] == dataset or re.match('<http://linkedspending.aksw.org/instance/' + dataset
                                                                   + '>', self.subject)

    def is_identifier(self):
        """Return True if the result is an Identifier"""
        return self.property == '<http://purl.org/dc/terms/identifier>'

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
        return self.property == '<http://linkedspending.aksw.org/ontology/'+type_name+'>'

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
        type_name = self.property.rsplit('/')[-1]
        type_name = re.sub('>', '', type_name)
        return type_name.strip()
