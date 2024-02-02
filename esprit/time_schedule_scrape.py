import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import os
from PyPDF2 import PdfReader, PdfWriter


class TimeSchedule:
    def __init__(self, session):
        self.url = "https://esprit-tn.com/ESPOnline/Etudiants/Emplois.aspx"
        self.session = session

    def get_table_schedules(self):
        response = self.session.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Check if the <strong> tag with the text "Emploi du temps" exists
        strong_tag = soup.find('strong', text='Emploi du temps')
        if strong_tag is None:
            print("The page does not contain the expected text.")
            return None

        table = soup.find('table', {'id': 'ContentPlaceHolder1_GridView1'})
        rows = table.find_all('tr')
        time_schedules = []
        for row in rows[1:]:
            row_data = []
            for cell in row.find_all('td'):
                cell_text = cell.text.strip()
                cell_link = cell.find('a')
                if cell_link is not None:
                    cell_text += ' ' + cell_link.get('href')
                row_data.append(cell_text)
            time_schedules.append(row_data)
        return time_schedules

    def get_last_week_schedule(self):
        time_schedules = self.get_table_schedules()
        if time_schedules is None:
            return None

        # Filter schedules that contain "Semaine" and extract dates
        week_schedules = [
            schedule for schedule in time_schedules if "Semaine" in schedule[0]]
        date_format = "%d-%m-%Y"
        dates_and_schedules = []

        for schedule in week_schedules:
            # Extract date from file name
            match = re.search(r"\d{2}-\d{2}-\d{4}", schedule[0])
            if match:
                date_str = match.group()
                date = datetime.strptime(date_str, date_format)
                dates_and_schedules.append((date, schedule))

        # Sort by date and return the latest schedule
        dates_and_schedules.sort(key=lambda x: x[0])
        return dates_and_schedules[-1][1] if dates_and_schedules else None

    def download_files(self, schedule):
        response = self.session.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract __VIEWSTATE and __EVENTVALIDATION values
        viewstate = soup.find('input', {'id': '__VIEWSTATE'})['value']
        eventvalidation = soup.find(
            'input', {'id': '__EVENTVALIDATION'})['value']

        # Extract eventTarget from the JavaScript function call
        event_target = schedule[1].split("'")[1]

        # Send a POST request to mimic the postback
        post_data = {
            '__EVENTTARGET': event_target,
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': viewstate,
            '__EVENTVALIDATION': eventvalidation,
        }
        file_response = self.session.post(self.url, data=post_data)

        # Save the file
        file_path = os.path.join(os.getcwd(), schedule[0])
        with open(file_path, 'wb') as f:
            f.write(file_response.content)

        return file_path

    def get_class_week_schedule(self, file_path, class_name):
        # Open the existing PDF
        with open(file_path, "rb") as file:
            reader = PdfReader(file)

            # Assume class_name is found on a specific page
            for page_number in range(len(reader.pages)):
                page = reader.pages[page_number]
                content = page.extract_text()

                # If class_name is found in content
                if class_name in content:
                    writer = PdfWriter()
                    writer.add_page(page)

                    # Save the page as a new PDF
                    new_file_path = f"{class_name}.pdf"
                    with open(new_file_path, "wb") as output_pdf:
                        writer.write(output_pdf)

                    return new_file_path

        return None
