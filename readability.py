import re
from typing import List, Tuple
from urllib.request import urlopen

import pandas as pd
from bs4 import BeautifulSoup
from konlpy.tag import Okt

def make_html_list(project_url: str) -> List:
    
    """
    [summary]

    [Args]:
        project_url (str): [description]

    [Returns]:
        List: [description]
    """

    html_list = []
    for i in project_url:
        html = urlopen(i)
        bsObject = BeautifulSoup(html, 'lxml')
        html_list.append(bsObject)
    return html_list

def cleaning_text(raw_html:str) -> str:
    
    """
    [summary]

    [Args]:
        raw_html (str): [description]

    [Returns]:
        str: [description]
    """

    str_text = str(raw_html)
    str_text = re.sub(r'<[^>]*>','',str_text)
    str_text = re.sub(r'(\xa0|\n)','',str_text)
    cleaned_text = re.sub('[a-zA-Z]' , '', str_text)
    cleaned_text = re.sub('[\{\}\[\]\/,;|\)*~`^\-_+<>@➤▶\#$%&\\\=\(\'\"]',
                          '', cleaned_text)
    return cleaned_text

def count_sentence(cleaned_text:str) -> Tuple[List, int]:
    
    """
    [summary]

    [Args]:
        cleaned_text (str): [description]

    [Returns]:
        Tuple[List, int]: [description]
    """

    text_fin =  re.split(r'(\.|\!|\?|\:)',cleaned_text)
    cleaned_list = [x for x in text_fin if len(x) >4]
    return cleaned_list, len(cleaned_list)


def syllables_count(clean_text:str) -> int:
    
    """
    [summary]

    [Args]:
        clean_text (str): [description]

    [Returns]:
        int: [description]
    """

    # 특수문자 완전제거
    clean_text2 = re.sub('[\{\}\[\]\/,;|\).!:?(\'\"]', '', clean_text)

    # 숫자 제거
    clean_text2 = re.sub(r'\d', '', clean_text2)

    # 공백 제거
    clean_text2 = re.sub(r'\s', '', clean_text2)

    # 음절
    len_syllables = len(clean_text2)
    return len_syllables

def readabilty_score(len_sentences:int, len_words:int, len_syllables:int) -> float:

    """
    [summary]

    [Args]:
        len_sentences (int): [description]
        len_words (int): [description]
        len_syllables (int): [description]

    [Returns]:
        float: [description]
    """

    score = 206.835 - 1.015*(len_words/len_sentences) - 84.6*(len_syllables/len_words)
    return score

def get_readability(data:pd.Series) -> List:
    """
    [summary]
        calculate readability score from input data

    Args:
        data (pd.Series): [description]

    Returns:
        List: [description]
    """

    urls = data['url']
    html_list = make_html_list(urls)

    # html 중에서 내용 부분만 파싱
    raw_html = []
    for i in html_list:
        raw_html.append(i.find_all('div', {'class': 'inner-contents fr-view'}))

    # 각 strong, u 개수
    strong_count = []
    u_count = []

    for i in raw_html:
        strong_count.append(str(i).count('<strong>'))
        u_count.append(str(i).count('<u>'))

    # 각 html 정제
    clean_text = []

    for i in raw_html:
        cleaned_text = cleaning_text(i)
        clean_text.append([cleaned_text])

    # 각 html 문장개수
    list_sentences = []
    len_sentences = []

    for i in clean_text:
        clean_str = str(i)
        list_sentences2, len_sentences2 = count_sentence(clean_str)
        list_sentences.append(list_sentences2)
        len_sentences.append(len_sentences2)

    # 각 정제문자에서 pos 구하기
    tag = Okt()
    pos_all = []

    for i in clean_text:
        clean_str = str(i)
        pos = tag.pos(clean_str)
        pos_all.append(pos)

    # pos 개수 구하기
    len_pos = []

    for i in pos_all:
        len_pos.append(len(i))

    # 각 음절 계산
    syllables_list = []

    for i in clean_text:
        clean_str = str(i)
        len_syllables = syllables_count(clean_str)
        syllables_list.append(len_syllables)

    read_score = []

    for i in range(len(data)):
        score = readabilty_score(data.문장수[i], data.단어수[i], data.음절수[i])
        read_score.append(score)

    return read_score
