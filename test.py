from typing import Dict

import pickle
import pandas as pd

from preprocessing import preprocess_data
from utils import load_yaml

def test(config: Dict[Dict]) -> None:

    """
    [summary]
        테스트 셋 데이터에 대한 테스트 수행 및 결과 파일 저장

    [Args]:
        config (Dict[Dict]): config.yaml를 load한 중첩된 Dict 객체 
    
    [Returns]:
        None
    """

    # test를 위한 config 파싱
    model_path = config['TRAIN']['model_file_name']         # model_path : 학습모델경로
    test_fname = config['TEST']['test_data_path']           # test_fname : 테스트셋 raw data 경로 (.xlsx 형식)
    test_result_fname = config['TEST']['test_result_path']  # test_result_fname : 테스트셋 inference 결과가 저장될 파일 경로

    # test set에 해당하는 raw data load
    test = pd.read_excel(test_fname, engine = 'openpyxl')

    # test set 데이터 전처리
    test_df = preprocess_data(test)

    # pretrained XGBClassifier 모델 load
    pretrained_model = pickle.load(open(model_path, "rb"))

    # test set에 대한 예측 수행
    y_pred = pretrained_model.predict(test_df)

    # 예측값 입력
    test_df['predictions'] = y_pred

    # test 결과 파일 저장
    test_df.to_excel(test_result_fname, index=False)

if __name__ == '__main__':

    # config 파일 load
    config = load_yaml('config.yaml')

    # config 사용한 모델 학습 수행
    test(config)