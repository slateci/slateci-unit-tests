from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from locator import *
# from element import BasePageElement


class BasePage():
    def __init__(self, driver):
        self.driver = driver
    
    def get_page_title(self):
        return self.driver.title

    def get_page_source(self):
        return self.driver.page_source

    def click_back_btn(self):
        self.driver.back()

    def go_to_home_page(self):
        pass
    
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


class HomePage(BasePage):
    pass


class AboutPage(BasePage):
    # def test_enter_page(self):
    #     print('enter about page')
    def wait_for_page_loaded(self):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, 'acknowledging-slate'))
        )
    def get_all_links(self):
        field1 = self.driver.find_element_by_xpath("//div[@id='top-of-page']/div[2]")
        links = field1.find_elements_by_tag_name('a')
        return links




class TechPage(BasePage):
    def wait_for_page_loaded(self):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, 'slate-technology'))
        )
    
    def get_all_links(self):
        field1 = self.driver.find_element_by_xpath("//div[@id='top-of-page']/div[2]")
        links = field1.find_elements_by_tag_name('a')

        # add the edit this page on github link to all links
        git_edit_field = self.driver.find_element_by_xpath("//div[@id='top-of-page']/div[3]")
        links.append(git_edit_field.find_element_by_tag_name('a'))
        return links
    


class DocsPage(BasePage):
    def wait_for_page_loaded(self):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, 'content-container'))
        )
    
    def get_links_in_doc_content(self):
        doc_content = self.driver.find_element_by_id('doc-content')
        links = doc_content.find_elements_by_tag_name('a')
        return links


class BlogPage(BasePage):
    def wait_for_page_loaded(self):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='container blog']"))
        )
    
    def get_links_in_container_blog(self):
        field = self.driver.find_element_by_xpath("//div[@class='container blog']")
        links = field.find_elements_by_tag_name('a')
        return links




    def get_older_btn(self):
        try:
            older_btn = self.driver.find_element_by_xpath("//div[@class='next col-xs-6 text-right']/a[1]")
            return older_btn
        except:
            return None
            

class CommPage(BasePage):
    def wait_for_page_loaded(self):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, 'our-community'))
        )

    def get_links_in_container_community(self):
        field = self.driver.find_element_by_xpath("//div[@class='container community']")
        links = field.find_elements_by_tag_name('a')
        return links
