from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv
import json

option = webdriver.ChromeOptions()
# I use the following options as my machine is a window subsystem linux. 
# I recommend to use the headless option at least, out of the 3
option.add_argument('--headless')
option.add_argument('--no-sandbox')
option.add_argument('--disable-dev-sh-usage')
# Replace YOUR-PATH-TO-CHROMEDRIVER with your chromedriver location
option.binary_location = "/usr/bin/google-chrome-stable" # "/opt/google/chrome/"
driver = webdriver.Chrome('/home/andy/Learning/Prog/Downloads/ChromeDriver/chromedriver', options=option)

# Author is already selected (it's me, Andrei Oskin)
# Default author link
#page = driver.get('https://inspirehep.net/authors/1774228') # Getting page HTML through request
# 100 per page
page = driver.get('https://inspirehep.net/literature?sort=mostrecent&size=100&page=1&q=Andrei%20Oskin')
soup = BeautifulSoup(driver.page_source, 'html.parser') # Parsing content using beautifulsoup

totalScrapedInfo = [] # In this list we will save all the information we scrape

# For By class
# ID = "id"
# XPATH = "xpath"
# LINK_TEXT = "link text"
# PARTIAL_LINK_TEXT = "partial link text"
# NAME = "name"
# TAG_NAME = "tag name"
# CLASS_NAME = "class name"
# CSS_SELECTOR = "css selector"

# Need to increase time here to avoid failure
WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test-id='search-results']")))  # We are waiting for 5 seconds for our element with the attribute data-testid set as `firstListCardGroup-editorial`
listElements = driver.find_elements(By.CSS_SELECTOR, "[data-test-id='literature-result-title-link']") # Extracting the editorial lists elements
links = []
for el in listElements[41:43]:
    #listNames.append(el.text)
    print()
    ArticleTitle = el.text
    #ArticleTitle.replace('\r', ' ').replace('\n', ' ')
    ArticleTitle = " ".join(ArticleTitle.split())
    print(ArticleTitle)
    print(el.get_attribute('href'))
    links.append(el.get_attribute('href'))

print('\n', '-----------------------------------------------', '\n')

for link in links:
    driver.get(link)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "mt3")))
    ArticleTitle = driver.find_element(By.CLASS_NAME, "__Latex__")
    ArticleTitle_str = " ".join(ArticleTitle.text.split())
    print(ArticleTitle_str)
    attributes = driver.find_element(By.CLASS_NAME, "mt3")
    #attributes = driver.find_elements(By.CSS_SELECTOR, "[class='mt3']")
    #
    attrs = attributes.find_elements(By.CLASS_NAME, "__InlineList__")
    print('number of attributes = ', len(attrs))
    print()
    print(attributes.text)
    print()
    Links_inside = attributes.find_elements(By.CSS_SELECTOR, "[target='_blank']")
    for link_inside in Links_inside:
        print(link_inside.text, ' -> ', link_inside.get_attribute('href'))
    print()
    # Try to click on cite
    cite_button = driver.find_element(By.CSS_SELECTOR, "[class='ant-btn']")
    print('Site button -> ', cite_button.text)
    cite_button.click()
    #driver.implicitly_wait(100) # seconds
    WebDriverWait(driver, 30).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "[role='document']"), 'author'))
    #WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CLASS_NAME, "anticon anticon-download")))
    #test = driver.find_elements(By.CLASS_NAME, "ant-row")
    cite_window = driver.find_element(By.CSS_SELECTOR, "[role='document']")
    test = cite_window.find_element(By.CLASS_NAME, 'ant-row')
    #print(cite_window.text)
    print(test.text)
    #print('How many of these elements on page -> ', len(test))
    print('#################################################')