import re

import qa3wrapper.wrapper as qa3
import qa3.query as qa3query
import qa3.question as qa3question


class QA3:
    def __init__(self, question, query, qa3_answer=None):
        self.question = question
        self.query = query
        self.get_qa3(qa3_answer=qa3_answer)

    def get_qa3(self, qa3_answer):
        question = qa3question.Qa3Question(clean_string(self.question))
        query = qa3query.split_query(query=clean_string(self.query))

        numbers = []
        refDates = []
        refYears = []

        if qa3_answer is None:
            qa3_answer = qa3.get_answer_from_qa3(question)

        question = question.expand_numbers()
        question = question.substitute_date(ref_dates=refDates, qa3_answer=qa3_answer)
        question = question.substitute_year(ref_years=refYears, qa3_answer=qa3_answer)
        question = question.substitute_num(numbers=numbers, qa3_answer=qa3_answer)
        print(numbers)
        question = question.substitute_from_qa3(qa3_answer=qa3_answer)
        query.clean_frow()
        query.replace_dataset(qa_dataset=qa3_answer.dataset)
        query.expand_prefix()
        query.substitute_values(values=refDates, replace_to='DATE')
        query.substitute_values(values=refYears, replace_to='YEAR')
        query.substitute_values(values=numbers, replace_to='NUM')
        query.update_rows(qa3_answer)
        query.replace_measure(qa_dataset=qa3_answer.dataset)
        query.substitute_variables(replace_to='var')
        query.generalize_properties()
        query.remove_xdsdecimal()

        self.question = question
        self.query = query.join_query()


def clean_string(c_string):
    c_string = re.sub('\n', '', c_string).strip()
    c_string = re.sub(' +', ' ', c_string)

    return c_string
