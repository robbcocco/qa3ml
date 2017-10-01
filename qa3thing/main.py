import json
import os
import re

import qa3wrapper.wrapper as qa3
import datacube.dataset as dc
import datacube.query as qa3query


def save_data_to_json(data):
    directory = os.path.dirname(__file__)
    data_path = os.path.join(directory, 'datasets/train.json')
    with open(data_path, 'w') as data_file:
        json.dump(data, data_file, indent=4)


def save_data_to_text(data):
    directory = os.path.dirname(__file__)
    data_path = os.path.join(directory, 'datasets/train.txt')
    with open(data_path, 'w') as data_file:
        data_file.write(data)


def answer2json(question, qa3_answer, query):
    answers = []
    # for dc_answer in question.answers:
    #     answer = {
    #         'var': dc_answer.var,
    #         'type': dc_answer.type,
    #         'value': dc_answer.value
    #     }
    #     answers.append(answer)

    results = []
    for qa3_result in qa3_answer.result:
        result = {
            'subject': qa3_result.subject,
            'property': qa3_result.property,
            'value': qa3_result.value
        }
        results.append(result)

    temp = {
        'id': question.id,
        'question': question.question,
        'aggregation': question.aggregation,
        'answers': answers,
        'query': question.query,
        'qa3_query': query,
        'qa3_dataset': qa3_answer.dataset,
        'qa3_result': results
    }

    return temp


def qa3questioner():
    dc_dataset = dc.Dataset()
    dataset = {}
    answers = []

    # print(dc_dataset.questions[1].question)
    for question in dc_dataset.questions:
        qa3_answer = qa3.get_answer_from_dump(question.id)

        if qa3_answer is None:
            # print(qa3_answer.api_status)
            break

        query = qa3query.get_qa3query(question)

        answer = answer2json(question=question, qa3_answer=qa3_answer, query=query)

        print(answer['id'])
        answers.append(answer)

    dataset['answers'] = answers

    return dataset


def qa3questioner_text():
    dc_dataset = dc.Dataset()
    text = ''

    for question in dc_dataset.questions:
        qa3_answer = qa3.get_answer_from_dump(question.id)

        if qa3_answer is None:
            # print(qa3_answer.api_status)
            break

        query = qa3query.get_qa3query(question)

        temp_question = re.sub('\n', '', question.question).strip()
        temp_query = re.sub('\n', '', query).strip()

        text = text + temp_question + '\t' + temp_query + '\n'

    return text


class Dump:
    dataset = qa3questioner()
    save_data_to_json(dataset)
    text = qa3questioner_text()
    save_data_to_text(text)
