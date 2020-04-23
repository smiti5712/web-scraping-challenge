#import dependencies 
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time


def init_browser():
    executable_path = {'executable_path':'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=True)

    
def scrape():
    mars_info = {}

   
    # Mars News 
    browser = init_browser()
    #visit Mars NASA url for latest news
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(5)

    # HTML object
    html = browser.html
    
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    #get the latest news title and teaser paragraph
    news_title =soup.find('div', class_='list_text').find('div', class_='content_title').text
    
    news_p = soup.find('div', class_='list_text').find('div', class_='article_teaser_body').text

    # populate dictionary from MARS NEWS
    mars_info['news_title'] = news_title
    mars_info['news_p'] = news_p

    browser.quit()
      
    
    # Featured Image
    browser = init_browser()

    # visit JPL mars Space Images site 
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)

    # using splinter click on Full Image button
    browser.links.find_by_partial_text('FULL IMAGE').click()

    # using splinter click on more info
    browser.links.find_by_partial_text('more info').click()
    time.sleep(5)

    # get the html of current page and get the featured image URL
    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")

    image_url = image_soup.find("figure",class_="lede").a["href"]

    base_url = "https://www.jpl.nasa.gov"
    featured_image_url = base_url+image_url
    
    mars_info['featured_image_url'] = featured_image_url

    browser.quit()

    
     
    # Mars Weather
    browser = init_browser()

    # visit Mars Weather in twitter
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    time.sleep(5)

    # HTML Object and creating soup with HTML parser
    html = browser.html
    
    weather_soup = BeautifulSoup(html, "html.parser")

    # find all span tags and store in spans list
    spans = weather_soup.find_all('span')
    
    # for every span look for the text sol, low and high that indicates it is a tweet about weather and store it in a variable
    for span in spans:
        if 'sol' and 'low' and 'high' in span.text.lower():
            mars_weather = span.text
            mars_info['mars_weather'] = mars_weather
            #break the loop if the first weather tweet is found, since we need only the latest tweet
            break
        else: 
            pass
         

    browser.quit()





    # Visit Mars facts site 
    facts_url = 'http://space-facts.com/mars/'

    # reading HTML using Panadas
    mars_facts_tables = pd.read_html(facts_url) 

    # get the first table
    mars_facts_df = mars_facts_tables[0]

    #Define columns
    mars_facts_df.columns = ['Description','Value']

    # Set Description as index
    mars_facts_df.set_index('Description', inplace=True)

    # store table as html string 
    mars_facts_html=mars_facts_df.to_html()
     
    mars_info['mars_facts_html'] = mars_facts_html

    

    # Mars hemispheres
    browser = init_browser()   

    # Visit astrogeology site 
    astrogeology_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(astrogeology_url)
    time.sleep(5)

    #HTML Object and creating soup with HTML parser
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    #loop thru the div tags and class = item to get all products
    products = soup.find_all("div",class_="item")

    #empty array to hold the title text that will be used later to click
    hemispheres=[]

    #loop through the products and get h3 text, i.e the names of the hemispheres
    for product in products:
    
        #get the h3 test and split thatbased on space , pick the first word
        h3_partial_text = product.h3.text.split(" ")[0]
    
        #append te h3 partial text to hemispheres array
        hemispheres.append(h3_partial_text)

    #empty list
    hemisphere_image_urls = []

    #loop through the hemispheres retrived above
    for hemisphere in hemispheres:
       
        #using splinter click on the link
        browser.links.find_by_partial_text(hemisphere).click()
        time.sleep(5)
    
        #create html object and parse
        html = browser.html
        hem_soup = BeautifulSoup(html, "html.parser")
    
        #get title and store it in dict
        title = hem_soup.find("div",class_="content").find("h2",class_="title").text
      
    
        #get all li tags
        lis = hem_soup.find("div",class_="downloads").find_all("li")
    
        #loop through the li tags
        for li in lis:
        
        #there are 2 image links, we want to get the image url for the "sample"
            if "sample" in li.text.lower():
                img_url = li.a["href"]
                                
        #append to the list
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    
        #using splinter have the browser go back, so the next hemisphere can be clicked
        browser.back()

    mars_info['hemisphere_image_urls'] = hemisphere_image_urls

    browser.quit()

    return mars_info
    












    
