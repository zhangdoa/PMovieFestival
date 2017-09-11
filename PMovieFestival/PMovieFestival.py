__author__ = 'zhangdoa'

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re

class MovieFestival:

    def __init__(self):
        self.FestivalTitle = '柏林国际电影节'
        self.AwardTitle = ['最佳影片', '金熊奖']
        self.DoubanURL = 'https://movie.douban.com/awards/berlinale/'

    def writeToFile(self, fileLocation, data):
        with (open(fileLocation + self.FestivalTitle + '.txt', 'a', encoding="utf-8-sig")) as m:
            m.write(data)
            m.write(u"\r\n")

    def getSingleYearUrl(self, year, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        print('正在抓取' + self.FestivalTitle + str(year) + self.AwardTitle[0])
        for mod in soup.find_all(class_ = 'mod'):
            for dt in mod.find_all('dt'):
                for string in dt.stripped_strings:
                    if string in self.AwardTitle:
                        for link in (dt.next_sibling.next_sibling).find_all('a'):
                            self.writeToFile('D:/', self.FestivalTitle + "||" + str(year) + '||' + self.AwardTitle[0] + '||' + link.string + '||' + link.get('href') + '||')
        print('抓取完成\n') 
        
    def getAllYearsUrl(self):
        #柏林电影节第一届网页有问题，没有历届回顾，需要加偏移值
        URL = self.DoubanURL + str(1) + '/'
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
        res = requests.get(URL)
        soup = BeautifulSoup(res.text, 'html.parser')
        for ya in soup.find_all(id='year_awards'):
            for ul in ya.find_all('ul'):
                for li in ul.find_all('li'):
                    self.getSingleYearUrl(int(li.a.string), li.a.get('href'))
                    time.sleep(1.5)

    def main(self):
        self.getAllYearsUrl()
        
class DummyBrowser:
    def __init__(self):
        self.browser = webdriver.Chrome('/path/to/chromedriver')
    def main(self):
        self.browser.get('http://www.douban.com/')
        driver = webdriver.Chrome('/path/to/chromedriver')  # Optional argument, if not specified will search path.
        driver.get('http://www.google.com/xhtml');
        time.sleep(5) # Let the user actually see something!
        search_box = driver.find_element_by_name('q')
        search_box.send_keys('ChromeDriver')
        search_box.submit()
        time.sleep(5) # Let the user actually see something!
        driver.quit()


#Berlin = MovieFestival()
#Berlin.main()

#Venice = MovieFestival()
#Venice.FestivalTitle = '威尼斯电影节'
#Venice.AwardTitle = ['金狮奖']
#Venice.DoubanURL = 'https://movie.douban.com/awards/venice/'
#Venice.main()

#Cannes = MovieFestival()
#Cannes.FestivalTitle = '戛纳电影节'
#Cannes.AwardTitle = ['金棕榈奖']
#Cannes.DoubanURL = 'https://movie.douban.com/awards/cannes/'
#Cannes.main()

dummyHand = DummyBrowser()
