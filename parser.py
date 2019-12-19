from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
import csv

# open Google Chrome
browser = webdriver.Chrome('./chromedriver')

# the starting mensa card number
cardNumber = 3060000

def parse(mensaCardNumber: int): 
    """
    Extracts the mensa card credit of the current card 
    and stores the result in a CSV file.
    """

    # visit the klarna website
    browser.get('https://topup.klarna.com/')

    # get the text field and fill it with the current number
    numberInput = browser.find_element_by_id('cs-card-number')
    numberInput.send_keys(mensaCardNumber)

    # wait until data is loaded
    time.sleep(1)

    try:
        creditField = browser.find_element_by_tag_name('strong').text 

        # extract the actual credit of the result sentence
        regex = re.search('[0-9]*\.[0-9]*', creditField)

        if regex:
            credit = float(regex.group(0))
        else:
            credit = 0.0

        print('Card: {} | Credit: {}'.format(mensaCardNumber, credit))

        # store the mensa card number and the credit to the CSV file and 
        # append a row to it.
        with open('mensacards.csv', 'a', encoding='utf-8') as output_file:
            writer = csv.writer(output_file)
            writer.writerow([mensaCardNumber, credit])

        # redo everything with the next number
        parse(mensaCardNumber + 1)
        
    except:
        print('No Card: {}'.format(mensaCardNumber))
        parse(mensaCardNumber + 1)

if __name__ == "__main__":
    parse(cardNumber)
