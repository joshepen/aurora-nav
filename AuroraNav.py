from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


class AuroraNav:
    def __init__(self, headless=True):
        options = Options()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("window-size=1400,900")
        self.driver = webdriver.Chrome(options=options)
        self.auroraHomeLink = (
            "https://aurora.umanitoba.ca/ssb/twbkwbis.P_GenMenu?name=bmenu.P_MainMnu"
        )

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

    """ Finds name and clicks it."""

    def GoToPage(self, name: str, elementType="*"):
        startUrl = self.driver.current_url
        try:
            element = self.driver.find_element(
                By.XPATH, "//%s[contains(text(), '%s')]" % (elementType, name)
            )

        except NoSuchElementException as nse:
            return False

        element.click()
        if self.driver.current_url == startUrl:
            return False
        return True

    """ The Look Up Classes page is unique in that the words you search for are not a button,
        but rather the button is beside it, so GoToPage can't be used."""

    def GoToLookupClass(self, courseNum: str):
        try:
            self.driver.find_element(
                By.XPATH,
                "//*[contains(text(), '%s')]/../td[last()]/form/input[@type='submit']"
                % courseNum,
            ).click()
        except NoSuchElementException as nse:
            return False

        try:
            self.driver.find_element(
                By.XPATH,
                "//*[contains(text(), '%s')]"
                % "No classes were found that meet your search criteria",
            )
            return False
        except NoSuchElementException as nse:
            return True

    """ Returns to Aurora home page."""

    def HomePage(self):
        self.driver.get(self.auroraHomeLink)

    def GetPageContents(self):
        return self.driver.page_source

    """ Select term from dropdown list and clicks submit."""

    def SelectTerm(self, term):
        courseList = Select(self.driver.find_element(By.TAG_NAME, "select"))
        courseList.select_by_visible_text(term)

        self.driver.find_element(By.XPATH, "//input[@type='submit']").click()

    """ Select department from dropdown list and clicks submit."""

    def SelectDepartment(self, departmentName):
        courseList = Select(self.driver.find_element(By.TAG_NAME, "select"))
        courseList.select_by_value(departmentName)

        self.driver.find_element(By.XPATH, "//input[@type='submit']").click()

    def CloseWindow(self):
        self.driver.close()
