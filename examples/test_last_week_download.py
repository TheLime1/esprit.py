from esprit import Esprit

# Create an Esprit object
esprit = Esprit()

# Replace with your actual ID and password
id = 'ID'
password = 'PASSWORD'

# Path where the downloaded file will be saved
path = '/path/to/save/file'

# Attempt to log in
if esprit.login(id, password):
    print("Login successful.")

    # Get the last week's schedule
    schedule = esprit.get_last_week_schedule()
    if schedule is not None:
        # Download the last week's schedule
        esprit.download_files(schedule, path)
        print("Downloaded the last week's schedule.")
    else:
        print("Failed to get the last week's schedule.")
else:
    print("Login failed.")
