from esprit import Esprit

# Create an Esprit object
esprit = Esprit()

# Replace with your actual ID and password
id = 'ID'
password = 'PASSWORD'

# Attempt to log in
esprit.login(id, password)

# Get tables
tables = esprit.get_table_schedules()
if tables is not None:
    for table in tables:
        print(table)
else:
    print("Failed to get tables.")
