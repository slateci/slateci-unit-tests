import unittest
from selenium.webdriver import Chrome, Firefox
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import page
import time

class WebPageBrowsing(unittest.TestCase):
    def setUp(self):
        path_local = '/Users/lizhang/Documents/webdriver/chromedriver'
        options = ChromeOptions()
        options.headless = False
        self.driver = Chrome(executable_path=path_local, options=options)

        self.driver.get('https://slateci.io/')
        self.driver.set_window_size(1920, 1080)
    
    def test_home_page(self):
        main_page = page.BasePage(self.driver)
        main_page.go_to_home_page()
        home_page = page.HomePage(self.driver)

        home_page.wait_for_page_loaded()
        links_in_try_slate = home_page.get_links_in_try_slate()
        number_of_links = len(links_in_try_slate)
        for i in range(number_of_links):
            print(links_in_try_slate[i].get_attribute('href'))
            links_in_try_slate[i].click()
            self.driver.implicitly_wait(5)
            self.driver.back()
            home_page.wait_for_page_loaded()
            links_in_try_slate = home_page.get_links_in_try_slate()
    
    def skip_test_about_page(self):
        main_page = page.BasePage(self.driver)
        main_page.go_to_about_page()
        about_page = page.AboutPage(self.driver)
        
        about_page.wait_for_page_loaded()
        links = about_page.get_all_links()
        number_of_links = len(links)
        for i in range(number_of_links):
            print(links[i].get_attribute('href'))
            links[i].click()
            self.driver.implicitly_wait(5)
            self.driver.back()
            about_page.wait_for_page_loaded()
            links = about_page.get_all_links()
    
    def skip_test_tech_page(self):
        main_page = page.BasePage(self.driver)
        main_page.go_to_tech_page()
        tech_page = page.TechPage(self.driver)

        tech_page.wait_for_page_loaded()
        links = tech_page.get_all_links()
        number_of_links = len(links)
        for i in range(number_of_links):
            print(links[i].get_attribute('href'))
            links[i].click()
            self.driver.implicitly_wait(5)
            # below implement page check later
            # cur_page = page.TechPage(self.driver)
            self.driver.back()
            # reload the page and get links
            tech_page.wait_for_page_loaded()
            links = tech_page.get_all_links()

    
    def skip_test_docs_page(self):
        main_page = page.BasePage(self.driver)
        main_page.go_to_docs_page()
        docs_page = page.DocsPage(self.driver)
        docs_page.wait_for_page_loaded()

        side_menu_btns = docs_page.get_main_items_in_side_menu()
        number_of_btns = len(side_menu_btns)
        for i in range(number_of_btns):
            print('index i:', i)
            print(side_menu_btns[i].get_attribute('href'))
            side_menu_btns[i].click()
            self.driver.implicitly_wait(5)
            print('-'*40)
            
            active_side_links = docs_page.get_links_in_active_side_item()
            number_of_active_links = len(active_side_links)
            for j in range(number_of_active_links):
                print('index j:', j)
                print(active_side_links[j].get_attribute('href'))
                active_side_links[j].click()
                self.driver.implicitly_wait(5)
                # iterate through the content links
                # if active_side_links[j].text == 'SLATE CLI Manual':
                #     continue
                # docs_page.iterate_links_doc_content()
                # get the side links again
                active_side_links = docs_page.get_links_in_active_side_item()

            print('*'*40)

            side_menu_btns = docs_page.get_main_items_in_side_menu()

    

    def skip_test_blog_page(self):
        main_page = page.BasePage(self.driver)
        main_page.go_to_blog_page()
        blog_page = page.BlogPage(self.driver)

        blog_page.wait_for_page_loaded()

        while True:
            # iterate links
            links = blog_page.get_links_in_container_blog()
            number_of_links = len(links)
            for i in range(number_of_links):
                # print(links[i].get_attribute('href'))
                # print(links[i].text)
                if links[i].text == 'Older' or links[i].text == 'Newer' or links[i].get_attribute('href')=='https://slateci.io/feed.xml':
                    continue
                links[i].click()
                self.driver.implicitly_wait(5)
                self.driver.back()
                blog_page.wait_for_page_loaded()
                links = blog_page.get_links_in_container_blog()


            # click Order button
            older_btn = blog_page.get_older_btn()
            if not older_btn:
                break
            older_btn.click()
            blog_page.wait_for_page_loaded()

    
    def skip_test_comm_page(self):
        main_page = page.BasePage(self.driver)
        main_page.go_to_comm_page()
        comm_page = page.CommPage(self.driver)

        comm_page.wait_for_page_loaded()
        links = comm_page.get_links_in_container_community()
        number_of_links = len(links)
        for i in range(number_of_links):
            if 'mailto:' in links[i].get_attribute('href'):
                continue
            links[i].click()
            self.driver.implicitly_wait(5)
            self.driver.back()
            comm_page.wait_for_page_loaded()
            links = comm_page.get_links_in_container_community()


    def tearDown(self):
        time.sleep(2)
        self.driver.close()

if __name__ == '__main__':
    unittest.main()