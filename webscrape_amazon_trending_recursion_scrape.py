#!/usr/bin/env python
# -*- coding: utf-8 -*-
#video link="https://www.youtube.com/watch?v=XQgXKtPSzUI"
#how to properly show rupee sign in excel: https://stackoverflow.com/questions/6002256/is-it-possible-to-force-excel-recognize-utf-8-csv-files-automatically/6488070#6488070
#if fresh install of python, pip3 install: bs4, pandas, requests, openpyxl, numpy==1.19.3(most stable version at the time of writing this comment(17/12/20))

from bs4 import BeautifulSoup as soup #to parse HTML
import pandas as pd
import numpy as np
import requests
from requests_html import HTMLSession #since requests does not work on indivivdual amazon products
import time


#"""TO RETRIEVE INDIVIDUAL PRODUCT LINK FROM AMAZON BESTSELLER PAGE(KITCHEN)"""

kitchen_bestsellers_url = "https://www.amazon.in/gp/bestsellers/kitchen/ref=zg_bs_pg_"
link_of_bestsellers_products=[]

def get_page_number(page_soup):
    no_of_pages = page_soup.find('li', class_='a-normal').find('a').text.split('/')[0] 
    return(no_of_pages)

def scrape_page(number=1):

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    headers = {'User-Agent': user_agent}

    #opening website url and downloading page
    page_html = requests.get((kitchen_bestsellers_url + str(number) + "?ie=UTF8&pg="+str(number)),headers=headers)
    
    time.sleep(5)
    
    page_content = page_html.text #instead of content used text because it has UTF-8 encoding so rupee symbol will be properly parsed.
    #to parse HTML
    page_soup = soup(page_content,"html.parser")

    bestseller_item_container = page_soup.find_all("li",{"class":"zg-item-immersion"})
    
    time.sleep(5)
    
    for item in (bestseller_item_container):

        bestseller_product_direct_url = "https://www.amazon.in" + item.a["href"]

        print(bestseller_product_direct_url)
        
        link_of_bestsellers_products.append(bestseller_product_direct_url)

        time.sleep(5)

        break

    return get_page_number(page_soup)

page_number = scrape_page()


if int(page_number) > 1:
    for i in range (1, int(page_number)):
        time.sleep(5)
        scrape_page(i+1)

print(link_of_bestsellers_products)

#"""TO RETRIEVE INDIVIDUAL PRODUCT LINK FROM AMAZON BESTSELLER PAGE(KITCHEN)"""

#using the list of all products links to go to them and retrieve information
for listurl in link_of_bestsellers_products:
    product_url = listurl

    df= pd.DataFrame(columns=["Product", "Seller", "Link", "Cost", "Length", "Width", "Height", "Weight"])

    

    def scrape_product(product_url):
        #print(product_url)
        page_content = requests.get(product_url).text
        
        time.sleep(5)
        
        #s = HTMLSession()
        #page_content = s.get(product_url)
        #page_content.html.render(sleep=0)
        page_soup = soup(page_content,"html.parser")

        time.sleep(5)

        #tree navigation
        product_name = (page_soup.find("span",{"class":"a-size-large product-title-word-break"})).text.strip()
        seller_name = (page_soup.find("a",{"id":"sellerProfileTriggerId"})).text
        #product price returns as a list, so reading each item in list and joining them to obtain one string
        product_cost = ''.join((page_soup.find("span",{"class":"a-size-medium a-color-price priceBlockBuyingPriceString"})).text.split()[0:2])
        product_length = get_product_info(page_soup)
        #product_width = (page_soup.find("span",{"class":"a-list-item"}).span).text
        #product_height = (page_soup.find("span",{"class":"a-list-item"}).span).text
        #product_weight = (page_soup.find("",{"":""}))

        

        #product_name = page_content.html.xpath('//*[@id="productTitle"]', first=True).text
        print("Product name:", product_name)
        print("Seller name:", seller_name)
        print("Product Cost:", product_cost)
        print("Product Length:", product_length)
        print("process_done")
        print('\n')
    
    def get_product_info(page_soup):
        for info in (page_soup.find("ul",{"class":"a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list"}).find_all("li", {"span":""})):
            #for bullet in info.findAll("span"):
            print(info)
            word = 'Dimension'
            if word in info.select('li > span')[0].text:
                info_result = info.select('li > span')[1].text
                print(info.select('li > span')[1].text)
            #if info == 'NavigableString':
            #    continue
            #elif info.span.span.text == 'Product Dimensions':
            #    print(info.span.span.text)
    return(info_result)
                
    scrape_product(product_url)

    #detailBullets_feature_div > ul > li:nth-child(12) > span > span:nth-child(2)
        



#print("Saved in excel")
