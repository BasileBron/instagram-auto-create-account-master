#!/usr/bin/python3
from random import choice
import random
import string
import sys
import os
from selenium import webdriver
from random import randint
import time
import logging
from selenium.webdriver.common.by import By

# create and configure logger
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
current_directory = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(filename = current_directory + "/" +"log.txt",
                    #reminder of the levels : NOTSET, DEBUG ,INFO, WARNING, ERROR, CRITICAL
                    level = logging.DEBUG,
                    format = LOG_FORMAT,
                    filemode = 'w')
logger = logging.getLogger()

def gen_password():
    """Generate a password."""
    characters = string.ascii_letters + string.punctuation  + string.digits
    password =  "".join(choice(characters) for x in range(randint(8, 16)))
    return password

def gen_nickname():
    """Generate a nickname."""
    logger.info("generating a nickname")

    #GENERATE NICKNAME/username
    VOWELS = "aeiou"
    CONSONANTS = "".join(set(string.ascii_lowercase) - set(VOWELS))
    nickname = ""
    for i in range(6):
        if i % 2 == 0:
            nickname += random.choice(CONSONANTS)
        else:
            nickname += random.choice(VOWELS)
    return nickname

class User:
    """The class User is the fictionnal character whom you will create an account
    here is the attributes of this object :
    nickname, first_name, last_name, full_name, email, tags

    Exemple of creation : User("tattoo, art, drawing, travel")
    """
    def __init__(self, tags):
        logger.info("initialisation of a new user")
        self.tags = list(tags.split(","))
        self.nickname = gen_nickname()
        self.first_name = self.nickname
        self.last_name = gen_nickname()
        self.email =  self.first_name + '.' + self.last_name
        self.password = gen_password()
        logger.info("\n<nickname : %s>\n<first_name : %s>\n<last_name : %s>\n<tags : %s>" % (self.nickname, self.first_name, self.last_name, self.tags))
    def full_name(self):
        logger.info("returning fullname")
        """Return the full name of the user."""
        return '{} {}'.format(self.first_name, self.last_name)
    def username(self):
        logger.info("returning username")
        """Return the username of the user."""
        return (self.nickname+ "_" +self.tags[0])
    def register_email(self):
        logger.info("Email registering of the user :", self.nickname)
        try:
            """Register new email account on mail.ru"""
            browser= webdriver.Chrome('chromedriver.exe')
            browser.get("https://account.mail.ru/signup?rf=auth.mail.ru&from=main")
            time.sleep(1) #time.sleep count can be changed depending on the Internet speed.
            name = self.username()

            #Fill the fullname value
            fullname_field = browser.find_element_by_xpath('//*[@id="app-canvas"]/div/div/div/div[1]/div[3]/form/div[3]/div/div/div[1]/div/div[2]/div[1]/input')
            fullname_field.send_keys(self.first_name)
            #Fill username value
            username_field = browser.find_element_by_xpath('//*[@id="app-canvas"]/div/div/div/div[1]/div[3]/form/div[3]/div/div/div[2]/div/div[2]/div[1]/input')
            username_field.send_keys(self.last_name)
            #click gender #triiigered
            browser.find_element_by_xpath(".//*[contains(text(), 'Мужской')]").click()
            #Fill the email value
            email_field = browser.find_element_by_xpath('//*[@id="app-canvas"]/div/div/div/div[1]/div[3]/form/div[6]/div/div[2]/div[1]/div/div[1]/span[3]/input')
            email_field.send_keys(self.email)

            #Fill password value
            password_field  = browser.find_element_by_name('password')
            password_field.send_keys(self.password) #You can determine another password here.

            #Fill password RETRY value
            password_field  = browser.find_element_by_xpath('//*[@id="passwordRetry"]')
            password_field.send_keys(self.password) #You can determine another password here.
            time.sleep(4)
            #click day born
            #DOBday = browser.find_element_by_xpath('//*[@name="birthdate"]/div[2]/div[1]/div/div[2]/select')
            DOBday= browser.find_element_by_css_selector('input[placeholder="День"]')
            #DOBday.click()
        except Exception as e:
            raise

    def register_instagram(self):
        """register a new account on instagram"""
        logger.info("Instagram registering of the user :", self.nickname)
        try:
            browser= webdriver.Chrome('chromedriver.exe')
            browser.get("http://www.instagram.com")
            time.sleep(2) #time.sleep count can be changed depending on the Internet speed.
            name = self.last_name
            #Fill the email value
            email_field = browser.find_element_by_name('emailOrPhone')
            email_field.send_keys(self.email)
            #Fill the fullname value
            fullname_field = browser.find_element_by_name('fullName')
            fullname_field.send_keys(self.full_name())
            #Fill username value
            username_field = browser.find_element_by_name('username')
            username_field.send_keys(self.username())
            #Fill password value
            password_field  = browser.find_element_by_name('password')
            password_field.send_keys(self.password) #You can determine another password here.
            #submit form
            submit = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[7]/div/button')
            submit.click()
            time.sleep(1)
            #check age restriction
            age_check = browser.find_element_by_xpath('//*[@id="igCoreRadioButtonageRadioabove_18"]')
            age_check.click()
            time.sleep(1)
            #validate age restriction
            age_validation = browser.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/button')
            #age_validation.click()
            time.sleep(1)
        except Exception as e:
            raise

#debug
user1 = User("tattoo, drawing, travel, art")
user1.register_email()
user1.register_instagram()
#open log file
os.startfile('log.txt')
