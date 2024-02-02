import requests


class Auth:
    def __init__(self, session=None):
        self.login_url = "https://esprit-tn.com/esponline/online/default.aspx"
        self.session = session if session else requests.session()

    def login(self, id, password):
        id_payload = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': '/wEPDwUJNDE1NjEwODA3D2QWAmYPZBYCAgMPZBYCAgUPDxYCHgRUZXh0BQkyMDIzLzIwMjRkZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WAQUSY3RsMDAkSW1hZ2VCdXR0b24x4A+yHAaVbbd+c/7zRnwYiufwfrp/gfS8JKpvS+xXvpE=',
            '__VIEWSTATEGENERATOR': '717FCBFE',
            '__EVENTVALIDATION': '/wEdAA3BKAYcHauA5ahZijRjSsR/D4zZrxX92uOlyIx1SyGTQokHj7KsGQZ9KI/q0cgR79eMO7fmjkJSfq6Zbgk2kTWn5BPdHG87XtyblNclsuAS8LvwPnslbtZbTzH+LM3KrmKoScikkrtCyMBYLZBZxv2YCNTGu6fpAlK5HiRhQ3QX7uQuDNsn18Vb/yPhT9ZPmVoNeSKFy2zxLVV4+zExdQxF5O2yeRHTM5Q6txDv+t953Rsahgpohlzzax1rmqU36I8bifdujSibODz2lHN+RHz6gNEqtVw0ulNZz52C7FdPSyEa0/J8qJqqEgP2sogExFA=',
            'ctl00$ContentPlaceHolder1$TextBox1': '',
            'ctl00$ContentPlaceHolder1$TextBox5': '',
            'ctl00$ContentPlaceHolder1$TextBox6': '',
            'ctl00$ContentPlaceHolder1$TextBox3': id,
            'ctl00$ContentPlaceHolder1$Button3': 'Suivant',
            'ctl00$ContentPlaceHolder1$TextBox4': '',
            'ctl00$ContentPlaceHolder1$pass_parent': '',
        }

        response_id = self.session.post(self.login_url, data=id_payload)

        password_payload = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': '/wEPDwUJNDE1NjEwODA3D2QWAmYPZBYCAgMPZBYEAgUPDxYCHgRUZXh0BQkyMDIzLzIwMjRkZAIJD2QWAgIQD2QWEAIBDw8WAh4HVmlzaWJsZWhkZAIDDw8WBB8ABQoyMjFKTVQ1MzI2HwFoZGQCBw8PFgIfAWdkZAIJDw8WAh8BZ2RkAgsPDxYCHgdFbmFibGVkZ2RkAg0PDxYCHwFnZGQCDw8PFgIfAWdkZAIRDw8WAh8BaGRkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBRJjdGwwMCRJbWFnZUJ1dHRvbjF0JCLryb54s4inGLRx9VnEDk2ACOOB+Q8HNhb+Z6hPjQ==',
            '__VIEWSTATEGENERATOR': '717FCBFE',
            '__EVENTVALIDATION': '/wEdAA6E6Tm89lU7S/3iqJUOatsjD4zZrxX92uOlyIx1SyGTQokHj7KsGQZ9KI/q0cgR79eMO7fmjkJSfq6Zbgk2kTWn5BPdHG87XtyblNclsuAS8LvwPnslbtZbTzH+LM3KrmKoScikkrtCyMBYLZBZxv2Y4YHt2yH9TCYlNrTCCQccHuaXknurQIHyJEMAivskpdkfOLtcwEziInaQqEgDH0GiDXkihcts8S1VePsxMXUMReTtsnkR0zOUOrcQ7/rfed0bGoYKaIZc82sda5qlN+iPG4n3bo0omzg89pRzfkR8+mvbAUFWGOWJTqU2Q6L6lue8OojTbFO8vtwsRzaPKiZW',
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
