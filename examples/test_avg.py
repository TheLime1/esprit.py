from esprit import Esprit

# Replace with your actual ID and password
id = 'ID'
password = 'PASSWORD'

grades = None

# Keep trying to get grades until it is successful cuz esprit use garabage servers
while grades is None:
    try:
        # Create an Esprit object
        esprit = Esprit(
            driver_path="C:/path/to/chromedriver.exe")

        # Attempt to log in
        esprit.login(id, password)

        # Get grades
        grades = esprit.get_grades()

    except Exception as e:
        print(f"An error occurred: {e}. Retrying...")

if grades is not None:
    for grade in grades:
        print(grade)
else:
    print("Failed to get grades.")

esprit.calculate_average(grades)
