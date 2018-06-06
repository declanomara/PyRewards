import time
import os
import random
import getpath

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
# Want to replace the time.sleep calls with webdriverwait, but not yet
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC

from BingSelectors import xpath
from load import load_accounts
from log import Logger
from bot import RewardsBot

numSearches = 30
numMobileSearches = 20
authPause = 10
searchPause = 5

starturl = "https://account.microsoft.com/rewards/dashboard"
directory = getpath.get_script_dir()

log = Logger()

accounts = load_accounts('accounts.txt')
#for account in accounts:
#    print(account,accounts[account])
for account in accounts:
    username = account
    password = accounts[account]

    # Create new bot account instance and login
    rb = RewardsBot(username, password)
    rb.driver = webdriver.Firefox()
    rb.login()

    # Get initial points of account to track growth
    initial = rb.get_points()
    initial = int(initial.replace(',', ''))
    msg = "Gathered initial point value of {}, {}".format(username, initial)
    log.log('System', msg)

    # Perform searches to receive points
    rb.terms = rb.get_random_queries(numSearches+numMobileSearches)
    rb.visit_PC_search_page()
    rb.do_searches(numSearches, rb.terms)

    # Get final points of account to track growth
    final = rb.get_points()
    final = int(final.replace(',', ''))
    msg = "Gathered final point value of {}, {}".format(username, final)
    log.log('System', msg)

    growth = final - initial
    msg = "Total growth of {}: {}".format(username, growth)
    log.log('Info', msg)



    rb.driver.close()
