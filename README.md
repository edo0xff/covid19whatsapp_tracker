# About this script

Script that scrapes covid-19 statistics for a specific country and send that info to a whatsapp group or contact.

# How it works

It scrapes the site:

[BNO News](https://docs.google.com/spreadsheets/d/e/2PACX-1vR30F8lYP3jG7YOq8es0PBpJIE5yvRVZffOyaqC0GgMBN6yt0Q-NI8pxS7hd1F9dYXnowSC6zpZmW9D/pubhtml?gid=0&amp;single=true&amp;widget=true&amp;headers=false&amp;range=A1:I202)

Using beatifulsoup to get lastest covid-19 statistics and it filters that info by country (or countries) which we indicates in an array. Then it uses selenium to open whatsapp web and send that info to an specific group/user.

# How to use it

First you need to install:

- BeautifulSoup
- Selenium
- Lastest chrome version
- chromedrive

The first time that you run the script you need to log-in to whatssapp scaning the QR code then after that your sesion data will be saved on a folder named User_Data, so if you want to change account delete that folder.
