from esprit import Esprit

# Create an Esprit object
esprit = Esprit()

# Replace with your actual ID and password
id = 'ID'
password = 'PASSWORD'

# Attempt to log in
if esprit.login(id, password):
    print("Login successful.")
else:
    print("Login failed.")

# Get absences
absences = esprit.get_absences()
if absences is not None:
    for absence in absences:
        print(absence)
else:
    print("Failed to get absences.")
