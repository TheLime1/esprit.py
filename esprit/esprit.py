import requests
from .auth import Auth
from .grade import Grade
from .absence import Absence
from .time_schedule import TimeSchedule
from .credit import Credit
from .utils import Utils
# from .exceptions import EspritException #TODO


class Esprit:
    def __init__(self, driver_path=None, driver=None, debug=False, headless=True):
        self.session = requests.Session()
        self.auth = Auth(driver_path, driver, debug, headless)
        self.grade_scrape = Grade(self.session)
        self.absence_scrape = Absence(self.session)
        self.time_schedule_scrape = TimeSchedule(self.session)
        self.credit = Credit(self.session)
        self.utils = Utils(self.session)

    def login(self, username, password):
        cookies = self.auth.login(username, password)
        cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
        self.session.cookies.update(cookies_dict)

    def get_grades(self):
        return self.grade_scrape.get_grades()

    def calculate_average(self, grades):
        return self.grade_scrape.calculate_average(grades)

    def get_absences(self):
        return self.absence_scrape.get_absences()

    def get_table_schedules(self):
        return self.time_schedule_scrape.get_table_schedules()

    def get_last_week_schedule(self):
        return self.time_schedule_scrape.get_last_week_schedule()

    def download_files(self, schedule, download_path):
        return self.time_schedule_scrape.download_files(schedule, download_path)

    def get_class_week_schedule(self, file_path, class_name, result_path):
        return self.time_schedule_scrape.get_class_week_schedule(file_path, class_name, result_path)

    def get_credits(self):
        return self.credit.get_credits()

    def get_student_name(self):
        return self.utils.get_student_name()

    def get_student_class(self):
        return self.utils.get_student_class()
