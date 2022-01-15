import re
from typing import List, Tuple
from urllib.request import urlopen

import pandas as pd
from bs4 import BeautifulSoup
from konlpy.tag import Okt

def make_html_list(project_url: pd.Series) -> List:
    
    """
    [summary]
        프로젝트 url 페이지의 html을 파싱한 결과들을 list로 저장

    [Args]:
        project_url (pd.Series): 프로젝트들의 url

    [Returns]:
        List: 각 프로젝트의 url 페이지 html을 파싱한 결과 list
    """

    # 저장할 html list 생성
    html_list = []

    # 프로젝트 url별 html 파싱
    for i in project_url:
        html = urlopen(i)
        bsObject = BeautifulSoup(html, 'lxml')
        html_list.append(bsObject)

    return html_list

def cleaning_text(raw_html:str) -> str:
    
    """
    [summary]
        html 태그 형식과 unicode, 영문, 특수기호를 제거하는 전처리 수행

    [Args]:
        raw_html (str): 해당 url의 파싱된 html

    [Returns]:
        str: 전처리 후 cleaned text
    """

    # html tag 제거
    x = re.sub(r'<[^>]*>','', raw_html)

    # unicode 제거
    x = re.sub(r'(\xa0|\n)','', x)

    # 영문 제거
    x = re.sub('[a-zA-Z]' , '', x)

    # 특수기호 제거
    x = re.sub('[\{\}\[\]\/,;|\)*~`^\-_+<>@➤▶\#$%&\\\=\(\'\"]',
                          '', x)
    return x

def count_sentence(cleaned_text:str) -> Tuple[List, int]:
    
    """
    [summary]
        문장 분리 후 문장 수 count 수행

    [Args]:
        cleaned_text (str): cleaning_text() 수행 결과인 전처리된 텍스트

    [Returns]:
        Tuple[List, int]:
            - cleaned_list(List): 분리된 문장 중 4음절 이상인 문장들의 list
            - num(int): 분리된 문장 수
    """

    # 특정 기호에 따른 문장분리
    text_fin =  re.split(r'(\.|\!|\?|\:)',cleaned_text)

    # 4음절 이상인 문장만 저장
    cleaned_list = [x for x in text_fin if len(x)>4]

    # 문장 수 저장
    num = len(cleaned_list)

    # 문장 list와 문장 수 반환
    return cleaned_list, num


def syllables_count(clean_text:str) -> int:
    
    """
    [summary]
        추가적으로 특수문자, 숫자, 공백 제거 후 음절 수 계산

    [Args]:
        clean_text (str): cleaning_text() 수행 결과인 전처리된 텍스트

    [Returns]:
        int: 음절 수
    """

    # 특수문자 완전제거
    clean_text2 = re.sub('[\{\}\[\]\/,;|\).!:?(\'\"]', '', clean_text)

    # 숫자 제거
    clean_text2 = re.sub(r'\d', '', clean_text2)

    # 공백 제거
    clean_text2 = re.sub(r'\s', '', clean_text2)

    # 음절 수 저장 및 반환
    len_syllables = len(clean_text2)
    return len_syllables

def readabilty_score(len_sentences:int, len_words:int, len_syllables:int) -> float:

    """
    [summary]
        가독성의 척도로 사용되는 Flesch reading ease score 관련 논문을 참고하여 해당 점수 계산

        Reference : 

        Kincaid, J.P., Fishburne, R.P., Rogers, R.L., & Chissom, B.S. (1975). 
        Derivation of new readability formulas (automated readability index, fog count, and flesch reading ease formula) for Navy enlisted personnel. 
        Research Branch Report 8–75. Chief of Naval Technical Training: Naval Air Station Memphis.

    [Args]:
        len_sentences (int): 문장 수
        len_words (int): 단어 수 (형태소 분석 기준)
        len_syllables (int): 음절 수

    [Returns]:
        float: 가독성 지수
    """

    # Flesch reading ease score 계산 (Reference 논문 수식 구현)
    score = 206.835 - 1.015*(len_words/len_sentences) - 84.6*(len_syllables/len_words)

    return score

def get_readability(data:pd.Series) -> List:

    """
    [summary]
        각 데이터의 텍스트에 대한 가독성 지수 산출

    Args:
        data (pd.Series): wadiz 데이터 내 텍스트 값을 포함한 pd.Series

    Returns:
        List: 프로젝트들에 대한 가독성 지수 list
    """

    # url 페이지의 html 파싱 결과 list
    urls = data['url']
    html_list = make_html_list(urls)

    # html 내 본문 section의 tag 분리 결과 list
    raw_html = []
    for i in html_list:
        raw_html.append(i.find_all('div', {'class': 'inner-contents fr-view'}))

    # <strong>, <u> count list
    strong_count = []
    u_count = []

    for i in raw_html:
        strong_count.append(str(i).count('<strong>'))
        u_count.append(str(i).count('<u>'))

    # 파싱된 html에 대한 텍스트 전처리, 저장
    clean_text = []

    for i in raw_html:
        cleaned_text = cleaning_text(i)
        clean_text.append([cleaned_text])

    # 문장분리 및 문장 수 list
    list_sentences = []
    len_sentences = []

    for i in clean_text:
        clean_str = str(i)

        # 문장분리 및 전처리
        list_sentences2, len_sentences2 = count_sentence(clean_str)

        # 문장분리 결과 list
        list_sentences.append(list_sentences2)

        # 분리된 문장 수 list
        len_sentences.append(len_sentences2)

    # 문장들에 대해 pos-tagging 수행
    tag = Okt()
    pos_all = []

    for i in clean_text:
        
        # pos-tagging 수행
        pos = tag.pos(clean_str)

        # pos-tagging 결과 저장
        pos_all.append(pos)

    # 형태소 개수 list
    len_pos = []

    # 형태소 개수 count
    for i in pos_all:
        len_pos.append(len(i))

    # 음절 수 list
    syllables_list = []

    # 전처리 후 음절 count
    for i in clean_text:
        clean_str = str(i)
        len_syllables = syllables_count(clean_str)
        syllables_list.append(len_syllables)

    # 가독성 지수 list
    read_score = []

    for i in range(len(data)):
        
        # 문장 수, 단어 수, 음절 수 기반 가독성 지수 계산
        score = readabilty_score(len_sentences[i], len_pos[i], len_syllables[i])
        read_score.append(score)

    return read_score
