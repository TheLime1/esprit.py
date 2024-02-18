from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class Auth:
    """
    A class used to represent an Authentication process

    ...

    Attributes
    ----------
    login_url : str
        a string representing the login URL
    debug : bool
        a boolean indicating if debug mode is on
    driver : WebDriver
        a WebDriver object to interact with the browser

    Methods
    -------
    login(id, password)
        Logs in to the website using the provided id and password
    """

    def __init__(self, driver_path=None, driver=None, debug=False, headless=True):
        """
        Constructs all the necessary attributes for the Auth object.

        Parameters
        ----------
            driver_path : str, optional
                Path to the WebDriver executable (default is None)
            driver : WebDriver, optional
                Existing WebDriver instance (default is None)
            debug : bool, optional
                Debug mode flag (default is False)
            headless : bool, optional
                Headless mode flag for the browser (default is True)
        """

        self.login_url = "https://esprit-tn.com/esponline/online/default.aspx"
        self.debug = debug

        # Set up Chrome options
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")

        # Set up Chrome service
        service = Service(executable_path=driver_path) if driver_path else None

        self.driver = driver if driver else webdriver.Chrome(
            service=service, options=chrome_options)

    def login(self, id, password):
        """
        Logs in to the website using the provided id and password.

        Parameters
        ----------
            id : str
                User's id
            password : str
                User's password

        Returns
        -------
        list
            List of cookies if login is successful, None otherwise
        """

        self.driver.get(self.login_url)

        # Fill in the ID
        id_input = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="ContentPlaceHolder1_TextBox3"]'))
        )
        id_input.send_keys(id)

        # Click the 'Suivant' button using XPath
        suivant_button = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="ContentPlaceHolder1_Button3"]'))
        )
        suivant_button.click()

        # Fill in the password using XPath
        password_input = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="ContentPlaceHolder1_TextBox7"]'))
        )
        password_input.send_keys(password)

        # Click the 'Connexion' button using XPath
        connexion_button = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="ContentPlaceHolder1_ButtonEtudiant"]'))
        )
        connexion_button.click()

        # Check if login was successful
        if 'Vous pouvez consulter dans cet espace :' in self.driver.page_source:
            print('''
                  -----------------
                  Login successful!
                  -----------------
                  ''')
            return self.driver.get_cookies()
        else:
            print('''
                  -------------
                  Login failed!
                  -------------
                  ''')
            return None


# Code for debugging login
if __name__ == "__main__":
    auth = Auth(debug=True)
    id = "your_id"
    password = "your_password"
    session = auth.login(id, password)
