from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
import openpyxl

import argparse
import time
import re
from utils import load_yaml
from typing import Dict

def login_wadiz(driver: Chrome, wadiz_id:str, wadiz_pw:str) -> Chrome:
    """
    [summary]
        와디즈(wadiz) 로그인 페이지 접속 및 로그인 수행

    [Args]:
        driver (Chrome): 실행중인 크롬 드라이버
        wadiz_id (str): wadiz 페이지의 개인 ID
        wadiz_pw (str): wadiz 페이지의 개인 Password

    [Returns]:
        Chrome: 실행중인 크롬 드라이버
    """
    login_link = 'https://www.wadiz.kr/web/waccount/wAccountLogin?returnUrl=https://www.wadiz.kr/web/main'
    driver.get(login_link)
    id_section = driver.find_element_by_css_selector('input#userName')
    id_section.send_keys(wadiz_id) # input e-mail
    pw_section = driver.find_element_by_css_selector('input#password')
    pw_section.send_keys(wadiz_pw) # input password
    login_btn = driver.find_element_by_css_selector('button#btnLogin')
    login_btn.click()
    time.sleep(1.5)
    return driver

def scroll_to_end(driver:Chrome) -> Chrome:
    """
    [summary]
        와디즈(wadiz) 내 리워드 프로젝트 목록 페이지에서 무한 스크롤 다운 수행

    [Args]:
        driver (Chrome): 실행중인 크롬 드라이버

    [Returns]:
        Chrome: 실행중인 크롬 드라이버
    """
    while True:
        try:
            target = driver.find_element_by_css_selector('button.ProjectListMoreButton_button__27eTb')
            actions = ActionChains(driver)
            actions.move_to_element(target)
            actions.perform()
            time.sleep(2)
        except:
            break
    return driver

def check_exists_by_css_selector(driver:Chrome, css_selector:str) -> bool:
    """
    [summary]
        특정 css_selector가 존재여부 check

    [Args]:
        driver (Chrome): 실행중인 크롬 드라이버
        css_selector (str): 존재여부를 check할 css_selector

    [Returns]:
        bool: css_selector 존재여부
    """
    try:
        driver.find_element_by_css_selector(css_selector)
    except:
        return False
    return True

