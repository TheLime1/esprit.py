import requests
from bs4 import BeautifulSoup


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
    session : requests.Session
        a requests Session object to maintain cookies and state

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
                Path to the WebDriver executable (deprecated, kept for compatibility)
            driver : WebDriver, optional
                Existing WebDriver instance (deprecated, kept for compatibility)
            debug : bool, optional
                Debug mode flag (default is False)
            headless : bool, optional
                Headless mode flag (deprecated, kept for compatibility)
        """

        self.login_url = "https://esprit-tn.com/esponline/online/default.aspx"
        self.home_url = "https://esprit-tn.com/esponline/Etudiants/Accueil.aspx"
        self.logout_urls = [
            "https://esprit-tn.com/esponline/Etudiants/Deconnexion.aspx",
            "https://esprit-tn.com/esponline/online/Deconnexion.aspx",
        ]
        self.debug = debug
        self.session = requests.Session()
        # Set user agent to mimic a real browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

    def _extract_viewstate(self, html):
        """Extract ASP.NET ViewState and EventValidation from HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        viewstate = soup.find('input', {'id': '__VIEWSTATE'})
        viewstate_generator = soup.find('input', {'id': '__VIEWSTATEGENERATOR'})
        event_validation = soup.find('input', {'id': '__EVENTVALIDATION'})
        
        data = {}
        if viewstate:
            data['__VIEWSTATE'] = viewstate.get('value', '')
        if viewstate_generator:
            data['__VIEWSTATEGENERATOR'] = viewstate_generator.get('value', '')
        if event_validation:
            data['__EVENTVALIDATION'] = event_validation.get('value', '')
        
        return data

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

        # Step 1: Get the initial login page
        response = self.session.get(self.login_url)
        if response.status_code != 200:
            print('Failed to load login page')
            return None
        
        # Extract ViewState and EventValidation
        form_data = self._extract_viewstate(response.text)
        
        # Step 2: Find the ID input field and checkbox on initial page
        soup = BeautifulSoup(response.text, 'html.parser')
        # Try to find ID field by various methods
        id_input = (soup.find('input', {'id': lambda x: x and 'textbox3' in x.lower()}) or
                   soup.find('input', {'id': lambda x: x and 'textbox1' in x.lower()}) or
                   soup.find('input', {'type': 'text', 'id': lambda x: x and 'textbox' in x.lower()}))
        id_field_name = None
        if id_input:
            id_field_name = id_input.get('name') or id_input.get('id', '')
            if self.debug:
                print(f'Found ID field: id={id_input.get("id")}, name={id_field_name}')
        
        # Find the checkbox on the initial page (before clicking Suivant)
        checkbox = soup.find('input', {'type': 'checkbox'})
        checkbox_name = None
        if checkbox:
            checkbox_name = checkbox.get('name') or checkbox.get('id', '')
            if self.debug:
                print(f'Found checkbox on initial page: id={checkbox.get("id")}, name={checkbox_name}')
        
        # Use dynamic name if found, otherwise try both with and without ctl00$ prefix
        if id_field_name:
            form_data[id_field_name] = id
        else:
            form_data['ctl00$ContentPlaceHolder1$TextBox3'] = id
            form_data['ContentPlaceHolder1$TextBox3'] = id
        
        # First, check the checkbox to reveal continue button
        if checkbox_name:
            form_data_checkbox = self._extract_viewstate(response.text)
            form_data_checkbox[id_field_name] = id
            form_data_checkbox[checkbox_name] = 'on'
            form_data_checkbox['__EVENTTARGET'] = checkbox_name
            form_data_checkbox['__EVENTARGUMENT'] = ''
            
            if self.debug:
                print('Checking checkbox to reveal continue button...')
            
            response_checkbox = self.session.post(self.login_url, data=form_data_checkbox)
            if response_checkbox.status_code == 200:
                # Check if continue button appeared
                soup_checkbox = BeautifulSoup(response_checkbox.text, 'html.parser')
                continue_button = (soup_checkbox.find('input', {'type': 'submit', 'value': lambda x: x and ('continuer' in x.lower() or 'continue' in x.lower())}) or
                                 soup_checkbox.find('input', {'type': 'button', 'value': lambda x: x and ('continuer' in x.lower() or 'continue' in x.lower())}) or
                                 soup_checkbox.find('button', string=lambda x: x and ('continuer' in x.lower() or 'continue' in x.lower())))
                
                # Debug: Check all buttons on the page after checking checkbox
                all_buttons = soup_checkbox.find_all('input', {'type': ['submit', 'button']})
                if self.debug:
                    print(f'Found {len(all_buttons)} buttons on page after checking checkbox')
                    for btn in all_buttons:
                        btn_id = btn.get('id', '')
                        btn_name = btn.get('name', '')
                        btn_value = btn.get('value', '')
                        print(f'  Button: id={btn_id}, name={btn_name}, value={btn_value}')
                
                if continue_button:
                    if self.debug:
                        print('Continue button appeared, clicking it...')
                    # Click continue button
                    form_data_continue = self._extract_viewstate(response_checkbox.text)
                    form_data_continue[id_field_name] = id
                    form_data_continue[checkbox_name] = 'on'
                    continue_button_name = continue_button.get('name') or continue_button.get('id', '')
                    form_data_continue['__EVENTTARGET'] = continue_button_name
                    form_data_continue['__EVENTARGUMENT'] = ''
                    
                    response_continue = self.session.post(self.login_url, data=form_data_continue)
                    if response_continue.status_code == 200:
                        response = response_continue
                        form_data = self._extract_viewstate(response_continue.text)
                        form_data[id_field_name] = id
                        form_data[checkbox_name] = 'on'
                    else:
                        response = response_checkbox
                        form_data = self._extract_viewstate(response_checkbox.text)
                        form_data[id_field_name] = id
                        form_data[checkbox_name] = 'on'
                else:
                    # No continue button found by text, but maybe it's the Suivant button that's now enabled?
                    # Or maybe we can proceed directly with Suivant
                    if self.debug:
                        print('Continue button not found, proceeding with Suivant')
                    response = response_checkbox
                    form_data = self._extract_viewstate(response_checkbox.text)
                    form_data[id_field_name] = id
                    form_data[checkbox_name] = 'on'
            else:
                # If checkbox interaction fails, proceed normally
                if self.debug:
                    print('Checkbox interaction failed, proceeding normally')
                form_data[id_field_name] = id
        
        # Find the Suivant button dynamically
        # After checking checkbox, Button3 becomes visible (Button1 is hidden)
        soup_current = BeautifulSoup(response.text, 'html.parser')
        suivant_button = (soup_current.find('input', {'id': lambda x: x and 'button3' in x.lower()}) or
                         soup_current.find('input', {'name': lambda x: x and 'button3' in x.lower()}) or
                         soup_current.find('input', {'type': 'submit', 'value': lambda x: x and ('suivant' in x.lower() or 'next' in x.lower())}) or
                         soup_current.find('input', {'id': lambda x: x and 'button1' in x.lower()}) or
                         soup_current.find('input', {'name': lambda x: x and 'button1' in x.lower()}))
        
        if suivant_button:
            button_name = suivant_button.get('name') or suivant_button.get('id', '')
            if button_name:
                form_data['__EVENTTARGET'] = button_name
                if self.debug:
                    print(f'Found suivant button: {button_name}')
        else:
            # Fall back to Button3 (after checkbox) or Button1
            form_data['__EVENTTARGET'] = 'ctl00$ContentPlaceHolder1$Button3'
            if self.debug:
                print('Using default suivant button name (Button3)')
        
        form_data['__EVENTARGUMENT'] = ''
        
        # Step 3: Submit the ID with checkbox checked (click 'Suivant' button)
        response = self.session.post(self.login_url, data=form_data)
        if response.status_code != 200:
            print('Failed to submit ID')
            return None
        
        # Check for incorrect ID error
        soup_after_id = BeautifulSoup(response.text, 'html.parser')
        
        # Check if we're still on the initial page (not moved to password page)
        # If ID field (TextBox3) is still present but password field (TextBox7) is not, ID is wrong
        password_field_check = soup_after_id.find('input', {'id': lambda x: x and 'textbox7' in x.lower()})
        id_field_still_present = soup_after_id.find('input', {'id': lambda x: x and 'textbox3' in x.lower()})
        
        # If we're still on ID page (TextBox3 present, TextBox7 absent), ID is incorrect
        if id_field_still_present and not password_field_check:
            # We're still on the ID page, not moved to password page
            print('Identifiant incorrect !')
            return None
        
        if self.debug:
            print('After submitting ID with checkbox checked, now on password page...')
        
        # Step 4: Extract ViewState again after clicking Suivant (now on password page)
        form_data = self._extract_viewstate(response.text)
        
        # Step 5: Submit the password (click 'Connexion' button)
        # Use the latest response (after continue button click)
        # Re-parse the latest response to find password field
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if self.debug:
            # Check what's on the current page
            all_inputs = soup.find_all('input')
            print(f'Current page has {len(all_inputs)} input fields')
            for inp in all_inputs:
                inp_type = inp.get('type', '')
                inp_id = inp.get('id', '')
                inp_name = inp.get('name', '')
                inp_value = inp.get('value', '')
                if inp_type == 'password' or 'password' in inp_id.lower() or 'password' in inp_name.lower():
                    print(f'  Password input: id={inp_id}, name={inp_name}, type={inp_type}, disabled={inp.get("disabled")}')
                elif inp_type == 'text':
                    print(f'  Text input: id={inp_id}, name={inp_name}, value={inp_value[:30] if inp_value else ""}')
                elif inp_type == 'hidden':
                    print(f'  Hidden input: id={inp_id}, name={inp_name}, value={inp_value[:30] if inp_value else ""}')
                elif inp_type in ['submit', 'button']:
                    print(f'  Button: id={inp_id}, name={inp_name}, value={inp_value}')
        
        # Find password field for student (TextBox7, not TextBox2!)
        password_input = (soup.find('input', {'id': lambda x: x and 'textbox7' in x.lower()}) or
                         soup.find('input', {'name': lambda x: x and 'textbox7' in x.lower()}) or
                         soup.find('input', {'type': 'password'}))
        password_field_name = None
        if password_input:
            password_field_name = password_input.get('name') or password_input.get('id', '')
            if self.debug:
                print(f'Found password field: {password_field_name}')
                # Check if it's disabled
                if password_input.get('disabled'):
                    print('WARNING: Password field is disabled!')
        
        # Use dynamic name if found, otherwise fall back to default
        if password_field_name:
            form_data[password_field_name] = password
        else:
            # Try both with and without ctl00$ prefix
            form_data['ctl00$ContentPlaceHolder1$TextBox7'] = password
            form_data['ContentPlaceHolder1$TextBox7'] = password
        
        # DO NOT include ID or checkbox - they don't exist on the password page after Suivant!
        
        # Find the connection button for student (ButtonEtudiant, not Button2!)
        connexion_button = (soup.find('input', {'id': lambda x: x and 'buttonetudiant' in x.lower()}) or
                          soup.find('input', {'name': lambda x: x and 'buttonetudiant' in x.lower()}) or
                          soup.find('input', {'type': 'submit', 'value': lambda x: x and ('connexion' in x.lower() or 'connect' in x.lower())}) or
                          soup.find('input', {'id': lambda x: x and 'button2' in x.lower()}) or
                          soup.find('input', {'name': lambda x: x and 'button2' in x.lower()}))
        
        if connexion_button:
            button_name = connexion_button.get('name') or connexion_button.get('id', '')
            if button_name:
                # For ASP.NET, use __EVENTTARGET with the button name
                form_data['__EVENTTARGET'] = button_name
                form_data['__EVENTARGUMENT'] = ''
                if self.debug:
                    print(f'Found connexion button: {button_name}, using __EVENTTARGET')
        else:
            # Fall back to default (ButtonEtudiant for student login)
            form_data['__EVENTTARGET'] = 'ctl00$ContentPlaceHolder1$ButtonEtudiant'
            form_data['__EVENTARGUMENT'] = ''
            if self.debug:
                print('Using default connexion button name (ButtonEtudiant)')
        
        if self.debug:
            print('Submitting password (without ID or checkbox)')
        
        if self.debug:
            print(f'Submitting password with form data keys: {list(form_data.keys())}')
        
        # Use the current page URL (password page) instead of login URL
        current_url = response.url if hasattr(response, 'url') else self.login_url
        if self.debug:
            print(f'Posting to URL: {current_url}')
        
        response = self.session.post(current_url, data=form_data, allow_redirects=True)
        
        if self.debug:
            print(f'After password submission:')
            print(f'  Status code: {response.status_code}')
            print(f'  Final URL: {response.url}')
            print(f'  Redirected: {response.url != self.login_url}')
            
            # Check what's in the response
            if 'error' in response.text.lower() or 'erreur' in response.text.lower():
                print('Response contains error/erreur')
            if 'invalid' in response.text.lower() or 'invalide' in response.text.lower():
                print('Response contains invalid/invalide')
        
        # Check for incorrect password (still on password page after submission)
        soup_after_password = BeautifulSoup(response.text, 'html.parser')
        password_field_still_present = soup_after_password.find('input', {'id': lambda x: x and 'textbox7' in x.lower()})
        is_still_on_login_page = 'default.aspx' in response.url.lower()
        
        # If we're still on default.aspx (login page) with password field present, password was incorrect
        if is_still_on_login_page and password_field_still_present:
            print('Mot de passe incorrect ! Redirection vers la page de connexion...')
            return None
        
        # Check if login was successful
        # After successful login, we should be redirected to Accueil.aspx (home page)
        # Check if we're on the login page (default.aspx) or home page (Accueil.aspx)
        is_on_login_page = 'default.aspx' in response.url.lower()
        is_on_home_page = 'accueil.aspx' in response.url.lower() or 'Accueil.aspx' in response.url
        
        # Look for multiple success indicators
        success_indicators = [
            'Vous pouvez consulter dans cet espace :',
            'Espace Etudiant',
            'Accueil.aspx',
            'Label2',  # Student name label
            'Label3'   # Student class label
        ]
        
        login_successful = (not is_on_login_page) and (is_on_home_page or any(indicator in response.text for indicator in success_indicators))
        
        if self.debug:
            print(f'Checking login success...')
            print(f'  On login page: {is_on_login_page}')
            print(f'  On home page: {is_on_home_page}')
            for indicator in success_indicators:
                if indicator in response.text:
                    print(f'  Found success indicator: {indicator}')
        
        if login_successful:
            print('''
                  -----------------
                  Login successful!
                  -----------------
                  ''')
            # Convert requests cookies to Selenium-like format for compatibility
            cookies = []
            for cookie in self.session.cookies:
                cookies.append({
                    'name': cookie.name,
                    'value': cookie.value,
                    'domain': cookie.domain,
                    'path': cookie.path
                })
            return cookies
        else:
            print('''
                  -------------
                  Login failed!
                  -------------
                  ''')
            return None
    
    def logout(self):
        """
        Logout from the ESPRIT website.
        
        Returns:
            bool: True if logout was successful, False otherwise.
        """
        if self.debug:
            print('Starting logout...')
        
        # Method 1: Try ASP.NET postback mechanism
        try:
            # Get the home page to retrieve ViewState
            response = self.session.get(self.home_url, allow_redirects=True)
            
            if response.status_code == 200 and 'default.aspx' not in response.url.lower():
                # We're logged in, now perform logout postback
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract ViewState for the postback
                form_data = self._extract_viewstate(response.text)
                
                # Set up the postback to trigger LinkButton1 (logout button)
                form_data['__EVENTTARGET'] = 'ctl00$LinkButton1'
                form_data['__EVENTARGUMENT'] = ''
                
                if self.debug:
                    print('Sending logout postback...')
                
                # Submit the logout postback
                logout_response = self.session.post(self.home_url, data=form_data, allow_redirects=True)
                
                # Check if we're redirected to login page
                if 'default.aspx' in logout_response.url or logout_response.status_code == 200:
                    if self.debug:
                        print('Logout successful (postback method)')
                    return True
        except Exception as e:
            if self.debug:
                print(f'Postback logout failed: {e}')
        
        # Method 2: Try direct logout URLs
        for logout_url in self.logout_urls:
            try:
                if self.debug:
                    print(f'Trying logout URL: {logout_url}')
                
                response = self.session.get(logout_url, allow_redirects=True)
                
                # Check if redirected to login page or session cleared
                if 'default.aspx' in response.url or response.status_code == 200:
                    if self.debug:
                        print(f'Logout successful via URL: {logout_url}')
                    return True
            except Exception as e:
                if self.debug:
                    print(f'Logout URL {logout_url} failed: {e}')
                continue
        
        # Method 3: Clear session cookies as fallback
        if self.debug:
            print('Clearing session cookies...')
        self.session.cookies.clear()
        
        return True
