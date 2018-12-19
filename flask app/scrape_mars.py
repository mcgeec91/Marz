import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pymongo
import requests
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver'}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser_open = init_browser()
    news = mars_news_page(browser_open)
    image_url = mars_featured_image(browser_open)
    weather = mars_twit_weather(browser_open)
    table = basic_mars_facts(browser_open)
    hemispheres = mars_hemispheres_pics(browser_open)
    mars_all_data ={"mars_news":news,"featured_image_url":image_url,"mars_weather": weather, "mars_facts":table, "mars_hemispheres": hemispheres}
   
    
    # Close the browser after scraping
    browser_open.quit()

    # Return results
    return mars_all_data

def mars_news_page(browser):
    mars_news=[]
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(4)
    html = browser.html
    get_headlines = bs(html, 'html.parser')

# NASA Mars News
    body = get_headlines.find("div", class_="list_text")

    title=body.find('div', class_="content_title").text.strip()
    mars_news.append(title)
    description=body.find('div', class_="article_teaser_body").text.strip()
    mars_news.append(description)

    return(mars_news)




#visiting a different web page
def mars_featured_image(browser):
    mars_images_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(mars_images_url)
    image_html = browser.html
    get_images = bs(image_html, 'html.parser')
    where=get_images.find('div', class_="default floating_text_area ms-layer")
    image = where.find('a')['data-fancybox-href']
    mars_url="https://www.jpl.nasa.gov"
    featured_image_url=mars_url+image
    return(featured_image_url)


def mars_twit_weather(browser):
    time.sleep(4)
    mars_weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_weather_url)
    weather_html = browser.html
    get_weather = bs(weather_html, 'html.parser')
    mars_weather = get_weather.find('div', class_="js-tweet-text-container").text.strip()
    return(mars_weather)

def basic_mars_facts(browser):
    time.sleep(4)
    mars_facts_url = "https://space-facts.com/mars/"
    browser.visit(mars_facts_url)
    mars_facts_df = pd.read_html(mars_facts_url)
    mars_facts_df = (mars_facts_df[0])
    mars_facts_df.columns = ["Category","Statistic"]
    mars_facts_html = mars_facts_df.to_html(index=False)
    return(mars_facts_html)



def mars_hemispheres_pics(browser):
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)
    # Use splinter to loop through the 4 images and load them into a dictionary
    hemi_html = browser.html
    soup = bs(hemi_html, 'html.parser')
    mars_hemis=[]
    for i in range (4):
        images = browser.find_by_tag('h3')
        images[i].click()
        hemi_html = browser.html
        soup = bs(hemi_html, 'html.parser')
        partial = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary={"title":img_title,"img_url":img_url}
        mars_hemis.append(dictionary)
        browser.back()
        return(mars_hemis)