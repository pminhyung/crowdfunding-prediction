from typing import Dict

import pickle
import numpy as np
import pandas as pd

from preprocessing import preprocess_data
from utils import load_yaml

def test(config: Dict[Dict]) -> None:

    """
    [summary]

    [Args]:
        config (Dict[Dict]): [description]
    """

    model_path = config['TRAIN']['model_file_name']
    test_fname = config['TEST']['test_data_path']
    test_result_fname = config['TEST']['test_result_path']

    test = pd.read_excel(test_fname, engine = 'openpyxl')
    test_df = preprocess_data(test)

    pretrained_model = pickle.load(open(model_path, "rb"))

    y_pred = pretrained_model.predict(test_df)

    test_df['predictions'] = y_pred
    test_df.to_excel(test_result_fname, index=False)

if __name__ == '__main__':
    # config 파일 load
    config = load_yaml('config.yaml')

    # config 사용한 모델 학습 수행
    test(config)