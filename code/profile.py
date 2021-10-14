import time
from bs4 import BeautifulSoup
from section import Section

__author__ = "Abhinav Thirupathi"


class Profile:
    """ Class that represents a Crunchbase profile"""

    def __init__(self, name=None):
        """
        Initialize a Crunchbase profile object
        :param name: Profile name
        @attribute soup: Beautiful soup object of the HTML content of the webpage
        @attribute data: The parsed data of the profile's Crunchbase page
        @attribute url: Crunchbase URL of the profile
        """
        self.name = name
        self.__soup = None
        self.__data = None
        self.__url = None

    def get_data(self):
        """
        Gets the data attribute
        :return: The data attribute with the parsed data
        """
        return self.__data

    def parse_profile(self, pro, driver):
        """
        Parses the Crunchbase profile page
        :return:
        """
        # Finds all the links on the Pro page
        tab = self.__soup.find("div", {"class": "mat-tab-links"})
        tab_links = tab.find_all("a")
        tab_links_lst = ["https://www.crunchbase.com" + tab_link['href'] for tab_link in tab_links]

        # Dictionary to store parsed data from all the sections
        profile_data = dict()
        self.name = self.__soup.find("h1").text.strip()
        profile_data[self.name] = dict()
        profile_data[self.name]["Crunchbase URL"] = self.__url

        # Iterates through every link in the tab links
        for link in tab_links_lst:
            driver.get(link)
            time.sleep(3)

            # Expands the description of the profile in the summary
            try:
                readMoreButton = driver.find_element_by_xpath("//a[@aria-label='Read More']")
                if readMoreButton is not None:
                    readMoreButton.click()
                    time.sleep(0.2)
            except:
                pass

            page_content = driver.page_source
            soup = BeautifulSoup(page_content, 'html.parser')

            # Finds all the sections (row-cards) on the page
            row_cards = soup.find_all("row-card")

            # Iterates through every section on the page, parses it, and stores it in the dictionary
            for row_card_index, row_card in enumerate(row_cards):
                section_soup = row_card.find("section-card")
                section_name = row_card.find("h2", {"class": "section-title"}).text.strip()
                section = Section(section_name)
                section_data = section.parse_section(section_soup, driver, row_card_index, pro=pro)
                if len(section_data) > 0:
                    profile_data[self.name][section_name] = section_data

        # Sets data attribute equal to the  dictionary with the parsed data
        self.__data = profile_data

    def process_profile(self, pro=False, driver=None):
        """
        Parses the page based on if its public or pro profile page
        :param pro: True if the profile page is pro, else False
        :param driver: Selenium driver to process the profile
        :return:
        """
        if self.__soup is not None:
            # Parses crunchbase page with the selenium driver is present
            if driver is not None:
                self.parse_profile(pro=pro, driver=driver)
            else:
                raise TypeError("NoneType parameter: 'driver'")
        else:
            raise TypeError("NoneType attribute: 'soup'")

    def get_profile_page(self, url=None, driver=None):
        """
        Gets the BeautifulSoup object of the page's HTML
        :param url: The crunchbase URL
        :param driver: The selenium driver
        :return: The selenium driver
        """
        # If driver and url are not None then gets the page at the URL, else raises Error
        if url is not None:
            self.__url = url
            if driver is not None:
                driver.get(url)
                time.sleep(3)
                self.__soup = BeautifulSoup(driver.page_source, 'html.parser')
                return driver
            elif driver is None:
                raise TypeError("NoneType parameter: 'driver'")
        else:
            raise TypeError("NoneType parameter: 'url'")
