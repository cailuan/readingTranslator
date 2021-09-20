from multiprocessing import Process, Queue
import os, time, random
import requests
from bs4 import BeautifulSoup
from lxml import etree
import pyttsx3
from selenium import webdriver
import re

headers={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'Hm_lvt_6dfe3c8f195b43b8e667a2a2e5936122=1605023049; Hm_lpvt_6dfe3c8f195b43b8e667a2a2e5936122=1606913785',
    'Host': 'www.biquge.info',
    'Referer': 'http://www.biquge.info/10_10240/5018707.html?zkvmpc=1etsd3',
    'Upgrade-Insecure-Requests': '1',
    'Pragma': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
}

globalError  = False


class readFiles():
    def __init__(self,q,count):
        self.q =q
        self.count = count
        print('初始化')

    def writeFile(self, fileName, content):
        with open(fileName, 'w') as f:
            f.write(content)

    def readFile(self, fileName):
        print('读取文件')
        with open(fileName, 'r') as f:
            self.currentUrl = f.read()
            return self.currentUrl

    def downQuests(self, url):
        print('下载文件')
        # self.readFile(content)
        try:
            # resp = requests.get(url,headers=headers)
            # resp.encoding = 'utf-8'
            # # print(resp.text)
            # self.resText = resp.text
            # print(self.resText,'self.resText')
            # return resp.text
            opt = webdriver.ChromeOptions()
            driver = webdriver.Chrome(options=opt)
            driver.get(url)
            print(driver.page_source)
            self.resText = driver.page_source
            driver.close()
            return  driver.page_source
        except BaseException:
            print(BaseException)
            return 'error'

    def parseTree(self):
        # print(self.resText)
        tree = etree.HTML(self.resText)

        if tree.xpath('//title/text()') and tree.xpath('//title/text()')[0] == '503 Service Temporarily Unavailable':
            print('出错了，从新加载！')
            self.downQuests(self.currentUrl)
            self.parseTree()
        else:
            soup = BeautifulSoup(self.resText, 'lxml')
            temStr = ''
            print(soup,'soup')
            for i in soup.find("div", class_="bottem1").contents:
                if(i.string == "下一章"):
                    if 'http://www.biquge.se' in i["href"] or 'http://www.biquge.info' in i["href"] :
                        self.newUrl =  i["href"]
                    else:
                        self.newUrl = 'http://www.biquge.se' + i['href']

            for child in soup.find(id="content").stripped_strings:
                temStr += child
            title = tree.xpath("//div[@class='bookname']/h1/text()")[0]
            return (temStr,title,self.newUrl)

    def updateUrl(self):
        self.writeFile('url.txt', self.newUrl)

    def updateCurrent(self,url):
        self.currentUrl = url

# 写数据进程执行的代码:
def write(q,count,target = 'file'):
    print('write')
    rf =  readFiles(q,count)
    if target == 'file':
        fdu = rf.readFile('url.txt')
        cu = rf.readFile('current.txt')
        du = fdu if fdu == cu else cu
    else:
        du = target
    rf.downQuests(du)
    returnStr,title,targeUrl = rf.parseTree()
    count -=1
    q.put({'content':returnStr,'title':title,'url':targeUrl})
    # print('Process to write: %s' % os.getpid())
    print(targeUrl)
    time.sleep(20)
    if count > 0 and targeUrl:
        write(q, count, target=targeUrl)
    else:
        rf.writeFile('url.txt',targeUrl)

# 读数据进程执行的代码:
def read(q,count):
    print('Process to read: %s' % os.getpid())
    temCount = 0
    while True:
        print('read')
        if globalError == True and q.empty():
            break
        temCount += 1
        rfs = readFiles(q,count)
        qStack = q.get(True)
        value = qStack['content']
        title = qStack['title']
        currentUrl = qStack['url']
        engine = pyttsx3.init()
        engine.say('开始阅读下一章')
        engine.say(title)
        time.sleep(2)
        engine.say(value)
        # engine.startLoop(False)
        print('Get %s from queue.' % value)
        rfs.writeFile('current.txt',currentUrl)
        engine.say('本章节阅读完成')
        engine.runAndWait()
        if temCount == count:
            engine.setProperty('voice', 'com.apple.speech.synthesis.voice.mei-jia')
            engine.say('您已经阅读完所有的章节，如需继续阅读，清重新开启！')
            engine.runAndWait()
            break

if __name__=='__main__':
    # 父进程创建Queue，并传给各个子进程：
    q = Queue()
    maxPrice= 3
    pw = Process(target=write, args=(q,maxPrice),daemon=True)
    pr = Process(target=read, args=(q,maxPrice),daemon=True)
    # 启动子进程pw，写入:
    pw.start()
    # 启动子进程pr，读取:
    pr.start()
    # 等待pw结束:
    pw.join()
    pr.join()
    # pr进程里是死循环，无法等待其结束，只能强行终止:
    pr.terminate()





