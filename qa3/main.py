import qa3.printer as qa3
import qa3.qaCube as qaCube


class Main:
    qa3.save_data(file_name='train', source_json='qald-6-train-datacube')
    qa3.save_data(file_name='test', source_json='qald-6-test-datacube')

    # question = 'Which department of whiteacre spent the most in 2010?'
    # query = 'select ?dep { select ?dep sum(xsd:decimal(?amount4)) as ?sum4 sum(xsd:decimal(?amount5)) as ?sum5 from <http://linkedspending.aksw.org/city-of-springfield-budget> { ?obs qb:dataSet ls:city-of-springfield-budget. ?obs lso:city-of-springfield-budget-to ?dep. { ?obs lso:city-of-springfield-budget-amount ?amount4. ?obs lso:refYear ?year4. filter(year(?year4)=2004). } union { ?obs lso:city-of-springfield-budget-amount ?amount5. ?obs lso:refYear ?year5. filter(year(?year5)=2005). } } } group by ?dep having(?sum4>?sum5)'
    # test = qaCube.QA3(question=question, query=query)
    # print(test.question)
    # print(test.query)
