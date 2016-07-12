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
        # driver.find_element_by_xpath("//html").send_keys(Keys.F11) - tried this for the click() bug, looks cooler that way
        signInButton = driver.find_element_by_id("sign-in-button")
        mouseOver = ActionChains(driver).move_to_element(signInButton).perform()
        driver.find_element_by_id("user_login").clear()
        driver.find_element_by_id("user_login").send_keys("gphitme@gmail.com")
        driver.find_element_by_id("user_password").clear()
        driver.find_element_by_id("user_password").send_keys("testPassw0rd")
        driver.find_element_by_id("sign-in-form").submit()
        copyButton = driver.find_element_by_xpath("//*[@id='welcome-page']/div[4]/div[2]/div/div[1]/button")
        ActionChains(driver).move_to_element(copyButton).perform()  # workaround for a click() bug in selenium
        copyButton.send_keys(Keys.RETURN)  # as above

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to.alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to.alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


class openTest(copyPopupTests):
    def runTest(self):
        print "Open test started..."
        driver = self.driver
        # Is pop-up present?
        self.assertTrue(self.is_element_present(By.ID, "copying-popup"))


class closeTest(copyPopupTests):
    def runTest(self):
        print "Close test started..."
        driver = self.driver
        closeButton = driver.find_element_by_xpath("//a[@class='copy-close']")
        closeButton.click()
        # Can pop-up be closed
        self.assertFalse(self.is_element_present(By.ID, "copying-popup"))


class helpTest(copyPopupTests):
    def runTest(self):
        print "Help test started..."
        driver = self.driver
        helpButton = driver.find_element_by_xpath("//a[@class='copy-help-toggle']")
        traderName = driver.find_element_by_xpath("//h4").text
        accountType = driver.find_element_by_xpath("//div[@class='account-name']/span[@class='value']").text
        helpButton.click()
        time.sleep(1)
        # Is help info shown?
        self.assertTrue(self.is_element_present(By.XPATH, "//div[@class='copying-popup-help']"))
        standardText = """Here's how the standard copying works:

Each time """ + traderName.split(' ')[0] + """ creates an order on their """ + accountType + """ account we'll copy the order with size of 0 lots (that's the amount you specified with copied position size)."""
        # Is help info for standard copy shown?
        self.assertTrue(driver.find_element_by_xpath("//div[@class='explanation']").text == standardText)
        dropDown = driver.find_element_by_xpath("//div[@class='dropdown-body']")
        dropDown.click()
        time.sleep(1)
        if driver.find_element_by_xpath("//span[@class='dropdown-body-text']").text == "Tradeo real":
            driver.find_element_by_xpath("//li[contains(.,'Tradeo demo')]").click()
        else:
            driver.find_element_by_xpath("//li[contains(.,'Tradeo real')]").click()
        # Is help info for standard copy shown?
        self.assertTrue(driver.find_element_by_xpath("//div[@class='explanation']").text == standardText)
        dynamicTab = driver.find_element_by_xpath("//span[contains(.,'Dynamic')]")
        dynamicTab.click()
        dynamicText = """Here's how the dynamic copying works:

Each time """ + traderName.split(' ')[0] + """ creates an order on their """ + accountType + """ account we'll copy the order with an approximate size of 0 lots (this is the preferred position size you entered divided by the average leverage of the account you are copying and multiplied by the leverage of the position)."""
        # Is help info for dynamic copy shown?
        self.assertTrue(driver.find_element_by_xpath("//div[@class='explanation']").text == dynamicText)
        dropDown = driver.find_element_by_xpath("//div[@class='dropdown-body']")
        dropDown.click()
        time.sleep(1)
        if driver.find_element_by_xpath("//span[@class='dropdown-body-text']").text == "Tradeo real":
            driver.find_element_by_xpath("//li[contains(.,'Tradeo demo')]").click()
        else:
            driver.find_element_by_xpath("//li[contains(.,'Tradeo real')]").click()
        # Is help info for dynamic copy shown?
        self.assertTrue(driver.find_element_by_xpath("//div[@class='explanation']").text == dynamicText,
                        "Dynamic text is shown incorrectly!")
        driver.find_element_by_xpath("//a[@class='copy-help-close']").click()
        time.sleep(3)
        self.assertTrue(self.is_element_present(By.XPATH, "//div[@class='copying-popup-help' and contains(@style,'display: none')]"))

