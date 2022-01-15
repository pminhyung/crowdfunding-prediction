import os
import pickle
from typing import Dict

from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier
import pandas as pd

from utils import load_yaml
from preprocessing import preprocess_data

def train(config:Dict[Dict[str:str]]) -> None:

    """
    [summary]

    Wadiz 리워드 프로젝트 달성률 예측을 위한 모델 학습 진행, 다음의 과정을 순차적으로 수행

        - 데이터 load
        - 전처리 수행 후 XGBClassifier 모델 학습
        - GridSearchCV를 통한 하이퍼파라미터 튜닝 수행
        - best parameter와 score 출력
        - 선택적으로 모델 저장
        - 저장 모델 경로 출력 (저장 시)

    [Args]:

        config (Dict[Dict]): 시드, 학습 관련, 하이퍼파라미터 튜닝 관련 값 arguments 정의

    [Returns]:
        None
    """

    # config값 파싱
    seed:int = config['SEED']                                         # seed : 랜덤시드번호
    save_model:bool = config['TRAIN']['SAVE_MODEL']                   # save_model : 학습모델 저장여부
    parent_dirname:str = config['TRAIN']['parent_dirname']            # parent_dirname : 학습모델의 부모 디렉토리 경로
    model_file_name:str = config['TRAIN']['model_file_name']          # model_file_nam : 저장할 학습모델의 basename
    test_size:float = config['TRAIN']['test_size']                    # test_size : 학습, 테스트 셋 split 시 사용할, 테스트 셋 사용 비율 (0과 1 사이)
    n_estimators:list = config['HYPERPARAMETERS']['n_estimators']     # n_estimators : 활용 트리 개수 (xgboost 학습 하이퍼파라미터)
    learning_rate:list = config['HYPERPARAMETERS']['learning_rate']   # learning_rate : 학습률 (xgboost 학습 하이퍼파라미터)
    wadiz_file_name:str = config['WADIZ']['wadiz_file_path']          # wadiz_file_name : 수집된 와디즈 raw data 파일경로

    # 크롤링 데이터 load
    wadiz = pd.read_excel(wadiz_file_name, engine = 'openpyxl')

    # 전처리 수행
    _, X, y = preprocess_data(wadiz)

    # Train/Validation set 분리
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed)

    # XGBoost Classifier 학습
    xgb_clf = XGBClassifier()
    xgb_clf.fit(X_train, y_train)

    # XGBoost Accuracy 계산 및 출력
    xgb_acc = xgb_clf.score(X_test, y_test)
    print(xgb_acc)

    # 하이퍼파라미터 튜닝 (GridsearchCV)
    xgb_params = {'n_estimators':n_estimators,
                'learning_rate':learning_rate}

    grid_xgb = GridSearchCV(xgb_clf, param_grid = xgb_params,
                cv= 5, n_jobs=-1)
    grid_xgb.fit(X_train, y_train)

    # GridSearchCV 결과 최적 score와 params 출력
    grid_score = grid_xgb.score(X_test,y_test)
    best_params = grid_xgb.best_params_

    print(f'Best Model Accuracy: {grid_score:.2f}')
    print(grid_xgb)
    print(best_params)

    # 최종 모델 저장
    if save_model:

        if not os.path.isdir(parent_dirname):
            os.mkdir(parent_dirname)

        pickle.dump(grid_xgb, open(os.join(parent_dirname, model_file_name), "wb"))

    print(f'Best Model Saved: {os.join(parent_dirname, model_file_name)}')

if __name__ == '__main__':

    # config 파일 load
    config = load_yaml('config.yaml')

    # config 사용한 모델 학습 수행
    train(config)