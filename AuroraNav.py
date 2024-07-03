from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import os
import time


class AuroraNav:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.auroraHomeLink = (
            "https://aurora.umanitoba.ca/ssb/twbkwbis.P_GenMenu?name=bmenu.P_MainMnu"
        )

        self.OpenAurora()
        self.Login(os.getenv("AURORA_USER"), os.getenv("AURORA_PASS"))

        self.GoToPage("Enrolment & Academic Records")
        self.GoToPage("Registration and Exams")
        self.GoToPage("Look Up Classes")

        self.SelectTerm("Fall 2024")
        self.SelectDepartment("MATH")
        print(self.GetPageContents())
        input()

    def OpenAurora(self):
        self.driver.get(self.auroraHomeLink)

    def Login(self, username: str, password: str):
        usernameField = self.driver.find_element(By.NAME, "sid")
        passwordField = self.driver.find_element(By.NAME, "PIN")
        loginButton = self.driver.find_elements(By.XPATH, "//input[@value='Login']")[0]

        usernameField.send_keys(username)
        passwordField.send_keys(password)
        loginButton.click()

        # In case new aurora breaks my automated login, this gives the user a chance to login and allow it to continue.
        WebDriverWait(self.driver, 300).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Main Menu')]")
            )
        )

    def GoToPage(self, name: str):
        self.driver.find_element(By.XPATH, "//*[contains(text(), '%s')]" % name).click()

    def HomePage(self):
        self.driver.get(self.auroraHomeLink)

    def GetPageContents(self):
        return self.driver.page_source

    def NewAuroraTab(self) -> int:
        numTabs = len(self.driver.window_handles)
        self.driver.execute_script("""window.open("url","_blank");""")
        self.driver.switch_to.window(self.driver.window_handles[numTabs])
        self.driver.get(self.auroraHomeLink)

    def SelectTab(self, tabNum: int):
        self.driver.switch_to.window(self.driver.window_handles[tabNum])

    def SelectTerm(self, term):
        courseList = Select(self.driver.find_element(By.TAG_NAME, "select"))
        courseList.select_by_visible_text(term)

        self.driver.find_element(By.XPATH, "//input[@type='submit']").click()

    def SelectDepartment(self, departmentName):
        courseList = Select(self.driver.find_element(By.TAG_NAME, "select"))
        courseList.select_by_value(departmentName)

        self.driver.find_element(By.XPATH, "//input[@type='submit']").click()


AuroraNav()