def scrap_wadiz(config:Dict[Dict]) -> str:

    """
    [summary]
        '와디즈 홈페이지 내 리워드형 프로젝트 데이터 수집'

    [프로젝트 수집 범위] : 
        마감된 리워드형 프로젝트 전체 (최근에서 오래된 순)

    [수집 변수] :
        'url', '제목', '카테고리', '메이커', '달성률', '달성액', '서포터수', '좋아요수', '요약글', '목표금액과기간', '글업데이트수', '댓글수', \
        '리워드종류수', '이미지수', '비디오수', '배송시작날짜', '인스타팔로워수', '와디즈팔로워수', '과거프로젝트수', '과거성공프로젝트수'

    [Args]:
        config (Dict[Dict[str]]): 뉴스기사 수집범위에 해당하는 시작일자, 종료일자, 키워드, 저장파일경로에 대한 key-value 가진 Dict

    [Returns]:
        str: 저장파일경로
    """

    wadiz_id:str = config['WADIZ']['wadiz_id']
    wadiz_pw:str = config['WADIZ']['wadiz_pw']
    file_path:str = config['WADIZ']['wadiz_file_path']

    wb = openpyxl.Workbook()
    sheet = wb.active

    sheet.append(['url', '제목', '카테고리', '메이커', '달성률', '달성액', '서포터수', '좋아요수', '요약글', '목표금액과기간', '글업데이트수', '댓글수', \
                  '리워드종류수', '이미지수', '비디오수', '배송시작날짜', '인스타팔로워수', '와디즈팔로워수', '과거프로젝트수', '과거성공프로젝트수'])

    driver = Chrome('./chromedriver')

    # 와디즈 로그인
    driver = login_wadiz(driver, wadiz_id, wadiz_pw)
    
    # 마감 프로젝트 리스트 페이지 (recent -> old)
    base_link = 'https://www.wadiz.kr/web/wreward/category/308?keyword=&endYn=Y&order=closing'
    driver.get(base_link)
    driver.maximize_window()

    time.sleep(1)

    # 페이지 마지막까지 스크롤 다운 수행
    driver = scroll_to_end(driver)

    # 개별 프로젝트 컨테이너
    projects = driver.find_elements_by_css_selector('div.ProjectCardList_item__1owJa')

    count = 1
    idx = 0

    # 전체 목록에서 정보 수집
    for p in projects:

        print(count)

        image = p.find_element_by_css_selector('a.ProjectCardLink_link__2X36I.CommonProjectCard_image__1aEog')

        # '이름' 저장
        try:
            name = p.find_element_by_css_selector('p.CommonProjectCard_title__28lHZ.RewardProjectCard_title__RDEBu').text
        except:
            name = 'no info'

        # '카테고리' 저장
        try:
            category = p.find_element_by_css_selector('span.RewardProjectCard_category__1vo_V').text
        except:
            category = 'no info'

        # '메이커' 저장
        try:
            maker = p.find_element_by_css_selector('span.RewardProjectCard_makerName__2sITk').text
        except:
            maker = 'no info'

        # '달성률(%)' 저장
        try:
            percent = p.find_element_by_css_selector('span.RewardProjectCard_percent__edRT9').text.replace('%', '')
        except:
            percent = 'no info'

        # '펀딩금액' 저장
        try:
            money = p.find_element_by_css_selector('span.RewardProjectCard_amount__2GV5X').text.replace(',', '')
        except:
            money = 'no info'

        print(name)


        # 새 탭으로 프로젝트 세부 페이지 접속 (new tab)
        project_url = image.get_attribute('href')

        driver.execute_script("window.open('');")
        time.sleep(1.5)


        # 해당 탭으로 포커싱 이동 (new tab)
        driver.switch_to.window(driver.window_handles[1])
        driver.get(project_url)
        time.sleep(1.5)

        # 서포터 수
        try:
            supporters = driver.find_element_by_css_selector('p.total-supporter strong').text
        except:
            supporters = 0

        # 좋아요 수
        try:
            likes = driver.find_element_by_css_selector('em.cnt-like').text
        except:
            likes = 0

        # 요약글 문장
        try:
            summary = driver.find_element_by_css_selector('div.campaign-summary').text
        except:
            summary = 'None'

        # 펀딩금액, 펀딩기간
        try:
            goal_amount = driver.find_element_by_css_selector('div.wd-ui-campaign-content > div > div:nth-child(4) p').text
        except:
            goal_amount = 'no info'

        # 새소식 포스팅 개수
        try:
            new_news = driver.find_element_by_css_selector('ul.tab-list li:nth-of-type(4) span').text
        except:
            new_news = 0

        # 새소식 포스팅 내 댓글 개수
        try:
            comment_num = driver.find_element_by_css_selector('ul.tab-list li:nth-of-type(5) span').text
        except:
            comment_num = 0

        # 리워드 상품 종류 개수
        try:
            reward_num = len(driver.find_elements_by_css_selector('button.rightinfo-reward-list'))
        except:
            reward_num = 0

        # 소개글 이미지 개수
        try:
            img_num = len(driver.find_elements_by_css_selector('div.inner-contents.fr-view img'))
        except:
            img_num = 0

        # 소개글 비디오 개수
        try:
            video_num = len(driver.find_elements_by_css_selector('span.fr-video.fr-fvc.fr-dvb.fr-draggable'))
            print(video_num)
        except:
            video_num = 0
            print(video_num)


        # 펀딩 안내 페이지 접속
        funding_info_btn = driver.find_element_by_css_selector('ul.tab-list li:nth-of-type(3) a')
        funding_info_btn.click()

        # 리워드 발송 시작일
        try:
            delivery_date = driver.find_element_by_css_selector('div#detail-funding-info div.content h3 em').text
        except:
            delivery_date = 'no info'

        # 커뮤니티
        community_btn = driver.find_element_by_css_selector('ul.tab-list li:nth-of-type(5) a')
        community_btn.click()

        # 인스타그램 정보 수집 (new tab)
        try:
            instagram = driver.find_element_by_css_selector('ul.social a.instagram')
            instagram_url = instagram.get_attribute('href')

            driver.execute_script("window.open('');")
            time.sleep(1.5)

            driver.switch_to.window(driver.window_handles[2])
            driver.get(instagram_url)
            time.sleep(1.5)
            try:
                # 팔로워 수 (Instagram)
                sns_followers = driver.find_element_by_css_selector('ul.k9GMp  li:nth-of-type(2)  span.g47SY').text
            except:
                # 프로필 페이지 미존재 시 예외처리
                sns_followers = 'link error'

            driver.close()
            time.sleep(1.5)

            driver.switch_to.window(driver.window_handles[1])
        except:
            sns_followers = 'no account'

        time.sleep(1.5)

        # (메이커) 프로필 페이지 (new tab)
        maker_profile = driver.find_element_by_css_selector('div.maker-info button')
        maker_profile.click()

        time.sleep(1.5)

        # (메이커) 와디즈 내 팔로워 수
        try:
            wadiz_followers = driver.find_element_by_css_selector('ul.activity-list li:nth-of-type(3) strong').text
        except:
            wadiz_followers = 0

        # (메이커) 과거 리워드 프로젝트 수
        try:
            past_projects_num = len(driver.find_elements_by_css_selector('li.all em.project-type.reward'))-1
        except:
            past_projects_num = 0

        # (메이커) 펀딩 성공 프로젝트 수
        try:
            past_projects = driver.find_elements_by_css_selector('li.all span.percent')
            n = 0
            for past in past_projects:
                if int(past.text.replace('%', '')) >= 100:
                    n += 1
            past_success_projects_num = n
        except:
            past_success_projects_num = 0


        sheet.append([project_url, name, category, maker, percent, money, supporters, likes, summary, goal_amount, 
                    new_news, comment_num, reward_num, img_num, video_num, delivery_date, sns_followers, wadiz_followers, 
                    past_projects_num, past_success_projects_num
                    ])


        # 세부 페이지 탭 닫기
        driver.close()
        time.sleep(1.5)

        # 원래 탭(전체 목록 페이지)로 돌아가기 이동
        driver.switch_to.window(driver.window_handles[0])

        count += 1

        fileName = 'wadiz{index}{ext}'.format(index=idx, ext='.xlsx')
        wb.save(fileName)
        idx += 1

    # 크롬드라이버 종료
    driver.close()

    print('Finished Scraping !!!')

    # 수집 파일 저장
    wb.save(file_path)
    return file_path

