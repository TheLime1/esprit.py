import requests
from bs4 import BeautifulSoup


class Auth:
    """
    A class used to represent an Authentication.

    ...

    Attributes
    ----------
    login_url : str
        a formatted string that represents the login URL
    session : requests.Session
        a Session object from the requests library

    Methods
    -------
    login(id: str, password: str):
        Logs in to the website using the provided id and password.
    """

    def __init__(self, session=None):
        self.login_url = "https://esprit-tn.com/esponline/online/default.aspx"
        self.session = session if session else requests.session()

    def login(self, id, password):
        """
        Logs in to the website using the provided id and password.

        Parameters
        ----------
            id : str
                the id to use for login
            password : str
                the password to use for login

        Returns
        -------
        requests.Session
            the Session object used for the login. This can be used for subsequent requests.
            Returns None if the login failed.
        """
        response = self.session.get(self.login_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        viewstate = soup.find('input', {'id': '__VIEWSTATE'})['value']
        viewstategenerator = soup.find(
            'input', {'id': '__VIEWSTATEGENERATOR'})['value']
        eventvalidation = soup.find(
            'input', {'id': '__EVENTVALIDATION'})['value']

        id_payload = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': viewstate,
            '__VIEWSTATEGENERATOR': viewstategenerator,
            '__EVENTVALIDATION': eventvalidation,
            'ctl00$ContentPlaceHolder1$TextBox1': '',
            'ctl00$ContentPlaceHolder1$TextBox5': '',
            'ctl00$ContentPlaceHolder1$TextBox6': '',
            'ctl00$ContentPlaceHolder1$TextBox3': id,
            'ctl00$ContentPlaceHolder1$Button3': 'Suivant',
            'ctl00$ContentPlaceHolder1$TextBox4': '',
            'ctl00$ContentPlaceHolder1$pass_parent': '',
        }

        response_id = self.session.post(self.login_url, data=id_payload)

        response = self.session.get(self.login_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        viewstate = soup.find('input', {'id': '__VIEWSTATE'})['value']
        viewstategenerator = soup.find(
            'input', {'id': '__VIEWSTATEGENERATOR'})['value']
        eventvalidation = soup.find(
            'input', {'id': '__EVENTVALIDATION'})['value']

        password_payload = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': viewstate,
            '__VIEWSTATEGENERATOR': viewstategenerator,
            '__EVENTVALIDATION': eventvalidation,
            'ctl00$ContentPlaceHolder1$TextBox1': '',
            'ctl00$ContentPlaceHolder1$TextBox5': '',
            'ctl00$ContentPlaceHolder1$TextBox6': '',
            'ctl00$ContentPlaceHolder1$TextBox7': password,
            'ctl00$ContentPlaceHolder1$ButtonEtudiant': 'Connexion',
            'ctl00$ContentPlaceHolder1$TextBox4': '',
            'ctl00$ContentPlaceHolder1$pass_parent': '',
        }

        response_password = self.session.post(
            self.login_url, data=password_payload)

        if 'Vous pouvez consulter dans cet espace :' in response_password.text:
            print("Login successful!")
            return self.session
        else:
            print("Login failed.")
