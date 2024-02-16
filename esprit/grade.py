import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


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

    def calculate_average(self, grades):
        # Convert the list of lists to a DataFrame
        df = pd.DataFrame(grades[1:], columns=grades[0])

        # Replace empty strings with NaN
        df.replace('', np.nan, inplace=True)

        # Replace comma with dot and convert to float
        for col in ['COEF', 'NOTE_CC', 'NOTE_TP', 'NOTE_EXAM']:
            df[col] = df[col].str.replace(',', '.').astype(float)

        # Calculate the average based on available grades

        def calculate_average(row):
            if pd.isna(row['NOTE_TP']):
                if pd.isna(row['NOTE_CC']):
                    return row['NOTE_EXAM']
                else:
                    return row['NOTE_EXAM'] * 0.6 + row['NOTE_CC'] * 0.4
            elif pd.isna(row['NOTE_CC']):
                return row['NOTE_EXAM'] * 0.8 + row['NOTE_TP'] * 0.2
            else:
                return row['NOTE_EXAM'] * 0.5 + row['NOTE_CC'] * 0.3 + row['NOTE_TP'] * 0.2

        df['MOYENNE'] = df.apply(calculate_average, axis=1)

        # Calculate the total average
        total_average = (df['MOYENNE'] * df['COEF']).sum() / df['COEF'].sum()

        # Append the total average to the DataFrame
        df = df._append({'DESIGNATION': 'Moyenne', 'COEF': df['COEF'].sum(
        ), 'MOYENNE': total_average}, ignore_index=True)

        print(df)
        return total_average
