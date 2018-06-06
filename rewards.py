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

log = Logger('System')

def get_offer_points():
    allOfferCardTitles = driver.find_elements_by_xpath(xpath['rewardsHomeCardTitle'])
    allOfferCardStatuses = driver.find_elements_by_xpath(xpath['rewardsHomeCardCheckmarkOrChevron'])
    allVisibleOfferCardStatuses = [x for x in allOfferCardStatuses if x.is_displayed()]

    allOfferCardPoints = driver.find_elements_by_xpath(xpath['rewardsHomeCardPoints'])
    allVisibleOfferCardPoints = [x for x in allOfferCardPoints if x.is_displayed()]

    for i in range(0,len(allVisibleOfferCardStatuses)):
        elem = allVisibleOfferCardStatuses[i]
        if "mee-icon-ChevronRight" in elem.get_attribute("class"):
            titleElem = allOfferCardTitles[i]

            # Got to clean this up
            if "Quiz" in titleElem.text or "quiz" in titleElem.text:
                numPointsStr = allVisibleOfferCardPoints[i].text.replace(' POINTS','')
                elem.click()
                time.sleep(searchPause)
                currTab = driver.window_handles[0]
                newTab = driver.window_handles[-1]
                driver.switch_to_window(newTab)
                click(xpath['startQuizButton'])
                solve_quiz(int(numPointsStr))
                driver.close()
                driver.switch_to_window(currTab)
                get_offer_points()
                return
            else:
                elem.click()
                time.sleep(searchPause)
                currTab = driver.window_handles[0]
                newTab = driver.window_handles[-1]
                driver.switch_to_window(newTab)
                driver.close()
                driver.switch_to_window(currTab)
                get_offer_points()
                return



accounts = load_accounts('accounts.txt')
log.log('System', accounts)
msg = "Botting {} accounts:".format(len(accounts.items()))
for account in accounts:
    msg += "\n{}".format(account)

log.log('Info', msg)
for account in accounts:
    username = account
    password = accounts[account]

    # Create new bot account instance and login
    rb = RewardsBot(username, password)
    rb.terms = rb.get_random_queries(numSearches+numMobileSearches)




    # Perform searches to receive points
    rb.set_pc()
    log.log('System', 'Using PC user agent')

    # Get initial points of account to track growth
    initial = rb.get_points()
    initial = int(initial.replace(',', ''))
    msg = "Gathered initial point value of {}, {}".format(username, initial)
    log.log('System', msg)

    rb.visit_search_page()

    rb.do_searches(numSearches, rb.terms)
    rb.driver.close()

    rb.set_mobile()
    log.log('System', 'Using mobile user agent')
    rb.visit_search_page()
    rb.do_searches(numMobileSearches, rb.terms)

    # Get final points of account to track growth
    final = rb.get_points()
    final = int(final.replace(',', ''))
    msg = "Gathered final point value of {}, {}".format(username, final)
    log.log('System', msg)


    growth = final - initial
    msg = "Total growth of {}: {}".format(username, growth)
    log.log('Info', msg)
    


    rb.driver.close()
