from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "D:\Program Files\chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def get_soup_from_url(url, browser):
    # visiting the page
    browser.visit(url)
    # using bs to write it into html
    html = browser.html
    soup = bs(html,"html.parser")
    return soup

def scrape():
    browser = init_browser()
    mars_data_dict = {}

    ##### ---------------------- For Title & Paragraph ----------------------------------------------------------
    soup = get_soup_from_url("https://mars.nasa.gov/news/", browser)
    news_title = soup.find("div",class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text
    print(f"Title is: {news_title}")
    print(f"Paragraph is : {news_p}")

    mars_data_dict['title'] = news_title
    mars_data_dict['paragraph'] = news_p
    
    ##### ------------------ For Mars featured Image URL -------------------------------------------------------------
    soup = get_soup_from_url('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars', browser)
    image_src = soup.find("a", class_="fancybox")['data-fancybox-href']
    featured_image_url = "https://www.jpl.nasa.gov" + image_src
    
    mars_data_dict['featured_image_url'] = featured_image_url

    ##### ------------------ For Mars weather -------------------------------------------------------------
    soup = get_soup_from_url("https://twitter.com/marswxreport?lang=en", browser)
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    mars_data_dict['mars_weather'] = mars_weather
    
    ##### ------------------ For Mars facts -------------------------------------------------------------
    url_facts = "https://space-facts.com/mars/"
    table = pd.read_html(url_facts)
    df_mars_facts = table[0]
    df_mars_facts.columns = ["Parameter", "Values"]
    df_mars_facts.set_index(["Parameter"])
    mars_facts_html = df_mars_facts.to_html(header=False, index=False)
    
    mars_data_dict['mars_facts_html'] = mars_facts_html

    ####### ------------------------------ Mars Hemispheres ----------------------------------------------------
    hemi_lists = []

    # Get 1,3,5,7 <a> tags to extract its title & url link for full image 
    for i in range(1,9,2):
        hemi_dict = {}

        hemispheres_soup = get_soup_from_url('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars', browser)
        hemi_name_links = hemispheres_soup.find_all('a', class_='product-item')
        hemi_name = hemi_name_links[i].text.strip('Enhanced')

        detail_links = browser.find_by_css('a.product-item')
        detail_links[i].click()
        time.sleep(1)
        browser.find_link_by_text('Sample').first.click()
        time.sleep(1)
        browser.windows.current = browser.windows[-1] # Keep track of previous window
        hemi_img_html = browser.html # Set as my current browser html as current
        browser.windows.current = browser.windows[0] 
        browser.windows[-1].close() # close the child window

        hemi_img_soup = bs(hemi_img_html, 'html.parser')
        hemi_img_path = hemi_img_soup.find('img')['src']

        hemi_dict['title'] = hemi_name.strip()       
        hemi_dict['img_url'] = hemi_img_path

        hemi_lists.append(hemi_dict)
      
    mars_data_dict['hemi_lists'] = hemi_lists

    browser.quit()
    return mars_data_dict
