# Hairpin Parser

This was at the behest of a loved one who read a lot of the website 'The Hairpin' (https://thehairpin.com) which shutdown at the end of January 2018.

I wanted to teach myself the basic of web scraping in Python so instead of finding pre-existing scripts I decided to hack together my own. There's probably tonnes wrong.

## Installation

Requires BeautifulSoup 4 and Python 3.

    sudo apt-get install python-pip
    sudo apt-get install python-bs4

## Usage
Download this script anywhere on your machine. Usually in its own folder.

Open a terminal, navigate to the script's location and enter the following to give the script permission to execute

    sudo chmod +x parser.py

Afterwards, you can run the script by running (in a terminal)

    ./parser.py

### Behaviour
The script will create a folder called `articles` at the same folder level where it lives. It will then download all the articles it can into that folder named with the date and title of the article.

Current version estimated to take ~2 hrs total time.

## TODO
+ Download local copies of the images and rewrite the img tags inside the articles to match the new file.
+ Render archive into an epub template for usage on e-readers
