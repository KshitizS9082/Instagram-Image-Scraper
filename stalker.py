from selenium.webdriver import Chrome
from time import sleep
import time
import os
import pandas as pd

numberOfProfilestoritrieve = int(input("enter number of profiles you want to scrape: "))
urls=[]
#take input URLs
for i in range(numberOfProfilestoritrieve):
    url = input("Enter InstaID of the user no. "+ str(i+1) + " : ")
    url = "https://www.instagram.com/"+url+"/"
    urls.append(url)
#USER SPECIFIC:change your driver's location here
webdriver = "/Users/kshitizsharma/Downloads/chromedriver"
driver = Chrome(webdriver)

#Start scraping each target user
for url in urls:
    try:
        driver.get(url)
    except:
        print("wrong username given: " + url.replace("https://www.instagram.com/","").replace("/",""))
        continue
    ##Time to pause after each scroll##
    SCROLL_PAUSE_TIME = 1.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    count=0
    picMenuLinks = []
    #Get links to individual post pages
    while True:
        items = driver.find_elements_by_class_name("ySN3v")
        for item in items:
            x=item.find_elements_by_tag_name("a")
            for el in x:
                try:
                    picMenuLink = el.get_attribute("href")
                except:
                    print("exception in line 30")
                    continue
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
    print(str(len(picMenuLinks)) + " posts found" )

    username = url.replace("https://www.instagram.com/","").replace("/","")
   
    #USER SPECIFIC: path of the file where you want to save your downloaded images
    path="/Users/kshitizsharma/Desktop/Stalker/"+url.replace("https://www.instagram.com/","").replace("/","")
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)


    #Go to individual post pages
    for picMenuLink in picMenuLinks:
        try:
            driver.get(picMenuLink)
            items=driver.find_elements_by_class_name("KL4Bh")
        except:
            print("Failed to ritrieve image")
            continue
        imageLinks=[]
        if(len(items)>0):
            x = items[0].find_elements_by_tag_name("img")
            for xt in x:
                try:
                    linkToImage=x[0].get_attribute("src")
                    imageLinks.append(linkToImage)
                except:
                    print("coulnot get src to image")
        
        #get to more images if any in this post
        moreImageinThisPost = True; shiftedRight=False
        while(moreImageinThisPost):
            try:
                # search for right button when current image is not leftmost
                button=driver.find_elements_by_xpath("/html/body/div[1]/section/main/div/div/article/div[1]/div/div/div[2]/div/button[2]")
                if len(button)==0 and shiftedRight==False: #search for right button when current image is not leftmost
                    button=driver.find_elements_by_xpath("/html/body/div[1]/section/main/div/div/article/div[1]/div/div/div[2]/div/button")
                if(len(button))>0:
                    button=button[0]
                
                button.click()
                shiftedRight=True
                items=driver.find_elements_by_class_name("KL4Bh")
                for item in items:
                    imgDivs = item.find_elements_by_tag_name("img")
                    for imgDiv in imgDivs:
                        linkToImage=imgDiv.get_attribute("src")
                        if linkToImage not in imageLinks:
                            imageLinks.append(linkToImage)
            except:
                moreImageinThisPost=False
                print("no more buttons to next image")
        print("no. of images in this post is : "+str(len(imageLinks)))

        #retrieve all the images from imageLinks found in this post page(picMenuLink)
        for imageLink in imageLinks:
            try:
                driver.get(imageLink)
            except:
                print("failed to download image from link: " + imageLink)
                continue
            driver.get_screenshot_as_file(path+"/"+username+str(count)+".png")
            
            print("did image number "+str(count)+" for "+username)
            count+=1
            if count%20==0:
                sleep(10)
            if count%100==0:
                sleep(100)