class realStandardTests(copyPopupTests):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.tradeo.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver
        driver.get(self.base_url)
        # driver.find_element_by_xpath("//html").send_keys(Keys.F11) - tried this for the click() bug, looks cooler that way
        signInButton = driver.find_element_by_id("sign-in-button")
        mouseOver = ActionChains(driver).move_to_element(signInButton).perform()
        driver.find_element_by_id("user_login").clear()
        driver.find_element_by_id("user_login").send_keys("gphitme@gmail.com")
        driver.find_element_by_id("user_password").clear()
        driver.find_element_by_id("user_password").send_keys("testPassw0rd")
        driver.find_element_by_id("sign-in-form").submit()
        # Whole function was copied because of the following line, should've done it smarter
        try:
            copyButton = driver.find_element_by_xpath(
                "//*[@id='welcome-page']/div[4]/div[2]/div/div[contains(.,'Tradeo real')][1]/button")
        except:
            self.fail("No real account found on my account page")
        ActionChains(driver).move_to_element(copyButton).perform()  # workaround for a click() bug in selenium
        copyButton.send_keys(Keys.RETURN)  # as above

    def runTest(self):
        print "Real account standard test started..."
        driver = self.driver
        if driver.find_element_by_xpath("//span[@class='dropdown-body-text']").text == "Tradeo demo":
            dropDown = driver.find_element_by_xpath("//div[@class='dropdown-body']")
            dropDown.click()
            time.sleep(1)
            driver.find_element_by_xpath("//li[contains(.,'Tradeo real')]").click()
        inputField = driver.find_element_by_xpath(
            "//div[@class = 'settings-form standard hidden']//input[@name='copying[data][position_size]']")
        copyButton = driver.find_element_by_xpath("//input[@class='copying-button save']")
        traderName = driver.find_element_by_xpath("//h4").text
        inputField.clear()
        inputField.send_keys("-1")
        # Check if negative value has ignored minus
        self.assertTrue(inputField.get_attribute("value") == "1")
        inputField.clear()
        inputField.send_keys("0")
        copyButton.click()
        # Check that error message is shown (this xpath has more logic than my first Pascal program)
        self.assertTrue(self.is_element_present(By.XPATH,
                                                "//div[@class = 'settings-form standard hidden']//div[@class='error-content' and not(contains(style,'display: block')) and contains(.,'must be greater than or equal to 0.01')]"))
        inputField.clear()
        inputField.send_keys("0.01")
        copyButton.click()
        # Check that the trader is followed
        self.assertTrue(self.is_element_present(By.XPATH,
                                                "//div[@class='copying-wrapper']//span[contains(.,'" + traderName + "')]"))

