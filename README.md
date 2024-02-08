# <img src="https://esprit.tn/favicon.ico" width="28px" /> esprit-py

> [!NOTE]
> Please note that this library is not an official API provided by Esprit and is intended for educational and personal use only.

## Features

- Get your exact timetable pdf *not 300 pages pdf*
- Get your grades
- Get your absences
- Get your credits

## Installation

```bash
pip install esprit-py
```

download `chromedriver` from [here](https://googlechromelabs.github.io/chrome-for-testing/#stable)

## Example

```python
from esprit import Esprit

# Create an Esprit object
esprit = Esprit(
    driver_path="C:/path/to/chromedriver.exe",)

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