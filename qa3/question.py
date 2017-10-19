import re
import string


class Qa3Question(str):
    def expand_numbers(self):
        """
        Returns the question with all the numbers in digits
        
        Replace numbers wrote in letters with the digit counterpart
    
        Returns
        -------
        Qa3Question
            The updated question
        """
        question = self
        magnitudes = [
                ['thousand', '000'],
                ['million', '000000'],
                ['billion', '000000000'],
                ['trillion', '000000000000'],
                ['quadrillion', '000000000000000'],
                ['quintillion', '000000000000000000'],
                ['sextillion', '000000000000000000000'],
                ['septillion', '000000000000000000000000'],
                ['octillion', '000000000000000000000000000'],
                ['nonillion', '000000000000000000000000000000'],
                ['decillion', '000000000000000000000000000000000']
        ]
        for magnitude, zeroes in magnitudes:
            pattern = re.compile('[0-9]+ ?'+magnitude)
            for match in re.finditer(pattern, question):
                match = match.group(0)
                num = re.search('[0-9]+', match).group(0)
                question = re.sub(re.escape(match), num+zeroes, question)
        return Qa3Question(question)

    def substitute_date(self, ref_dates, qa3_answer):
        """
        Returns the question with the dates tagged
        
        Replace dates found in the question with the tag <DATE>
    
        Parameters
        ----------
        ref_dates : List(str)
            The list containing the dates
        qa3_answer
            The results received from qa3
    
        Returns
        -------
        Qa3Question
            The updated question
        """
        question = self
        for match in re.finditer('[0-9]{4}-[0-9]{2}-[0-9]{2}', question):
            date = match.group(0)
            i = qa3_answer.index_by_chunk(date)
            if i is None or qa3_answer.result[i].get_type() != 'refYear':
                if date not in ref_dates:
                    ref_dates.append(date)
                question = re.sub(date, '<NUM' + string.ascii_uppercase[ref_dates.index(date)] + '>', question, 1)
        return Qa3Question(question)

    def substitute_year(self, ref_years, qa3_answer):
        """
        Returns the question with the years tagged
        
        Replace years found in the question with the tag <YEAR>
    
        Parameters
        ----------
        ref_years : List(str)
            The list containing the years
        qa3_answer
            The results received from qa3
    
        Returns
        -------
        Qa3Question
            The updated question
        """
        question = self
        for match in re.finditer('[0-9]{4}', question):
            year = match.group(0)
            if 1899 < int(year) < 2099:
                i = qa3_answer.index_by_chunk(year)
                if i is None or qa3_answer.result[i].get_type() != 'refYear':
                    if year not in ref_years:
                        ref_years.append(year)
                    question = re.sub(year, '<NUM' + string.ascii_uppercase[ref_years.index(year)] + '>', question, 1)
        return Qa3Question(question)

    def substitute_num(self, numbers, qa3_answer):
        """
        Returns the question with the numbers tagged
        
        Replace numbers found in the question with the tag <NUM>
    
        Parameters
        ----------
        numbers : List(str)
            The list containing the numbers
        qa3_answer
            The results received from qa3
    
        Returns
        -------
        Qa3Question
            The updated question
        """
        question = self
        for match in re.finditer('[0-9]+', question):
            num = match.group(0)
            i = qa3_answer.index_by_chunk(num)
            if i is None or qa3_answer.result[i].get_type() != 'refYear':
                if num not in numbers:
                    numbers.append(num)
                question = re.sub(num, '<NUM' + string.ascii_uppercase[numbers.index(num)] + '>', question, 1)
        return Qa3Question(question)

    def substitute_from_qa3(self, result, index, dataset):
        """
        Returns the question with the result from qa3.link step1
        
        Replace the results' type from the corresponding chunk of text with a tag
    
        Parameters
        ----------
        result : Result
            Result from qa3.link
        index: int
            Index of the result from the results list
        dataset: str
            The dataset found by qa3
    
        Returns
        -------
        Qa3Question
            The updated question
        """
        question = self
        if re.search(result.chunk, question):
            if result.is_dataset(dataset):
                question = re.sub(result.chunk, '<DATASET>', question)
            elif result.is_type('refYear'):
                question = re.sub(result.chunk, '<YEAR' + str(index) + '>', question)
            elif result.is_identifier():
                question = re.sub(result.chunk, '<PROP' + str(index) + '>', question)
            else:
                question = re.sub(result.chunk, '<VALUE' + str(index) + '>', question)
        return Qa3Question(question)
