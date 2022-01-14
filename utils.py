from typing import Dict
import time
import yaml

from selenium import webdriver

def load_yaml(filename:str) -> Dict[Dict]:
    """
    [summary]

    [Args]:
        filename (str): [description]

    [Returns]:
        Dict[Dict]: [description]
    """
    with open(filename, 'r') as f:
        return yaml.load(f, Loader=yaml.FullLoader)

def get_cat_success_rate() -> None:
    """
    [summary]
        와디즈 페이지에서의 특정 카테고리 내 성공 및 실패 프로젝트 수 count
            - 성공 및 실패 프로젝트 개수 print
            - 해당 카테고리 성공률 print

    [Returns]:
        None
    """
    driver = webdriver.Chrome('./chromedriver')
    category_num = 310

    # 프로젝트 리스트 페이지 (recent -> old)
    base_link = f'https://www.wadiz.kr/web/wreward/category/{category_num}?keyword=&endYn=Y&order=closing'
    driver.get(base_link)

    time.sleep(1)

    # 무한 스크롤 다운 수행
    SCROLL_PAUSE_TIME = 1
    while True:
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            else:
                last_height = new_height
                continue

    time.sleep(10)

    # 프로젝트 개별 컨테이너
    projects = driver.find_elements_by_css_selector('div.ProjectCardList_item__1owJa')

    success = 0
    fail = 0

    # 프로젝트별 성공 또는 실패 여부 count
    for p in projects:
        percent = p.find_element_by_css_selector('span.RewardProjectCard_percent__edRT9').text.replace('%', '')
        if int(percent) < 100:
            fail += 1
        else:
            success += 1

    print('전체 갯수:', len(projects))
    print('성공률:', success/len(projects)*100)