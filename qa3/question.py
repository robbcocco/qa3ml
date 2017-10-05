import re

import qa3wrapper.wrapper as qa3


def get_qa3question(dc_question, dump_name=None):
    question = dc_question.question

    if dump_name is None:
        qa3_answer = qa3.get_answer_from_qa3(dc_question.question)
    else:
        qa3_answer = qa3.get_answer_from_dump(dc_question.id, dump_name)

    for i, result in enumerate(qa3_answer.result):
        if re.search(result.chunk, question):
            if result.isyear():
                question = re.sub(result.chunk, '<YEAR>', question)
            elif result.isidentifier():
                question = re.sub(result.chunk, '<ID>', question)
            else:
                question = re.sub(result.chunk, '<X>', question)

    # magnitude = {
    #     'thousand': 000,
    #     'million': 000000,
    #     'billion': 000000000,
    #     'trillion': 000000000000,
    #     'quadrillion': 000000000000000,
    #     'quintillion': 000000000000000000,
    #     'sextillion': 000000000000000000000,
    #     'septillion': 000000000000000000000000,
    #     'octillion': 000000000000000000000000000,
    #     'nonillion': 000000000000000000000000000000,
    #     'decillion': 000000000000000000000000000000000,
    # }
    #
    # for word in magnitude:
    #     re.sub('[0-9]*'+word, question)

    for match in re.finditer('[0-9]+', question):
        num = '' + match.group(0)
        if 1899 < int(num) < 2099:
            question = re.sub(re.escape(num), '<YEAR>', question, 1)
        else:
            question = re.sub(re.escape(num), '<N>', question, 1)

    return question
