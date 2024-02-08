from esprit import Esprit

# Create an Esprit object
esprit = Esprit(
    driver_path="C:/path/to/chromedriver.exe")

# Replace with your actual ID and password
id = 'ID'
password = 'PASSWORD'

# Attempt to log in
if esprit.login(id, password):
    print("Login successful.")
else:
    print("Login failed.")

# Get tables
tables = esprit.get_table_schedules()
if tables is not None:
    for table in tables:
        print(table)
else:
    print("Failed to get tables.")
