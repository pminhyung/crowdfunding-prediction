import datetime
import pandas as pd
import numpy as np
import openpyxl
from derived_variables import gen_variables

def preprocess_data(data:pd.DataFrame) -> pd.DataFrame:
    """ preprocess data before training

        Keyword arguments:
        data -- raw data (dataframe)

        return : dataframe
        """

    data = gen_variables(data)

    # 펀딩기간 정수 변환
    data['펀딩기간'] = data.펀딩기간.dt.days

    # 과거 프로젝트 수 컬럼에서 -1값들을 0으로 변경
    data['과거프로젝트수'] = data['과거프로젝트수'].apply(lambda x: 0 if x == -1 else x)

    # 과거 프로젝트 성공 개수 처리 (성공한 프로젝트일 경우 과거 프로젝트 성공 개수에서 1 빼기)
    for index, row in data.iterrows():
        if row['펀딩성공여부'] == '성공':
            data.at[index, '과거성공프로젝트수'] = data.iloc[index]['과거성공프로젝트수'] - 1

    # 위의결과 -1이 되어버린 값들을 0으로 변경
    data['과거성공프로젝트수'] = data['과거성공프로젝트수'].apply(lambda x: 0 if x == -1 else x)

    # 종속변수 log transformation
    # data["log_count"] = np.log(data["달성률"] + 1)

    data = data.drop(columns=['목표금액과기간', '달성률'], axis=1)

    # 펀딩시작요일 원핫인코딩
    data_new = pd.concat([data, pd.get_dummies(data['펀딩시작요일'])], axis=1)

    feature_names = ['log_count',  # 정답값
                     '좋아요수',
                     '목표금액',
                     '리워드종류수',
                     '이미지수',
                     '비디오수',
                     '마감배송차이',
                     '와디즈팔로워수',
                     '과거프로젝트수',
                     '과거성공프로젝트수',
                     '앵콜펀딩여부',
                     '음절수',
                     '단어수',
                     '문장수',
                     'Strong',
                     'Under',
                     '가독성',
                     '가독성2',
                     '제목단어수',
                     '펀딩성공여부',
                     # '카테고리',
                     '디자인소품',
                     '반려동물',
                     '뷰티',
                     '스포츠·모빌리티',
                     '여행·레저',
                     '테크·가전',
                     '패션·잡화',
                     '푸드',
                     '홈리빙',
                     'Fri',
                     'Mon',
                     'Sat',
                     'Sun',
                     'Thu',
                     'Tue',
                     'Wed',
                     # '성공비율',
                     '펀딩기간',
                     '일펀딩금액',
                     '일글수',
                     '문장당강조',
                     '문장당밑줄']

    prep_data = data_new[feature_names]

    X = prep_data.drop(['log_count'], axis=1)
    y = prep_data['log_count']

    return prep_data, X, y