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
import random
from datetime import datetime


#"""TO RETRIEVE INDIVIDUAL PRODUCT LINK FROM AMAZON BESTSELLER PAGE(KITCHEN)"""
delay = random.randint(1,10) 

def get_time():
    now = datetime.now()

    current_time = now.strftime("%d/%m/%Y, %H:%M:%S")
    return(current_time)

def get_page_number(page_soup):
    
    no_of_pages = page_soup.find('li', class_='a-normal').find('a').text.split('/')[0] 
    return(no_of_pages)

def scrape_page(number=1):

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 OPR/73.0.3856.284' #'Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko'
    headers = {'User-Agent': user_agent}

    #opening website url and downloading page
    page_html = requests.get((kitchen_bestsellers_url + str(number) + "?ie=UTF8&pg="+str(number)),headers=headers)
    
    time.sleep(delay)
    
    page_content = page_html.text #instead of content used text because it has UTF-8 encoding so rupee symbol will be properly parsed.
    #to parse HTML
    page_soup = soup(page_content,"html.parser")

    bestseller_item_container = page_soup.find_all("li",{"class":"zg-item-immersion"})
    
    time.sleep(delay)
    
    for item in (bestseller_item_container):

        bestseller_product_direct_url = "https://www.amazon.in" + item.a["href"]

        print(bestseller_product_direct_url)
        
        link_of_bestsellers_products.append(bestseller_product_direct_url)

        time.sleep(delay)

        break

    return get_page_number(page_soup)


print("\n")
start_time = get_time()
print("Start time of scrapper:", start_time)
kitchen_bestsellers_url = "https://www.amazon.in/gp/bestsellers/kitchen/ref=zg_bs_pg_"
link_of_bestsellers_products=[]   

page_number = scrape_page()


if int(page_number) > 1:
    for i in range (1, int(page_number)):
        time.sleep(delay)
        scrape_page(i+1)

print("\n")
print("The list of bestsellers URLs are obtained")
print("Moving onto individual product scraping")
print("\n")

#print(link_of_bestsellers_products)

#"""TO RETRIEVE INDIVIDUAL PRODUCT LINK FROM AMAZON BESTSELLER PAGE(KITCHEN)"""

#using the list of all products links to go to them and retrieve information

df= pd.DataFrame(columns=["Product", "Seller", "Cost", "Length", "Width", "Height", "Weight", "Link"])

list_of_unavailable_product_links=[]

for listurl in link_of_bestsellers_products: 

    def scrape_product(product_url):

        global df

        print("\n")
        print(product_url)
        page_content = requests.get(product_url, timeout=(3,20)).text
        
        time.sleep(delay)
        
        #s = HTMLSession()
        #page_content = s.get(product_url)
        #page_content.html.render(sleep=0)
        page_soup = soup(page_content,"html.parser")

        time.sleep(delay)

        #tree navigation
        try:
            product_name = (page_soup.find("span",{"class":"a-size-large product-title-word-break"})).text.strip()
        except Exception:
            product_name = None
            

        time.sleep(delay)

        try:
            seller_name = (page_soup.find("a",{"id":"sellerProfileTriggerId"})).text
        except Exception:
            seller_name = None
            
        
        time.sleep(delay)
        
        #product price returns as a list, so reading each item in list and joining them to obtain one string
        try:
            product_cost = ''.join((page_soup.find("span",{"class":"a-size-medium a-color-price priceBlockBuyingPriceString"})).text.split()[0:2])
        except Exception:
            product_cost = None
            
        
        time.sleep(delay)
        
        try:
            product_dimensions_retrival = get_product_dimensions(page_soup)
            product_length = product_dimensions_retrival[0]
            product_width = product_dimensions_retrival[1]
            product_height = product_dimensions_retrival[2]
        except Exception:
            product_length = None
            product_width = None
            product_height = None
            
        
        time.sleep(delay)

        try:
            product_weight_retrival = get_product_weight(page_soup)
            product_weight = product_weight_retrival
        except Exception:
            product_weight = None
            
        
        #product_width = (page_soup.find("span",{"class":"a-list-item"}).span).text
        #product_height = (page_soup.find("span",{"class":"a-list-item"}).span).text
        #product_weight = (page_soup.find("",{"":""}))

        

        #product_name = page_content.html.xpath('//*[@id="productTitle"]', first=True).text
        print("Product name:", product_name)
        print("Seller name:", seller_name)
        print("Product Cost:", product_cost)
        print("Product Length: {} cm".format(product_length))
        print("Product Width: {} cm".format(product_width))
        print("Product Height: {} cm".format(product_height))
        print("Product Weight: {}".format(product_weight))
        print("\n")
        #print("process_done")
        
        
        df = df.append({"Product": product_name, "Seller": seller_name, "Cost": product_cost, "Length": product_length, "Width": product_width, "Height": product_height, "Weight": product_weight, "Link": product_url}, ignore_index=True)
        print(df)
    
    def get_product_dimensions(page_soup):

        time.sleep(delay)

        for dimension in (page_soup.find("ul",{"class":"a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list"}).find_all("li", {"span":""})):
            #for bullet in info.findAll("span"):
            #print(info)
            word = 'Item Dimensions LxWxH'
            if word in dimension.select('li > span')[0].text:

                time.sleep(delay)

                dimension_result = dimension.select('li > span')[0].text.split()[4:10:2]
                #print("dimen list")
                #print(dimension_result)
                
        return(dimension_result)
        
            #if info == 'NavigableString':
            #    
            #elif info.span.span.text == 'Product Dimensions':
            #    print(info.span.span.text)
    
    def get_product_weight(page_soup):

        time.sleep(delay)

        for weight in (page_soup.find("ul",{"class":"a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list"}).find_all("li", {"span":""})):
            word = "Item Weight"
            if word in weight.select('li > span')[0].text:

                time.sleep(delay)

                weight_result = ''.join(weight.select('li > span')[0].text.split()[3:5])
                #print("weight list")
                #print(weight_result)
                
        return(weight_result)
    
    try:
        product_url = listurl               
        scrape_product(product_url)
    except Exception:
        list_of_unavailable_product_links.append(product_url)
        
#Finally convert the dataframe into a readable format for Excel, both spreadsheet and CSV, and set the first index to 1        

#df = df.append({"Product": "product", "Seller": "name", "Cost": "cost", "Length": "length", "Width": "width", "Height": "height", "Weight": "weight", "Link": "url"}, ignore_index=True)

#df.reset_index()

df.to_excel(r'E:\MyPrograms\proj6-webscraping\amazon_scrape\Amazon_Bestsellers_list_Home&Kitchen.xlsx', index = True)
df.to_csv("Amazon_Bestsellers_list_Home&Kitchen.csv")
print("Saved in excel")
end_time = get_time()
print("Start time of scrapper:", start_time)
print("End time of scrapper:", end_time)       

    #detailBullets_feature_div > ul > li:nth-child(12) > span > span:nth-child(2)
        



#print("Saved in excel")
