from datetime import datetime, timedelta
from loguru import logger
import numpy as np
import pandas as pd
import time 
from channel.twitter import Twitter

if __name__ == "__main__" :
    keyword = 'class101'
    startdate = datetime.strftime(datetime.now(),'%Y-%m-%d')
    enddate = datetime.strftime(datetime.now()+timedelta(days=1),'%Y-%m-%d')
    companyCode = 99999    
    twitter = Twitter()
    twitter.Twitter_Crawl(keyword, startdate, enddate, companyCode)