class realDynamicTests(copyPopupTests):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.tradeo.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver
        driver.get(self.base_url)
        # driver.find_element_by_xpath("//html").send_keys(Keys.F11) - tried this for the click() bug, looks cooler that way
        signInButton = driver.find_element_by_id("sign-in-button")
        mouseOver = ActionChains(driver).move_to_element(signInButton).perform()
        driver.find_element_by_id("user_login").clear()
        driver.find_element_by_id("user_login").send_keys("gphitme@gmail.com")
        driver.find_element_by_id("user_password").clear()
        driver.find_element_by_id("user_password").send_keys("testPassw0rd")
        driver.find_element_by_id("sign-in-form").submit()
        # Whole function was copied because of the following line, should've done it smarter
        try:
            copyButton = driver.find_element_by_xpath(
                "//*[@id='welcome-page']/div[4]/div[2]/div/div[contains(.,'Tradeo real')][1]/button")
        except:
            self.fail("No real account found on my account page")
        ActionChains(driver).move_to_element(copyButton).perform()  # workaround for a click() bug in selenium
        copyButton.send_keys(Keys.RETURN)  # as above

    def runTest(self):
        print "Real account dynamic test started..."
        driver = self.driver
        traderName = driver.find_element_by_xpath("//h4").text
        if driver.find_element_by_xpath("//span[@class='dropdown-body-text']").text == "Tradeo demo":
            dropDown = driver.find_element_by_xpath("//div[@class='dropdown-body']")
            dropDown.click()
            time.sleep(1)
            driver.find_element_by_xpath("//li[contains(.,'Tradeo real')]").click()
        dynamicTab = driver.find_element_by_xpath("//span[contains(.,'Dynamic')]")
        dynamicTab.click()
        preferredField = driver.find_element_by_xpath(
            "//div[@class = 'settings-form dynamic hidden']//input[@name='copying[data][position_size]']")
        maxField = driver.find_element_by_xpath(
            "//div[@class = 'settings-form dynamic hidden']//input[@name='copying[data][max_position_size]']")
        copyButton = driver.find_element_by_xpath("//input[@class='copying-button save']")
        preferredField.clear()
        preferredField.send_keys("-1")
        maxField.clear()
        maxField.send_keys("-1")
        # Check that the fields have ignored the minus
        self.assertTrue(preferredField.get_attribute("value") == "1")
        self.assertTrue(maxField.get_attribute("value") == "1")
        maxField.clear()
        maxField.send_keys("0")
        preferredField.clear()
        preferredField.send_keys("0")
        time.sleep(2)
        copyButton.click()
        # Check that 0 value is not correct
        self.assertTrue(self.is_element_present(By.XPATH,
                                                "//div[@class='settings-form dynamic hidden']//div[@class='field position-size']//div[@class='error-content' and contains(.,'must be greater than 0') and not(contains(style,'display: none'))]"))
        self.assertTrue(self.is_element_present(By.XPATH,
                                                "//div[@class = 'settings-form dynamic hidden']//div[@class='field max-position-size']//div[@class='error-content' and contains(.,'must be greater than 0') and not(contains(style,'display: none'))]"))
        maxField.clear()
        maxField.send_keys("1")
        preferredField.clear()
        preferredField.send_keys("1")
        copyButton.click()
        # Check that the trader is followed
        self.assertTrue(self.is_element_present(By.XPATH,
                                                "//div[@class='copying-wrapper']//span[contains(.,'" + traderName + "')]"))

