import time
import os
import random
import argparse
import getpath

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
# Want to replace the time.sleep calls with webdriverwait, but not yet
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from BingSelectors import xpath


class RewardsBot:
    def __init__(self, usnm, pswd):
        self.username = usnm
        self.password = pswd
        self.numSearches = 30
        self.numMobileSearches = 20
        self.authPause = 10
        self.searchPause = 5
        self.profile = None
        self.driver = None
        self.mobile = False

        self.starturl = "https://account.microsoft.com/rewards/dashboard"
        self.directory = getpath.get_script_dir()

    def get_random_queries(self, numQueries):
        with open(os.path.join(self.directory, "queries"), "r") as queryTxtfile:
            allWords = list(queryTxtfile)

        queries = set()
        while len(queries) < numQueries:
            queries.add(random.choice(allWords).rstrip())
        return queries

    def get_points(self):
        if self.driver.current_url == 'https://account.microsoft.com/rewards':
            pass
        else:
            self.driver.get('https://account.microsoft.com/rewards')

        time.sleep(5)
        source = self.driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        content = soup.find_all('p', {'class':'bold number margin-top-1'})
        points = content[0].text

        return points

    def get_offer_points(self):
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

    def do_searches(self, numSearches, searchQueries):
        for _ in range(0, numSearches):
            try:
                if self.mobile:
                    term = searchQueries.pop().replace(' ', '+')
                    url = "https://www.bing.com/?q={}".format(term)
                    self.driver.get(url)
                    time.sleep(self.searchPause)
                else:
                    self.clear(xpath['search'])
                    self.send(xpath['search'], searchQueries.pop())
                    self.click(xpath['searchButton'])
                    time.sleep(self.searchPause)
            except selenium.common.exceptions.UnexpectedAlertPresentException:
                alert = browser.switch_to.alert
                alert.accept()
                




    def visit_search_page(self):
        self.driver.get('https://www.bing.com')

    def set_pc(self):
        self.mobile = False
        self.profile = webdriver.FirefoxProfile('/home/declan/.mozilla/firefox/18he6f1k.auto')
        userAgentString = "Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0"
        self.profile.set_preference("general.useragent.override", userAgentString)
        self.driver = webdriver.Firefox(self.profile)
        self.login()

    def set_mobile(self):
        self.mobile = True
        self.profile = webdriver.FirefoxProfile('/home/declan/.mozilla/firefox/18he6f1k.auto')
        userAgentString = "Mozilla/5.0 (Android 5.0.1; Mobile; rv:58.0) Gecko/58.0 Firefox/58.0"
        self.profile.set_preference("general.useragent.override", userAgentString)
        self.driver = webdriver.Firefox(self.profile)
        self.login()

    def clear(self, xpath):
        try:
            elem = self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            print("Couldn't find element specified by xpath: {x}".format(x=xpath))
        elem.clear()

    # Send to element by xpath
    def send(self, xpath, value):
        try:
            elem = self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            print("Couldn't find element specified by xpath: {x}".format(x=xpath))
        elem.send_keys(value)

    # "click" elements by xpath
    def click(self, xpath):
        try:
            elem = self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            print("Couldn't find element specified by xpath: {x}".format(x=xpath))
        elem.click()

    # Authenticate Bing Rewards Account
    def login(self):
        #self.driver.maximize_window()
        #self.driver.set_window_size(0, 0)
        self.driver.set_window_position(-2000, 0)
        self.driver.get(self.starturl)
        self.click(xpath['signInLink'])
        time.sleep(self.authPause/2)
        self.send(xpath['usernameBox'], self.username)
        self.click(xpath['submit'])
        time.sleep(self.authPause/4)
        self.send(xpath['pswdBox'], self.password)
        self.click(xpath['submit'])
        time.sleep(self.authPause)
