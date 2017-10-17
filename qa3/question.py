import re
import string


class Qa3Question(str):
    def expand_numbers(self):
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
            for match in re.finditer(pattern, self):
                match = match.group(0)
                num = re.search('[0-9]+', match).group(0)
                self = re.sub(re.escape(match), num+zeroes, self)
        return Qa3Question(self)

    def substitute_date(self, ref_dates, qa3_answer):
        for match in re.finditer('[0-9]{4}-[0-9]{2}-[0-9]{2}', self):
            date = match.group(0)
            i = qa3_answer.index_by_chunk(date)
            if i is None or qa3_answer.result[i].get_type() != 'refYear':
                if date not in ref_dates:
                    ref_dates.append(date)
                self = re.sub(date, '<NUM' + string.ascii_uppercase[ref_dates.index(date)] + '>', self, 1)
        return Qa3Question(self)

    def substitute_year(self, ref_years, qa3_answer):
        for match in re.finditer('[0-9]{4}', self):
            year = match.group(0)
            if 1899 < int(year) < 2099:
                i = qa3_answer.index_by_chunk(year)
                if i is None or qa3_answer.result[i].get_type() != 'refYear':
                    if year not in ref_years:
                        ref_years.append(year)
                    self = re.sub(year, '<NUM' + string.ascii_uppercase[ref_years.index(year)] + '>', self, 1)
        return Qa3Question(self)

    def substitute_num(self, numbers, qa3_answer):
        for match in re.finditer('[0-9]+', self):
            num = match.group(0)
            i = qa3_answer.index_by_chunk(num)
            if i is None or qa3_answer.result[i].get_type() != 'refYear':
                if num not in numbers:
                    numbers.append(num)
                self = re.sub(num, '<NUM' + string.ascii_uppercase[numbers.index(num)] + '>', self, 1)
        return Qa3Question(self)

    def substitute_from_qa3(self, qa3_answer):
        for i, result in enumerate(qa3_answer.result):
            if re.search(result.chunk, self):
                if result.is_dataset(qa3_answer.dataset):
                    self = re.sub(result.chunk, '<DATASET>', self)
                elif result.is_type('refYear'):
                    self = re.sub(result.chunk, '<YEAR' + str(i) + '>', self)
                # elif result.is_integer():
                #     self = re.sub(result.chunk, '<NUM' + str(i) + '>', self)
                elif result.is_identifier():
                    self = re.sub(result.chunk, '<PROP' + str(i) + '>', self)
                else:
                    self = re.sub(result.chunk, '<VALUE' + str(i) + '>', self)
        return Qa3Question(self)
