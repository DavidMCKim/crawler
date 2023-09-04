import requests
import re
import time
import json
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from common.Chromedriver import ChromeDriver
from selenium.webdriver.common.keys import Keys
from database.mssql_helper import MSSQLConnector
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

import time

class Twitter():
    def __init__(self) -> None:
        self.db = MSSQLConnector()        
        chromedriver = ChromeDriver()
        chromedriver.Decompress_Chrome_Driver()
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument('headless')
        self.options.add_argument('disable-gpu')
        chrome_path = f'{chromedriver.driver_path}\{chromedriver.current_version}\chromedriver-win32\chromedriver.exe'
        self.driver = webdriver.Chrome(executable_path=chrome_path)
    
    def Twitter_Crawl(self, keyword, startdate, enddate, companyCode):
        try:
            result = True
            login_result = self.Login_Twitter('id','pw')
            if not login_result:
                raise Exception("로그인 실패")
            
            page_url = f"https://twitter.com/search?q={keyword}since:{startdate}until:{enddate}&src=typd&f=live&vertical=default"
            

            self.driver.get(page_url)
            time.sleep(5)

            soup = BeautifulSoup(self.driver.page_source,'html.parser')

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
                        writeTime  = datetime.strftime(datetime.strptime(div.find('div',{'class':'css-1dbjc4n r-18u37iz r-1q142lx'}).find('time')['datetime'].replace('T',' ').replace('Z','').replace('.000',''),'%Y-%m-%d %H:%M:%S')+timedelta(hours=9),'%Y-%m-%d %H:%M:%S')
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

                            '''
                            self.db.insert(query)
        except Exception as e:
            print(e)

    def Login_Twitter(self, login_id, login_pw):
        try:
            login_result = True
            login_url = 'https://twitter.com/login?lang=ko'
            self.driver.get(login_url)
            time.sleep(10)

            id_element = self.driver.find_element(By.NAME, "text")
            id_element.send_keys(f'{login_id}')
            time.sleep(5)
            id_element.send_keys(Keys.ENTER)
            time.sleep(5)

            pw_element = self.driver.find_element(By.NAME, "password")
            pw_element.send_keys(f'{login_pw}')
            time.sleep(3)
            pw_element.send_keys(Keys.ENTER)
            time.sleep(10)
        except Exception as e:
            login_result = False      

        return login_result        