import pyttsx3
import requests
from bs4 import BeautifulSoup
from lxml import etree
from threading import Thread,Lock
import time

class readFiles():
    def __init__(self):
        self.engine = pyttsx3.init()
        # self.downQuests()

    def writeFile(self,fileName,content):
        with open(fileName,'w') as f:
            f.write(content)

    def readFile(self,fileName):
        with open(fileName,'r') as f:
            # self.currentUrl = f.read()
            self.resText = f.read()

    def downQuests(self,content):
        self.readFile(content)
        print(self.currentUrl)
        resp = requests.get(self.currentUrl)
        resp.encoding = 'utf-8'
        print(resp.text)
        self.resText = resp.text
        return resp.text


    def parseTree(self):
        tree = etree.HTML(self.resText)
        print(tree)
        if tree.xpath('//title/text()')[0] == '503 Service Temporarily Unavailable':
            print('出错了，从新加载！')
            self.downQuests('url.txt')
            self.parseTree()
        else:
            print(tree.xpath("//div[@class='bookname']/h1/text()")[0])
            soup = BeautifulSoup(self.resText,'lxml')


            for i in soup.find("div", class_="bottem1").contents:
                if (i.string == "下一章"):
                    self.newUrl = i["href"]

            for child in soup.find(id="content").stripped_strings:
                self.readEngine(child)
            self.engine.runAndWait()

    def updateUrl(self):
        self.writeFile('url.txt',self.newUrl)


    def readEngine(self,content):
        self.engine.say(content)



def run(n):

    print(n)
    engine = pyttsx3.init()
    engine.say(n)
    # engine.startLoop(False)
    engine.runAndWait()
    # engine.endLoop()

def downLode(n):
    print(n)
    print(n)
    # time.sleep(1)
    print(n)

if __name__ == '__main__':
    p1 = readFiles()
    p1.readFile('current.txt')
    # textUrl = p1.downQuests('url.txt')


    p1.parseTree()
    # lock = Lock()

    # t1 = Thread(target=run, args=('ti呵呵呵额9092033',))
    # t2 = Thread(target=downLode, args=('t2也诶iIE能否接受',))
    # # t1.setDaemon(True)
    # # t2.setDaemon(True)
    # t1.start()
    # t2.start()
    # t1.join()
    # t2.join()
    # print('901')



iot.gzm2mapn



# count = 1
# max = 5
# engine = pyttsx3.init()
# with open('url.txt','r') as f:
#     oldUrl = f.read()
#
# # url = 'http://www.biquge.info/43_43149/11586301.html'
#
# def readFile(url,count):
#     resp = requests.get(url)
#     resp.encoding = 'utf-8'
#     if count > max:
#         engine.say('请重新启动!')
#         return
#     if count == max:
#         with  open('current.txt', 'w') as f:
#             f.write(resp.text)
#     count += 1
#     engine.say('开始阅读!')
#     tree = etree.HTML(resp.text)
#     soup = BeautifulSoup(resp.text, 'lxml')
#
#     if tree.xpath('//title/text()')[0] == '503 Service Temporarily Unavailable':
#         print('出错了，从新加载！')
#         count -= 1
#         readFile(url, count)
#         return
#
#     for child in soup.find(id="content").stripped_strings:
#         engine.say(child)
#
#     for i in soup.find("div", class_="bottem1").contents:
#         if (i.string == "下一章"):
#             print(i["href"])
#             # if count == max:
#             with open('url.txt','w') as f:
#                 f.write(i["href"])
#             newUrl = i["href"]
#             readFile(newUrl,count)
#
#
# if __name__ == '__main__':
#     readFile(oldUrl,count)
#
# engine.say('Greetings!')
# engine.runAndWait()