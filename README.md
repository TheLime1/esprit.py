# esprit-py

[![PyPI version](https://badge.fury.io/py/esprit-py.svg)](https://pypi.org/project/esprit-py/)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/esprit-py?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/esprit-py)
![PyPI - Downloads](https://img.shields.io/pypi/dm/esprit-py)

> [!NOTE]
> Please note that this library is not an official API provided by Esprit and is intended for educational and personal use only.

## Features

- **Fast & Lightweight**: 5-10x faster than previous versions (no Selenium/browser required)
- Get your exact timetable pdf *not 300 pages pdf*
- Get your grades
- Get your absences
- Get your credits
- Calculate your total semester average
- **New**: Logout functionality for proper session management

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

# Logout when done
esprit.logout()

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

# Logout when done
esprit.logout()

```

More examples can be found in the [examples folder](examples)
