from splinter import Browser
from bs4 import BeautifulSoup as bs
import pymongo
import requests
import pandas as pd
import tweepy
import time

# coding: utf-8
def mars_scrape():
    # initialize dictionary to store scraped information
    mars_dictionary = {}

    # mars news website
    url = 'https://mars.nasa.gov/news/?page=0&per_page=15&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    # use 'requests' to retrieve requests object and then convert to html through beautifulsoup
    response = requests.get(url)
    soup = bs(response.text,'lxml')

    # print(soup.prettify())

    # scrape using beautifulsoup
    first_article = soup.find('div',class_='slide')
    news_title = first_article.find('div',class_='content_title').a.text.strip()
    news_summary = first_article.find('div',class_='rollover_description_inner').text.strip()

    # store info into dictionary

    # start up chromebrowser to scrape images from JPL's website
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path)

    images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    jpl_url = 'https://www.jpl.nasa.gov'

    browser.visit(images_url)

    # assign current page's html to 'html' variable
    html = browser.html

    # use beautifulsoup to parse the html
    soup = bs(html,'html.parser')

    # click on the 'Full Image' link from featured image
    browser.click_link_by_id('full_image')

    time.sleep(1)

    # assign html from current browser
    image_html = browser.html
    image_soup = bs(image_html,'html.parser')
     
    # scrape for featured image's url
    try:
        modal_img_url = image_soup.find('div',class_='fancybox-inner').img['src']
        # build full url 
        featured_image_url = jpl_url + modal_img_url
         # store info in dictionary
        mars_dictionary['featured_image_url'] = featured_image_url
    except:
        try:
            print("Image source not found - need to wait before scraping image url")
            
            time.sleep(10)

            modal_img_url = image_soup.find('div',class_='fancybox-inner').img['src']
            # build full url 
            featured_image_url = jpl_url + modal_img_url
             # store info in dictionary
        except:
            browser.windows.current.close
            print("YOUR INTERNET HATES YOU. SORRY!")

    # Twitter API Keys
    consumer_key = "Ed4RNulN1lp7AbOooHa9STCoU"
    consumer_secret = "P7cUJlmJZq0VaCY0Jg7COliwQqzK0qYEyUF9Y0idx4ujb3ZlW5"
    access_token = "839621358724198402-dzdOsx2WWHrSuBwyNUiqSEnTivHozAZ"
    access_token_secret = "dCZ80uNRbFDjxdU2EckmNiSckdoATach6Q8zb7YYYE5ER"


    # Setup Tweepy API Authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())


    target_user = 'MarsWxReport'

    mars_weather_tweets = api.user_timeline(target_user)

    for tweet in mars_weather_tweets:
        if 'Sol' in tweet['text']:
            mars_weather = tweet['text']

    # store into dictionary
    

    # initialize dictionary
    mars_facts = {}
    mars_facts_url = 'https://space-facts.com/mars/'

    # request html from url and import into beautifulsoup
    response = requests.get(mars_facts_url)
    soup = bs(response.text,'lxml')

    # find table -> tbody
    table_html = str(soup.table).replace("\n","")
    marsfacts_df = pd.read_html(table_html,index_col=0)[0]
    marsfacts_html_string = marsfacts_df.to_html(header=False).replace("\n","")


    # start up chromebrowser to scrape hemisphere images 
    hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(hem_url)

    hem_html = browser.html
    hem_soup = bs(hem_html,'html.parser')

    products_html = hem_soup.find_all('div',class_='item')

    hemisphere_image_urls = []
    usgs_url = 'https://astrogeology.usgs.gov'

    for product in products_html:
        title = product.h3.text
        
        browser.click_link_by_partial_text(title)
        
        hem2_html = browser.html
        hem2_soup = bs(hem2_html,'html.parser')
        
        temp_url = hem2_soup.find('img',class_='wide-image')['src']
        
        temp_dictionary = {}
        
        temp_dictionary['img_url'] = usgs_url + temp_url
        temp_dictionary['title'] = title
        
        hemisphere_image_urls.append(temp_dictionary)
        
        browser.visit(hem_url)

    browser.windows.current.close
    mars_dictionary['featured_image_url'] = featured_image_url
    mars_dictionary['news_summary'] = news_summary
    mars_dictionary['news_title'] = news_title
    mars_dictionary['weather_tweet'] = mars_weather
    mars_dictionary['facts_html'] = marsfacts_html_string
    mars_dictionary['hemispheres'] = hemisphere_image_urls

    

    print(mars_dictionary)
    return mars_dictionary

