import time
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import openpyxl

def scrap_wadiz(fname = 'wadiz.xlsx'):
    """ scrap project info in Wadiz

    Keyword arguments:
    fname -- file name to save (xlsx)

    return : saved filename (.xlsx)
    """
    wb = openpyxl.Workbook()
    sheet = wb.active

    sheet.append(['url', '제목', '카테고리', '메이커', '달성률', '달성액', '서포터수', '좋아요수', '요약글', '목표금액과기간', '글업데이트수', '댓글수', \
                  '리워드종류수', '이미지수', '비디오수', '배송시작날짜', '인스타팔로워수', '와디즈팔로워수', '과거프로젝트수', '과거성공프로젝트수'])

    driver = webdriver.Chrome('./chromedriver')

    # login
    login_link = 'https://www.wadiz.kr/web/waccount/wAccountLogin?returnUrl=https://www.wadiz.kr/web/main'
    driver.get(login_link)
    id = driver.find_element_by_css_selector('input#userName')
    id.send_keys('') # input e-mail
    pw = driver.find_element_by_css_selector('input#password')
    pw.send_keys('') # input password
    login_btn = driver.find_element_by_css_selector('button#btnLogin')
    login_btn.click()

    time.sleep(1.5)

    # project lists (recent -> old)
    base_link = 'https://www.wadiz.kr/web/wreward/category/308?keyword=&endYn=Y&order=closing'
    driver.get(base_link)
    driver.maximize_window()

    time.sleep(1)


    # scroll down
    while True:
        try:
            target = driver.find_element_by_css_selector('button.ProjectListMoreButton_button__27eTb')
            actions = ActionChains(driver)
            actions.move_to_element(target)
            actions.perform()
            time.sleep(2)
        except:
            break


    # container of projects
    projects = driver.find_elements_by_css_selector('div.ProjectCardList_item__1owJa')

    count = 1
    idx = 0

    for p in projects:

        print(count)

        image = p.find_element_by_css_selector('a.ProjectCardLink_link__2X36I.CommonProjectCard_image__1aEog')

        try:
            name = p.find_element_by_css_selector('p.CommonProjectCard_title__28lHZ.RewardProjectCard_title__RDEBu').text
        except:
            name = 'no info'

        try:
            category = p.find_element_by_css_selector('span.RewardProjectCard_category__1vo_V').text
        except:
            category = 'no info'

        try:
            maker = p.find_element_by_css_selector('span.RewardProjectCard_makerName__2sITk').text
        except:
            maker = 'no info'

        try:
            percent = p.find_element_by_css_selector('span.RewardProjectCard_percent__edRT9').text.replace('%', '')
        except:
            percent = 'no info'

        try:
            money = p.find_element_by_css_selector('span.RewardProjectCard_amount__2GV5X').text.replace(',', '')
        except:
            money = 'no info'

        print(name)


        # project main page (new tab)
        project_url = image.get_attribute('href')

        driver.execute_script("window.open('');")
        time.sleep(1.5)


        # move focus in chrome (new tab)
        driver.switch_to.window(driver.window_handles[1])
        driver.get(project_url)
        time.sleep(1.5)

        # supporters-num
        try:
            supporters = driver.find_element_by_css_selector('p.total-supporter strong').text
        except:
            supporters = 0

        # likes
        try:
            likes = driver.find_element_by_css_selector('em.cnt-like').text
        except:
            likes = 0

        # summary text
        try:
            summary = driver.find_element_by_css_selector('div.campaign-summary').text
        except:
            summary = 'None'

        # amount of funding and period
        try:
            goal_amount = driver.find_element_by_css_selector('div.wd-ui-campaign-content > div > div:nth-child(4) p').text
        except:
            goal_amount = 'no info'

        # updated-postings-num
        try:
            new_news = driver.find_element_by_css_selector('ul.tab-list li:nth-of-type(4) span').text
        except:
            new_news = 0

        # comments-num (community-posting-nums)
        try:
            comment_num = driver.find_element_by_css_selector('ul.tab-list li:nth-of-type(5) span').text
        except:
            comment_num = 0

        # rewards-num
        try:
            reward_num = len(driver.find_elements_by_css_selector('button.rightinfo-reward-list'))
        except:
            reward_num = 0

        # intro image-num
        try:
            img_num = len(driver.find_elements_by_css_selector('div.inner-contents.fr-view img'))
        except:
            img_num = 0

        # intro video-num
        try:
            video_num = len(driver.find_elements_by_css_selector('span.fr-video.fr-fvc.fr-dvb.fr-draggable'))
            print(video_num)
        except:
            video_num = 0
            print(video_num)



        # main page of funding
        funding_info_btn = driver.find_element_by_css_selector('ul.tab-list li:nth-of-type(3) a')
        funding_info_btn.click()

        # start date of delievery
        try:
            delivery_date = driver.find_element_by_css_selector('div#detail-funding-info div.content h3 em').text
        except:
            deliver_date = 'no info'

        # community
        community_btn = driver.find_element_by_css_selector('ul.tab-list li:nth-of-type(5) a')
        community_btn.click()

        # comments (X)

        # Instagram (new tab)
        try:
            instagram = driver.find_element_by_css_selector('ul.social a.instagram')
            instagram_url = instagram.get_attribute('href')

            driver.execute_script("window.open('');")
            time.sleep(1.5)

            driver.switch_to.window(driver.window_handles[2])
            driver.get(instagram_url)
            time.sleep(1.5)
            try:
                # follower-num (Instagram)
                sns_followers = driver.find_element_by_css_selector('ul.k9GMp  li:nth-of-type(2)  span.g47SY').text
            except:
                # profile deleted, link error
                sns_followers = 'link error'

            driver.close()
            time.sleep(1.5)

            driver.switch_to.window(driver.window_handles[1])
        except:
            sns_followers = 'no account'

        time.sleep(1.5)


        # maker profile page (new tab)
        maker_profile = driver.find_element_by_css_selector('div.maker-info button')
        maker_profile.click()

        time.sleep(1.5)

        # follower-num in wadiz
        try:
            wadiz_followers = driver.find_element_by_css_selector('ul.activity-list li:nth-of-type(3) strong').text
        except:
            wadiz_followers = 0

        # reward project-num in the past
        try:
            past_projects_num = len(driver.find_elements_by_css_selector('li.all em.project-type.reward'))-1
        except:
            past_projects_num = 0

        # succeeded project-num so far
        try:
            past_projects = driver.find_elements_by_css_selector('li.all span.percent')
            n = 0
            for past in past_projects:
                if int(past.text.replace('%', '')) >= 100:
                    n += 1
            past_success_projects_num = n
        except:
            past_success_projects_num = 0


        sheet.append([project_url, name, category, maker, percent, money, supporters, likes, summary, goal_amount, new_news, comment_num,\
                      reward_num, img_num, video_num, delivery_date, sns_followers, wadiz_followers, past_projects_num, \
                      past_success_projects_num])


        # close detail-page tab
        driver.close()
        time.sleep(1.5)

        # back to initial tab
        driver.switch_to.window(driver.window_handles[0])

        count += 1

        fileName = 'Wadiz1{index}{ext}'.format(index=idx, ext='.xlsx')
        wb.save(fileName)
        idx += 1

    driver.close()

    print('finish scraping')

    wb.save(fname)
    return fname

