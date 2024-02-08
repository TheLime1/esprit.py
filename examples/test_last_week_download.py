from esprit import Esprit

# Create an Esprit object
esprit = Esprit(
    driver_path="C:/path/to/chromedriver.exe")

# Replace with your actual ID and password
id = 'ID'
password = 'PASSWORD'

# Attempt to log in
esprit.login(id, password)

# Get the last week's schedule
schedule = esprit.get_last_week_schedule()
if schedule is not None:
    # Download the last week's schedule
    esprit.download_files(schedule)
    print("Downloaded the last week's schedule.")
else:
    print("Failed to get the last week's schedule.")
