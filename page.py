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

    def is_page_valid(self):
        pg_source = self.driver.page_source
        return '404' not in pg_source or 'Page not found' not in pg_source

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


class HomePage(BasePage):
    def wait_for_page_loaded(self):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='row d-flex justify-content-between px-5']"))
        )
    
    def get_links_in_try_slate(self):
        field1 = self.driver.find_element_by_xpath("//div[@class='row d-flex justify-content-between px-5']")
        links = field1.find_elements_by_tag_name('a')
        return links


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


    # needs debug for SLATE CLI Manual
    def iterate_links_doc_content(self):
        links = self.get_links_in_doc_content()
        number_of_links = len(links)
        for i in range(number_of_links):
            links[i].click()
            self.driver.implicitly_wait(5)
            #here check 404/500?
            assert self.is_page_valid()
            self.driver.back()
            self.wait_for_page_loaded()
            links = self.get_links_in_doc_content()
    
    def get_main_items_in_side_menu(self):
        # side_menu = self.driver.find_element_by_id('side-menu')
        items = self.driver.find_elements_by_xpath("//li[@class='parent-li']/a[@role='button']")
        # links = self.driver.find_elements_by_xpath("//dic[@id='side-menu']/ul/li[@class='parent-li']")
        return items

    def get_links_in_active_side_item(self):
        try:
            active_item = self.driver.find_element_by_xpath("//div[@class='collapse collapsable-parent show active-menu-link']")
            links = active_item.find_elements_by_tag_name('a')
            return links
        except:
            None
    
    



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
