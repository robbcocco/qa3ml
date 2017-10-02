import qa3thing.manipulator as qa3


class Main:
    qa3.save_data(file_name='train', source_json='qald-6-train-datacube')
    qa3.save_data(file_name='test', source_json='qald-6-test-datacube')
