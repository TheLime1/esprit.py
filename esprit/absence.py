from bs4 import BeautifulSoup


class Absence:
    """
    A class used to represent an Absence.

    ...

    Attributes
    ----------
    url : str
        a formatted string that represents the URL of the absence page
    session : requests.Session
        a Session object from the requests library

    Methods
    -------
    get_absences():
        Returns a list of absences for the student.
    """

    def __init__(self, session):
        self.url = "https://esprit-tn.com/ESPOnline/Etudiants/absenceetud.aspx"
        self.session = session

    def get_absences(self):
        """
        Returns a list of absences for the student.

        Returns
        -------
        list
            a list of absences, each represented as a list of strings. The first list is the headers.
            Returns None if the page does not contain the expected text.
        """

        response = self.session.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Check if the <strong> tag with the text "Absence" exists
        strong_tag = soup.find('strong', text='Absence')
        if strong_tag is None:
            print("The page does not contain the expected text.")
            return None

        table = soup.find('table', {'id': 'ContentPlaceHolder1_GridView2'})
        rows = table.find_all('tr')
        headers = [cell.text.strip() for cell in rows[0].find_all('th')]
        absences = [headers] + [[cell.text.strip() for cell in row.find_all('td')]
                                for row in rows[1:]]  # Skip header row
        return absences
