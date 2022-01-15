from typing import Tuple
import pandas as pd
from derived_variables import gen_variables

def prep_insta_follower_num(x:str) -> int:

    """
    [summary]
        메이커의 인스타그램 팔로워 수에 대해 전처리 수행

    [Args]:
        x (int): string type의 전처리 및 표기변환 전 인스타 팔로워 수

    [Returns]:
        int: 전처리 후 int type의 인스타 팔로워 수
    """

    # 천 단위 이상일 경우 ',' 제거
    x = x.replace(',', '') if '천' not in x else x

    # 단위 '천' 제거
    x = x.replace('천', '')

    # 천단위가 아닌 실제 단위로 표기 변환
    x = float(x)*1000 if '.' in x else int(x)

    # int type으로 출력
    x = int(x)
    
    return x

def bin_target(x:int) -> int:

    """
    [summary]
        classification task를 위한, 달성률 분포에 따른 binning 처리

    [Args]:
        x (int): 달성률(%)

    [Returns]:
        int: 100, 700에 따라 cut한 후 mapping 된 int type의 class
    """

    # 달성률 100% 미만 cut
    if x < 100:
        return 0

    # 달성률 100% 이상, 700% 미만 cut
    elif x < 700:
        return 1
    
    # 달성률 700% 이상 cut
    else:
        return 2

def preprocess_data(data:pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series]:

    """
    [summary]
        Wadiz 수집 데이터에 대해 파생변수 생성 및 전처리 수행
    
    [Args]:
        data (pd.DataFrame): 수집된 Wadiz raw data의 데이터프레임

    [Returns]:
        Tuple[pd.DataFrame, pd.DataFrame, pd.Series]: 다음 원소들로 이루어진 Tuple return

            - prep_data : 데이터프레임 타입의 타겟을 포함한 전처리 후 데이터
            - X: 데이터프레임 타입의 타겟 제외한 전처리 후 데이터
            - y: 시리즈 타입의 타겟
    """

    # 파생변수 생성
    data = gen_variables(data)

    # 날짜 데이터들 datatime 데이터로 변환
    data['펀딩시작날짜'] = pd.to_datetime(data['펀딩시작날짜'])
    data['펀딩마감날짜'] = pd.to_datetime(data['펀딩마감날짜'])
    data['배송시작날짜'] = pd.to_datetime(data['배송시작날짜'])

    # 펀딩기간 datetime to int
    data['펀딩기간'] = data['펀딩기간'].dt.days

    # 과거 프로젝트 수 컬럼에서 -1값들을 0으로 변경
    data['과거프로젝트수'] = data['과거프로젝트수'].apply(lambda x: 0 if x == -1 else x)

    # 과거 프로젝트 성공 개수 처리 (성공한 프로젝트일 경우 과거 프로젝트 성공 개수에서 1 빼기)
    for index, row in data.iterrows():
        if row['펀딩성공여부'] == '성공':
            data.at[index, '과거성공프로젝트수'] = data.iloc[index]['과거성공프로젝트수'] - 1

    # 위의결과 -1이 되어버린 값들을 0으로 변경
    data['과거성공프로젝트수'] = data['과거성공프로젝트수'].apply(lambda x: 0 if x == -1 else x)

    # 인스타그램팔로워수 - 표기 변환
    data['인스타팔로워수'] = data['인스타팔로워수'].apply(prep_insta_follower_num)

    # 달성액, 서포터수 - str to int 변환
    data['달성액'] = data['달성액'].apply(lambda x: int(x.replace('원', '')))
    data['서포터수'] = data['서포터수'].apply(lambda x: int(x.replace(',', '')))

    data = data.drop(columns=['목표금액과기간', '달성률'], axis=1)

    # 펀딩시작요일 - One Hot Encoding
    data_new = pd.concat([data, pd.get_dummies(data['펀딩시작요일'])], axis=1)

    # 명목형 달성률 생성
    data['타겟'] = data['달성률'].apply(bin_target)

    # 최종사용 변수 list
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
                     '펀딩기간',
                     '일펀딩금액',
                     '일글수',
                     '문장당강조',
                     '문장당밑줄']

    # 사용변수만을 포함한 데이터프레임 생성
    prep_data = data_new[feature_names]

    # 학습을 위한 X, y 정의
    X = prep_data.drop(['log_count'], axis=1)
    y = prep_data['log_count']

    # 전처리 결과 전체데이터, 타겟 제외 데이터, 타겟 반환
    return prep_data, X, y