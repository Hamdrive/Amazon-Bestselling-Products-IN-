#!/usr/bin/env python
# -*- coding: utf-8 -*-
#video link="https://www.youtube.com/watch?v=XQgXKtPSzUI"
#how to properly show rupee sign in excel: https://stackoverflow.com/questions/6002256/is-it-possible-to-force-excel-recognize-utf-8-csv-files-automatically/6488070#6488070
#if fresh install of python, pip3 install: bs4, pandas, requests, openpyxl, numpy==1.19.3(most stable version at the time of writing this comment(17/12/20))

from bs4 import BeautifulSoup as soup #to parse HTML
import pandas as pd
import numpy as np
import requests


#"""TO RETRIEVE INDIVIDUAL PRODUCT LINK FROM AMAZON BESTSELLER PAGE(KITCHEN)"""

kitchen_bestsellers_url = "https://www.amazon.in/gp/bestsellers/kitchen/ref=zg_bs_pg_"
link_of_bestsellers_products=[]

def get_page_number(page_soup):
    no_of_pages = page_soup.find('li', class_='a-normal').find('a').text.split('/')[0] 
    return(no_of_pages)

def scrape_page(number=1):

    #user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    #headers = {'User-Agent': user_agent}

    #opening website url and downloading page
    page_html = requests.get(kitchen_bestsellers_url + str(number) + "?ie=UTF8&pg="+str(number))
    page_content = page_html.text #instead of content used text because it has UTF-8 encoding so rupee symbol will be properly parsed.
    #to parse HTML
    page_soup = soup(page_content,"html.parser")

    bestseller_item_container = page_soup.find_all("li",{"class":"zg-item-immersion"})

    for item in (bestseller_item_container):

        bestseller_product_direct_url = "https://www.amazon.in" + item.a["href"]

        #print(bestseller_product_direct_url)
        
        link_of_bestsellers_products.append(bestseller_product_direct_url)

    return get_page_number(page_soup)

page_number = scrape_page()

if int(page_number) > 1:
    for i in range (1, int(page_number)):
        scrape_page(i+1)



#"""TO RETRIEVE INDIVIDUAL PRODUCT LINK FROM AMAZON BESTSELLER PAGE(KITCHEN)"""

#using the list of all products links to go to them and retrieve information
for listurl in link_of_bestsellers_products:
    product_url = listurl

    df= pd.DataFrame(columns=["Product", "Seller", "Cost", "Length", "Width", "Height", "Weight", "Link"])

    def scrape_product():
        page_content = (requests.get(product_url)).text
        page_soup = soup(page_content,"html.parser")

        product_name = (page_soup.find("span",{"class":"a-size-large product-title-word-break"})).text
        print(product_name)
        



#print("Saved in excel")
