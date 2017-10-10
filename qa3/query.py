import re

import qa3wrapper.wrapper as qa3


def get_qa3query(dc_question, dump_name=None, return_list=False, aggregators=True):
    dc_query = re.sub(' +', ' ', dc_question.query)

    query = split_query(query=dc_query)

    if dump_name is None:
        qa3_answer = qa3.get_answer_from_qa3(dc_question.question)
    else:
        qa3_answer = qa3.get_answer_from_dump(dc_question.id, dump_name)

    query.remove_dataset()
    query.replace_keyword(qa_dataset=qa3_answer.dataset)
    query.expand_prefix()
    query.update_rows(qa3_answer)
    query.remove_xdsdecimal()
    if aggregators:
        query.substitute_aggregators()

    if return_list:
        return query.list_rows()
    else:
        return query.join_query()


def fillin_qa3query(qa3query, dc_question, dump_name=None):
    query = split_query(query=qa3query)

    if dump_name is None:
        qa3_answer = qa3.get_answer_from_qa3(dc_question.question)
    else:
        qa3_answer = qa3.get_answer_from_dump(dc_question.id, dump_name)

    return None


def split_query(query):
    first_split = re.split('{ ', query)
    center_rows = re.split('\. ', first_split[1])

    first_row = first_split[0] + '{ '
    rows = []
    for row in center_rows:
        if row.startswith('}'):
            last_row = row
            return Qa3Query(firts_row=first_row, rows=rows, last_row=last_row)
        else:
            rows.append(row + ' . ')

    query = Qa3Query(firts_row=first_row, rows=rows)

    return query