class demoStandardTests(copyPopupTests):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.tradeo.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver
        driver.get(self.base_url)
        # driver.find_element_by_xpath("//html").send_keys(Keys.F11) - tried this for the click() bug, looks cooler that way
        signInButton = driver.find_element_by_id("sign-in-button")
        mouseOver = ActionChains(driver).move_to_element(signInButton).perform()
        driver.find_element_by_id("user_login").clear()
        driver.find_element_by_id("user_login").send_keys("gphitme@gmail.com")
        driver.find_element_by_id("user_password").clear()
        driver.find_element_by_id("user_password").send_keys("testPassw0rd")
        driver.find_element_by_id("sign-in-form").submit()
        # Whole function was copied because of the following line, should've done it smarter
        try:
            copyButton = driver.find_element_by_xpath(
                "//*[@id='welcome-page']/div[4]/div[2]/div/div[contains(.,'Tradeo demo')][1]/button")
        except:
            self.fail("No demo account found on my account page")
        ActionChains(driver).move_to_element(copyButton).perform()  # workaround for a click() bug in selenium
        copyButton.send_keys(Keys.RETURN)  # as above

    def runTest(self):
        print "Demo account standard test started..."
        driver = self.driver
        if driver.find_element_by_xpath("//span[@class='dropdown-body-text']").text == "Tradeo real":
            dropDown = driver.find_element_by_xpath("//div[@class='dropdown-body']")
            dropDown.click()
            time.sleep(1)
            driver.find_element_by_xpath("//li[contains(.,'Tradeo demo')]").click()
        inputField = driver.find_element_by_xpath(
            "//div[@class = 'settings-form standard hidden']//input[@name='copying[data][position_size]']")
        copyButton = driver.find_element_by_xpath("//input[@class='copying-button save']")
        traderName = driver.find_element_by_xpath("//h4").text
        inputField.clear()
        inputField.send_keys("-1")
        # Check if negative value has ignored minus
        self.assertTrue(inputField.get_attribute("value") == "1")
        inputField.clear()
        inputField.send_keys("0")
        copyButton.click()
        # Check that error message is shown
        self.assertTrue(self.is_element_present(By.XPATH,
                                                "//div[@class = 'settings-form standard hidden']//div[@class='error-content' and not(contains(style,'display: block')) and contains(.,'must be greater than or equal to 0.01')]"))
        inputField.clear()
        inputField.send_keys("0.01")
        copyButton.click()
        # Check that the trader is followed
        self.assertTrue(self.is_element_present(By.XPATH,
                                                "//div[@class='copying-wrapper']//span[contains(.,'" + traderName + "')]"))


class demoDynamicTests(copyPopupTests):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.tradeo.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver
        driver.get(self.base_url)
        # driver.find_element_by_xpath("//html").send_keys(Keys.F11) - tried this for the click() bug, looks cooler that way
        signInButton = driver.find_element_by_id("sign-in-button")
        mouseOver = ActionChains(driver).move_to_element(signInButton).perform()
        driver.find_element_by_id("user_login").clear()
        driver.find_element_by_id("user_login").send_keys("gphitme@gmail.com")
        driver.find_element_by_id("user_password").clear()
        driver.find_element_by_id("user_password").send_keys("testPassw0rd")
        driver.find_element_by_id("sign-in-form").submit()
        # Whole function was copied because of the following line, should've done it smarter
        try:
            copyButton = driver.find_element_by_xpath(
                "//*[@id='welcome-page']/div[4]/div[2]/div/div[contains(.,'Tradeo demo')][1]/button")
        except:
            self.fail("No demo account found on my account page")
        ActionChains(driver).move_to_element(copyButton).perform()  # workaround for a click() bug in selenium
        copyButton.send_keys(Keys.RETURN)  # as above

    def runTest(self):
        print "Demo account dynamic test started..."
        driver = self.driver
        traderName = driver.find_element_by_xpath("//h4").text
        if driver.find_element_by_xpath("//span[@class='dropdown-body-text']").text == "Tradeo real":
            dropDown = driver.find_element_by_xpath("//div[@class='dropdown-body']")
            dropDown.click()
            time.sleep(1)
            driver.find_element_by_xpath("//li[contains(.,'Tradeo demo')]").click()
        dynamicTab = driver.find_element_by_xpath("//span[contains(.,'Dynamic')]")
        dynamicTab.click()
        preferredField = driver.find_element_by_xpath(
            "//div[@class = 'settings-form dynamic hidden']//input[@name='copying[data][position_size]']")
        maxField = driver.find_element_by_xpath(
            "//div[@class = 'settings-form dynamic hidden']//input[@name='copying[data][max_position_size]']")
        copyButton = driver.find_element_by_xpath("//input[@class='copying-button save']")
        preferredField.clear()
        preferredField.send_keys("-1")
        maxField.clear()
        maxField.send_keys("-1")
        # Check that the fields have ignored the minus
        self.assertTrue(preferredField.get_attribute("value") == "1")
        self.assertTrue(maxField.get_attribute("value") == "1")
        maxField.clear()
        maxField.send_keys("0")
        preferredField.clear()
        preferredField.send_keys("0")
        time.sleep(2)
        copyButton.click()
        # Check that 0 value is not correct
        self.assertTrue(self.is_element_present(By.XPATH,
                                                "//div[@class='settings-form dynamic hidden']//div[@class='field position-size']//div[@class='error-content' and contains(.,'must be greater than 0') and not(contains(style,'display: none'))]"))
        self.assertTrue(self.is_element_present(By.XPATH,
                                                "//div[@class = 'settings-form dynamic hidden']//div[@class='field max-position-size']//div[@class='error-content' and contains(.,'must be greater than 0') and not(contains(style,'display: none'))]"))

        maxField.clear()
        maxField.send_keys("1")
        preferredField.clear()
        preferredField.send_keys("1")
        copyButton.click()
        # Check that the trader is followed
        self.assertTrue(self.is_element_present(By.XPATH,
                                                "//div[@class='copying-wrapper']//span[contains(.,'" + traderName + "')]"))


