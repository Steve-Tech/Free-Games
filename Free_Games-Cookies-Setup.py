#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import pickle

# You will want to replace the user-agent below for yours. Just Google 'what is my user agent' and copy that between the single quotes below
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'

# Main store page for Epic Games Store
web_path = '''https://www.epicgames.com/store/en-US'''

profile = webdriver.FirefoxProfile()

# We will use the user-agent to trick the website into thinking we are a real person. This usually subverts most basic security
profile.set_preference("general.useragent.override", user_agent)

options = FirefoxOptions()

# Setup the browser object to use our modified profile
browser = webdriver.Firefox(profile, options=options)

# Get login page then wait for a human to login and save cookies
browser.get(web_path + '/login')
input("Press enter to save cookies...")
pickle.dump(browser.get_cookies(), open("EpicCookies.pkl","wb"))

browser.quit()