import time
import os
import random
import getpath

import datetime
from tz import EST5EDT


from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
# Want to replace the time.sleep calls with webdriverwait, but not yet
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC

from BingSelectors import xpath
from load import load_list, load_names
from log import Logger
from random import randint

accounts_to_create = 'accounts_to_create.txt'
account_details = load_list(accounts_to_create)
word_list = 'words.txt'
words = load_list(word_list)

rewards_url ='https://rewards.microsoft.com'
signup_url = 'https://signup.live.com/newuser.aspx'
sleep_time = 1

# XPaths
usernameBox = '//*[@id="MemberName"]'
submitButton = '//*[@id="iSignupAction"]'
passwordBox = '//*[@id="PasswordInput"]'
firstNameBox = '//*[@id="FirstName"]'
lastNameBox = '//*[@id="LastName"]'
monthDropdown = '//*[@id="BirthMonth"]'
dayDropdown = '//*[@id="BirthDay"]'
yearDropdown = '//*[@id="BirthYear"]'
spamBox = '//*[@id="Verification"]/div[2]/div[3]/div/label/span'
verificationBox = '//*[@id="VerificationCode"]'
tryButton = '/html/body/div[1]/div/div[2]/div/ul/li[2]/div/p/a'


# Details
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
days = [str(x) for x in range(1,31)]
years = [str(x) for x in range(1970, 1995)]
names = load_names('names.txt')
first_names = names[0]
last_names = names[1]

'''
print(months)
print(days)
print(years)
'''
def random_password(words):
    first = words[randint(0, len(words))].capitalize()
    second = words[randint(0, len(words))].capitalize()

    return(first+second)

def append_account(filename, credentials):
    with open(filename, 'a') as f:
        f.write("{};{}".format(credentials[0], credentials[1]))

def append(filename, text):
    with open(filename, 'a') as f:
        f.write(text)

def send(xpath, value):
    try:
        elem = driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        print("Couldn't find element specified by xpath: {x}".format(x=xpath))
    elem.send_keys(value)

def click(xpath):
    try:
        elem = driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        print("Couldn't find element specified by xpath: {x}".format(x=xpath))
    elem.click()

for account in account_details:
    username = account
    password = random_password(words)
    print('Generated: {}'.format(password))

    driver = webdriver.Firefox()
    driver.get(signup_url)
    send(usernameBox, username)
    click(submitButton)
    time.sleep(sleep_time)
    send(passwordBox, password)
    click(submitButton)
    time.sleep(sleep_time)
    send(firstNameBox, first_names[randint(0, len(first_names))])
    send(lastNameBox, last_names[randint(0, len(last_names))])
    click(submitButton)
    time.sleep(sleep_time)

    month_dropdown = Select(driver.find_element_by_xpath(monthDropdown))
    month_dropdown.select_by_visible_text(months[randint(0, len(months))])

    day_dropdown = Select(driver.find_element_by_xpath(dayDropdown))
    day_dropdown.select_by_visible_text(days[randint(0, len(days))])

    year_dropdown = Select(driver.find_element_by_xpath(yearDropdown))
    year_dropdown.select_by_visible_text(years[randint(0, len(years))])

    click(submitButton)
    time.sleep(sleep_time)
    click(spamBox)

    msg = 'Input verfication code sent to email: {}\nCode: '.format(username)
    verification_code = str(input(msg))

    send(verificationBox, verification_code)
    send(verificationBox, Keys.RETURN)

    print('Complete captcha')
    input('PRESS ANY KEY TO CONTINUE')

    driver.get(rewards_url)
    click(tryButton)


    timestamp = "#Created {}".format(datetime.datetime.now(tz=EST5EDT()))

    append(account_file, '\n' + timestamp)
    append_account(account_file, (username, password))

    print('Successfully added rewards account: {} {}'.format(username, password))
    append(accounts_to_create, timestamp)






    driver.close()
