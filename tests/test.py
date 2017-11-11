import qa3.query as qa3query
import qa3.qaCube as qaCube

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


class Qa31:
    question = 'Which departments of the city of Springfield had a higher budget in 2004 then in 2005?'
    query = 'select ?dep { select ?dep sum(xsd:decimal(?amount4)) as ?sum4 sum(xsd:decimal(?amount5)) as ?sum5 from <http://linkedspending.aksw.org/city-of-springfield-budget> { ?obs qb:dataSet ls:city-of-springfield-budget. ?obs lso:city-of-springfield-budget-to ?dep. { ?obs lso:city-of-springfield-budget-amount ?amount4. ?obs lso:refYear ?year4. filter(year(?year4)=2004). } union { ?obs lso:city-of-springfield-budget-amount ?amount5. ?obs lso:refYear ?year5. filter(year(?year5)=2005). } } } group by ?dep having(?sum4>?sum5)'

    qa3 = qaCube.QACube(question=question, query=query)
    print(qa3.question)
    print(qa3.query)
    qa3.get_qa3()
    print(qa3.question)
    print(qa3.query)
    test = qa3.fillin_query(question=question)
    print(test)
    print(qa3.question)
    print(qa3.query)


class Qa32:
    question = 'What are the top 3 expenditure categories in Cheshire West and Chester council spending?'
    query = 'select distinct(?result) from <http://linkedspending.aksw.org/cheshire_west_and_chester_april_2013> { ?obs qb:dataSet ls:cheshire_west_and_chester_april_2013. ?obs lso:cheshire_west_and_chester_april_2013-expenditure-category ?result. ?obs lso:cheshire_west_and_chester_april_2013-amount ?amount. } order by desc(sum(xsd:decimal(?amount))) limit 3'

    qa3 = qaCube.QACube(question=question, query=query)
    print(qa3.question)
    print(qa3.query)
    qa3.get_qa3(site=qaCube.TAGME)
    print(qa3.question)
    print(qa3.query)
    test = qa3.fillin_query(question=question, site=qaCube.TAGME)
    print(test)
    print(qa3.question)
    print(qa3.query)


class TagMe1:
    question = 'How much did Pulp Fiction cost?'
    query = 'SELECT DISTINCT ?n WHERE {  <http://dbpedia.org/resource/Pulp_Fiction> <http://dbpedia.org/ontology/budget> ?n . } '

    qa3 = qaCube.QACube(question=question, query=query)
    print(qa3.question)
    print(qa3.query)
    qa3.get_qa3(site=qaCube.TAGME)
    print(qa3.question)
    print(qa3.query)
    test = qa3.fillin_query(question=question, site=qaCube.TAGME)
    print(test)
    print(qa3.question)
    print(qa3.query)
