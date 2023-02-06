from re import search

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from locator import *

# from element import BasePageElement


class BasePage:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    def get_page_title(self):
        return self.driver.title

    def get_page_source(self):
        return self.driver.page_source

    def is_page_valid(self):
        pg_source = self.driver.page_source
        return "404" not in pg_source or "Page not found" not in pg_source

    def click_back_btn(self):
        self.driver.back()

    def go_to_home_page(self):
        home_btn = self.driver.find_element(*BasePageLocators.HOME_TOP_BTN)
        home_btn.click()

    def go_to_about_page(self):
        about_btn = self.driver.find_element(*BasePageLocators.ABOUT_TOP_BTN)
        about_btn.click()

    def go_to_tech_page(self):
        tech_btn = self.driver.find_element(*BasePageLocators.TECH_TOP_BTN)
        tech_btn.click()

    def go_to_docs_page(self):
        docs_btn = self.driver.find_element(*BasePageLocators.DOCS_TOP_BTN)
        docs_btn.click()

    def go_to_blog_page(self):
        blog_btn = self.driver.find_element(*BasePageLocators.BLOG_TOP_BTN)
        blog_btn.click()

    def go_to_comm_page(self):
        comm_btn = self.driver.find_element(*BasePageLocators.COMM_TOP_BTN)
        comm_btn.click()

    def getEditOnGitHubLink(self):
        expr = "//a[@class='btn btn-slate btn-edit-on-github pull-right']"
        edit_on_github_link = self.driver.find_element(by=By.XPATH, value=expr)
        return edit_on_github_link


class HomePage(BasePage):
    def wait_for_page_loaded(self):
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='row d-flex justify-content-between px-5']")
            )
        )

    def get_links_in_try_slate(self):
        expr = "//div[@class='row d-flex justify-content-between px-5']"
        field1 = self.driver.find_element(by=By.XPATH, value=expr)
        links = field1.find_elements(by=By.TAG_NAME, value="a")
        return links


class AboutPage(BasePage):
    # def test_enter_page(self):
    #     print('enter about page')
    def wait_for_page_loaded(self):
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, "//h2[@id='journal-and-conference-papers']")
            )
        )
        # WebDriverWait(self.driver, 20).until(
        #     EC.presence_of_element_located((By.ID, 'journal-and-conference-papers'))
        # )

    def get_all_links(self):
        expr = "//div[@id='top-of-page']/div[2]"
        field1 = self.driver.find_element(by=By.XPATH, value=expr)
        links = field1.find_elements(by=By.TAG_NAME, value="a")
        return links


class TechPage(BasePage):
    def wait_for_page_loaded(self):
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.ID, "slate-technology"))
        )

    def get_all_links(self):
        expr = "//div[@id='top-of-page']/div[2]"
        field1 = self.driver.find_element(by=By.XPATH, value=expr)
        links = field1.find_elements(by=By.TAG_NAME, value="a")

        # add the edit this page on github link to all links
        expr2 = "//div[@id='top-of-page']/div[3]"
        git_edit_field = self.driver.find_element(by=By.XPATH, value=expr2)
        links.append(git_edit_field.find_element(by=By.TAG_NAME, value="a"))
        return links


class DocsPage(BasePage):
    def wait_for_page_loaded(self):
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.ID, "content-container"))
        )

    def get_links_in_doc_content(self):
        doc_content = self.driver.find_element(by=By.ID, value="doc-content")
        links = doc_content.find_elements(by=By.TAG_NAME, value="a")
        return links

    def iterate_links_doc_content(self, linkL1, linkL2):
        links = self.get_links_in_doc_content()
        number_of_links = len(links)

        for i in range(number_of_links):
            # print('url:', links[i].get_attribute('href'))
            self.logger.info("Docs Page: {} -> {} -> {}".format(linkL1, linkL2, links[i].text))
            # print("Docs Page: {} -> {} -> {}".format(linkL1, linkL2, links[i].text))
            if (
                links[i].text
                in [
                    "for Linux",
                    "for Mac OS",
                    "A Docker-in-Docker Kubernetes node",
                ]
                or "mailto:" in links[i].get_attribute("href")
            ):
                # 'for Linux', 'for Mac OS' to prevent download
                # 'A Docker-in-Docker Kubernetes node' 404, link to fix still unknown
                continue

            if search('^.*\.pdf$', links[i].get_attribute("href")):
                self.logger.info('PDF download detected: {}'.format(links[i].get_attribute("href")))
            else:
                self.logger.info(f'Clicking "{links[i].text}"')
                links[i].click()
                self.driver.implicitly_wait(5)
                # here check 404/500
                self.logger.info(f"Link destination page title: {self.get_page_title()}")
                if not self.is_page_valid():
                    self.logger.error(f'"{self.get_page_title()}" is not valid.')
                    raise AssertionError("See the logs")

                # in case a new tab is open, close tab and switch back to original tab
                if len(self.driver.window_handles) == 2:
                    self.driver.switch_to.window(window_name=self.driver.window_handles[-1])
                    self.logger.info(f"Link destination page title: {self.get_page_title()}")
                    if not self.is_page_valid():
                        self.logger.error(f'"{self.get_page_title()}" is not valid.')
                        raise AssertionError("See the logs")
                    self.driver.close()
                    self.driver.switch_to.window(window_name=self.driver.window_handles[0])

                self.driver.back()
                self.wait_for_page_loaded()
                links = self.get_links_in_doc_content()
                # print('length is:', len(links))

    def get_main_items_in_side_menu(self):
        expr = "//li[@class='parent-li']/a[@role='button']"
        items = self.driver.find_elements(by=By.XPATH, value=expr)
        return items

    def get_links_in_active_side_item(self):
        try:
            expr = "//div[@class='collapse collapsable-parent show active-menu-link']"
            active_item = self.driver.find_element(by=By.XPATH, value=expr)
            links = active_item.find_elements(by=By.TAG_NAME, value="a")
            return links
        except:
            None


class BlogPage(BasePage):
    def wait_for_page_loaded(self):
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='container blog']"))
            )
        except NoSuchElementException:
            self.logger.error(f"Unable to find wait element on page: {self.driver.title}")

    def get_links_in_container_blog(self):
        expr = "//div[@class='container blog']"
        field = self.driver.find_element(by=By.XPATH, value=expr)
        links = field.find_elements(by=By.TAG_NAME, value="a")
        return links

    def get_older_btn(self):
        try:
            expr = "//div[@class='next col-xs-6 text-right']/a[1]"
            older_btn = self.driver.find_element(by=By.XPATH, value=expr)
            return older_btn
        except:
            return None


class CommPage(BasePage):
    def wait_for_page_loaded(self):
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.ID, "our-community"))
        )

    def get_links_in_container_community(self):
        expr = "//div[@class='container community']"
        field = self.driver.find_element(by=By.XPATH, value=expr)
        links = field.find_elements(by=By.TAG_NAME, value="a")
        return links
