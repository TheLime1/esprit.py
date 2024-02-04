from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# Read requirements.txt
with open(os.path.join(here, 'requirements.txt')) as f:
    requirements = f.read().splitlines()

VERSION = '0.2.4'
DESCRIPTION = ' A Python library for interacting with data from esprit-tn.com'
LONG_DESCRIPTION = 'esprit-py, provides a set of tools for interacting with data from the Esprit website. It includes functionalities for scraping grades, absences, time schedules, and credits. It also provides the ability to download files and get class week schedules.'

# Setting up
setup(
    name="esprit-py",
    version=VERSION,
    author="Lime1 (Aymen Hmani)",
    author_email="<everpadd4@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=requirements,
    keywords=['python', 'api'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    package_data={"": ["requirements.txt"]},
    url="https://github.com/TheLime1/esprit.py"
)

'''
python setup.py sdist bdist_wheel
twine check dist/*
twine upload dist/*
-
username: __token__
password: pypi-...
'''
