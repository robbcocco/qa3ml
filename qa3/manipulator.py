import json
import os
import re

import datacube.dataset as dc
import qa3.query as qa3query
import qa3.question as qa3question
import qa3wrapper.wrapper as qa3


def save_data_to_json(data, file_name):
    directory = os.path.dirname(__file__)
    data_path = os.path.join(directory, 'datasets/'+file_name+'.json')
    with open(data_path, 'w') as data_file:
        json.dump(data, data_file, indent=4)


def save_data_to_text(data, file_name):
    directory = os.path.dirname(__file__)
    data_path = os.path.join(directory, 'datasets/'+file_name+'.txt')
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


def qa3questioner(file_name):
    dc_dataset = dc.Dataset(file_name)
    dataset = {}
    answers = []

    # print(dc_dataset.questions[1].question)
    for question in dc_dataset.questions:
        qa3_answer = qa3.get_answer_from_dump(question.id, file_name)

        if qa3_answer is None:
            # print(qa3_answer.api_status)
            break

        query = qa3query.get_qa3query(question, file_name)

        answer = answer2json(question=question, qa3_answer=qa3_answer, query=query)

        print(answer['id'])
        answers.append(answer)

    dataset['answers'] = answers

    return dataset


def qa3questioner_text(file_name):
    dc_dataset = dc.Dataset(file_name=file_name)
    text = ''

    for question in dc_dataset.questions:
        qa3_answer = qa3.get_answer_from_dump(question.id, file_name)

        if qa3_answer is None:
            # print(qa3_answer.api_status)
            break

        query = qa3query.get_qa3query(question, file_name, aggregators=False)
        query_aggr = qa3query.get_qa3query(question, file_name)
        qa3_question = qa3question.get_qa3question(question, file_name)

        temp_dcquestion = clean_string(question.question)
        temp_question = clean_string(qa3_question)
        temp_dcquery = clean_string(question.query)
        temp_query = clean_string(query)
        temp_query_aggr = clean_string(query_aggr)
        temp_dcdataset = clean_string(question.dataset)
        temp_dataset = clean_string(qa3_answer.dataset)

        text = text + file_name + '\t' + question.id + '\t' + temp_dcdataset + '\t' + temp_dataset \
               + '\t' + temp_dcquestion + '\t' + temp_question + '\t' + temp_dcquery + '\t' + temp_query \
               + '\t' + temp_query_aggr + '\n'

    return text


def clean_string(string):
    string = re.sub('\n', '', string).strip()
    string = re.sub(' +', ' ', string)

    return string


def save_data(file_name, source_json, use_cache=False):
    dataset = qa3questioner(source_json)
    text = qa3questioner_text(source_json)
    save_data_to_json(dataset, file_name)
    save_data_to_text(text, file_name)
