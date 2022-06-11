import unittest
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
import os
import page
import time
import sys
from logtools import CustomLogging
from selenium.common.exceptions import ElementClickInterceptedException


class WebPageBrowsing(unittest.TestCase):
    __logger = CustomLogging('banana').get_logger();

    URL = 'https://slateci.io/'
    __logger.info(f"URL under test: {URL}")

    def setUp(self):
        options = ChromeOptions()
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')

        #- The following should allow PDFs to be viewed instead of downloaded but does not...
        # options.add_experimental_option("prefs",
        #                                 {
        #                                     "plugins.always_open_pdf_externally": False,
        #                                     "plugins.plugins_list": [{
        #                                         "enabled": True, "name": "Chrome PDF Viewer"
        #                                     }]
        #                                 })

        self.driver = Chrome(options=options)

        self.driver.get(self.URL)

    def test_home_page(self):
        main_page = page.BasePage(self.driver, self.__logger)
        main_page.go_to_home_page()
        home_page = page.HomePage(self.driver, self.__logger)
        self.assertTrue(home_page.is_page_valid(), f"{home_page.get_page_title()} is not valid.")

        home_page.wait_for_page_loaded()
        links_in_try_slate = home_page.get_links_in_try_slate()
        number_of_links = len(links_in_try_slate)
        for i in range(number_of_links):
            self.__logger.info('Home Page: Try SLATE -> {}'.format(links_in_try_slate[i].text))
            links_in_try_slate[i].click()
            self.driver.implicitly_wait(5)
            cur_page = page.BasePage(self.driver, self.__logger)
            self.assertTrue(cur_page.is_page_valid(), f"{cur_page.get_page_title()} is not valid.")
            self.driver.back()
            home_page.wait_for_page_loaded()
            links_in_try_slate = home_page.get_links_in_try_slate()

        # test Edit This Page on GitHub link
        # edit_on_github_link = home_page.getEditOnGitHubLink()
        # edit_on_github_link.click()

    def test_about_page(self):
        main_page = page.BasePage(self.driver, self.__logger)
        main_page.go_to_about_page()
        about_page = page.AboutPage(self.driver, self.__logger)
        self.assertTrue(about_page.is_page_valid(), f"{about_page.get_page_title()} is not valid.")

        about_page.wait_for_page_loaded()
        links = about_page.get_all_links()
        number_of_links = len(links)
        for i in range(number_of_links):
            self.__logger.info(links[i].get_attribute('href'))

            links[i].click()
            self.driver.implicitly_wait(5)
            cur_page = page.BasePage(self.driver, self.__logger)
            self.assertTrue(cur_page.is_page_valid(), f"{cur_page.get_page_title()} is not valid.")

            self.__logger.info(cur_page.get_page_title())

            if cur_page.get_page_title() == 'SLATE / About':
                continue
            self.driver.back()
            about_page.wait_for_page_loaded()
            links = about_page.get_all_links()

    def test_tech_page(self):
        main_page = page.BasePage(self.driver, self.__logger)
        main_page.go_to_tech_page()
        tech_page = page.TechPage(self.driver, self.__logger)
        self.assertTrue(tech_page.is_page_valid(), f"{tech_page.get_page_title()} is not valid.")

        tech_page.wait_for_page_loaded()
        links = tech_page.get_all_links()
        number_of_links = len(links)
        for i in range(number_of_links):
            # self.__logger.info(links[i].get_attribute('href'))
            self.__logger.info('Tech Page: {}'.format(links[i].text))
            links[i].click()
            self.driver.implicitly_wait(5)
            cur_page = page.BasePage(self.driver, self.__logger)
            self.assertTrue(cur_page.is_page_valid(), f"{cur_page.get_page_title()} is not valid.")
            self.driver.back()
            # reload the page and get links
            tech_page.wait_for_page_loaded()
            links = tech_page.get_all_links()

    def test_docs_page(self):
        main_page = page.BasePage(self.driver, self.__logger)
        main_page.go_to_docs_page()
        docs_page = page.DocsPage(self.driver, self.__logger)
        self.assertTrue(docs_page.is_page_valid(), f"{docs_page.get_page_title()} is not valid.")

        docs_page.wait_for_page_loaded()
        side_menu_btns = docs_page.get_main_items_in_side_menu()
        number_of_btns = len(side_menu_btns)
        for i in range(number_of_btns):
            # self.__logger.info(side_menu_btns[i].get_attribute('href'))
            linkL1 = side_menu_btns[i].text



            # A giant hack to scroll the side-menu for non-visible elements.
            try:
                side_menu_btns[i].click()
            except ElementClickInterceptedException:

                if os.environ.get('SCREENSHOTS') == 1:
                    self.driver.save_screenshot('/opt/project/screenshots/{}.png'.format(side_menu_btns[i].text))
                self.__logger.info('Unable to click element: "{}". Trying a manual scroll of side-menu...'.format(
                    side_menu_btns[i].text))
                actions = ActionChains(self.driver)
                actions.move_to_element(side_menu_btns[i])
                actions.click()
                actions.perform()

            self.driver.implicitly_wait(5)
            self.assertTrue(docs_page.is_page_valid(), f"{docs_page.get_page_title()} is not valid.")

            active_side_links = docs_page.get_links_in_active_side_item()
            if not active_side_links:
                docs_page.iterate_links_doc_content()
                side_menu_btns = docs_page.get_main_items_in_side_menu()
                continue
            number_of_active_links = len(active_side_links)
            for j in range(number_of_active_links):
                # self.__logger.info(active_side_links[j].get_attribute('href'))
                linkL2 = active_side_links[j].text
                active_side_links[j].click()
                self.driver.implicitly_wait(5)
                cur_page = page.BasePage(self.driver, self.__logger)
                self.assertTrue(cur_page.is_page_valid(), f"{cur_page.get_page_title()} is not valid.")

                docs_page.iterate_links_doc_content(linkL1, linkL2)
                # get the side links again
                active_side_links = docs_page.get_links_in_active_side_item()

            side_menu_btns = docs_page.get_main_items_in_side_menu()

    def test_blog_page(self):
        main_page = page.BasePage(self.driver, self.__logger)
        main_page.go_to_blog_page()
        blog_page = page.BlogPage(self.driver, self.__logger)
        self.assertTrue(blog_page.is_page_valid(), f"{blog_page.get_page_title()} is not valid.")

        blog_page.wait_for_page_loaded()
        while True:
            # iterate links
            links = blog_page.get_links_in_container_blog()
            number_of_links = len(links)
            for i in range(number_of_links):
                # self.__logger.info(links[i].get_attribute('href'))
                self.__logger.info('Blog Page: {}'.format(links[i].text))
                if links[i].text == 'Older' or links[i].text == 'Newer' or links[i].get_attribute(
                        'href') == 'https://slateci.io/feed.xml':
                    continue
                links[i].click()
                self.driver.implicitly_wait(5)
                cur_page = page.BasePage(self.driver, self.__logger)
                self.assertTrue(cur_page.is_page_valid(), f"{cur_page.get_page_title()} is not valid.")
                self.driver.back()
                blog_page.wait_for_page_loaded()
                links = blog_page.get_links_in_container_blog()

            # click Order button
            older_btn = blog_page.get_older_btn()
            if not older_btn:
                break
            older_btn.click()
            blog_page.wait_for_page_loaded()

    def test_comm_page(self):
        main_page = page.BasePage(self.driver, self.__logger)
        main_page.go_to_comm_page()
        comm_page = page.CommPage(self.driver, self.__logger)
        self.assertTrue(comm_page.is_page_valid(), f"{comm_page.get_page_title()} is not valid.")

        comm_page.wait_for_page_loaded()
        links = comm_page.get_links_in_container_community()
        number_of_links = len(links)
        for i in range(number_of_links):
            if 'mailto:' in links[i].get_attribute('href'):
                continue
            self.__logger.info('Community Page: {}'.format(links[i].text))
            links[i].click()
            self.driver.implicitly_wait(5)
            cur_page = page.BasePage(self.driver, self.__logger)
            self.assertTrue(cur_page.is_page_valid(), f"{cur_page.get_page_title()} is not valid.")
            self.driver.back()
            comm_page.wait_for_page_loaded()
            links = comm_page.get_links_in_container_community()

    def tearDown(self):
        time.sleep(2)
        self.driver.close()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        WebPageBrowsing.URL = sys.argv.pop()
    unittest.main()
