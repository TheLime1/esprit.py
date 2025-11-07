from bs4 import BeautifulSoup


class Credit:
    """
    A class used to represent a Credit.

    ...

    Attributes
    ----------
    url : str
        a formatted string that represents the URL of the credit page
    session : requests.Session
        a Session object from the requests library

    Methods
    -------
    get_credits():
        Returns a list of credits for the student.
    """

    def __init__(self, session):
        self.url = "https://esprit-tn.com/ESPOnline/Etudiants/Historique_Cr%C3%A9dit.aspx"
        self.session = session

    def get_credits(self):
        """
        Returns a list of credits for the student.

        Returns
        -------
        list
            a list of credits, each represented as a list of strings. The first list is the headers.
            Returns None if the page does not contain the expected text.
        """
        response = self.session.get(self.url, allow_redirects=False)
        if response.status_code == 302 or response.status_code == 301:
            # Follow redirect
            response = self.session.get(self.url, allow_redirects=True)
        
        if response.status_code != 200:
            print("Failed to load credits page.")
            return None
        
        # Check if we were redirected to login page
        if 'default.aspx' in response.url or 'login' in response.url.lower():
            print("Session expired or invalid - redirected to login page.")
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the table with id='ContentPlaceHolder1_GridView1'
        table = soup.find('table', {'id': 'ContentPlaceHolder1_GridView1'})
        if table is None:
            # Try to find table by structure (has headers like "Année universitaire")
            all_tables = soup.find_all('table')
            for tbl in all_tables:
                rows = tbl.find_all('tr')
                if len(rows) > 0:
                    first_row = rows[0]
                    ths = first_row.find_all('th')
                    if len(ths) > 0:
                        headers = [th.text.strip() for th in ths]
                        if 'Année universitaire' in headers or 'Unité d\'enseignement' in headers:
                            table = tbl
                            break
            
            if table is None:
                print("Credits table not found on page.")
                return None

        rows = table.find_all('tr')
        if len(rows) == 0:
            print("No rows found in credits table.")
            return None
        
        # Extract headers from first row
        headers = [cell.text.strip() for cell in rows[0].find_all('th')]
        if len(headers) == 0:
            print("No headers found in credits table.")
            return None
        
        # Extract data rows
        credits = [headers]
        for row in rows[1:]:  # Skip header row
            cells = [cell.text.strip() for cell in row.find_all('td')]
            if len(cells) > 0:
                credits.append(cells)
        
        return credits
