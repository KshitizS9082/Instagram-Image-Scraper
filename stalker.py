from selenium.webdriver import Chrome
from time import sleep
import time
import os
import pandas as pd

n = int(input("enter number of profiles you want to scrape: "))
urls=[]
for i in range(n):
    url = input("Enter URL of the user no. "+ str(i) + " : ")
    urls.append(url)
#USER SPECIFIC:change your driver's location here
webdriver = "/Users/kshitizsharma/Downloads/chromedriver"
driver = Chrome(webdriver)

for url in urls:
    driver.get(url)
    ###############
    SCROLL_PAUSE_TIME = 1.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    count=0
    picMenuLinks = []
    while True:
        items = driver.find_elements_by_class_name("ySN3v")
        for item in items:
            x=item.find_elements_by_tag_name("a")
            for el in x:
                picMenuLink = el.get_attribute("href")
                if picMenuLink not in picMenuLinks:
                    picMenuLinks.append(picMenuLink)

        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    username = url.replace("https://www.instagram.com/","").replace("/","")
   
    #USER SPECIFIC: path of the file where you want to save your downloaded images
    path="/Users/kshitizsharma/Desktop/Stalker/"+url.replace("https://www.instagram.com/","").replace("/","")
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

    print(str(len(picMenuLinks)) + " posts found" )
    for picMenuLink in picMenuLinks:
        driver.get(picMenuLink)
        items=driver.find_elements_by_class_name("KL4Bh")
        if(len(items)>0):
            x = items[0].find_elements_by_tag_name("img")
            for xt in x:
                linkToImage=x[0].get_attribute("src")
                driver.get(linkToImage)
                driver.get_screenshot_as_file(path+"/"+username+str(count)+".png")
                print("did image number "+str(count)+" for "+username)
                count+=1
