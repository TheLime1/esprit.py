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

# Get credits
credits = esprit.get_credits()
if credits is not None:
    for credit in credits:
        print(credit)
else:
    print("Failed to get credits.")
