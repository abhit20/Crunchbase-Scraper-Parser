from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import time
from bs4 import BeautifulSoup

__author__ = "Abhinav Thirupathi"


class Section:
    """ Class that represents a 'Section' in a Crunchbase profile page"""

    def __init__(self, name=None):
        """
        Initialize a section
        :param name: Section name
        """
        self.name = name

    def parse_big_values_card(self, big_values_card_soup=None):
        """
        Parses the big values card in the section
        :param big_values_card_soup: Beautiful soup object of the HTML content of the specific card
        :return: Dictionary with the parsed data of the card
        """
        # Dictionary to store and return the parsed data of the card
        card_output = dict()

        # Iterates through the big values card, stores the labels and values in the dictionary
        if big_values_card_soup is not None:
            labels = big_values_card_soup.find_all('label-with-info')
            values = big_values_card_soup.find_all('field-formatter')

            for index in range(0, len(labels)):
                card_label = labels[index].text.strip("\xa0")
                card_val = values[index].text.strip("\xa0")
                card_output[card_label] = card_val

        return card_output

    def parse_timeline_card(self, timeline_card_soup=None):
        """
        Parses the timeline card in the section
        :param timeline_card_soup: Beautiful soup object of the HTML content of the specific card
        :return: Dictionary with the parsed data of the card
        """
        # Dictionary to store and return the parsed data of the card
        card_output = dict()

        if timeline_card_soup is not None:

            # Extracts the fields and values in the card
            fields = timeline_card_soup.find_all("field-formatter")
            values = timeline_card_soup.find_all("press-reference")

            # Iterates through the fields and values, and stores them in the dictionary
            if len(fields) == len(values):
                for i in range(0, len(fields)):
                    card_output[i] = dict()
                    card_output[i][fields[i].text.strip()] = values[i].text.strip()

        return card_output

    def parse_phrase_list_card(self, phrase_list_card_soup=None):
        """
        Parses the phrase list card in the section
        :param phrase_list_card_soup: Beautiful soup object of the HTML content of the specific card
        :return: Dictionary with the parsed data of the card
        """
        # Dictionary to store and return the parsed data of the card
        card_output = dict()

        # Extracts the information from the phrase list card and returns it
        if phrase_list_card_soup is not None:
            card_output['Summary'] = phrase_list_card_soup.text.strip().replace("\xa0", " ")

        return card_output

    def parse_list_card(self, list_card_soup=None):
        """
        Parses the list card in the section
        :param list_card_soup: Beautiful soup object of the HTML content of the specific card
        :return: Dictionary with the parsed data of the card
        """
        # Dictionary to store and return the parsed data of the card
        card_output = dict()

        if list_card_soup is not None:

            # Extracts the columns and rows from the table
            table_head = list_card_soup.find("thead").find("tr").find_all("th")
            table_rows = list_card_soup.find("tbody").find_all("tr")

            # Extracts data from the columns and rows and stores them in the dictionary
            for row_index, row in enumerate(table_rows):
                card_output[row_index] = {}
                row_cells = row.find_all("td")
                for i in range(0, len(row_cells)):
                    card_output[row_index][table_head[i].text.strip()] = row_cells[i].text.strip().replace(
                        "Sign up for free to unlock and follow the latest funding activities", "")

        return card_output

    def parse_fields_card(self, fields_card_soup):
        """
        Parses the fields card in the section
        :param fields_card_soup: Beautiful soup object of the HTML content of the specific card
        :return: Dictionary with the parsed data of the card
        """
        # Dictionary to store and return the parsed data of the card
        card_output = dict()

        if fields_card_soup is not None:
            # Extracts the labels and values from the fields card
            labels = fields_card_soup.find_all('label-with-info')
            values = fields_card_soup.find_all('field-formatter', {'class': 'ng-star-inserted'})

            if len(labels) == len(values):

                # Iterates through the labels and values and stores them in the dictionary
                social_media = ['Website', 'Facebook', 'LinkedIn', 'Twitter']
                for i in range(0, len(values)):

                    # Iterates through separate things in a value slot
                    # Creates a comma-separated string and stores it in the dictionary with the correct label (key)
                    if values[i].find("mat-chip-list") is not None:
                        mat_chip_list = values[i].find("mat-chip-list").find_all("mat-chip")
                        mat_chip_info = ""
                        for mat_chip_index, mat_chip in enumerate(mat_chip_list):
                            mat_chip_info += mat_chip.text.strip()
                            if mat_chip_index < len(mat_chip_list) - 1:
                                mat_chip_info += ', '
                        card_output[labels[i].text.strip("\xa0")] = mat_chip_info
                        continue

                    # Gets the links for social media websites
                    if labels[i].text.strip() in social_media:
                        card_output[labels[i].text.strip("\xa0")] = values[i].a['href'].strip("\xa0")
                    else:
                        card_output[labels[i].text.strip("\xa0")] = values[i].text.strip("\xa0").strip()

        return card_output

    def parse_image_list_card(self, image_list_card_soup=None):
        """
        Parses the image list card in the section
        :param image_list_card_soup: Beautiful soup object of the HTML content of the specific card
        :return: Dictionary with the parsed data of the card
        """
        # Dictionary to store and return the parsed data of the card
        card_output = dict()

        if image_list_card_soup is not None:
            list_items = image_list_card_soup.find_all("li")

            for list_item in list_items:
                # Extracts the div tag information from the list item
                div = list_item.find("div", {"class": "fields"})

                # Extracts the name, and crunchbase url and inserts them
                name = div.find("a")
                crunchbase_url = "https://www.crunchbase.com" + name['href']

                card_output[name.text.strip()] = {}

                # Extracts the fields from the card
                fields = div.find_all("field-formatter")

                # Iterates through the fields in the section and stores them in the dictionary
                for index, field in enumerate(fields):
                    card_output[name.text.strip()][index] = field.text.strip()

                card_output[name.text.strip()]["Crunchbase URL"] = crunchbase_url

        return card_output

    def parse_hub_list_card(self, hub_list_card_soup=None):
        """
        Parses the hub list card in the section
        :param hub_list_card_soup: Beautiful soup object of the HTML content of the specific card
        :return: Dictionary with the parsed data of the card
        """
        # Dictionary to store and return the parsed data of the card
        card_output = dict()

        if hub_list_card_soup is not None:

            # Extracts the fields in the card
            fields = hub_list_card_soup.find_all('div', {'class': 'flex layout-column layout-align-center-start'})

            # Iterates through the fields and stores them in the dictionary
            for i in range(0, len(fields)):
                card_output[i] = dict()
                card_output[i][0] = fields[i].find("a").text.strip()
                subtext = fields[i].find('div', {'class': 'subtext hide show-gt-sm cb-margin-medium-top'})
                if subtext is not None:
                    card_output[i][1] = subtext.text.strip()

        return card_output

    def parse_description_card(self, description_card_soup=None):
        """
        Parses the description card in the section
        :param description_card_soup: Beautiful soup object of the HTML content of the specific card
        :return: Dictionary with the parsed data of the card
        """
        # Dictionary to store and return the parsed data of the card
        card_output = dict()

        if description_card_soup is not None:

            # Extracts the text from the 'p' tags in the card and stores it in the dictionary
            p_tags = description_card_soup.find_all("p")
            description = ""

            for p_tag in p_tags:
                description += p_tag.text.strip()

            card_output["Description"] = description

        return card_output

    def parse_image_with_fields_card(self, image_with_fields_card_soup=None):
        """
        Parses the image with fields card in the section
        :param image_with_fields_card_soup: Beautiful soup object of the HTML content of the specific card
        :return: Dictionary with the parsed data of the card
        """
        # Dictionary to store and return the parsed data of the card
        card_output = dict()

        # Keys (labels) for the fields
        labels = ['Name', 'Brief', 'Location']

        if image_with_fields_card_soup is not None:

            # # Extracts the fields and store it in the dictionary
            fields = image_with_fields_card_soup.find_all("field-formatter")
            for field_index, field in enumerate(fields):
                card_output[labels[field_index]] = field.text.strip()

        return card_output

    def parse_tabs_card(self, tabs_card_soup=None, driver=None, index=None):
        """
        Parses the tabs card in the section
        :param tabs_card_soup: Beautiful soup object of the HTML content of the specific card
        :param driver: Selenium driver
        :param index: Index of the section on the page
        :return: Dictionary with the parsed data of the card
        """
        # Dictionary to store and return the parsed data of the card
        card_output = dict()

        if tabs_card_soup is not None:
            # Extracts the tabs from the section
            mat_tabs = tabs_card_soup.find("div", {"class": "mat-tab-labels"})
            mat_tabs_labels = mat_tabs.find_all("div", {"role": "tab"})

            # Iterates through the tabs in the section
            for mat_tab_label in mat_tabs_labels:
                mat_tab_label_xpath = '//*[@id="' + mat_tab_label['id'] + '"]'
                try:
                    #  Clicks on the tab in the section
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, mat_tab_label_xpath))).click()
                    time.sleep(2)

                    # Extracts the updated information from the section
                    temp_row_cards = BeautifulSoup(driver.page_source, 'html.parser').find_all("row-card")
                    temp_tabs_card = temp_row_cards[index].find("tabs-card")
                    temp_section_card = temp_tabs_card.find("section-card")

                    # Parses the updated information from the section
                    card_output[mat_tab_label.text.strip()] = self.parse_section(section_soup=temp_section_card, driver=driver, index=index, ignore=True)

                # Ignores tab that couldn't be clicked on
                except ElementClickInterceptedException:
                    pass

        return card_output

    def parse_card_more_results(self, card_more_results_soup, driver):
        """
        Expands the section view all content and parses the section
        :param card_more_results_soup: Beautiful soup object of the HTML content with the link to all the content
        :param driver: Selenium driver
        :return: Dictionary with the parsed data of the card
        """
        # Dictionary to store and return the parsed data of the card
        card_output = dict()

        if card_more_results_soup is not None:
            # Extracts the link to the all the content and gets that page
            more_results_link = "https://www.crunchbase.com" + card_more_results_soup.a['href']
            driver.get(more_results_link)
            time.sleep(3)

            # Extracts the all the content of that section and parses it
            temp_section_card = BeautifulSoup(driver.page_source, 'html.parser').find("section-card")
            card_output = self.parse_section(section_soup=temp_section_card, driver=driver, ignore=True)

            # Goes back to the after parsing
            driver.back()
            time.sleep(2)

        return card_output

    def parse_section(self, section_soup=None, driver=None, index=None, ignore=False, pro=False):
        """
        Parses the section
        :param section_soup: Beautiful soup object of the HTML content of the specific section
        :param driver: Selenium driver with the page
        :param index: Index of the section on the page
        :param ignore: True if being called from specific cards, else False
        :param pro: True if parsing section with Crunchbase Pro, else false
        :return: Dictionary with the parsed data of the section
        """
        # Dictionary to store and return the parsed data of the entire section
        section_output = {}

        card_types = ['tabs-card', 'list-card-more-results', 'big-values-card', 'phrase-list-card', 'fields-card',
                      'timeline-card', 'list-card', 'image-list-card', 'hub-list-card', 'description-card',
                      'image-with-fields-card']

        # Iterates through the card_types and finds if each card exists
        for card_type in card_types:
            cards = section_soup.find_all(card_type)

            # Iterates through every one of the found cards and parses the cards using the right functions
            for card in cards:
                parsed_data = dict()

                if card_type == 'big-values-card':
                    parsed_data = self.parse_big_values_card(card)
                elif card_type == 'phrase-list-card':
                    parsed_data = self.parse_phrase_list_card(card)
                elif card_type == 'fields-card':
                    parsed_data = self.parse_fields_card(card)
                elif card_type == 'timeline-card':
                    parsed_data = self.parse_timeline_card(card)
                elif card_type == 'list-card':
                    parsed_data = self.parse_list_card(card)
                elif card_type == 'image-list-card':
                    parsed_data = self.parse_image_list_card(card)
                elif card_type == 'hub-list-card':
                    parsed_data = self.parse_hub_list_card(card)
                elif card_type == 'description-card':
                    parsed_data = self.parse_description_card(card)
                elif card_type == 'image-with-fields-card':
                    parsed_data = self.parse_image_with_fields_card(card)
                elif card_type == 'tabs-card' and pro is True:
                    parsed_data = self.parse_tabs_card(card, driver, index)
                elif card_type == 'list-card-more-results' and ignore is False and pro is True:
                    parsed_data = self.parse_card_more_results(card, driver)

                # If the parsed data exists, then it is stored in the dictionary
                if len(parsed_data) > 0:
                    for label, value in parsed_data.items():
                        section_output[label] = value

                # Processes the 'tabs-card' and 'list-card-more-results' for Pro page and returns it
                if pro is True and (card_type == 'tabs-card' or card_type == 'list-card-more-results'):
                    return section_output

        return section_output
