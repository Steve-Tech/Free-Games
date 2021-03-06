#!/usr/bin/python3

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from datetime import datetime
import pickle

import lxml.html
import time

print(datetime.now())

# You will want to replace the user-agent below for yours. Just Google 'what is my user agent' and copy that between the single quotes below
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'

# Find the xpath of a given soup object.
# Full credit goes to ergoithz over at:               https://gist.github.com/ergoithz
# Here is the link to the function on their GitHub:   https://gist.github.com/ergoithz/6cf043e3fdedd1b94fcf
def xpath_soup(element):
    # type: (typing.Union[bs4.element.Tag, bs4.element.NavigableString]) -> str
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:  # type: bs4.element.Tag
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name if 1 == len(siblings) else '%s[%d]' % (
                child.name,
                next(i for i, s in enumerate(siblings, 1) if s is child)
                )
            )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)

# Make a function to actually get the game that we can call later
def getGame():
    time.sleep(7)
    # Re-get the source so that we can look for any "Continue" buttons
    html = BeautifulSoup(browser.page_source, 'lxml')
    try:
        spans = html.find_all('span')
        # Check for a "Continue" button for the 18+ games. If we find it, click it
        for span in spans:
            if span.get_text().upper() == 'CONTINUE':
                # Get the xpath
                xpath = xpath_soup(span)
                # Use the xpath to grab the browser element (so we can click it)
                geez_dad_im_not_a_kid_anymore = browser.find_element_by_xpath(xpath)
                geez_dad_im_not_a_kid_anymore.click()
                break
        time.sleep(7)
    except:
        pass

    # Get the source again, just incase we came from clicking the potential "Continue" button
    html = BeautifulSoup(browser.page_source, 'lxml')

    # Get all the button tags so we can see whether we need to grab the game or leave
    buttons = html.find_all('button')
    
    for button in buttons:
        if button.get_text().upper() == 'OWNED':
            print('already owned')
            break
        if button.get_text().upper() == 'GET':
            # Get the xpath of this button
            xpath = xpath_soup(button)
            # Use the xpath to grab the browser element (so we can click it)
            browser_element = browser.find_element_by_xpath(xpath)
            browser_element.click()
            time.sleep(4)

            # Re-get the source (again)
            html = BeautifulSoup(browser.page_source, 'lxml')
            # Get all the spans so we can get the "Place Order" button
            spans = html.find_all('span')

            for span in spans:
                if span.get_text().upper() == 'PLACE ORDER':
                    print('placing order')
                    # Get the xpath
                    xpath = xpath_soup(span)
                    # Use the xpath to grab the browser element (so we can click it)
                    purchase_button_element = browser.find_element_by_xpath(xpath)
                    # Create object and add it to the list
                    purchase_button_element.click()
                    break
            # If the EULA prompt shows up, click it
            try:
                browser.find_element_by_xpath('''//span[contains(text(),'I Agree')]''')
            except:
                pass
            else:
                EU_Refund_and_Right_of_Withdrawal_Information = browser.find_element_by_xpath('''//span[contains(text(),'I Agree')]''')
                EU_Refund_and_Right_of_Withdrawal_Information.click()
                time.sleep(2)
            # We only want the first one (usually the game), so leave
            break


##### MAIN #####

# Main store page for Epic Games Store
web_path = '''https://www.epicgames.com/store/en-US'''

profile = webdriver.FirefoxProfile()

# We will use the user-agent to trick the website into thinking we are a real person. This usually subverts most basic security
profile.set_preference("general.useragent.override", user_agent)

options = FirefoxOptions()
#options.add_argument("--headless")

# Setup the browser object to use our modified profile
browser = webdriver.Firefox(profile, options=options)

# Load the cookies and load page
browser.get(web_path)
for cookie in pickle.load(open("EpicCookies.pkl", "rb")):
    browser.add_cookie(cookie)
browser.get(web_path + "/free-games")


# Give the page enough time to load before grabbing the source text
# If you get any weird errors related to 'root' or anything, start here and adjust the time
time.sleep(4)

# Grab the source text, and make a beautiful soup object
html = BeautifulSoup(browser.page_source, 'lxml')

# Check for, and close, the cookies banner
try:
    browser.find_element_by_xpath('''/html/body/div/div/div[4]/header/div/button/span''')
except:
    pass
else:
    cookies = browser.find_element_by_xpath('''/html/body/div/div/div[4]/header/div/button/span''')
    print('closing cookie banner')
    cookies.click()
    time.sleep(2)

# Get all the span tags to make sure we get every available game
spans = html.find_all('span')

# Create a list for all the game dictionaries
games = []
for span in spans:
    if span.get_text().upper() == 'FREE NOW' or span.get_text().upper() == 'FREE NOW | REQUIRES 2FA':
        print('found free game')
        # Get the xpath
        xpath = xpath_soup(span)
        # Use the xpath to grab the browser element (so we can click it)
        browser_element = browser.find_element_by_xpath(xpath)
        # Create object and add it to the list
        games.append({'xpath': xpath,
                        'element': browser_element
                        })

print('enumerating games')
# Go thru each game we found and get it!
for index, game in enumerate(games):
    print('clicking game')
    game['element'].click()
    getGame()
    # Go back to the store page to get the other game
    browser.get(web_path + "/free-games")
    # Give the page enough time to load before grabbing the source text
    time.sleep(5)
    # Selenium complains this object no longer exists, so we need to re-get it so it doesn't explode
    try:
        games[index + 1]['element'] = browser.find_element_by_xpath(games[index + 1]['xpath'])
    except:
        break
    

pickle.dump(browser.get_cookies(), open("EpicCookies.pkl","wb"))

# Close everything
browser.quit()
print('done.')