def scrap_navernews(keyword: str = '크라우드펀딩'):
    """ scrap naver news with specific keyword

    Keyword arguments:
    keyword -- search keyword in naver news

    return : saved filename (.xlsx)
    """

    wb = openpyxl.Workbook()
    sheet = wb.active

    sheet.append(['키워드', '날짜', '기사제목'])

    keyword = '크라우드펀딩'

    # headless chromedriver
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    driver = webdriver.Chrome('./chromedriver', options=options)

    # max_num of articles scrapped
    max = 3999

    def check_exists_by_css_selector(css_selector):
        try:
            driver.find_element_by_css_selector(css_selector)
        except:
            return False
        return True

    for n in range(1, max, 10):
        driver.get('https://search.naver.com/search.naver?&where=news&query=크라우드펀딩&sm=tab_pge&sort=1&photo=0&field=0&reporter_article=&pd=3&ds=2019.06.01&de=2019.08.14&docid=&nso=so:dd,p:from20190601to20190814,a:all&mynews=0&start='+str(n)+'&refresh_start=0')
        articles = driver.find_elements_by_css_selector('ul.type01>li')

        for a in articles:
            # title
            title = a.find_element_by_css_selector("a._sp_each_title").text
            # date
            date = a.find_element_by_css_selector("dd.txt_inline").text

            print(title)
            sheet.append([keyword, date, title])

            # similar articles
            if check_exists_by_css_selector('ul.type01>li dl dd:nth-of-type(3)') == True:
                # see more button
                try:
                    more_button = a.find_element_by_css_selector('ul.type01>li div.newr_more').text
                    num_of_more_articles = re.search(r'(\d+)', more_button)
                    for _ in range(int(num_of_more_articles.group(1))):
                        sheet.append([keyword, date, '[연관기사]'+title])
                        print('similar articles')

                # few similar articles
                except:
                    related_articles = a.find_elements_by_css_selector('ul.type01>li ul.relation_lst li')
                    for r in related_articles:
                        related_articles_title = r.find_element_by_css_selector('ul.type01>li ul.relation_lst li a').text
                        related_articles_date = r.find_element_by_css_selector('ul.type01>li ul.relation_lst li span.txt_sinfo').text

                        print(related_articles_title)
                        sheet.append([keyword, related_articles_date, related_articles_title])

    print('finish scrapping!')
    fname = "navernews_{}.xlsx".format(keyword)
    wb.save(fname)
    return fname