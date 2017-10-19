import re
import string


class Qa3Query(str):
    def substitute_from_qa3(self, result, index):
        """
        Returns the query with the result from qa3.link step1
        
        Replace the results' type with a tag
    
        Parameters
        ----------
        result : Result
            Result from qa3.link
        index: int
            Index of the result from the results list
    
        Returns
        -------
        Qa3Query
            The updated query
        """
        query = self
        # Types to leave as they are
        known_types = ['refYear', 'refDate']
        query = query.replace_qa3_result(qa3_element=result.subject, replace_to='SUB', index=index)
        query = query.replace_qa3_result(qa3_element=result.value, replace_to='VAL', index=index)
        if result.get_type() not in known_types:
            query = query.replace_qa3_result(qa3_element=result.property, replace_to='PROP', index=index)
        if result.is_type('refYear'):
            year_value = re.split('"', result.value)[1]
            query = query.replace_qa3_result(qa3_element=str(year_value), replace_to='YEAR', index=index)
        return Qa3Query(query)

    def replace_qa3_result(self, qa3_element, replace_to, index):
        query = self
        for match in re.finditer(qa3_element.strip(), query):
            variable = match.group(0)
            query = re.sub(variable, '<' + replace_to + str(index) + '>', query)
        return Qa3Query(query)

    def clean_frow(self):
        """
        Returns the query without "from <dataset>" and "as ?variable"
        
        Remove all "from <dataset>" recurrences and "as ?variable" from the first select
    
        Returns
        -------
        Qa3Query
            The updated query
        """
        query = self

        query = re.sub(' from <[^ >]+> ', ' ', query)
        temp = re.split('{', query)[0]
        temp2 = re.sub(' as \?[a-zA-Z0-9_]+ ', ' ', temp)
        query = re.sub(re.escape(temp), temp2, query)
        return Qa3Query(query)

    def remove_xsddecimal(self):
        """
        Returns the query without "xsd:decimal()"
        
        Replace all "xsd:decimal(?variable)" recurrences with ?variable
    
        Returns
        -------
        Qa3Query
            The updated query
        """
        query = self
        pattern = re.compile(r'xsd:decimal\((?P<content>[?a-zA-Z0-9<>]+)\)')
        for match in re.finditer(pattern, query):
            query = re.sub(re.escape(match.group(0)), match.group('content'), query)
        return Qa3Query(query)

    def expand_prefix(self):
        """
        Returns the query without the prefixes
        
        Replace all the prefixes with the corresponding url
    
        Returns
        -------
        Qa3Query
            The updated query
        """
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

    def replace_dataset(self, qa3_dataset):
        """
        Returns the query with the dataset tagged
        
        Replace the dataset's url with the tag <DATASET>
    
        Parameters
        ----------
        qa3_dataset : str
            The dataset found by qa3
    
        Returns
        -------
        Qa3Query
            The updated query
        """
        query = self
        pattern = re.compile('<http://linkedspending.aksw.org/instance/' + qa3_dataset + '>')
        query = re.sub(pattern, '<DATASET>', query)
        return Qa3Query(query)

    def replace_measure(self, qa3_dataset):
        """
        Returns the query with the measure tagged
        
        Replace the measure's url with the tag <MEASURE>
    
        Parameters
        ----------
        qa3_dataset : str
            The dataset found by qa3
    
        Returns
        -------
        Qa3Query
            The updated query
        """
        query = self
        pattern = re.compile('<http://linkedspending.aksw.org/ontology/' + qa3_dataset + '-amount>')
        query = re.sub(pattern, '<MEASURE>', query)
        return Qa3Query(query)

    def substitute_variables(self):
        """
        Returns the query with the variables standardized
        
        Replace all the variables with a standardized format ?varN
    
        Returns
        -------
        Qa3Query
            The updated query
        """
        query = self
        qa3_list = []
        keywords = ['?obs']
        pattern = re.compile('\?[a-zA-Z0-9_]+')
        for match in re.finditer(pattern, query):
            variable = match.group(0)
            if variable not in keywords:
                if variable not in qa3_list:
                    qa3_list.append(variable)
                query = re.sub(re.escape(variable), '?var' + string.ascii_uppercase[qa3_list.index(variable)],
                               query)
        return Qa3Query(query)

    def substitute_values(self, values, replace_to):
        """
        Returns the query with the values from the question tagged
        
        Replace the values found in the question with a tag
    
        Parameters
        ----------
        values : List(str)
            The list containing the values found in the question
        replace_to
            The tag that will replace the values
    
        Returns
        -------
        Qa3Query
            The updated query
        """
        query = self
        for val in values:
            for match in re.finditer(val, query):
                query = re.sub(match.group(0), ' <'+replace_to+string.ascii_uppercase[values.index(val)]+'> ', query)
        return Qa3Query(query)

    def generalize_properties(self):
        """
        Returns the query with the properties anonimized
        
        Replace unessential properties with the anonimous variable []
    
        Returns
        -------
        Qa3Query
            The updated query
        """
        query = self
        pattern = re.compile('<http[^ ]+ (?P<subject>(<SUB[0-9]+>))')
        for match in re.finditer(pattern, query):
            query = re.sub(match.group(0), '[] '+match.group('subject'), query)
        return Qa3Query(query)

    def reorder_query(self):
        """
        Returns the query with the elements reordered alphabetically
        
        Reorder the content of the query
    
        Returns
        -------
        Qa3Query
            The updated query
        """
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
