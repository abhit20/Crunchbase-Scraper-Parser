from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from profile import Profile

__author__ = "Abhinav Thirupathi"


class Crunchbase:
    """ Class that represents Crunchbase website"""

    def __init__(self):
        """
        Initialize a Crunchbase
        @attribute loggedIn: True if logged into Crunchbase, else False
        @attribute driver: Selenium driver
        """
        self.__loggedIn = False
        self.__driver = None

    def start_selenium(self):
        """
        Starts a selenium driver
        :return: The selenium driver
        """
        # Starts a new selenium driver
        self.__driver = webdriver.Chrome(ChromeDriverManager().install())

    def login(self, email=None, password=None):
        """
        Logs into Crunchbase
        :param email: Email to login
        :param password: Password to login
        :return: Selenium driver after logging into Crunchbase
        """
        if email is not None and password is not None:
            # Logins into the Crunchbase after getting selenium driver with Crunchbase login page
            self.start_selenium()

            self.__driver.get(url="https://www.crunchbase.com/login")
            time.sleep(10)

            email_input = self.__driver.find_elements_by_xpath("//input[@name='email']")
            email_input[0].send_keys(email)

            password_input = self.__driver.find_elements_by_xpath("//input[@name='password']")
            password_input[0].send_keys(password)

            login_button = self.__driver.find_element_by_xpath("//button[@type='submit']")
            login_button.click()
            time.sleep(10)

            self.__loggedIn = True

        else:
            raise TypeError("NoneType parameter: 'email' or 'url'")

    def process_profile(self, pro=False, name=None, url=None):
        """
        Parses the profile page
        :param pro: If the logged into Crunchbase Pro its True, else False
        :param name: Name of the profile
        :param url: Crunchbase URL of the profile
        :return: Dictionary of the parsed profile data
        """
        # Crunchbase profile object
        profile = Profile(name)

        # Parses public profile page using selenium
        if name is not None and url is not None:
            if pro is False:
                if self.__driver is not None and self.__loggedIn is True:
                    self.__driver.quit()
                if self.__driver is None and self.__loggedIn is False:
                    self.start_selenium()
                self.__driver = profile.get_profile_page(url=url, driver=self.__driver)
                profile.process_profile(pro=False, driver=self.__driver)
            # Parses profile page when pro is enabled after logging in with selenium
            elif pro or self.__loggedIn is True:
                self.__driver = profile.get_profile_page(url=url, driver=self.__driver)
                profile.process_profile(pro=True, driver=self.__driver)
            # Raises error when parsing a pro page without logging into Crunchbase Pro
            elif pro and self.__loggedIn is False:
                raise TypeError("Not logged into Crunchbase")
        else:
            if name is None and url is not None:
                raise TypeError("NoneType parameter: 'name'")
            elif name is not None and url is None:
                raise TypeError("NoneType parameter   : 'url'")
            elif name is None and url is None:
                raise TypeError("NoneType parameters: 'name', 'url'")

        # Returns the parsed profile data
        data = profile.get_data()
        return data
