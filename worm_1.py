import bs4
from selenium import webdriver
import time
import requests
from bs4 import BeautifulSoup
import json
import re

driver = webdriver.Chrome()

# 输入关键字
# keyWord = 'people'
# 输入模型类型
# model_type = 'obj'

# driver.get('https://github.com/')
# driver.get('https:free3d.com/')
# driver.find_element_by_link_text('继续访问').click()
# driver.get('https://www.turbosquid.com/3d-model/free/'+keyWord+'/'+model_type+'?synonym='+keyWord)
# driver.find_element_by_id('Asset1334834').click
# driver.find_element_by_id('Asset-48').click()
driver.get('https://www.turbosquid.com/Login/Index.cfm')
driver.find_element_by_xpath("//input[@name='user[email]']").clear()
# driver.find_element_by_xpath("//input[@name='user[application_uid]']").clear()
driver.find_element_by_xpath("//input[@name='user[email]']").send_keys('chengyihengok@126.com')
driver.find_element_by_xpath("//input[@name='user[password]']").clear()
driver.find_element_by_xpath("//input[@name='user[password]']").send_keys('project0808')
driver.find_element_by_xpath("//input[@name='commit']").click()
time.sleep(10)
# driver.get('https://www.turbosquid.com/AssetManager/Index.cfm?stgAction=getFiles&subAction=Download&intID=1447788&intType=3')


driver.get('https://www.turbosquid.com/Login/Index.cfm')
post = {}
#获取cookies
cookie_items = driver.get_cookies()
for cookie_item in cookie_items:
    post[cookie_item['name']] = cookie_item['value']
cookie_str = json.dumps(post)
with open('cookie.txt', 'w', encoding='utf-8') as f:
    f.write(cookie_str)
f.close()


#driver.get('https://www.baidu.com/')

#driver.find_element_by_id('kw').send_keys('tree')
#driver.find_element_by_id('su').click()
# driver.find_element_by_id('NavTextField').send_keys('tree')
# driver.find_element_by_id('NavButton').click()


with open('cookie.txt', 'r', encoding='utf-8') as f:
    cookie = f.read()
cookies = json.loads(cookie)

# 1.寻找基础url
formats = 'obj'  # 确定文件格式
key = 'tree'  # 搜索内容
download_num = 4  # 下载数量

base_url = 'https://www.turbosquid.com/3d-model/free/'+key+'/'+formats
download_url = 'https://www.turbosquid.com/AssetManager/Index.cfm'
# 2.设置headers字典和params字典，再发请求
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
}
params = {
    'synonym': key
}

# driver.get(download_url, cookies=cookies, headers=headers, params=download_params)
response = requests.get(base_url, cookies=cookies, headers=headers, params=params)
demo = response.text
soup = BeautifulSoup(demo, "html.parser")
# print(soup.prettify())
for i in range(download_num):
    if i == 0:
        soup2 = soup.find("div", "AssetInner").find("div", "thumbnail thumbnail-md")
    else:
        soup2 = soup2.find_next("div", "thumbnail thumbnail-md")
    check_url = soup2.find('a')["href"]
    check_response = requests.get(check_url, cookies=cookies)
    demo_free = check_response.text
    soup_check = BeautifulSoup(demo_free, "html.parser")
    if soup_check.find("div", "priceSection price").find("span")["class"] == ['price', 'free-price']:
        identifier = soup2['data-id']
        print(soup2['data-id'])
        # 跳转至对应模型的下载页面
        driver.get('https://www.turbosquid.com/AssetManager/Index.cfm?stgAction=getFiles&subAction=Download&intID='+identifier+'&intType=3')
        driver.find_element_by_xpath("//div[@id='ProductFileRow"+identifier+"']").find_element_by_xpath("//span[@class='mainFileName']").click()

        #---------------------延迟操作-----------------------#
        time.sleep(30)
        #--------------------------------------------------#

        driver.find_element_by_xpath("//input[@id='cbItemAll']").click()
        driver.find_element_by_xpath("//div[@id='miRemove']").click()
        driver.find_element_by_xpath("//span[@class='yui-button yui-push-button btn_remove']").click()
        time.sleep(5)
    else:
        print("This model is not free!")





'''download_params = {
    'stgAction': 'getFiles',
    'subAction': 'Download',
    'intID': identifier,
    'intType': 3
}

download_response = requests.get(download_url, cookies=cookies, headers=headers, params=download_params)
print(download_response.url)

demo2 = download_response.text
soup3 = BeautifulSoup(demo2, "html.parser")
print(soup3.prettify())
print(soup3.find("div", id="page-container"))'''

# free3d.com
'''key = 'tree'
base_url = 'https://free3d.com/3d-models/'+key
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
}
response = requests.get(base_url, headers=headers)
demo = response.text
soup = BeautifulSoup(demo, "html.parser")
print(soup.find('div', 'search-result'))'''



