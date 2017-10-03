import qa3.query as qa3query

# class Qa3Test:
#     question = 'Which programs were done under the class of public works and utilities in the expenditure of the Town of Cary?'
#     q_id = '1'
#     # test = qa3.get_answer_from_qa3(question=question)
#     test = qa3.get_answer_from_dump(q_id)
#     print(question)
#     print(test.question)
#     print(test.dataset)
#     for result in test.result:
#         print(result.subject)
#         print(result.value)


# class DatacubeTest:
#     dataset = dc.Dataset()
#     test_question = dataset.questions[1]
#     print(test_question.question)
#     print(test_question.query)
#     print(test_question.aggregation)
#     print(test_question.vars)
#     for answer in test_question.answers:
#         print(answer.type)
#         print(answer.value)


class QueryTest:
    qa3_question = 'Over which programmes more than 1000000 pound but less than 10000000 pound in grants were given by the Big Lottery Fund?'
    qa3_query = 'select ?programme from <http://linkedspending.aksw.org/big-lottery-fund-grants> { ?obs qb:dataSet ls:big-lottery-fund-grants. ?obs lso:big-lottery-fund-grants-programme-name ?programme. ?obs lso:big-lottery-fund-grants-amount ?amount. } group by ?programme having (sum(xsd:decimal(?amount))>1000000&&sum(xsd:decimal(?amount))<10000000)'

    question = qa3query.Question(question=qa3_question, query=qa3_query)
    query = qa3query.get_qa3query(question)
    rows = qa3query.get_qa3rows(question)
    print(query)
    print(rows)
