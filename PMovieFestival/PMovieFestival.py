__author__ = 'zhangdoa'

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re

class MovieFestivalSpider:

    def __init__(self):
        self.URL = 'https://movie.douban.com/awards/'

    def writeToFile(self, fileLocation, data):
        with (open(fileLocation + '.txt', 'a', encoding="utf-8-sig")) as m:
            for i in data:
                m.write(i)

    def getSingleYearUrl(self, url, movieFestivalCodeName, result):
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        sectionTags = soup.find_all('div', class_="info")
        festivalTitle = "DefaultFestivalTitle"
        for sectionTag in sectionTags:
            festivalTitle = sectionTag.h1.get_text().strip()
            festivalTitle = festivalTitle.split("(")[0].strip()
            print('正在抓取' + festivalTitle)
        awardLists = soup.find_all('div', class_="section award_list")
        for awardList in awardLists:
            awards = awardList.find_all('div', class_="mod")
            for award in awards:
                if award.find_all('h4'):
                    awardTitle = award.find_all('h4')[0].get_text().strip()
                else:
                    awardTitle = "- 其他 / Others -"
                datas = award.find_all('ul')
                for data in datas:
                    if data.find_all('li'):
                        subAwardTitle = data.find_all('li')[0].find_all('dt')[0].get_text().strip()
                        movieTitle = "《" + data.find_all('li')[0].find_all('a')[0].get_text() + "》"
                        link = data.find_all('li')[0].find_all('a')[0]['href'].strip()
                        result.append(festivalTitle + "||" + awardTitle + "||" + subAwardTitle + '||' + movieTitle  + '||' + link + '||' + u"\r\n")
        print(festivalTitle + '抓取完成') 
        
    def getAllYearsUrl(self, movieFestivalCodeName, savePath):
        result = []
        i = 1
        URL = self.URL + movieFestivalCodeName + '/' + str(i) + "/"
        res = requests.get(URL)
        while res:
            self.getSingleYearUrl(URL, movieFestivalCodeName, result)
            i = i + 1
            time.sleep(0.1)
            URL = self.URL + movieFestivalCodeName + '/' + str(i) + "/"
            res = requests.get(URL)
        self.writeToFile(savePath + movieFestivalCodeName, result)                      
        
    def main(self, movieFestivalCodeName, savePath):
        self.getAllYearsUrl(movieFestivalCodeName, savePath)
        
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


Berlin = MovieFestivalSpider()
Berlin.main("berlinale", 'D:/')

Venice = MovieFestivalSpider()
Venice.main("venice", 'D:/')

Cannes = MovieFestivalSpider()
Cannes.main("cannes", 'D:/')

#dummyHand = DummyBrowser()
