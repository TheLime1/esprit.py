from esprit import Esprit

# Create an Esprit object
esprit = Esprit(
    driver_path="C:/path/to/chromedriver.exe")

# Replace with your actual ID and password
id = 'ID'
password = 'PASSWORD'

download_path = "C:/path/to/download/folder/"

# Attempt to log in
if esprit.login(id, password):
    print("Login successful.")

    # Get the last week's schedule
    schedule = esprit.get_last_week_schedule()
    if schedule is not None:
        # Download the last week's schedule
        file_path = esprit.download_files(schedule, download_path)
        print("Downloaded the last week's schedule.")

        # Get the schedule for class 2A23
        class_schedule_path = esprit.get_class_week_schedule(
            file_path, '2A23', download_path)
        if class_schedule_path is not None:
            print(
                f"Downloaded the schedule for class 2A23 at {class_schedule_path}")
        else:
            print("Failed to get the schedule for class 2A23.")
    else:
        print("Failed to get the last week's schedule.")
else:
    print("Login failed.")
