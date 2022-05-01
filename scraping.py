# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title,news_paragraph= mars_news(browser)
    #this say python that we will be using mars_news to pull this data

    #cretar the data dictionary
    # #store all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "hemispheres": hemisphere(browser),
      "last_modified": dt.datetime.now()
      

      
    }

    # Stop webdriver and return data
    browser.quit()
    return data

# Visit the mars nasa news site
def mars_news(browser):
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    try:
        #This variable holds a ton of information, so look inside of that information to find this specific data." 
        #The data we're looking for is the content title, which we've specified by saying, #
        #"The specific data is in a <div /> with a class of 'content_title'."
        slide_elem = news_soup.select_one('div.list_text')

        news_title=slide_elem.find('div', class_='content_title').get_text()
        #news_title

        #news_title.get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        #news_p
    except AttributeError:
        return None, None

    return news_title, news_p
# ### Featured Images mars

def featured_image(browser):
    # Visit U
    url='https://spaceimages-mars.com/'
    browser.visit(url)

    full_image=browser.find_by_tag('button')[1]
    full_image.click()

    #With the new page loaded onto our automated browser, it needs to be parsed so we can continue and scrape the full-size image URL.
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    #An img tag is nested within this HTML, so we've included it.
    #.get('src') pulls the link to the image.
    try:
        img_url=img_soup.find('img',class_='fancybox-image').get('src')
        img_url
    #This is where the image we want lives—use the link that's inside these tags."
    except AttributeError:
        return None

    img_url_complete=f'{url}{img_url}'
    return img_url_complete

######mars facts table
def mars_facts():
    try:
        # use 'read_html" to scrape the facts table into a dataframe
        df=pd.read_html('https://galaxyfacts-mars.com/')[0]
        #df.columns=['Description', 'Mars', 'Earth']
        #df.set_index('Description',inplace=True)
        #df
    except BaseException:
      return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)


    return df.to_html(classes="table table-striped")

def hemisphere(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)


    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []


    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    for x in range (4):
        
        link=browser.find_by_css('a.product-item h3')[x]
        link.click()

        html = browser.html
        hemis_soup = soup(html, 'html.parser')
    
        hemis_url = hemis_soup.find('img',class_='wide-image').get('src')
        
        
        complete_url=f'{url}{hemis_url}'
        
        
        title = hemis_soup.find('h2', class_='title').text
        
        hemispheres = {}
        hemispheres['title'] = title
        hemispheres['img_url'] = complete_url
    
        hemisphere_image_urls.append(hemispheres)
        
        browser.back()

    return hemisphere_image_urls


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())






