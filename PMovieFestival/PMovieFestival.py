# coding:utf-8
__author__ = 'zhangdoa'
import requests
from bs4 import BeautifulSoup
import time
import re

class MovieFestival:

    def __init__(self):
        self.getAll = False
        self.FestivalTitle = '柏林国际电影节'
        self.AwardTitle = ['最佳影片', '金熊奖']
        self.DoubanURL = 'https://movie.douban.com/awards/berlinale/'
        self.FirstYear = 1951
        self.LastYear = 2017
        self.StartYear = self.FirstYear
        self.EndYear = self.LastYear
        self.LeakYear = []
        self.LeakYearOffset = 0
        self.MovieInfo = []

    def getSingleUrl(self, year):
        self.LeakYearOffset = 0
        if year in self.LeakYear:
            print(str(year) + '年未举办' + self.FestivalTitle + '\n')
            return
        for i in self.LeakYear:
            if year > i:
                self.LeakYearOffset+=1
        URL = self.DoubanURL + str(year - self.FirstYear - self.LeakYearOffset + 1) + '/'
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
        res = requests.get(URL)
        soup = BeautifulSoup(res.text, 'html.parser')
        print('正在抓取' + self.FestivalTitle + '(' + str(year - self.FirstYear - self.LeakYearOffset + 1) + ')' + str(year) + self.AwardTitle[0] + 'URL...')
        for mod in soup.find_all(class_ = 'mod'):
            for dt in mod.find_all('dt'):
                for string in dt.stripped_strings:
                    if string in self.AwardTitle:
                        for link in (dt.next_sibling.next_sibling).find_all('a'):
                            self.MovieInfo.append(self.FestivalTitle + "||" + str(year - self.FirstYear - self.LeakYearOffset + 1) + '||' + self.AwardTitle[0] + '||' + link.string + '||' + link.get('href') + '\n')                          
                            print(link.get('href'))
        print('抓取完成\n') 
        
    def getAllUrl(self):
        URL = self.DoubanURL + str(1) + '/'
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
        res = requests.get(URL)
        soup = BeautifulSoup(res.text, 'html.parser')
        for ya in soup.find_all(id='year_awards'):
            for ul in ya.find_all('ul'):
                for li in ul.find_all('li'):
                    self.getSingleUrl(int(li.a.string))
                    time.sleep(1.75)

    def getUrlInRange(self, StartYear, EndYear):
        for x in range(StartYear, EndYear + 1):
            self.getSingleUrl(x)  
            time.sleep(1.75)

    def main(self):
        if self.getAll:
            self.getAllUrl()
            return
        else:
            self.getUrlInRange(self.StartYear, self.EndYear)
            return

Berlin = MovieFestival()
Berlin.StartYear = 2015
Berlin.main()

Venice = MovieFestival()
Venice.FestivalTitle = '威尼斯电影节'
Venice.AwardTitle = ['金狮奖']
Venice.DoubanURL = 'https://movie.douban.com/awards/venice'
Venice.FirstYear = 1932
Venice.LeakYear = [1933, 1943, 1944, 1945]#@TODO
Venice.getAll = True
Venice.main()

Cannes = MovieFestival()
Cannes.FestivalTitle = '戛纳电影节'
Cannes.AwardTitle = ['金棕榈奖']
Cannes.DoubanURL = 'https://movie.douban.com/awards/cannes/'
Cannes.FirstYear = 1946
Cannes.LeakYear = [1948, 1950]
Cannes.getAll = True
Cannes.main()

