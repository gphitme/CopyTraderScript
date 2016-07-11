
__author__ = "Georgi Petkov"
__date__ = "$2016-7-11 9:33:30$"

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains

import time

import unittest, time, re

class copyPopupTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.tradeo.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver
        driver.get(self.base_url)
        #driver.find_element_by_xpath("//html").send_keys(Keys.F11) - tried this for the click() bug, looks cooler that way
        signInButton = driver.find_element_by_id("sign-in-button")
        mouseOver = ActionChains(driver).move_to_element(signInButton).perform()
        driver.find_element_by_id("user_login").clear()
        driver.find_element_by_id("user_login").send_keys("gphitme@gmail.com")
        driver.find_element_by_id("user_password").clear()
        driver.find_element_by_id("user_password").send_keys("testPassw0rd")
        driver.find_element_by_id("sign-in-form").submit()
        copyButton = driver.find_element_by_xpath("//*[@id='welcome-page']/div[4]/div[2]/div/div[1]/button")
        ActionChains(driver).move_to_element(copyButton).perform() #workaround for a click() bug in selenium
        copyButton.send_keys(Keys.RETURN) #as above

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)
        
class openTest(copyPopupTests):
    def runTest(self):
        print "Open test started..."
        driver = self.driver
        self.assertTrue(self.is_element_present(By.ID,"copying-popup"))
        
class closeTest(copyPopupTests):    
    def runTest(self):
        print "Close test started..."
        driver = self.driver
        closeButton = driver.find_element_by_xpath("//a[@class='copy-close']")
        closeButton.click()
        self.assertFalse(self.is_element_present(By.ID,"copying-popup"))
        
class copyData(copyPopupTests):
    def runTest(self):
        print "Copy data test started..."
        driver = self.driver
        copyUserName = driver.find_element_by_xpath("//h4[contains(@title,.)]").text
        dropDown = driver.find_element_by_xpath("//div[@class='dropdown-body']")
        dropDownText = driver.find_element_by_xpath("//span[@class='dropdown-body-text']")
        self.assertTrue(self.is_element_present(By.XPATH, "//span[@class='dropdown-body-text' and contains(.,'Tradeo demo')]"))
        self.assertTrue(self.is_element_present(By.XPATH,"//div[@class='not-allowed-copying-text']"))
        dropDown.click()
        realAccount = driver.find_element_by_xpath("//li[contains(.,'Tradeo real')]")
        realAccount.click()
        time.sleep(1)
        valueField = driver.find_element_by_xpath("//input[contains(@name,'copying[data][position_size]')]")
        copyButton = driver.find_element_by_xpath("//input[@class='copying-button save']")
        valueField.clear()
        valueField.send_keys("-1")
        time.sleep(1)
        self.assertTrue(valueField.get_attribute('value') == "1")
        valueField.clear()
        valueField.send_keys("0")
        copyButton.click()
        time.sleep(1)
        self.assertTrue(self.is_element_present(By.XPATH, "//div[contains(.,'must be greater than or equal to 0.01')]"))
        valueField.clear()
        valueField.send_keys("0.01")
        copyButton.click();
        self.assertTrue(self.is_element_present(By.XPATH,"//div[contains(@class, 'copying-wrapper') and contains(.,'"+copyUserName+"')]"))

if __name__ == "__main__":
    unittest.main()

#copyDataTest = copyPopupTests('copyData')
#copyDataTest.run()