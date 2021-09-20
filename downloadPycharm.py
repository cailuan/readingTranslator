from selenium import webdriver

opt = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=opt)
driver.get('http://www.biquge.info/10_10240/5018748.html')
print(driver.page_source)