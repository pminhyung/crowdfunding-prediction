import datetime
import pandas as pd

from readability import get_readability

def gen_variables(data):
    # 5개 필요변수 추가
    fund_amt = []  # 목표금액
    start_dt = []  # 펀딩시작날짜
    fin_dt = []  # 펀딩마감날짜
    dlv_dt = []  # 배송시작날짜
    fin_dlv_term = []  # 마감일과 배송시작일 차이

    for _ in range(0, len(data)):
        split_data = data.loc[_][['목표금액과기간']].str.split(' ')
        ls = split_data['목표금액과기간']

        # 목표금액 추출
        price = ls[2].replace(",", "").replace("원", "")
        fund_amt.append(int(price))

        # 펀딩 시작, 마감 날짜 추출
        start_date, end_date = ls[8].split('-')
        start_dt.append(start_date)
        fin_dt.append(end_date)

        # 첫 배송날짜 추출
        deliver_date = data.loc[_][['배송시작날짜']].str.split('/')
        dlv_dt.append(deliver_date[0][0].replace(" ", ""))

        # 첫 배송날짜와 펀딩마감 날짜의 차이 일수 계산
        oneDatetime = datetime.datetime.strptime(fin_dt[_], '%Y.%m.%d')
        twoDatetime = datetime.datetime.strptime(dlv_dt[_], '%Y.%m.%d')
        result = twoDatetime - oneDatetime
        fin_dlv_term.append(result.days)

    data['목표금액'] = fund_amt
    data['펀딩시작날짜'] = start_dt
    data['펀딩마감날짜'] = fin_dt
    data['마감배송차이'] = fin_dlv_term

    # 펀딩기간 추가 및 정수 변환
    data['펀딩기간'] = (data['펀딩마감날짜'] - data['펀딩시작날짜'])

    # 펀딩 시작 요일 추가
    start_dt = pd.to_datetime(start_dt)
    data['펀딩시작요일'] = start_dt.strftime('%a')

    # 펀딩 성공 여부 ( '성공' vs '실패')
    data['펀딩성공여부'] = data['달성률'].apply(lambda x: 1 if x > 99 else 0)

    # 앵콜펀딩 여부 ('앵콜' vs '최초')
    data['앵콜펀딩여부'] = data['제목'].apply(lambda x: 1 if '앵콜' in x else 0)

    # 인스타 여부 컬럼추가
    data['인스타존재여부'] = data['인스타팔로워수'].apply(lambda x: 1 if x in ['no account', 'link error'] else 0)

    # 인스타그램 no account와 link error값들을 0으로 바꾸기
    data['인스타팔로워수'] = data['인스타팔로워수'].apply(lambda x: 0 if x in ['no account', 'link error'] else x)

    # 텍스트 처리
    data['일펀딩금액'] = data.목표금액 / data.펀딩기간
    data['일글수'] = data.글업데이트수 / data.펀딩기간
    data['문장당강조'] = data.Strong / data.문장수
    data['문장당밑줄'] = data.Under / data.문장수

    # 시각화 지수
    data['시각화지수'] = data.좋아요수 + (data.이미지수 * 10) + (100 - data.비디오수 * 10)

    def bin_target(x):
        if x < 100:
            return 0
        elif x < 700:
            return 1
        else:
            return 2

    # 가독성 지수
    data['가독성'] = get_readability(data)

    # 명목형 달성률 생성
    data['타겟'] = data['달성률'].apply(bin_target)

    return data

