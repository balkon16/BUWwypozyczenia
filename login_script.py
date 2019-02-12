# tutaj wstawić wykonywanie skryptu, który do ścieżki będzie dołączał bin virtual environment, a następnie ścieżkę do gecko executable

# the following code starts the virtual environment
import os
import sys

gecko_abs = os.path.abspath('./gecko/')
os.environ['PATH'] = os.environ['PATH'] + ":" + gecko_abs

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

import credentials
import scraping_script

browser = webdriver.Firefox()
browser.set_window_position(0,0)
browser.set_window_size(960,1080)

browser.get('https://chamo.buw.uw.edu.pl/search/query?theme=system')

print("### Finding the form elements ###")
library_card_no = browser.find_element_by_id("h_username")
passwd = browser.find_element_by_id("h_password")
login_button = browser.find_element_by_name("login")

print("### Clearing content from the form ###\n")
library_card_no.clear() #clear any content
passwd.clear() #clear any content

print("### Entering form data ###\n")
library_card_no.send_keys(credentials.login)
passwd.send_keys(credentials.pwd)
login_button.click()

print("### Switching to History tab ###\n")
tab_history = "#tabContents-6"
history_button = browser.find_element_by_xpath('//a[@href="'+tab_history+'"]')
history_button.click()

print("### Start pagination ###\n")

title_next = "Przejdź do następnej strony"

while True:
    next_button = browser.find_element_by_xpath('//*[@title=\"'+title_next+'\"]') #title attribute is the same for all pages
    #print(next_button.get_attribute("href")) #this differ depending on the session

    page = browser.page_source
    print("No of the page: ", scraping_script.find_page_no(page))
    #scraping_script.get_table_rows(page)

    if not next_button.get_attribute("href"): #inactive button has title only
        break
    print("Next page!")
    next_button.click()

    ## function that scrapes the webpage
        ## its logic here
    ##
    scraping_script.get_table_rows(page)




print("### Sleeping for 5 seconds ###\n")
time.sleep(5)

print("### Logging out ###\n")
url_logout = "../../auth/logout?theme=system"
logout_button = browser.find_element_by_xpath('//a[@href="'+url_logout+'"]')
logout_button.click()