class Qa3Query:
    def __init__(self, firts_row, rows, last_row='}'):
        self.first_row = firts_row
        self.rows = rows
        self.last_row = last_row

    def join_query(self):
        query = self.first_row
        for row in self.rows:
            if re.search('<dataset>|<measure>|variable', row):
                if not re.search('<http://linkedspending.aksw.org/ontology/refYear>|filter ?\(year'):
                    query = query + row
        query = query + self.last_row

        return query

    def list_rows(self):
        query = [self.first_row]
        for row in self.rows:
            query.append(row)
        query.append(self.last_row)

        return query

        # test = re.search(' [a-z]*\(([a-z]|\(|\)|:|\?)*\)', self.first_row)
        # if test is not None:
        #     self.first_row = self.first_row.replace(test.group(0), ' ('+test.group(0)+' as ?sumans )')

    def update_rows(self, qa3_answer):
        subjetcs = []
        properties = []
        values = []

        variables = []

        numbers = []

        for i, result in enumerate(qa3_answer.result):
            self.substitute_from_qa3(qa3_list=subjetcs, qa3_element=result.subject, replace_to='subject##',
                                     index=i)
            # self.substitute_from_qa3(qa3_list=properties, qa3_element=result.property, replace_to='property##',
            #                          index=i)
            self.substitute_from_qa3(qa3_list=values, qa3_element=result.value, replace_to='value##', index=i)
            year_value = re.split('"', result.value)[1]
            if year_value.isdigit():
                self.substitute_from_qa3(qa3_list=values, qa3_element=year_value, replace_to='value##', index=i)

        self.substitute_variables(qa3_list=variables, replace_to='variable##')

        self.substitute_values(numbers=numbers, pattern=re.compile(' ?< ?[0-9]+'), replace_to='< <num##')
        self.substitute_values(numbers=numbers, pattern=re.compile(' ?> ?[0-9]+'), replace_to='> <num##')
        self.substitute_values(numbers=numbers, pattern=re.compile('limit [0-9]+'), replace_to='limit <num##')

    def add_groupbyvar(self):
        match = re.search('group by', self.last_row)
        if match is not None:
            self.first_row = self.first_row.replace('select', 'select <groupbyvar>')
            self.last_row = self.last_row.replace('group by', '<groupby>')

    def remove_dataset(self):
        self.first_row = re.sub(' from <([a-z]|[0-9]|-|_|\.|/|:)*> ', ' ', self.first_row)
        self.first_row = re.sub(' as \?[a-z]* ', ' ', self.first_row)

    def remove_xdsdecimal(self):
        for match in re.finditer('xsd:decimal\(<[a-z]*##[0-9]*>\)', self.first_row):
            frow_match = match.group(0)
            frow_match = re.sub('xsd:decimal\(', '', frow_match)
            frow_match = re.sub('\)', '', frow_match)
            self.first_row = re.sub(re.escape(match.group(0)), frow_match, self.first_row)
        for i, row in enumerate(self.rows):
            for match in re.finditer('xsd:decimal\(<[a-z]*##[0-9]*>\)', self.rows[i]):
                row_match = match.group(0)
                row_match = re.sub('xsd:decimal\(', '', row_match)
                row_match = re.sub('\)', '', row_match)
                self.rows[i] = re.sub(re.escape(match.group(0)), row_match, self.rows[i])
        for match in re.finditer('xsd:decimal\(<[a-z]*##[0-9]*>\)', self.last_row):
            lrow_match = match.group(0)
            lrow_match = re.sub('xsd:decimal\(', '', lrow_match)
            lrow_match = re.sub('\)', '', lrow_match)
            self.last_row = re.sub(re.escape(match.group(0)), lrow_match, self.last_row)

    def expand_prefix(self):
        prefixes = [{
            'pattern': 'lso:(\S)*',
            'prefix': 'lso:',
            'url': 'http://linkedspending.aksw.org/ontology/'
        }, {
            'pattern': 'ls:(\S)*',
            'prefix': 'ls:',
            'url': 'http://linkedspending.aksw.org/instance/'
        }]

        # , {
        #     'pattern': 'xsd:(\S)*',
        #     'prefix': 'xsd:',
        #     'url': 'http://www.w3.org/2001/XMLSchema#'
        # }

        for prefix in prefixes:
            fmatch = re.search(re.compile(prefix['pattern']), self.first_row)
            # if fmatch is not None:
            #     expanded_row = re.sub(prefix['prefix'], prefix['url'], fmatch.group(0))
            #     self.first_row = re.sub(re.compile(prefix['pattern']), '<'+expanded_row+'>', self.first_row)
            #
            # lmatch = re.search(re.compile(prefix['pattern']), self.last_row)
            # if lmatch is not None:
            #     expanded_row = re.sub(prefix['prefix'], prefix['url'], lmatch.group(0))
            #     self.last_row = re.sub(re.compile(prefix['pattern']), '<' + expanded_row + '>', self.last_row)

            for i, row in enumerate(self.rows):
                match = re.search(re.compile(prefix['pattern']), self.rows[i])
                if match is not None:
                    expanded_row = re.sub(prefix['prefix'], prefix['url'], match.group(0))
                    self.rows[i] = re.sub(re.compile(prefix['pattern']), '<'+expanded_row+'>', self.rows[i])

    def replace_keyword(self, qa_dataset):
        for i, row in enumerate(self.rows):
            if re.search(qa_dataset+' ?\.', row):
                self.rows[i] = '?obs qb:dataSet <dataset> . '

            elif re.search(qa_dataset + '-amount', row):
                amount_variable = re.split(' ', row)[2]
                self.replace_variable(amount_variable, '?measure')
                self.rows[i] = '?obs <measure> ?measure . '

    def replace_variable(self, pattern, variable):
        self.first_row = re.sub(re.escape(pattern), variable, self.first_row)
        for i, row in enumerate(self.rows):
            self.rows[i] = re.sub(re.escape(pattern), variable, self.rows[i])
        self.last_row = re.sub(re.escape(pattern), variable, self.last_row)

    def substitute_from_qa3(self, qa3_list, qa3_element, replace_to, index):
        for i, row in enumerate(self.rows):
            if re.search(qa3_element, self.rows[i]) is not None:
                row_match = re.search(qa3_element, self.rows[i]).group(0)
                if row_match not in qa3_list:
                    qa3_list.append(row_match)
                self.rows[i] = re.sub(row_match, '<' + replace_to + str(index + 1) + '>', self.rows[i])

    def substitute_variables(self, qa3_list, replace_to):
        keywords = ['?obs']
        pattern = re.compile('\?[a-z0-9]*')

        for match in re.finditer(pattern, self.first_row):
            variable = match.group(0)
            if variable not in qa3_list:
                qa3_list.append(variable)
            self.first_row = re.sub(re.escape(variable), '<' + replace_to + str(qa3_list.index(variable) + 1) + '>',
                                    self.first_row)

        for match in re.finditer(pattern, self.last_row):
            variable = match.group(0)
            if variable not in qa3_list:
                qa3_list.append(variable)
            self.last_row = re.sub(re.escape(variable), '<' + replace_to + str(qa3_list.index(variable) + 1) + '>',
                                   self.last_row)

        for i, row in enumerate(self.rows):
            for match in re.finditer(pattern, row):
                variable = match.group(0)
                if variable not in keywords:
                    if variable not in qa3_list:
                        qa3_list.append(variable)
                    self.rows[i] = re.sub(re.escape(variable), '<' + replace_to + str(qa3_list.index(variable) + 1) + '>',
                                          self.rows[i])

    def substitute_aggregators(self):
        aggregators = ['sum', 'avg', 'max', 'min']
        for aggregator in aggregators:
            self.first_row = re.sub(aggregator, '<aggr>', self.first_row)
            self.last_row = re.sub(aggregator, '<aggr>', self.last_row)

    def substitute_values(self, numbers, replace_to, pattern):
        for match in re.finditer(pattern, self.first_row):
            frow_match = match.group(0)
            if frow_match not in numbers:
                numbers.append(frow_match)
            self.first_row = re.sub(frow_match, replace_to+str(numbers.index(frow_match)+1)+'>', self.first_row)

        for match in re.finditer(pattern, self.last_row):
            lrow_match = match.group(0)
            if lrow_match not in numbers:
                numbers.append(lrow_match)
            self.last_row = re.sub(lrow_match, replace_to+str(numbers.index(lrow_match)+1)+'>', self.last_row)

    def fillin_keywords(self, dataset):
        for i, row in enumerate(self.rows):
            if re.search('<dataset>', self.rows[i]):
                self.rows[i] = re.sub('<dataset>', '<http://linkedspending.aksw.org/instance/'+dataset+'>',
                                      self.rows[i])
            if re.search('<measure>', self.rows[i]):
                self.rows[i] = re.sub('<measure>', '<http://linkedspending.aksw.org/instance/'+dataset+'-amount>',
                                      self.rows[i])

    def fillin_variables(self):
        variables = []
        pattern = re.compile('<variable##[0-9]*')

        for match in re.finditer(pattern, self.first_row):
            variable = match.group(0)
            if variable not in variables:
                variables.append(variable)
            self.first_row = re.sub(re.escape(variable), '?variable' + str(variables.index(variable) + 1),
                                    self.first_row)

        for match in re.finditer(pattern, self.last_row):
            variable = match.group(0)
            if variable not in variables:
                variables.append(variable)
            self.last_row = re.sub(re.escape(variable), '?variable' + str(variables.index(variable) + 1), self.last_row)

        for i, row in enumerate(self.rows):
            for match in re.finditer(pattern, row):
                variable = match.group(0)
                if variable not in variables:
                    variables.append(variable)
                self.rows[i] = re.sub(re.escape(variable), '?variable' + str(variables.index(variable) + 1),
                                      self.rows[i])

    def fillin_costraints(self, qa3_answer):
        for result in qa3_answer:
            if not result.isdataset():
                if result.isyear():
                    self.rows.append('?obs <http://linkedspending.aksw.org/ontology/refYear> ' + result.value + ' .')
                    # self.rows.append(' ?obs <http://linkedspending.aksw.org/ontology/refYear> <?year> .')
                    # self.rows.append(' filter (year(<?year>)=<' + result. + '>) .')
                if result.isidentifier():
                    None


class Question:
    def __init__(self, question, query):
        self.question = question
        self.query = query