def scrap_navernews(config:Dict[Dict[str:str]]) -> str:

    """
    [summary]
        키워드(쿼리) 검색결과에 해당되는 네이버 뉴스 수집

    [Args]:
        config (Dict[Dict]): 뉴스기사 수집범위에 해당하는 시작일자, 종료일자, 키워드, 저장파일경로에 대한 key-value 가진 Dict

    [Returns]:
        str: 저장된 파일경로 return
    """

    wb = openpyxl.Workbook()
    sheet = wb.active

    sheet.append(['키워드', '날짜', '기사제목'])

    start_date:str = config['NEWS']['start_date']    # 시작일자
    end_date:str = config['NEWS']['end_date']        # 종료일자
    keyword:str = config['NEWS']['news_keyword']     # 검색 쿼리(키워드)
    file_path:str = config['NEWS']['news_file_path'] # 저장 파일 경로
    max_num:int = config['NEWS']['max_num']          # 최대 기사 개수

    # headless 크롬드라이버 실행
    options = ChromeOptions()
    options.add_argument('headless')
    driver = Chrome('./chromedriver', options=options)

    # 페이지별 뉴스기사 수집 (1페이지당 10개)
    for n in range(1, max_num, 10):
        driver.get(f'https://search.naver.com/search.naver?&where=news&query={keyword}&sm=tab_pge&sort=1&photo=0&field=0&reporter_article=&pd=3&ds={start_date}&de={end_date}&docid=&nso=so:dd,p:from20190601to20190814,a:all&mynews=0&start='+str(n)+'&refresh_start=0')
        articles = driver.find_elements_by_css_selector('ul.type01>li')

        for a in articles:

            # 제목
            title = a.find_element_by_css_selector("a._sp_each_title").text

            # 날짜
            date = a.find_element_by_css_selector("dd.txt_inline").text

            print(title)
            sheet.append([keyword, date, title])

            # 연관 기사 존재
            if check_exists_by_css_selector(driver, 'ul.type01>li dl dd:nth-of-type(3)') == True:

                # 연관기사 다수 - "더보기" 클릭 후 연관기사 제목 수집
                try:
                    more_button = a.find_element_by_css_selector('ul.type01>li div.newr_more').text
                    num_of_more_articles = re.search(r'(\d+)', more_button)
                    for _ in range(int(num_of_more_articles.group(1))):
                        sheet.append([keyword, date, '[연관기사]'+title])
                        print('similar articles')

                # 연관기사 소수 - 연관기사 제목 수집
                except:
                    related_articles = a.find_elements_by_css_selector('ul.type01>li ul.relation_lst li')
                    for r in related_articles:
                        related_articles_title = r.find_element_by_css_selector('ul.type01>li ul.relation_lst li a').text
                        related_articles_date = r.find_element_by_css_selector('ul.type01>li ul.relation_lst li span.txt_sinfo').text

                        print(related_articles_title)
                        sheet.append([keyword, related_articles_date, related_articles_title])

    print('Finished Scraping !!!')

    # 수집 파일 저장
    wb.save(file_path)
    return file_path

def main(args:Dict) -> str:

    """
    [summary]
        목적에 따른 크롤링 함수 실행

    Args:
        args (Dict): to_scrap 속성값이 'wadiz'인 경우 wadiz 크롤링 수행,
                     'navernews' 인 경우 news 크롤링 수행,
                     'all' 인 경우 모두 수행

    Returns:
        str: 저장된 파일경로 return, 'all'인 경우 두개를 합친 하나의 문자열 출력
    """
    
    config = load_yaml('config.yaml')

    # wadiz 프로젝트 정보 수집
    if args.to_scrap == 'wadiz':
        saved_fname = scrap_wadiz(config)

    # '크라우드 펀딩' 검색 결과 관련 네이버 뉴스 수집
    elif args.to_scrap == 'navernews':
        saved_fname = scrap_navernews(config)

    # wadiz, navernews 수집 모두 수행
    elif args.to_scrap == 'all':
        saved_fname1 = scrap_wadiz(config)
        saved_fname2 = scrap_navernews(config)
        saved_fname = saved_fname1 + ', ' + saved_fname2

    return saved_fname

if __name__ == '__main__':
    
    # 실행 대상 함수 input
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--to_scrap', help="input 'wadiz' or 'navernews' or 'all'", type=str, default='wadiz')
    args = parser.parse_args()

    # 함수 실행
    main(args)