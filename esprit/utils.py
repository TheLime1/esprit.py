from bs4 import BeautifulSoup


class Utils:
    """
    A utility class for interacting with the ESPRIT website.
    """

    def __init__(self, session):
        # Try both URL formats (case might matter)
        self.url = "https://esprit-tn.com/ESPOnline/Etudiants/Accueil.aspx"
        self.url_alt = "https://esprit-tn.com/esponline/Etudiants/Accueil.aspx"
        self.session = session

    def get_student_name(self):
        """
        Get the name of the student from the ESPRIT website.

        Returns:
            The name of the student, or None if the name could not be found.
        """
        # Try primary URL first
        response = self.session.get(self.url, allow_redirects=True)
        
        # Check if we were redirected to login page
        if 'default.aspx' in response.url or 'login' in response.url.lower():
            # Try alternative URL
            response = self.session.get(self.url_alt, allow_redirects=True)
            if 'default.aspx' in response.url or 'login' in response.url.lower():
                print("Session expired or invalid - redirected to login page.")
                return None
        
        if response.status_code != 200:
            print("Failed to load student page.")
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the span with id='Label2' and class='h4 text-info'
        span = soup.find('span', {'id': 'Label2', 'class': 'h4 text-info'})
        if span is not None and span.text.strip():
            return span.text.strip()
        
        # Try alternative: ContentPlaceHolder1_Label2
        span = soup.find('span', {'id': 'ContentPlaceHolder1_Label2'})
        if span is not None and span.text.strip():
            return span.text.strip()
        
        # Try alternative: just find by id='Label2'
        span = soup.find('span', {'id': 'Label2'})
        if span is not None and span.text.strip():
            return span.text.strip()
        
        print("Student name not found on page.")
        return None

    def get_student_class(self):
        """
        Get the class of the student from the ESPRIT website.

        Returns:
            The class of the student, or None if the class could not be found.
        """
        # Try primary URL first
        response = self.session.get(self.url, allow_redirects=True)
        
        # Check if we were redirected to login page
        if 'default.aspx' in response.url or 'login' in response.url.lower():
            # Try alternative URL
            response = self.session.get(self.url_alt, allow_redirects=True)
            if 'default.aspx' in response.url or 'login' in response.url.lower():
                print("Session expired or invalid - redirected to login page.")
                return None
        
        if response.status_code != 200:
            print("Failed to load student page.")
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the span with id='Label3'
        span = soup.find('span', {'id': 'Label3'})
        if span is not None and span.text.strip():
            return span.text.strip()
        
        # Try alternative: ContentPlaceHolder1_Label3
        span = soup.find('span', {'id': 'ContentPlaceHolder1_Label3'})
        if span is not None and span.text.strip():
            return span.text.strip()
        
        print("Student class not found on page.")
        return None

