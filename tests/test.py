import qa3wrapper.wrapper as qa3
import datacube.dataset as dc
import datacube.query as qa3query


class Qa3Test:
    question = 'Which programs were done under the class of public works and utilities in the expenditure of the Town of Cary?'
    q_id = '1'
    # test = qa3.get_answer_from_qa3(question=question)
    test = qa3.get_answer_from_dump(q_id)
    print(question)
    print(test.question)
    print(test.dataset)
    for result in test.result:
        print(result.subject)
        print(result.value)


class DatacubeTest:
    dataset = dc.Dataset()
    test_question = dataset.questions[1]
    print(test_question.question)
    print(test_question.query)
    print(test_question.aggregation)
    print(test_question.vars)
    for answer in test_question.answers:
        print(answer.type)
        print(answer.value)


class QueryTest:
    dataset = dc.Dataset()
    question = dataset.questions[4]
    query = qa3query.get_qa3query(question)
    rows = qa3query.get_qa3rows(question)
    print(query)
    print(rows)