class realOnDemoTests(copyPopupTests):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.tradeo.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver
        driver.get(self.base_url)
        # driver.find_element_by_xpath("//html").send_keys(Keys.F11) - tried this for the click() bug, looks cooler that way
        signInButton = driver.find_element_by_id("sign-in-button")
        mouseOver = ActionChains(driver).move_to_element(signInButton).perform()
        driver.find_element_by_id("user_login").clear()
        driver.find_element_by_id("user_login").send_keys("gphitme@gmail.com")
        driver.find_element_by_id("user_password").clear()
        driver.find_element_by_id("user_password").send_keys("testPassw0rd")
        driver.find_element_by_id("sign-in-form").submit()
        # Whole function was copied because of the following line, should've done it smarter
        try:
            copyButton = driver.find_element_by_xpath(
                "//*[@id='welcome-page']/div[4]/div[2]/div/div[contains(.,'Tradeo demo')][1]/button")
        except:
            self.fail("No demo account found on my account page")
        ActionChains(driver).move_to_element(copyButton).perform()  # workaround for a click() bug in selenium
        copyButton.send_keys(Keys.RETURN)  # as above

    def runTest(self):
        print "Real account on demo account test started..."
        driver = self.driver
        if driver.find_element_by_xpath("//span[@class='dropdown-body-text']").text == "Tradeo demo":
            dropDown = driver.find_element_by_xpath("//div[@class='dropdown-body']")
            dropDown.click()
            time.sleep(1)
            driver.find_element_by_xpath("//li[contains(.,'Tradeo real')]").click()
        self.assertTrue(driver.find_element_by_xpath(
            "//div[@class='not-allowed-copying-text' and contains(.,'Copying between DEMO and REAL accounts is not possible.')]").is_displayed())
        self.assertFalse(driver.find_element_by_xpath("//input[@class='copying-button save']").is_displayed())
        dynamicTab = driver.find_element_by_xpath("//span[contains(.,'Dynamic')]")
        dynamicTab.click()
        self.assertTrue(driver.find_element_by_xpath(
            "//div[@class='not-allowed-copying-text' and contains(.,'Copying between DEMO and REAL accounts is not possible.')]").is_displayed())
        self.assertFalse(driver.find_element_by_xpath("//input[@class='copying-button save']").is_displayed())


