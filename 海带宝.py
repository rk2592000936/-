'''
@Author:巴啦啦拉粑粑
使用过程中有任何问题请开issue

环境要求：
python 3
pip install selenium
pip install requests

使用方法：
在下方login()中填入你的账号密码，在cmd中运行即可
'''


from selenium import webdriver
import requests
import time
import re


driver = webdriver.Chrome()


def login(account,password):
# 打开网站(登录页面)
    driver.get('http://www.haidaibao.com/Box/MyBox.aspx?pagetabs=3&centercode=&overboxorderremark=')  
# 查找元素
    element = driver.find_element_by_xpath('//*[@id="username"]')
    element2 = driver.find_element_by_xpath('//*[@id="firstpassword"]')  
# 在该元素里输入数据
    element.send_keys(account)  
    element2.send_keys(password)
    driver.find_element_by_id('btn_llogin').click()  # 登录  
# '待签收'页面
    driver.get('http://www.haidaibao.com/Box/MyBox.aspx?pagetabs=3&centercode=&overboxorderremark=#logisticsinfo')  
    time.sleep(1)


def load():
# 加载页面所有包裹
    while True:
        try:
            driver.find_element_by_xpath('//*[@id="loadmode"]/a').click()
        except:
            break
# 等待全部元素加载完成
    time.sleep(15)
    print('加载完毕')


def find_boxing_number():
# 查找已从国内发出包裹的元素，通过'签收'button，并把箱子号存在boxing_numbers中
    boxing_numbers = []
    element_list = driver.find_elements_by_class_name('btn_nblue')
    tracking_temp_numbers = []
    for n in range(len(element_list)):
        tracking_temp_numbers.append(str((element_list[n].get_attribute('id'))))  # 获取该元素的属性值
        if tracking_temp_numbers[n] == '':
            break
        boxing_numbers.append(tracking_temp_numbers[n][9:26])  
    return boxing_numbers


def search_one_by_one(boxing_number):
    aspx = []
    match = []
    sf = []
    ems = []
    if len(boxing_number) == 0:
        print('暂无发出包裹')
    else:
        for n in range(len(boxing_number)):
    # 如果待签收中有包裹，利用搜索，遍历tracking numbers中的箱子信息
            driver.find_element_by_xpath('//*[@id="overboxorderremark"]').clear()
            driver.find_element_by_xpath('//*[@id="overboxorderremark"]').send_keys(boxing_number[n])
            driver.find_element_by_xpath('//*[@id="submitform"]/div[3]/table/tbody/tr/td[2]/button').click()
            time.sleep(1.5)
    # 获取‘物流详情’处的onclick值，存在aspx列表中
            aspx.append(driver.find_element_by_xpath('//*[@id="submitform"]/table[2]/tbody[1]/tr[2]/td/table/tbody/tr/td[2]/a').get_attribute('onclick'))
    # 获取pi值，存在match列表中
            match.append(re.search(r'BM[0-9]+',aspx[n]).group())
            url = 'http://www.haidaibao.com/Box/LogisticsInfo.aspx?pi='+str(match[n])
            source = requests.get(url).text
            if re.search(r'顺丰 [0-9]+', source) is not None:
                sf.append(re.search(r'(?<=顺丰\s)\d+', source).group())
            else:
                ems.append(re.search(r'(?<=EMS\s)\d+', source).group())
    print(sf)
    print(ems)
    time.sleep(5)
    driver.quit()
    return sf, ems


def write(list1, list2):
    with open('tracking2.txt','w') as f:
        f.write('SF:')
        f.write('\n')
        for a in list1:
            f.write(a)
            f.write('\n')
    with open('tracking2.txt','a')as f:
        f.write('EMS:')
        f.write('\n')
        for a in list2:
            f.write(a)
            f.write('\n')


if __name__ == '__main__':
    login('yor account here','your password here')  #在此处填入你的账号密码
    load()
    boxing = find_boxing_number()
    a = search_one_by_one(boxing)
    write(a[0],a[1])





