from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import openpyxl
import requests
import time

def get_cat_success_rate():
    """ Print funding success rate by categories in Wadiz through scrapping

    Keyword arguments:

    return : None
    """
    driver = webdriver.Chrome('./chromedriver')

    # project lists (recent -> old)
    base_link = 'https://www.wadiz.kr/web/wreward/category/310?keyword=&endYn=Y&order=closing'
    driver.get(base_link)

    time.sleep(1)

    # scroll down
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

    # container of projects
    projects = driver.find_elements_by_css_selector('div.ProjectCardList_item__1owJa')

    success = 0
    fail = 0

    for p in projects:
        percent = p.find_element_by_css_selector('span.RewardProjectCard_percent__edRT9').text.replace('%', '')
        if int(percent) < 100:
            fail += 1
        else:
            success += 1

    print('전체 갯수:', len(projects))
    print('성공률:', success/len(projects)*100)