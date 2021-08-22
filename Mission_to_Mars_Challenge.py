
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')
slide_elem.find('div', class_='content_title')

# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()


# ### JPL Space Images Featured Image
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup

# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)
# Parse the resulting html with soup
html = browser.html
thumb_soup = soup(html, 'html.parser')

#retrieve links to full res images
results = thumb_soup.find_all('div', class_='description')
hemispheres = []
for result in results:
    thumb_url_r = result.find('a', class_='itemLink').get('href') 
    thumb_url = f'https://marshemispheres.com/{thumb_url_r}'
    hemispheres.append(thumb_url)
hemispheres

hemisphere_image_urls = []
#surf through links to get image link and title
for url in hemispheres:
    browser.visit(url)
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    results = img_soup.find_all('div', class_='downloads')
    
    for result in results:
        res = result.ul.li
        # Identify and return link to listing
        img_url_r = res.a['href']
        #compose absolute path
        img_url = f'https://marshemispheres.com/{img_url_r}'
        
    #parse title    
    title = img_soup.find('h2', class_='title').text
    #make dictionary of each image url and title
    b = {
        'img_url': img_url,
        'title': title,        
    }
    #add dictionary to a list
    hemisphere_image_urls.append(b)
    
    #return to original page
    browser.back()

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()


