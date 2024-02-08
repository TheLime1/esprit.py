from esprit import Esprit

# Create an Esprit object
esprit = Esprit(
    driver_path="C:/path/to/chromedriver.exe")

# Replace with your actual ID and password
id = 'ID'
password = 'PASSWORD'

# Attempt to log in
esprit.login(id, password)

# Get grades
grades = esprit.get_grades()
if grades is not None:
    for grade in grades:
        print(grade)
else:
    print("Failed to get grades.")
