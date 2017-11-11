import qa3.printer as printer
import qa3.qaCube as qaCube


class Main:
    printer.save_data(file_name='train', source_json='qald-6-train-datacube', use_cache=True)
    printer.save_data(file_name='test', source_json='qald-6-test-datacube', use_cache=True)
    printer.save_data(file_name='tagmetrain', source_json='qald-7-train-multilingual', use_cache=True, site=qaCube.TAGME)
