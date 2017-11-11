import json
import os
import re

import datacube.dataset as dc
import qa3.qaCube as qaCube
import wrapper.qa3Wrapper as qa3Wrapper
import wrapper.tagMeWrapper as tagMeWrapper


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
    # for qa3_result in qa3_answer.result:
    #     result = {
    #         'subject': qa3_result.subject,
    #         'property': qa3_result.property,
    #         'value': qa3_result.value
    #     }
    #     results.append(result)

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


def get_answers(file_name, use_cache, site):
    dc_dataset = dc.Dataset(file_name=file_name)
    dataset = {}
    answers = []
    text = ''

    for question in dc_dataset.questions:
        print(question.id)

        if use_cache is True:
            if site is qaCube.QA3:
                qa3_answer = qa3Wrapper.get_answer_from_dump(question.id, file_name)
            elif site is qaCube.TAGME:
                qa3_answer = tagMeWrapper.get_answer_from_dump(question.id, file_name)
        else:
            if site is qaCube.QA3:
                qa3_answer = qa3Wrapper.get_answer_from_web(question.question)
            elif site is qaCube.TAGME:
                qa3_answer = tagMeWrapper.get_answer_from_web(question.question)

            if qa3_answer is None:
                # print(qa3_answer.api_status)
                break

        qa3 = qaCube.QACube(question=question.question, query=question.query)
        qa3.get_qa3(qa3_answer=qa3_answer)

        answer = answer2json(question=question, qa3_answer=qa3_answer, query=qa3.query)
        answers.append(answer)

        temp_dcquestion = clean_string(question.question)
        temp_question = clean_string(qa3.question)
        temp_dcquery = clean_string(question.query)
        temp_query = clean_string(qa3.query)
        temp_dcdataset = clean_string(question.dataset)
        temp_dataset = clean_string(qa3_answer.dataset)
        text = text + file_name + '\t' + question.id + '\t' + temp_dcdataset + '\t' + temp_dataset \
               + '\t' + temp_dcquestion + '\t' + temp_question + '\t' + temp_dcquery + '\t' + temp_query + '\n'

    dataset['answers'] = answers
    return dataset, text


def clean_string(c_string):
    c_string = re.sub('[\n\t]', ' ', c_string).strip()
    c_string = re.sub(' +', ' ', c_string)
    return c_string


def save_data(file_name, source_json, use_cache=False, site=qaCube.QA3):
    dataset, text = get_answers(source_json, use_cache, site)
    save_data_to_json(dataset, file_name)
    save_data_to_text(text, file_name)
