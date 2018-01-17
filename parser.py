#!/usr/bin/env python3
from urllib.request import urlopen
from urllib.request import urlretrieve
from datetime import datetime
from bs4 import BeautifulSoup
from string import Template
import codecs
import os


PAGE_COUNT = 0
ARTICLE_COUNT = 0
# =============================================
# Downloads an image into the file system and renames it.
# Returns the reference to the new filepath
# =============================================
def downloadImagefromUrl(url):
    return None;




# =============================================
# Prints a nice done message
# Note: abstracted into a function in case we want
#      other ending behaviour to be programmed later
# =============================================
def end():
    print("=====DONE====")

# =============================================
# Parse an 'index' page for article urls and
# return an array of them
# =============================================
def getArticleUrlsFromPage(soup):
    # Set up array
    urls = list()

    # Find all the anchors
    page_anchors = soup.findAll("a", class_="hitbox")

    # Extract the url from the anchors and add to the array
    for a in page_anchors:
        urls.append(a.get('href'))

    # Return array
    return urls



# =============================================
# Parse a single article and return the contents
# in a map
# =============================================
def parseArticleFromUrl(url):
    # Parse the url
    page = urlopen(url)
    soup = BeautifulSoup(page, "lxml")

    # Set up map
    article_data = dict()

    # Get the Post title
    article_data['title'] = soup.find("h1", class_ = "post__title")

    # Get the Post Author
    article_data['author'] = soup.find("a", class_= "author")

    # Get the Post Date
    article_data['date'] = soup.find("span", class_="post__dateline")

    # Get the Post Body
    article_data['body'] = soup.find("div", class_ = "post__body")

    # Download any image files contained in the article
    img_tags = article_data['body'].findAll('img')

    for img_tag in img_tags:
        print(img_tag.get('src'))


    # print(post_body.findAll('p'))
    return article_data

# =============================================
# Generates a nice filename from article data
# =============================================
def getFileNameFromArticleData(article_data):

    # Manipulate the date string to make it nicer
    date_string = article_data['date'].string.strip().lower().replace(',',"").replace(' ', "-")

    # Transform it into a datetime object so we can reconfigure the date format
    date_string = datetime.strptime(date_string, "%B-%d-%Y").strftime("%Y-%m-%d")

    # Replace the string with the new formatted output
    # date_string = date.strftime("%Y-%m-%d")

    # Manipulate the article's title to make it nicer
    title_string = article_data['title'].get_text().strip().lower().replace(' ',"-")

    # Return a formatted file title
    return "%s_%s.html" % (date_string, title_string)

# =============================================
# Converts parsed article into nice HTML
# =============================================
def getHTMLTemplateFromArticleData(article_data):

    # Do some fancy stuff with the body string to join all the p tags together in a string as a string
    body_string = "".join(str(item) for item in article_data['body'] )

    # Generate a basic html template to render posts. Css can be used later
    template = Template('<html> <meta charset="UTF-8"><head><title>$title</title></head> <body><h1>$title<h1><h2>by $author</h2> <h3>Posted $date</h3> $body </body></html>')

    # Render the template and return
    return template.safe_substitute(title=article_data['title'].get_text().strip(), date=article_data['date'].string.strip(), author=article_data['author'].string.strip(), body=body_string)

# =============================================
# Saves an article to a file on the system
# =============================================
def saveArticleToLocalFile(article_data):

    # Get a nice filename
    fileName = getFileNameFromArticleData(article_data)
    print("\t::Writing file %s" % (fileName))

    # Open a new file in write mode (note, unicode stuff)
    new_file = open("articles/%s" % (fileName), "w")
    # Generate the HTML template
    html = getHTMLTemplateFromArticleData(article_data)
    # Save the file contents to the file and close
    new_file.write(html)
    new_file.close()


# =============================================
# Given a page of articles, downloads them all
# =============================================
def downloadArticlesOnPage(page_url):
    # Nice messages
    global PAGE_COUNT
    PAGE_COUNT += 1
    print(".: Working on Page %d :." % (PAGE_COUNT))

    # Get soup for the page
    page = urlopen(page_url)
    soup = BeautifulSoup(page, "lxml")

    # Loop over article urls
    for url in getArticleUrlsFromPage(soup):
        # Nice messages

        global ARTICLE_COUNT
        ARTICLE_COUNT += 1

        print("\t::Parsing Article %d" % (ARTICLE_COUNT))

        # parse articles
        article_data = parseArticleFromUrl(url)

        # save to file
        saveArticleToLocalFile(article_data)


    # check if we have a next-page url
    next_page_url = soup.find('div', class_="more__button").find('a')

    # extract it and run again or run end
    if next_page_url is None:
        print("Done")
    else:
        next_page_url = next_page_url.get('href')
        downloadArticlesOnPage(next_page_url)
#
def init():
    # Get base url
    index_url="https://www.thehairpin.com/"

    # Create a nice subfolder for the articles to live in :-)
    if(not os.path.isdir("articles")):
        os.mkdir("articles")
    # and the images
    if(not os.path.isdir("articles/img")):
        os.mkdir("articles/img")

    # Run the program
    # downloadArticlesOnPage(index_url)

def test():
    url = "https://www.thehairpin.com/2017/12/watching-alyssa-milano-grow-up/"

    url2 = "https://www.thehairpin.com/2017/12/lace-underwear-that-was-sexy-until-all-your-pubes-poked-through-it/"

    # article_data = parseArticleFromUrl(url)
    article_data = parseArticleFromUrl(url)

test()
