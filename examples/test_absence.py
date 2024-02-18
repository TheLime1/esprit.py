from esprit import Esprit

# Create an Esprit object
esprit = Esprit()

# Replace with your actual ID and password
id = 'ID'
password = 'PASSWORD'

# Attempt to log in
esprit.login(id, password)

# Get absences
absences = esprit.get_absences()
if absences is not None:
    for absence in absences:
        print(absence)
else:
    print("Failed to get absences.")
