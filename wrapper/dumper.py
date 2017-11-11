import json
import os
import time

import wrapper.interface as qa3
import datacube.dataset as dc


def save_data(data, file_name):
    directory = os.path.dirname(__file__)
    data_path = os.path.join(directory, 'dumps/'+file_name+'.json')
    with open(data_path, 'w') as data_file:
        json.dump(data, data_file, indent=4)


def qa3questioner(file_name, site=qa3.QA3):
    dc_dataset = dc.Dataset(file_name)
    dataset = {}

    for i, question in enumerate(dc_dataset.questions):
        # if i is not 0 and i % 10 is 0:
        #     time.sleep(300)
        # else:
        #     time.sleep(10)

        # if 40 < (i+2) or i > 130:
        qa3_answer = qa3.get_json(question.question, site)

        if qa3_answer is None:
            break

        print(question.id)

        dataset[question.id] = qa3_answer

    return dataset


class Dump:
    dataset_name = 'qald-7-train-multilingual'
    site = qa3.TAGME
    dataset = qa3questioner(dataset_name, site)
    save_data(dataset, dataset_name)
