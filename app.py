from flask import Flask, redirect, url_for, render_template
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os
import pandas as pd
from termcolor import colored
from pyfiglet import Figlet

f = Figlet(font='standard')
print(colored(f.renderText('EtsyScraper'), 'green'))

print('Etsy Listing Scraper v.1.00 by mujibanget')

keyword = input('Masukan Keyword: ')
#url='https://www.etsy.com/search?q={}&page=2&ref=pagination'.format(keyword)
#scrollnum=int(input("Scroll: "))
sleepTimer=1

options=webdriver.ChromeOptions()
options.add_argument("--headless") # Runs Chrome in headless mode.
options.add_argument('--no-sandbox') # Bypass OS security model
options.add_argument('--disable-gpu')  # applicable to windows os only
options.add_argument('start-maximized') # 
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")
driver = webdriver.Chrome(chrome_options=options, executable_path=r'C:\Program Files\Google\Chrome\Application\chromedriver.exe')
#driver=webdriver.Chrome(executable_path='C:\Program Files\Google\Chrome\Application\chromedriver.exe', options=options)

#driver.get(url)
harga, listing, badge, gambar, links = [], [], [], [], []
for page in range(1, 3):
    driver.get('https://www.etsy.com/search?q={}&page={}&ref=pagination'.format(keyword, page))
    html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    soup = BeautifulSoup(html,"html.parser")
    header_contents = soup.find_all('li', 'wt-list-unstyled')
    time.sleep(sleepTimer)


    for content in header_contents:
        try:
            thumb = content.find('img').get('src')
        except:
            thumb = 'none'
        try:
            product = content.find('h3', 'wt-text-caption v2-listing-card__title wt-text-truncate').text
        except:
            product = 'none'
        try:
            shop = content.find('p', 'wt-text-caption wt-text-truncate wt-text-gray wt-mb-xs-1').text
        except:
            shop = 'none'
        try:
            price = content.find('span', 'currency-value').text
        except:
            price = 'none'
        try:
            sale = content.find('span', 'wt-badge').text
        except:
            sale = '-'
        try:
            link_produk = content.find('div').a.get('href')
        except:
            continue

        listing.append(product)
        harga.append(price)
        badge.append(sale)
        gambar.append(thumb)
        links.append(link_produk)

driver.close()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", len = len(listing), listing=listing, harga=harga, badge=badge, gambar=gambar, links=links)

 
if __name__ == "__main__":
    app.run(debug=True)

print('Silahkan buka link diatas untuk melihat hasilnnya')