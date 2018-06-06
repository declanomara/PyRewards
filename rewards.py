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
from bot import RewardsBot

numSearches = 30
numMobileSearches = 20
authPause = 10
searchPause = 5

starturl = "https://account.microsoft.com/rewards/dashboard"
directory = getpath.get_script_dir()


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
for account in accounts:
    print(account,accounts[account])
for account in accounts:
    username = account
    password = accounts[account]

    rb = RewardsBot(username, password)
    rb.driver = webdriver.Firefox()
    rb.login()
    rb.terms = rb.get_random_queries(numSearches+numMobileSearches)
    rb.visit_PC_search_page()
    rb.do_searches(numSearches, rb.terms)
    rb.driver.close()
