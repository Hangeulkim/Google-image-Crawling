import urllib.request
from selenium import webdriver
import urllib.parse
from multiprocessing import Pool
import time
import os
import pandas as pd

key=pd.read_csv('./keyword.txt',encoding='cp949',names=['keyword'])
keyword=[]
[keyword.append(key['keyword'][x]) for x in range(len(key))]

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)


def image_download(search):
    url = f'https://www.google.com/search?q={urllib.parse.quote_plus(search)}&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjIvaygpr7xAhXMy4sBHe3BBuMQ_AUoAXoECAEQAw&biw=1202&bih=754'

    options= webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--ignore-certificate-error")
    options.add_argument("--ignore-ssl-errors")
    driver = webdriver.Chrome("c:\\chromedriver.exe",options=options)
    driver.get(url)

    SCROLL_PAUSE_TIME = 1
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            try:
                driver.find_element_by_css_selector(".mye4qd").click()
            except:
                break
        last_height = new_height

    images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")

    createFolder("크롤링 사진/"+search)
    count = 1
    for image in images:
        try:
            image.click()
            time.sleep(1)
            imgUrl = driver.find_element_by_xpath('//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img').get_attribute("src")
            hak=imgUrl[imgUrl.rfind('.'):]
            print(hak)
            opener=urllib.request.build_opener()
            opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
            urllib.request.install_opener(opener)
            ###urllib.request.urlretrieve(imgUrl, "c:\\크롤링 사진"+search+"/"+search+str(count) + ".jpg")
            print(imgUrl)
            mem=urllib.request.urlopen(imgUrl, timeout = 0.5).read()

            with open("크롤링 사진/"+search+"/"+search+str(count) + hak,mode="wb") as f:
                f.write(mem)
            count = count + 1
            
            print(count)

            

        except:
            pass

    driver.close()

if __name__=='__main__':
    search = input('검색어:')
    pool = Pool(processes=4) # 4개의 프로세스를 사용합니다.
    pool.map(image_download, keyword)
    ###image_download(search)