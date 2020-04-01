import time
import unidecode

from requests import get
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

countries = ['mexico', 'united states'] # check the countries names in URL
timesleep = 7200 # time between every data check, 2 hrs in seconds
wp_target = '"Covid19TrackerBot"' # whatsapp group/user to send the scraped data


url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR30F8lYP3jG7YOq8es0PBpJIE5yvRVZffOyaqC0GgMBN6yt0Q-NI8pxS7hd1F9dYXnowSC6zpZmW9D/pubhtml?gid=0&amp;single=true&amp;widget=true&amp;headers=false&amp;range=A1:I202"

def scrap_data():
    print "Scraping data..."
    response = get(url)

    soup = BeautifulSoup(response.text, 'lxml')
    tables = soup.find_all("table")
    rows = tables[0].find_all("tr")

    string = ''

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
                    string += "Casos de Covid-19 en %s : %s confirmados %s muertes %s graves %s recuperados\n" % (country, confirmed, deaths, serious, recovered)

        except Exception as e:
            pass

    print string
    return string

options = webdriver.ChromeOptions();
options.add_argument('--user-data-dir=./User_Data')
driver = webdriver.Chrome(chrome_options=options)
driver.get("https://web.whatsapp.com/")
wait = WebDriverWait(driver, 600)

try:
    print "Coded By: edo <https://edo0xff.me/>\n"

    while True:
        try:
            data = scrap_data()
            data = "*[BOT]*\n%s*[BOT]*" %(data)

            if data:
                x_arg = '//span[contains(@title,' + wp_target + ')]'
                group_title = wait.until(EC.presence_of_element_located((
                	By.XPATH, x_arg)))
                group_title.click()


                message = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]
                message.send_keys(data)

                sendbutton = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')[0]
                sendbutton.click()

        except:
            pass

        time.sleep(timesleep)

except KeyboardInterrupt:
    driver.close()
