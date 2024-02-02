import requests
from auth import Auth
from grade_scrape import Grade
from absence_scrape import Absence
from time_schedule_scrape import TimeSchedule
from credit import Credit


class Esprit:
    def __init__(self):
        self.session = requests.Session()
        self.auth = Auth(self.session)
        self.grade_scrape = Grade(self.session)
        self.grade_scrape = Grade(self.session)
        self.absence_scrape = Absence(self.session)
        self.time_schedule_scrape = TimeSchedule(self.session)
        self.credit = Credit(self.session)

    def login(self, username, password):
        return self.auth.login(username, password)

    def get_grades(self):
        return self.grade_scrape.get_grades()

    def get_absences(self):
        return self.absence_scrape.get_absences()

    def get_table_schedules(self):
        return self.time_schedule_scrape.get_table_schedules()

    def get_last_week_schedule(self):
        return self.time_schedule_scrape.get_last_week_schedule()

    def download_files(self, schedule):
        return self.time_schedule_scrape.download_files(schedule)

    def get_class_week_schedule(self, file_path, class_name):
        return self.time_schedule_scrape.get_class_week_schedule(file_path, class_name)

    def get_credits(self):
        return self.credit.get_credits()
