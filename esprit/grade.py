import requests
from bs4 import BeautifulSoup


class Grade:
    """
    A class used to represent a Grade.

    ...

    Attributes
    ----------
    url : str
        a formatted string that represents the URL of the grade page
    session : requests.Session
        a Session object from the requests library

    Methods
    -------
    get_grades():
        Returns a list of grades for the student.
    """

    def __init__(self, session):
        self.url = "https://esprit-tn.com/ESPOnline/Etudiants/Resultat2021.aspx"
        self.session = session

    def get_grades(self):
        """
        Returns a list of grades for the student.

        Returns
        -------
        list
            a list of grades, each represented as a list of strings. The first list is the headers.
            Returns None if the page does not contain the expected text.
        """
        response = self.session.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Check if the <h1> tag with the text "Notes Des Modules" exists
        h1_tag = soup.find('h1', text=' Notes Des Modules ')
        if h1_tag is None:
            print("The page does not contain the expected text.")
            return None

        table = soup.find('table', {'id': 'ContentPlaceHolder1_GridView1'})
        rows = table.find_all('tr')
        headers = [cell.text.strip() for cell in rows[0].find_all('th')]
        grades = [headers] + [[cell.text.strip() for cell in row.find_all('td')]
                              for row in rows[1:]]  # Skip header row
        return grades
