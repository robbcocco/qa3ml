import qa3.printer as printer
import qa3.qaCube as qaCube


class Main:
    printer.save_data(file_name='train', source_json='qald-6-train-datacube')
    printer.save_data(file_name='test', source_json='qald-6-test-datacube')

    # question = 'Which departments of the city of Springfield had a higher budget in 2004 then in 2005?'
    # query = 'select ?dep { select ?dep sum(xsd:decimal(?amount4)) as ?sum4 sum(xsd:decimal(?amount5)) as ?sum5 from <http://linkedspending.aksw.org/city-of-springfield-budget> { ?obs qb:dataSet ls:city-of-springfield-budget. ?obs lso:city-of-springfield-budget-to ?dep. { ?obs lso:city-of-springfield-budget-amount ?amount4. ?obs lso:refYear ?year4. filter(year(?year4)=2004). } union { ?obs lso:city-of-springfield-budget-amount ?amount5. ?obs lso:refYear ?year5. filter(year(?year5)=2005). } } } group by ?dep having(?sum4>?sum5)'
    # print(question)
    # print(query)
    # qa3 = qaCube.QA3(question=question, query=query)
    # qa3.get_qa3()
    # print(qa3.question)
    # print(qa3.query)
    # test = qa3.fillin_query(question=question)
    # print(test)
    # print(qa3.question)
    # print(qa3.query)
