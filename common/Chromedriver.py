import os
import re
import json
import zipfile
import requests
from bs4 import BeautifulSoup

class ChromeDriver():
    def __init__(self) -> None:
        print()
        
    def Check_Current_Chrome_version(self):
        try:
            url = 'https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json'
            req = requests.get(url)
            result = json.loads(req.text)
            self.current_version = result['channels']['Stable']['version']
            current_version_download_links = result['channels']['Stable']['downloads']['chromedriver']
            for link in current_version_download_links:
                if link['platform'] == 'win32':
                    self.link = link['url']
                    break
        except Exception as e:
            print(e)

    def Download_Stable_Chrome_Version(self):
        try:
            url = 'https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json'
            req = requests.get(url)
            result = json.loads(req.text)
            chrome_versions = result['versions']
            for version in chrome_versions:
                try:
                    if version['version'] == self.current_version:
                        self.versions = version['downloads']['chromedriver']
                        break
                except Exception as e:
                    print(e)
            for version in self.versions:
                try:
                    if version['platform'] == 'win32':
                        self.download_link = version['url']
                        break
                except Exception as e:
                    print(e)
            # 드라이버를 저장할 파일 경로
            self.driver_filename = "chromedriver_win32.zip"  # 저장할 파일명
            self.driver_path = f'D:\\0_mckim\\TIL2\\crawler\\chrome_version'  # 실제 저장할 경로로 수정

            
            if self.Check_Folder_Exist():
                # 드라이버 다운로드 및 저장
                response = requests.get(self.download_link)       
                with open(self.driver_path+'\\'+self.current_version+'\\'+self.driver_filename, "wb") as driver_file:
                    driver_file.write(response.content)        
        except Exception as e:
            print(e)

    def Decompress_Chrome_Driver(self):
        try:
            self.Check_Current_Chrome_version()
            self.Download_Stable_Chrome_Version()
            zipfile.ZipFile(self.driver_path+'\\'+self.current_version+'\\'+self.driver_filename).extractall(self.driver_path+'\\'+self.current_version)
        except Exception as e:
            print(e)

    def Check_Folder_Exist(self):
        result = True
        try:
            if not os.path.exists(self.driver_path+'\\'+self.current_version):
                os.makedirs(self.driver_path+'\\'+self.current_version)
        except Exception as e:
            result = False
            print(e)
        return result            

# if __name__  == '__main__':
#     c = Chromedriver()
#     c.Check_Current_Chrome_version()
#     c.Download_Stable_Chrome_Version()
#     c.Decompress_Chrome_Driver()