class demoOnRealTests(copyPopupTests):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.tradeo.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver
        driver.get(self.base_url)
        # driver.find_element_by_xpath("//html").send_keys(Keys.F11) - tried this for the click() bug, looks cooler that way
        signInButton = driver.find_element_by_id("sign-in-button")
        mouseOver = ActionChains(driver).move_to_element(signInButton).perform()
        driver.find_element_by_id("user_login").clear()
        driver.find_element_by_id("user_login").send_keys("gphitme@gmail.com")
        driver.find_element_by_id("user_password").clear()
        driver.find_element_by_id("user_password").send_keys("testPassw0rd")
        driver.find_element_by_id("sign-in-form").submit()
        # Whole function was copied because of the following line, should've done it smarter
        try:
            copyButton = driver.find_element_by_xpath(
                "//*[@id='welcome-page']/div[4]/div[2]/div/div[contains(.,'Tradeo real')][1]/button")
        except:
            self.fail("No real account found on my account page")
        ActionChains(driver).move_to_element(copyButton).perform()  # workaround for a click() bug in selenium
        copyButton.send_keys(Keys.RETURN)  # as above

    def runTest(self):
        print "Demo account on real account test started..."
        driver = self.driver
        if driver.find_element_by_xpath("//span[@class='dropdown-body-text']").text == "Tradeo real":
            dropDown = driver.find_element_by_xpath("//div[@class='dropdown-body']")
            dropDown.click()
            time.sleep(1)
            driver.find_element_by_xpath("//li[contains(.,'Tradeo demo')]").click()
        self.assertTrue(driver.find_element_by_xpath(
            "//div[@class='not-allowed-copying-text' and contains(.,'Copying between DEMO and REAL accounts is not possible.')]").is_displayed())
        self.assertFalse(driver.find_element_by_xpath("//input[@class='copying-button save']").is_displayed())
        dynamicTab = driver.find_element_by_xpath("//span[contains(.,'Dynamic')]")
        dynamicTab.click()
        self.assertTrue(driver.find_element_by_xpath(
            "//div[@class='not-allowed-copying-text' and contains(.,'Copying between DEMO and REAL accounts is not possible.')]").is_displayed())
        self.assertFalse(driver.find_element_by_xpath("//input[@class='copying-button save']").is_displayed())


class updateStopCopy(copyPopupTests):
    def runTest(self):
        print "Account update/stop copying test started..."
        driver = self.driver
        traderName = driver.find_element_by_xpath("//h4").text
        dropDown = driver.find_element_by_xpath("//div[@class='dropdown-body']")
        dropDown.click()
        driver.find_element_by_xpath("//div[@class='dropdown-menu']//li[@class='']").click()
        inputField = driver.find_element_by_xpath(
            "//div[@class = 'settings-form standard hidden']//input[@name='copying[data][position_size]']")
        copyButton = driver.find_element_by_xpath("//input[@class='copying-button save']")
        inputField.clear()
        inputField.send_keys("1")
        time.sleep(1)
        copyButton.click()
        time.sleep(2)
        followBlock = driver.find_element_by_xpath(
            "//div[@class='copying-wrapper']//span[contains(.,'" + traderName + "')]/parent::a/parent::div")
        followBlock.click()
        time.sleep(1)
        inputField = driver.find_element_by_xpath(
            "//div[@class = 'settings-form standard hidden']//input[@name='copying[data][position_size]']")
        copyButton = driver.find_element_by_xpath("//input[@class='copying-button save']")
        inputField.clear()
        inputField.send_keys("2")
        time.sleep(1)
        copyButton.click()
        time.sleep(2)
        followBlock = driver.find_element_by_xpath(
            "//div[@class='copying-wrapper']//span[contains(.,'" + traderName + "')]/parent::a/parent::div")
        followBlock.click()
        time.sleep(1)
        inputField = driver.find_element_by_xpath(
            "//div[@class = 'settings-form standard hidden']//input[@name='copying[data][position_size]']")
        # Check if value is updated
        self.assertEqual(inputField.get_attribute("value"), "2")
        stopButton = driver.find_element_by_xpath("//input[@class='copying-button stop']")
        stopButton.click()
        time.sleep(1)
        driver.find_element_by_xpath("//button[@class='pretty-confirm-confirm']").click()
        time.sleep(3)
        # Check that we've stopped copying the trader
        self.assertTrue(self.is_element_present(By.XPATH,
                                                "//div[@class='copying-wrapper state-disabled']//span[contains(.,'" + traderName + "')]"))

if __name__ == "__main__":
    unittest.main()

