import re

import qa3wrapper.wrapper as qa3


def get_qa3query(dc_question):
    query = split_query(dc_query=dc_question.query)

    query.qacubize(dc_question)

    return query.join_query()


def get_qa3rows(dc_question):
    query = split_query(dc_query=dc_question.query)

    query.qacubize(dc_question)

    return query.list_rows()


def split_query(dc_query):
    first_split = re.split('{ ', dc_query)
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

    def dataset_found(self, qa3_answer):
        return re.search('<.*'+qa3_answer.dataset+'>', self.first_row)

    def join_query(self):
        query = self.first_row
        for row in self.rows:
            query = query + row
        query = query + self.last_row

        return query

    def list_rows(self):
        query = [self.first_row]
        for row in self.rows:
            query.append(row)
        query.append(self.last_row)

        return query

    def qacubize(self, question):
        qa3_answer = qa3.get_answer_from_dump(question.id)

        # if self.dataset_found(qa3_answer=qa3_answer):
        self.remove_dataset()

        self.replace_amount()

        self.update_rows(qa3_answer)

        #         self.first_row = re.sub(' as \?[a-z]* ', ' ', self.first_row)
        #
        #         test = re.search(' [a-z]*\(([a-z]|\(|\)|:|\?)*\)', self.first_row)
        #         if test is not None:
        #             self.first_row = self.first_row.replace(test.group(0), ' ('+test.group(0)+' as ?sumans )')

    def update_rows(self, qa3_answer):
        subjetcs = []
        properties = []
        values = []

        for i, row in enumerate(self.rows):
            if re.search('qb:dataSet', row):
                self.rows[i] = '?obs qb:dataSet <dataset>. '

            elif re.search('\?amount', row):
                self.rows[i] = '?obs <measure> ?measure. '

            else:
                self.expand_prefix(i)

                for u, result in enumerate(qa3_answer.result):
                    self.substitute_from_qa3(qa3_list=subjetcs, qa3_element=result.subject, replace_to='?subject##',
                                             i=i, u=u)
                    self.substitute_from_qa3(qa3_list=properties, qa3_element=result.property, replace_to='?property##',
                                             i=i, u=u)
                    self.substitute_from_qa3(qa3_list=values, qa3_element=result.value, replace_to='?value##', i=i, u=u)
                    year_value = re.split('"', result.value)[1]
                    if year_value.isdigit():
                        self.substitute_from_qa3(qa3_list=values, qa3_element=year_value, replace_to='?value##', i=i,
                                                 u=u)

    def add_groupbyvar(self):
        match = re.search('group by', self.last_row)
        if match is not None:
            self.first_row = self.first_row.replace('select', 'select <groupbyvar>')
            self.last_row = self.last_row.replace('group by', '<groupby>')

    def remove_dataset(self):
        self.first_row = re.sub(' from <.*> ', ' ', self.first_row)

    def replace_amount(self):
        self.first_row = re.sub('\?amount', '?measure', self.first_row)

    def expand_prefix(self, i):
        match = re.search('lso:(\S)*', self.rows[i])
        if match is not None:
            temp = match.group(0)
            expanded_row = re.sub('lso:', 'http://linkedspending.aksw.org/ontology/', temp)
            self.rows[i] = re.sub('lso:(\S)*', '<'+expanded_row+'>', self.rows[i])
        match = re.search('ls:(\S)*', self.rows[i])
        if match is not None:
            temp = match.group(0)
            expanded_row = re.sub('ls:', 'http://linkedspending.aksw.org/instance/', temp)
            self.rows[i] = re.sub('ls:(\S)*', '<'+expanded_row+'>', self.rows[i])

    def substitute_from_qa3(self, qa3_list, qa3_element, replace_to, i, u):
        if re.search(qa3_element, self.rows[i]) is not None:
            if qa3_element not in qa3_list:
                qa3_list.append(qa3_element)
            self.rows[i] = re.sub(qa3_element, '<'+replace_to+str(u+1)+'>', self.rows[i])
