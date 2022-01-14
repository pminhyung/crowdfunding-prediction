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

            - SEED : random seed로 사용되는 seed number

            - TRAIN, save_model : 
            - TRAIN, test_size : 
            - TRAIN, parent_dirname : 
            - TRAIN, model_file_name : 

            - HYPERPARAMETERS, n_estimators :
            - HYPERPARAMETERS, learning_rate :

    [Returns]:
        None
    """

    # config값 파싱
    seed:int = config['SEED']
    save_model:bool = config['TRAIN']['SAVE_MODEL']
    parent_dirname:str = config['TRAIN']['parent_dirname']
    model_file_name:str = config['TRAIN']['model_file_name']
    test_size:float = config['TRAIN']['test_size']
    n_estimators:list = config['HYPERPARAMETERS']['n_estimators']
    learning_rate:list = config['HYPERPARAMETERS']['learning_rate']
    wadiz_file_name:str = config['WADIZ']['wadiz_file_path']

    # 크롤링 데이터 load
    wadiz = pd.read_excel(wadiz_file_name, engine = 'openpyxl')

    # 전처리 수행
    _, X, y = preprocess_data(wadiz)

    # Train/Validation set 분리
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed)

    ## XGBoost Classifier 학습
    xgb_clf = XGBClassifier()
    xgb_clf.fit(X_train, y_train)

    xgb_acc = xgb_clf.score(X_test, y_test)
    print(xgb_acc)

    # 하이퍼파라미터 튜닝 (GridsearchCV)
    xgb_params = {'n_estimators':n_estimators,
                'learning_rate':learning_rate}

    grid_xgb = GridSearchCV(xgb_clf, param_grid = xgb_params,
                cv= 5, n_jobs=-1)
    grid_xgb.fit(X_train, y_train)
    grid_score = grid_xgb.score(X_test,y_test)
    best_params = grid_xgb.best_params_

    print(f'Best Model Accuracy: {grid_score:.2f}')
    print(grid_xgb)
    print(best_params)

    # save model
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