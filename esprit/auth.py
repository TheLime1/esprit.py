from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class Auth:
    def __init__(self, driver_path=None, driver=None, debug=False, headless=True):
        self.login_url = "https://esprit-tn.com/esponline/online/default.aspx"
        self.debug = debug

        # Set up Chrome options
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")

        self.driver = driver if driver else webdriver.Chrome(
            executable_path=driver_path, options=chrome_options)

    def login(self, id, password):
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
            return self.driver
        else:
            print('''
                  -------------
                  Login failed!
                  -------------
                  ''')


# Code for debugging login
if __name__ == "__main__":
    auth = Auth(
        driver_path="C:/custom/bins/chromedriver-win64/chromedriver.exe", debug=True)
    id = "your_id"
    password = "your_password"
    session = auth.login(id, password)
