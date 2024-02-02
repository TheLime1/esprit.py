import requests
from bs4 import BeautifulSoup


class Credit:
    def __init__(self, session):
        self.url = "https://esprit-tn.com/ESPOnline/Etudiants/Historique_Cr%C3%A9dit.aspx"
        self.session = session

    def get_credits(self):
        response = self.session.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Check if the <span> tag with the class "style5" and the text "Historique des Crédits" exists
        span_tag = soup.find(
            'span', {'class': 'style5'}, text='   Historique des Crédits  ')
        if span_tag is None:
            print("The page does not contain the expected text.")
            return None

        table = soup.find('table', {'id': 'ContentPlaceHolder1_GridView1'})
        rows = table.find_all('tr')
        headers = [cell.text.strip() for cell in rows[0].find_all('th')]
        grades = [headers] + [[cell.text.strip() for cell in row.find_all('td')]
                              for row in rows[1:]]  # Skip header row
        return grades
