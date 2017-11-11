import re

import wrapper.qa3Wrapper as qa3Wrapper
import wrapper.tagMeWrapper as tagMeWrapper
import qa3.query as qa3query
import qa3.question as qa3question

QA3 = 'QA3'
TAGME = 'TagMe'


class QACube:
    def __init__(self, question, query):
        self.question = question
        self.query = query

    def get_qa3(self, qa3_answer=None, site=QA3):
        question = qa3question.Qa3Question(_clean_string(self.question))
        query = qa3query.Qa3Query(_clean_string(self.query))

        if qa3_answer is None:
            if site is QA3:
                qa3_answer = qa3Wrapper.get_answer_from_web(question)
            elif site is TAGME:
                qa3_answer = tagMeWrapper.get_answer_from_web(question)

        numbers = []
        refDates = []
        refYears = []

        question = question.expand_numbers()
        question = question.substitute_date(ref_dates=refDates, qa3_answer=qa3_answer)
        question = question.substitute_year(ref_years=refYears, qa3_answer=qa3_answer)
        question = question.substitute_num(numbers=numbers, qa3_answer=qa3_answer)

        query = query.clean_frow()
        query = query.expand_prefix()
        query = query.replace_dataset(qa3_dataset=qa3_answer.dataset)
        query = query.substitute_values(values=refDates, replace_to='DATE')
        query = query.substitute_values(values=refYears, replace_to='YEAR')
        query = query.substitute_values(values=numbers, replace_to='NUM')

        for i, result in enumerate(qa3_answer.result):
            query = query.substitute_from_qa3(result=result, index=i)
            question = question.substitute_from_qa3(result=result, index=i, dataset=qa3_answer.dataset)

        query = query.replace_measure(qa3_dataset=qa3_answer.dataset)
        query = query.substitute_variables()
        query = query.generalize_properties()
        # query = query.remove_xsddecimal()
        query = query.reorder_query()

        self.question = _clean_string(question)
        self.query = _clean_string(query)

    def fillin_query(self, question, qa3_answer=None, site=QA3):
        new_question = qa3question.Qa3Question(_clean_string(question))
        qa3_question = qa3question.Qa3Question(_clean_string(self.question))
        qa3_query = qa3query.Qa3Query(_clean_string(self.query))

        if qa3_answer is None:
            if site is QA3:
                qa3_answer = qa3Wrapper.get_answer_from_web(question)
            elif site is TAGME:
                qa3_answer = tagMeWrapper.get_answer_from_web(question)

        numbers = []
        refDates = []
        refYears = []

        new_question = new_question.expand_numbers()
        new_question = new_question.substitute_date(ref_dates=refDates, qa3_answer=qa3_answer)
        new_question = new_question.substitute_year(ref_years=refYears, qa3_answer=qa3_answer)
        new_question = new_question.substitute_num(numbers=numbers, qa3_answer=qa3_answer)

        for i, result in enumerate(qa3_answer.result):
            new_question = new_question.substitute_from_qa3(result=result, index=i, dataset=qa3_answer.dataset)

        qa3_question = qa3_question.fillin_from_qa3(qa3_answer=qa3_answer)
        qa3_question = qa3_question.fillin_date(ref_dates=refDates)
        qa3_question = qa3_question.fillin_year(ref_years=refYears)
        qa3_question = qa3_question.fillin_num(numbers=numbers)

        qa3_query = qa3_query.fillin_dataset(qa3_dataset=qa3_answer.dataset)
        qa3_query = qa3_query.fillin_measure(qa3_dataset=qa3_answer.dataset)
        qa3_query = qa3_query.fillin_from_qa3(qa3_answer=qa3_answer)
        qa3_query = qa3_query.fillin_values(values=refDates, replace_from='DATE')
        qa3_query = qa3_query.fillin_values(values=refYears, replace_from='YEAR')
        qa3_query = qa3_query.fillin_values(values=numbers, replace_from='NUM')

        self.question = _clean_string(qa3_question)
        self.query = _clean_string(qa3_query)
        return new_question


def _clean_string(c_string):
    c_string = re.sub('[\n\t]', ' ', c_string).strip()
    c_string = re.sub(' +', ' ', c_string)
    return c_string
