# <br/> 크라우드 펀딩 프로젝트 성공요인 분석 및 예측 모델 개발
### "Crowdfunding Success Factors Analysis and Development of Prediction model for Achievement Rate"
## "빅데이터 청년인재" 수료 PROJECT (2019. 08. 01 ~ 2019. 08. 24)

## 1. 빅데이터 청년인재
  
연세대학교(Yonsei Univ.)과 데이터산업진흥원(KDATA)가 공동으로 진행한 데이터청년캠퍼스 교육

*관련기사
- [빅데이터 청년인재](http://bigjob.dbguide.net/)
- [데이터산업진흥원, '2019 데이터 청년 캠퍼스' 성료...데이터산업 이끌 청년인재 600명 배출](http://www.digitaltoday.co.kr/news/articleView.html?idxno=214353)

## 2. 크라우드 펀딩 프로젝트 성공요인 분석 및 예측 모델 개발 
#### (Crowdfunding Success Factors Analysis and Development of Prediction model for Achievement Rate)
**설명 하단에 발표자료 포함**  
  
팀원 : 박민형, 박현준, 신채원, 임준희, 임효주, 최원재  
  
## 프로젝트 배경  
- 머신러닝을 활용한 리워드형 프로젝트의 달성률 예측 모델 개발, 중요 변수 도출
- 프로젝트 메이커들에게 가이드라인 제공하고, 서포터들에게는 성공할 프로젝트 선별을 통한 시간 및 비용 절약에 기여

## 3. Usage

### 3-0. `config.yaml` setting
- SEED: 랜덤시드번호
- WADIZ
    - wadiz_id: wadiz 개인 ID
    - wadiz_pw: wadiz 개인 pw
    - wadiz_file_path: wadiz 파일 저장 경로 (상대경로)
- NEWS
  - start_date: 뉴스 수집 범위 시작일자
  - end_date: 뉴스 수집 범위 종료일자
  - news_keyword: 뉴스 검색 쿼리 (키워드)
  - news_file_path: 뉴스 수집 파일 저장 경로 (상대경로)
  - max_num: 뉴스기사 수집 최대 개수 

- TRAIN
  - save_model: 학습모델 저장여부
  - wadiz_file_path: 수집된 와디즈 raw data 파일경로 
  - test_size: 학습, 테스트 셋 split 시 사용할, 테스트 셋 사용 비율 (0과 1 사이)
  - parent_dirname: 학습모델의 부모 디렉토리 경로
  - model_file_name: 저장할 모델 파일 basename

- HYPERPARAMETERS:
  - n_estimators: 활용 트리 개수 (xgboost 학습 하이퍼파라미터)
  - learning_rate: 학습률 (xgboost 학습 하이퍼파라미터)

- TEST
  - test_data_path: 테스트셋 파일 경로
  - test_result_path: 테스트셋 예측 결과 파일 저장 경로

### 3-1. Data Scraping
- wadiz 데이터 수집
```
python scraping.py -s wadiz
```
- navernews 데이터 수집
```
python scraping.py -s navernews
```
- wadiz, navernews 데이터 모두 수집 
```
python scraping.py -s all
```
  
### 3-2. Train
```
python train.py
```
- `train.py` : 데이터 수집, 전처리, 학습, 모델저장(optional) 수행

### 3-3. Test
```
python test.py
```
- `test.py` : 학습 모델 load 후 테스트 데이터에 대한 전처리, 예측 수행

## Updates
- (22. 01. 15) docs issues #3, #4 : 코드별, 함수별 주석 추가, type hint 추가
- (22. 01. 14) feat issues #2 : scraping.py에 argparse, config.yaml 활용을 통한 argument 파싱 기능 추가
- (22. 01. 14) feat issues #1 : scraping.py 독립 실행 기능 추가
- (21. 04. 08) 프로젝트 형태로 Refactoring

## Project Presentation

<img src = '/slides/slide1.PNG'>
<img src = '/slides/slide2.PNG'>
<img src = '/slides/slide3.PNG'>
<img src = '/slides/slide4.PNG'>
<img src = '/slides/slide5.PNG'>
<img src = '/slides/slide6.PNG'>
<img src = '/slides/slide7.PNG'>
<img src = '/slides/slide8.PNG'>
<img src = '/slides/slide9.PNG'>
<img src = '/slides/slide10.PNG'>
<img src = '/slides/slide11.PNG'>
<img src = '/slides/slide12.PNG'>
<img src = '/slides/slide13.PNG'>
<img src = '/slides/slide14.PNG'>
<img src = '/slides/slide15.PNG'>
<img src = '/slides/slide16.PNG'>
<img src = '/slides/slide17.PNG'>
<img src = '/slides/slide18.PNG'>
<img src = '/slides/slide19.PNG'>
<img src = '/slides/slide20.PNG'>
<img src = '/slides/slide21.PNG'>
<img src = '/slides/slide22.PNG'>
<img src = '/slides/slide23.PNG'>
<img src = '/slides/slide24.PNG'>
<img src = '/slides/slide25.PNG'>
<img src = '/slides/slide26.PNG'>
<img src = '/slides/slide27.PNG'>
<img src = '/slides/slide28.PNG'>
<img src = '/slides/slide29.PNG'>
<img src = '/slides/slide30.PNG'>
<img src = '/slides/slide31.PNG'>
<img src = '/slides/slide32.PNG'>
<img src = '/slides/slide33.PNG'>
<img src = '/slides/slide34.PNG'>
<img src = '/slides/slide35.PNG'>
<img src = '/slides/slide36.PNG'>
<img src = '/slides/slide37.PNG'>
<img src = '/slides/slide38.PNG'>
<img src = '/slides/slide39.PNG'>
<img src = '/slides/slide40.PNG'>
<img src = '/slides/slide41.PNG'>
<img src = '/slides/slide42.PNG'>
<img src = '/slides/slide43.PNG'>
<img src = '/slides/slide44.PNG'>
<img src = '/slides/slide45.PNG'>

