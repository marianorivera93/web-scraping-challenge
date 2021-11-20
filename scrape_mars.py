# dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)
def scrape():
    browser=init_browser()
    mars_dict={}
    ### NASA Mars News

    # scarped URL
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html=browser.html
    soup=bs(html,'html.parser')

    # Latest news title
    news_title=soup.find_all('div', class_='content_title')[0].text
    # Latest news paragraph
    news_p=soup.find_all('div', class_='rollover_description_inner')[0].text
    
    ### JPL Mars Space Image

    featured_image_url = 'https://spaceimages-mars.com/'
    browser.visit(featured_image_url)

    html=browser.html
    # Parse HTML
    soup=bs(html,"html.parser")
    # Retrieve image url
    featured_image_url=soup.find('img', class_="headerimage fade-in")
    featured_imagelink='https://spaceimages-mars.com/' + featured_image_url["src"]
    
    ### Mars Fact

    url='https://galaxyfacts-mars.com/'
    tables=pd.read_html(url)
    tables
    
    mars_fact=tables[0]
    mars_fact=mars_fact.rename(columns={0:"Profile",1:"Value"},errors="raise")
    mars_fact.set_index("Profile",inplace=True)
    mars_fact
    
    fact_table=mars_fact.to_html()
    fact_table.replace('\n','')
    
    ### Mars Hemispheres

    usgs_url='https://astrogeology.usgs.gov'
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html=browser.html
    soup=bs(html,'html.parser')

    # Hemispheres
    mars_hems=soup.find('div',class_='collapsible results')
    mars_item=mars_hems.find_all('div',class_='item')
    hemisphere_image_urls=[]

    for item in mars_item:
        # Error handling
        try:
            # Extract title
            hem=item.find('div',class_='description')
            title=hem.h3.text
            # Extract image url
            hem_url=hem.a['href']
            browser.visit(url+hem_url)
            html=browser.html
            soup=bs(html,'html.parser')
            image_src=soup.find('li').a['href']
            if (title and image_src):
                # Print results
                print('-'*50)
                print(title)
                print(image_src)
            # Create dictionary for title and url
            hem_dict={
                'title':title,
                'image_url':"https://marshemispheres.com/" + image_src
            }
            hemisphere_image_urls.append(hem_dict)
        except Exception as e:
            print(e)

    # Dict for all scraped info
    mars_dict={
        "news_title":news_title,
        "news_p":news_p,
        "featured_image_url":featured_imagelink,
        "fact_table":fact_table,
        "hemisphere_images":hemisphere_image_urls
    }
    # Close the browser after scraping
    browser.quit()
    return mars_dict

