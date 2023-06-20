# Now the last step of this project will be to automate this to do it once every day!
# I will basically create the whole process I did previously, but I will make the whole block of code, a function
# make that function repeat itself every day, and to the new data to be added in the existent csv file.
import requests
import time
import numpy
import csv
import pandas as pd
from bs4 import BeautifulSoup

# base URL for the Kijiji website
base_url = "https://www.kijiji.ca"

# Using the inspect tool we can see that each of the ads are contained in a div element with a search-item class. Also,
# the titles of each ad are within an element with a title class and an associated URL (href).

page_1_url = base_url + "/b-bijoux-montre/ville-de-montreal/watches-for-men/k0c133l1700281?rb=true&ll=45.496845%2C-73.577866&address=1400+Maisonneuve+Blvd+W%2C+Montreal%2C+QC+H3G+1M8%2C+Canada&radius=10.0"
page_2_url = base_url + "/b-bijoux-montre/ville-de-montreal/watches-for-men/page-2/k0c133l1700281?radius=10.0&address=1400+Maisonneuve+Blvd+W%2C+Montreal%2C+QC+H3G+1M8%2C+Canada&ll=45.496845,-73.577866&rb=true"
pages = [page_1_url, page_2_url]


def new_data():
    df = pd.DataFrame(columns=["title", "price", "description", "date_posted",
                               "address", "url"])
    for page in pages:

        response = requests.get(page)
        soup = BeautifulSoup(response.text, "lxml")
        ads = soup.find_all("div", class_=['search-item', 'regular-ad'])
        # Code for removing third-party ads, But I will not, so I keep it as a note
        # ads = [x for x in ads if ("cas-channel" not in x["class"]) & ("third-party" not in x["class"])]

        # Now I will create a list to store all the links of every ad
        ad_links = []
        for ad in ads:
            link = ad.find_all("a", class_='title')
            for l in link:
                ad_links.append(base_url + l['href'])
        print(len(ad_links))

        # From here I will explore every link individually in my list ad_links, and take the necessary directly from the given link
        # Note:The Python AttributeError is an exception that occurs when an attribute reference or assignment fails. This can
        # occur when an attempt is made to reference an attribute on a value that does not support the attribute.

        for i in ad_links:
            response = requests.get(i)
            soup = BeautifulSoup(response.text, "lxml")

            # get ad title

            try:
                title = soup.find("h1").text
            except AttributeError:
                title = ""

            # get ad price
            try:
                price = soup.find("span", itemprop="price").get_text().strip()
            except AttributeError:
                price = ""

            # get date posted
            try:
                date_posted = soup.find("div", itemprop="datePosted")['content']
            except (AttributeError, TypeError):
                date_posted = ""

            # get ad description
            try:
                description = soup.find("div", itemprop="description").get_text().strip()
            except AttributeError:
                description = ""

            # get the ad city

            try:
                address = soup.find("span", itemprop="address").get_text().strip()
            except AttributeError:
                address = ""
            df = df.append({
                "title": title,
                "price": price,
                "description": description,
                "date_posted": date_posted,
                "address": address,
                "url": i},
                ignore_index=True
            )
        with open("kijiji_watch_data.csv", "a+", newline='', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(df)

# This is final part of the code where the function is repeating itself every day. I left it as a comment because
# I don't want the code to be running on the background.

#    while True:
#       new_data()
#       time.sleep(86400)


# SOME REMARKS AND PROBLEMS WITH THIS PROJECT:
# 1)THE MAIN PROBLEM IS THAT EVERY DAY THE CODE WILL FETCH THE DATA OF ONLY THE FIRST TWO WEBSITES IN "WATCHES" CATEGORY
# OF KIJIJI. THIS IS A PROBLEM BECAUSE, IN OTHER CASES, THERE MIGHT BE MORE PAGES THAN TWO.
# 2) IF THE WEBSITE HAS NEW ADS TOO OFTEN, THE TIMER OF ONE DAY IS TOO LONG.VALUABLE DATA CAN BE MISSED.
# 3) IF THE WEBSITE ALMOST NEVER HAS NEW ADS. THEN, MY CODE WILL FETCH REPEATED ADDS. THEREFORE, HAVING REPEATED DATA.
# 4) LASTLY, I AM NOT SURE ABOUT THIS ONE BUT, I BELIEVE THAT THE URLS OF THE WEBSITES MIGHT CHANGE EVENTUALLY OR STOP
# EXISTING, SO IT WOULD BE GREAT TO FIND A SOLUTION TO THAT PROBLEM IF IT EVER OCCURS. MAYBE USING SELENIUM?
