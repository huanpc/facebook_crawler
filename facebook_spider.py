#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import json
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = ROOT_DIR + "/data"
LIB_DIR = ROOT_DIR + "/lib"
CHROME_PROFILE = ROOT_DIR + "/ChromeProfile/Profile"
FACEBOOK_LOGIN_URL = "https://www.facebook.com/login.php"
FB_URL_LIKERS = "https://www.facebook.com/search/{page_id}/likers"
FB_USER_PAGE_URL = "https://www.facebook.com/profile.php?id={fb_id}"

class FacebookSpider(object):

    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.driver = None
        self.init_chrome()
        self.login_facebook()

    def init_chrome(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--incognito")
        options.add_argument("--lang=en")
        options.add_argument('--user-data-dir=' + CHROME_PROFILE)
        options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(LIB_DIR + "/chromedriver", chrome_options=options)
        self.driver.set_window_size(1920, 1080)

    def login_facebook(self):
        self.driver.get(FACEBOOK_LOGIN_URL)
        time.sleep(2)
        self.driver.find_element_by_id('email').send_keys(self.user)
        self.driver.find_element_by_id("pass").send_keys(self.password)
        self.driver.find_element_by_id('loginbutton').click()

    def get_page_likers(self, page_id, limit=1000):
        try:
            self.driver.get(FB_URL_LIKERS.format(page_id=page_id))
            time.sleep(5)
            likers = []
            i = 0
            while len(likers) < limit:
                try:
                    i += 1
                    elems = self.driver.find_elements_by_xpath('//div[contains(@class,"_3u1 _gli _uvb")]')
                    if len(elems) == 0:
                        break
                    for elem in elems[len(likers):]:
                        meta_raw = elem.get_attribute('data-bt')
                        meta_json = dict(json.loads(meta_raw))
                        fb_id = meta_json['id']
                        rank = meta_json['rank']
                        full_name = elem.find_element_by_xpath('.//a[@class="_32mo"]/span').text
                        job_e = elem.find_element_by_xpath('.//div[@class="_pac"]').text
                        extra_e = elem.find_elements_by_xpath('.//div[@class="_glo"]//div[@class="_52eh"]')
                        extra = []
                        for item in extra_e:
                            extra.append(item.text)
                        extra.append(job_e)
                        likers.append({'id': fb_id, 'rank': rank, 'full_name': full_name, 'extra': extra})
                    self.driver.execute_script("window.scrollBy(0,1080*5)", "")
                    time.sleep(1)
                    print ">>> page: " + str(i) + "|count:" + str(len(likers))

                except Exception as e:
                    print "[ERROR] Search likers", e
            return likers
        except Exception as e:
            print "### Exception: ", e

    def get_page_about_category(self, page_url):
        self.driver.get(page_url)
        about_categories = []
        elements = self.driver.find_elements_by_css_selector("a[href*=page_about_category]")

        if elements is not None and len(elements) > 0:
            for ele in elements:
                about_categories.append(ele.text)
        return about_categories

    def get_user_profile_page(self, fb_id):
        self.driver.get(FB_USER_PAGE_URL.format(fb_id=fb_id))
        time.sleep(2)
        about = []
        ava_ele = self.driver.find_element_by_xpath('//a[contains(@class, "profilePicThumb")]/img')
        avatar_url = ava_ele.get_attribute('src')
        name = self.driver.find_element_by_xpath('//span[@id="fb-timeline-cover-name"]/a').text
        about_eles = self.driver.find_elements_by_xpath('//div[@id="intro_container_id"]//div[contains(@class, "textContent")]')
        for ele in about_eles:
            es = ele.find_elements_by_xpath("./div//text()")
            about.append(" ".join([e.text for e in es]))
        return {'name': name, 'avatar_url': avatar_url, 'about': about}

