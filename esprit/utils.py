from bs4 import BeautifulSoup


class Utils:
    """
    A utility class for interacting with the ESPRIT website.
    """

    def __init__(self, session):
        self.url = "https://esprit-tn.com/ESPOnline/Etudiants/Accueil.aspx"
        self.session = session

    def get_student_name(self):
        """
        Get the name of the student from the ESPRIT website.

        Returns:
            The name of the student, or None if the name could not be found.
        """
        response = self.session.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Check if the <p> tag with the class "lead" and the text "Vous pouvez consulter dans cet espace :" exists
        p_tag = soup.find('p', class_='lead',
                          text='Vous pouvez consulter dans cet espace :')
        if p_tag is None:
            print("The page does not contain the expected text.")
            return None

        span = soup.find('span', {'id': 'Label2', 'class': 'h4 text-info'})
        if span is not None:
            return span.text.strip()
        else:
            return None

    def get_student_class(self):
        """
        Get the class of the student from the ESPRIT website.

        Returns:
            The class of the student, or None if the class could not be found.
        """
        response = self.session.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Check if the <p> tag with the class "lead" and the text "Vous pouvez consulter dans cet espace :" exists
        p_tag = soup.find('p', class_='lead',
                          text='Vous pouvez consulter dans cet espace :')
        if p_tag is None:
            print("The page does not contain the expected text.")
            return None

        span = soup.find(
            'span', {'id': 'Label3', 'style': 'color:#CC0000;font-weight:bold;'})
        if span is not None:
            return span.text.strip()
        else:
            return None
