import qa3.printer as qa3
import qa3.qaCube as qaCube


class Main:
    qa3.save_data(file_name='train', source_json='qald-6-train-datacube')
    qa3.save_data(file_name='test', source_json='qald-6-test-datacube')

    # question = 'Which department of whiteacre spent the most in 2010?'
    # query = 'select ?dep from <http://linkedspending.aksw.org/city-of-whiteacre-spending> { ?obs qb:dataSet ls:city-of-whiteacre-spending. ?obs lso:city-of-whiteacre-spending-to ?dep. ?obs lso:city-of-whiteacre-spending-amount ?amount. ?obs lso:refYear ?year. filter (year(?year)=2010). } order by desc(sum(xsd:decimal(?amount))) limit 1'
    # test = qaCube.QA3(question=question, query=query)
    # print(test.question)
    # print(test.query)
