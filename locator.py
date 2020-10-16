from selenium.webdriver.common.by import By

class BasePageLocators():
    HOME_TOP_BTN = (By.XPATH, "//a[@class='nav-item nav-link text-white'][@href='/']")
    ABOUT_TOP_BTN = (By.XPATH, "//a[@class='nav-item nav-link text-white'][@href='/about/']")
    TECH_TOP_BTN = (By.XPATH, "//a[@class='nav-item nav-link text-white'][@href='/technology/']")
    DOCS_TOP_BTN = (By.XPATH, "//a[@class='nav-item nav-link text-white'][@href='/docs/quickstart']")
    BLOG_TOP_BTN = (By.XPATH, "//a[@class='nav-item nav-link text-white'][@href='/blog/']")
    COMM_TOP_BTN = (By.XPATH, "//a[@class='nav-item nav-link text-white'][@href='/community/']")
    PORTAL_TOP_BTN = (By.XPATH, "//a[@class='nav-item nav-link text-white'][@href='https://portal.slateci.io/']")
