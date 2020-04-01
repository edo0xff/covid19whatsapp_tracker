import time
import unidecode
import hashlib

from requests import get
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

countries = ['mexico', 'united states'] # check the countries names in URL
timesleep = 60 # 7200 # time between every data check, 2 hrs in seconds
wp_target = '"Covid19TrackerBot"' # whatsapp group/user to send the scraped data

twitter_accounts = ['COVID19_ES','SSalud_mx','HLGatell']

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR30F8lYP3jG7YOq8es0PBpJIE5yvRVZffOyaqC0GgMBN6yt0Q-NI8pxS7hd1F9dYXnowSC6zpZmW9D/pubhtml?gid=0&amp;single=true&amp;widget=true&amp;headers=false&amp;range=A1:I202"

def scrap_statistics():
    print "Scraping data..."
    response = get(url)

    soup = BeautifulSoup(response.text, 'lxml')
    tables = soup.find_all("table")
    rows = tables[0].find_all("tr")

    statistics = []

    for row in rows:
        cells = row.find_all("td")
        cells = [unidecode.unidecode(cell.text.strip()) for cell in cells]

        try:
                country = cells[0]
                confirmed = cells[1]
                deaths = cells[3]
                serious = cells[6]
                recovered = cells[7]

                if country.lower() in countries:
                    string = "*MENSAJE AUTOMATICO:* Casos de Covid-19 en %s : %s confirmados %s muertes %s graves %s recuperados\n" % (country, confirmed, deaths, serious, recovered)
                    statistics.append(string)

        except Exception as e:
            pass

    return statistics

def scrap_tweets():
    tweets = []

    for account in twitter_accounts:
        url = "https://twitter.com/%s" %(account)
        response = get(url)

        soup = BeautifulSoup(response.text, 'lxml')
        tweets_containers = soup.find_all("div", {"class":"js-tweet-text-container"})

        account_tweets = []

        for tweets_container in tweets_containers:
            tweet = tweets_container.find_all("p")[0]
            tweet = unidecode.unidecode(tweet.text).replace("http", " http")
            tweet = tweet.replace("pic.twitter.com", " https://pic.twitter.com")
            tweet = tweet.replace("\n", " ")
            account_tweets.append("*MENSAJE AUTOMATICO:* @%s %s\n" %(account,tweet))

        tweets += account_tweets[:3]

    return tweets

options = webdriver.ChromeOptions();
options.add_argument('--user-data-dir=./User_Data')
driver = webdriver.Chrome(chrome_options=options)
driver.get("https://web.whatsapp.com/")
wait = WebDriverWait(driver, 600)

f = open('messages_checksum.txt', 'r+')
messages_checksum = f.read().split("\n")

try:
    print "Coded By: edo <https://edo0xff.me/>\n"

    while True:
        try:
            string = ''

            statistics = scrap_statistics()

            for country in statistics:
                checksum = "country:%s" %(hashlib.md5(country).hexdigest())

                if not checksum in messages_checksum:
                    messages_checksum.append(checksum)
                    string += country

            tweets = scrap_tweets()

            for tweet in tweets:
                checksum = "tweet:%s" %(hashlib.md5(tweet).hexdigest())

                if not checksum in messages_checksum:
                    messages_checksum.append(checksum)
                    string += tweet

            x_arg = '//span[contains(@title,' + wp_target + ')]'
            group_title = wait.until(EC.presence_of_element_located((
                By.XPATH, x_arg)))
            group_title.click()

            if string:

                message = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]
                message.send_keys(string.strip("\n"))

                sendbutton = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')[0]
                sendbutton.click()

        except:
            pass

        time.sleep(timesleep)

except KeyboardInterrupt:
    f = open('messages_checksum.txt', 'w+')
    f.write("\n".join(messages_checksum))
    f.close()

    driver.close()
