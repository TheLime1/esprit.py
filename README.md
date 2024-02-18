# <img src="https://esprit.tn/favicon.ico" width="28px" /> esprit-py

[![PyPI version](https://badge.fury.io/py/esprit-py.svg)](https://pypi.org/project/esprit-py/)

> [!NOTE]
> Please note that this library is not an official API provided by Esprit and is intended for educational and personal use only.

## Features

- Get your exact timetable pdf *not 300 pages pdf*
- Get your grades
- Get your absences
- Get your credits
- Calculate your total semester average

## Installation

```bash
pip install --upgrade esprit-py
```

## Examples

get your total avreage:

```python
from esprit import Esprit

# Replace with your actual ID and password
id = 'ID'
password = 'PASSWORD'

grades = None

# Keep trying to get grades until it is successful cuz esprit use garabage servers
while grades is None:
    try:
        # Create an Esprit object
        esprit = Esprit()

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

```

get a list of all your absences;

```python
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

```

More examples can be found in the [examples folder](examples)