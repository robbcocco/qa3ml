import re
import string


class Qa3Query(str):
    def update_rows(self, qa3_answer):
        query = self
        known_types = ['refYear', 'refDate']
        subjetcs = []
        properties = []
        values = []

        for i, result in enumerate(qa3_answer.result):
            if result.get_type() not in known_types:
                query = query.substitute_from_qa3(qa3_list=properties, qa3_element=result.property, replace_to='PROP',
                                                  index=i)
            query = query.substitute_from_qa3(qa3_list=subjetcs, qa3_element=result.subject, replace_to='SUB',
                                              index=i)
            query = query.substitute_from_qa3(qa3_list=values, qa3_element=result.value, replace_to='VAL',
                                              index=i)
            if result.is_type('refYear'):
                year_value = re.split('"', result.value)[1]
                query = query.substitute_from_qa3(qa3_list=values, qa3_element=str(year_value), replace_to='YEAR',
                                                  index=i)
        return Qa3Query(query)

    def substitute_from_qa3(self, qa3_list, qa3_element, replace_to, index):
        query = self
        for match in re.finditer(qa3_element.strip(), query):
            variable = match.group(0)
            if variable not in qa3_list:
                qa3_list.append(variable)
            query = re.sub(variable, '<' + replace_to + str(index) + '>', query)
        return Qa3Query(query)

    def clean_frow(self):
        query = self
        query = re.sub(' from <[^ >]+> ', ' ', query)
        temp = re.split('{', query)[0]
        temp2 = re.sub(' as \?[a-zA-Z0-9_]+ ', ' ', temp)
        query = re.sub(re.escape(temp), temp2, query)
        return Qa3Query(query)

    def remove_xdsdecimal(self):
        query = self
        pattern = re.compile(r'xsd:decimal\((?P<content>[?a-zA-Z0-9<>]+)\)')
        for match in re.finditer(pattern, query):
            query = re.sub(re.escape(match.group(0)), match.group('content'), query)
        return Qa3Query(query)

    def expand_prefix(self):
        query = self
        prefixes = [{
            'prefix': 'lso:',
            'url': 'http://linkedspending.aksw.org/ontology/'
        }, {
            'prefix': 'ls:',
            'url': 'http://linkedspending.aksw.org/instance/'
        }]
        for prefix in prefixes:
            pattern = re.compile(prefix['prefix']+r'(?P<content>[^ .]+)')
            for match in re.finditer(pattern, query):
                query = re.sub(re.escape(match.group(0)), '<'+match.group(0)+'>', query)
                query = re.sub(re.escape(match.group(0)), prefix['url']+match.group('content'), query)
        return Qa3Query(query)

    def replace_dataset(self, qa_dataset):
        query = self
        pattern = re.compile('<http://linkedspending.aksw.org/instance/'+qa_dataset+'>')
        query = re.sub(pattern, '<DATASET>', query)
        return Qa3Query(query)

    def replace_measure(self, qa_dataset):
        query = self
        pattern = re.compile('<http://linkedspending.aksw.org/ontology/'+qa_dataset+'-amount>')
        query = re.sub(pattern, '<MEASURE>', query)
        return Qa3Query(query)

    def substitute_variables(self, replace_to):
        query = self
        qa3_list = []
        keywords = ['?obs']
        pattern = re.compile('\?[a-zA-Z0-9_]+')
        for match in re.finditer(pattern, query):
            variable = match.group(0)
            if variable not in keywords:
                if variable not in qa3_list:
                    qa3_list.append(variable)
                query = re.sub(re.escape(variable), '?' + replace_to + string.ascii_uppercase[qa3_list.index(variable)],
                               query)
        return Qa3Query(query)

    def substitute_values(self, values, replace_to):
        query = self
        for val in values:
            for match in re.finditer(val, query):
                query = re.sub(match.group(0), ' <'+replace_to+string.ascii_uppercase[values.index(val)]+'> ', query)
        return Qa3Query(query)

    def generalize_properties(self):
        query = self
        pattern = re.compile('<http[^ ]+ (?P<subject>(<SUB[0-9]+>))')
        for match in re.finditer(pattern, query):
            query = re.sub(match.group(0), '[] '+match.group('subject'), query)
        return Qa3Query(query)

    def reorder_query(self):
        query = self
        pattern = re.compile('(?P<brace>[{}])[^{}]+')
        for match in re.finditer(pattern, query):
            rows = re.sub(re.escape(match.group('brace')), '', match.group(0))
            rows = re.split('\. ', rows)
            if len(rows) > 1:
                temp2 = []
                for row in rows:
                    if row is not '' and row is not ' ':
                        temp2.append(row.strip())
                temp2 = sorted(temp2)
                temp = ' '
                for row in temp2:
                    temp = temp + row + ' . '
                query = re.sub(re.escape(match.group(0)), match.group('brace')+temp, query)
        return Qa3Query(query)
