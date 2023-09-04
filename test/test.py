# from bs4 import BeautifulSoup
# from database.mssql_helper import MSSQLConnector
# import re
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# from webdriver_manager.chrome import ChromeDriverManager
import pymysql

def dbconnect():
    juso_db = pymysql.connect(
                    host='host',
                    user='id',
                    port='portnumber',
                    password="pw",
                    database="dbname",
                    autocommit=True
    )

    cursor = juso_db.cursor(pymysql.cursors.DictCursor)


def Login_Twitter(driver, login_id, login_pw):
    try:
        login_result = True
        login_url = 'https://twitter.com/login?lang=ko'
        driver.get(login_url)
        time.sleep(10)

        id_element = driver.find_element(By.NAME, "text")
        id_element.send_keys(f'{login_id}')
        time.sleep(5)
        id_element.send_keys(Keys.ENTER)
        time.sleep(5)

        pw_element = driver.find_element(By.NAME, "password")
        pw_element.send_keys(f'{login_pw}')
        time.sleep(3)
        pw_element.send_keys(Keys.ENTER)
        time.sleep(10)
    except Exception as e:
        login_result = False      

    return login_result    

def Crawl_Twitter(driver):
    try:
        keyword = 'iphone'
        startdate = '2023-01-01'
        enddate = '2023-07-21'
        companyCode = 99999
        result = True
        login_result = Login_Twitter(driver, id, pw)
        if not login_result:
            raise Exception("로그인 실패")

        page_url = f"https://twitter.com/search?q={keyword}since:{startdate}until:{enddate}&src=typd&f=live&vertical=default"
        driver.get(page_url)
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source,'html.parser')

        no_div = soup.find_all('div',{'class':'css-1dbjc4n'})
        for div in no_div:
            if (div.text == 'No results' or '대한 검색 결과 없음' in div.text):
                result = False
                break
        
        while(result):
            divs = soup.find_all('div',{'data-testid':'cellInnerDiv'})
            if len(divs) > 0:
                for div in divs:
                    writer     = div.find('a', {'class':'css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1wbh5a2 r-dnmrzs r-1ny4l3l'})['href'][1:]
                    url        = 'https://twitter.com' + div.find('div',{'class':'css-1dbjc4n r-18u37iz r-1q142lx'}).find('a')['href']
                    temp_contents   = div.find('div',{'dir':'auto'}).text.strip()
                    contents   = re.sub('#[A-Za-z0-9가-힣]+', '', temp_contents).strip().replace('\n',' ')
                    hashtags   = ' '.join(re.findall('#[A-Za-z0-9가-힣]+', temp_contents))
                    title      = contents[:20] + "...."
                    wrtieTime  = div.find('div',{'class':'css-1dbjc4n r-18u37iz r-1q142lx'}).find('time')['datetime']
                    count_div  = div.find('div', {'role':'group'})
                    imgUrl = ''
                    isImg = div.find('img')
                    if isImg:
                        imgUrl = isImg['src'].strip()
                    OgDescription = title
                    AnalysisFlag = 'N'      
                    ImgFlag = 'N'
                    CompanyCode = companyCode
                    AutoCrawlFlag = 'Y'            

                    # 찾아서 추가
                    cmtCount   = 0
                    viewCount  = 0
                    likeCount  = 0
                    reqCount   = 0
                    shareCount = 0   
                    if contents != '':
                        query = f'''
                            INSERT INTO tbScrapData (ContentType, Sno, PostNo, ChannelCode, SearchKeyWord, Url, Title, Writer, WriteTime, Contents, RegDate, ViewCount, CmtCount, SymCount, RepCount, ShareCount, HashTag, AnalysisFlag, SubUrl, Og_ImageUrl, Og_Description, ImgFlag, CompanyCode, AutoCrawlFlag)
                            VALUES ('P', 0, 0, 4001, '{keyword}', '{url}', '{title}', '{writer}', '{wrtieTime}', '{contents}', CURRENT_TIMESTAMP, {viewCount}, {cmtCount}, {likeCount}, {reqCount}, {shareCount}, '{hashtags}', '{AnalysisFlag}', '', '{imgUrl}', '{OgDescription}', 'N', 'N', {companyCode}, '{AutoCrawlFlag}')
                        '''
                        MSSQLConnector.insert(query)


    except Exception as e:
        print(e)
        

if __name__ == "__main__" :
    try:
        dbconnect()
        # options = Options()
        # options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.49 Safari/537.3')
        # # options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        # driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        # Crawl_Twitter(driver)
    except Exception as e:
        print(e)