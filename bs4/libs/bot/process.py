from bs4 import BeautifulSoup
import requests
# from abc import ABC, abstractmethod
from datetime import datetime
# import re
# import urllib.parse
import time
from pathlib import Path
import os
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

_path = os.path.join('bs4', 'libs', 'constants', 'merchant.json')
f = open(_path, 'r')
MERCHANT = json.load(f)
f.close()

def openChrome(url):
  options = webdriver.ChromeOptions()
  options.add_argument('--headless')  # If you want to run Chrome in headless mode
  options.add_argument('--disable-gpu')  # Required for headless mode to work on Windows
  # options.add_argument("--enable-javascript")
  driver = webdriver.Chrome(options=options) # driver = webdriver.Chrome()
  driver.get(url)
  time.sleep(10)
  content = driver.page_source
  return content

def writeToFile(fileName, content):
  _path = os.path.join("source", fileName)
  f = open(_path, "w")
  f.write(content)
  f.close()

def readContentFromFile(fileName):
  _path = os.path.join("source", fileName)
  f = open(_path, "r")
  soup = BeautifulSoup(f.read(), "html.parser")
  f.close()
  return soup

def writeToCsv(date, merchantName, productName, productPriceSale, productBasePrice, productUrl):
  rawZonePath = os.path.join("RawZone", datetime.now().strftime("%Y%m%d") + ".csv")
  if Path(rawZonePath).is_file() == False:
    f = open(rawZonePath, "w")
    f.write("date,merchant,name,priceSale,basePrice,url\n")
    f.close()

  f = open(rawZonePath, "a")
  row = ",".join([date, merchantName, productName, productPriceSale, productBasePrice, productUrl]) + "\n"
  f.write(row)
  f.close()

class BotScaper:
  # def __init__(self) -> None:
  #   pass
  def __init__(self):
    pass

  def processBigC(self, url):
    print('processBigC...')

    # SECTION - 1/1 http req to link
    response = requests.get(url)
    content = response.content

    # SECTION 1/2 - open browser and navigate to url wait then for page load
    # content = openChrome(url)

    # SECTION 2 - parse content to beautifulsoup
    soup = BeautifulSoup(content, "html.parser")

    # SECTION 3 - write to file like html
    writeToFile("index-big-c.html", soup.prettify())

    # SECTION 4 - process from html file or content
    soup = readContentFromFile("index-big-c.html")

    # SECTION 5 - parse data
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    merchantName = MERCHANT['BIG_C']
    productName = ""
    productPriceSale = None
    productBasePrice = None
    productUrl = url
    
    productName = soup.select_one('h1[id="pdp_product-title"]').text.strip()
    productPriceSale = soup.select_one('div[id="pdp_product-price"] div[class*="productDetail_product_price"]')
    for item in productPriceSale.select('span[class*="productDetail_"]'):
      item.decompose()
    productPriceSale = productPriceSale.text.strip()
    productBasePrice = soup.select_one('div[class*="productDetail_product_baseprice"] span[id="pdp_price-base"]')
    if productBasePrice != None:
      productBasePrice = productBasePrice.text.strip()
    else:
      productBasePrice = ""

    # DEBUG
    # print("---------- DEBUG ----------")
    # print(f'name: {productName}')
    # print(f'price sale: {productPriceSale}')
    # print(f'basePrice {productBasePrice}')

    # SECTION 6 - WRITE TO FILE LIKE CSV
    writeToCsv(date, merchantName, productName, productPriceSale, productBasePrice, productUrl)


  def processMakroPro(self, url):
    print('processMakroPro...')

    # SECTION - 1/1 http req to link
    # response = requests.get(url)
    # content = response.content

    # SECTION 1/2 - open browser and navigate to url wait then for page load
    content = openChrome(url)

    # SECTION 2 - parse content to beautifulsoup
    soup = BeautifulSoup(content, "html.parser")

    # SECTION 3 - write to file like html
    writeToFile("index-makro-pro.html", soup.prettify())

    # SECTION 4 - process from html file or content
    soup = readContentFromFile("index-makro-pro.html")

    # SECTION 5 - parse data
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    merchantName = MERCHANT['MAKRO_PRO']
    productName = soup.find("div", attrs={'class': 'MuiBox-root css-13u9jxe'}).text.strip()
    productPriceSale = None
    productBasePrice = None
    productUrl = url

    # priceElement
    priceElement = soup.find("div", attrs={"class": "MuiBox-root css-17633zz"})
    if (priceElement.find("div", attrs={"class": "slab"})):
      productPriceSale = priceElement.div.div.find_all("div")[1].text.strip().split("\n")[0]
      productBasePrice = priceElement.div.div.find_all("div")[3].p.text.strip().split(" ")[0]
    else:
      productPriceSale = priceElement.div.div.div.p.text.strip()
      productBasePrice = productPriceSale

    # DEBUG
    # print("---------- DEBUG ----------")
    # print(f'name: {productName}')
    # print(f'price sale: {productPriceSale}')
    # print(f'basePrice {productBasePrice}')

    # SECTION 6 - WRITE TO FILE LIKE CSV
    writeToCsv(date, merchantName, productName, productPriceSale, productBasePrice, productUrl)


  def processWatsons(self, url):
    print('processWatsons...')

    # SECTION - 1/1 http req to link
    # response = requests.get(url)
    # content = response.content

    # SECTION 1/2 - open browser and navigate to url wait then for page load
    content = openChrome(url)

    # SECTION 2 - parse content to beautifulsoup
    soup = BeautifulSoup(content, "html.parser")

    # SECTION 3 - write to file like html
    writeToFile("index-watsons.html", soup.prettify())

    # SECTION 4 - process from html file or content
    soup = readContentFromFile("index-watsons.html")

    # SECTION 5 - parse data
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    merchantName = MERCHANT['WATSONS']
    productName = ""
    productPriceSale = ""
    productBasePrice = ""
    productUrl = url

    # product-summary-container
    elementProductSummaryContainer = soup.find("div", class_="product-summary-container")
    productName = elementProductSummaryContainer.find("div", class_="summary-main-group").find("div", class_="product-name").text.strip()

    # purchase-info-group
    elementPurchasePanal = soup.find("div", attrs={"class": "purchase-info-group"}).find("div", attrs={"class": "price-summary"})
    if elementPurchasePanal.find("div", attrs={"class": "display-price-group"}) != None:
      productPriceSale = elementPurchasePanal.find("div", attrs={"class": "display-price-group"}).find("div", class_="display-price").find("span", class_="price").text.strip()
      productBasePrice = productPriceSale
    if elementPurchasePanal.find("div", attrs={"class": "recommended-retail-price"}) != None:
      productBasePrice = elementPurchasePanal.find("div", attrs={"class": "recommended-retail-price"}).find("span", class_="retail-price").text.strip().replace("฿", "")
      

    # DEBUG
    # print("---------- DEBUG ----------")
    # print(f'name: {productName}')
    # print(f'price sale: {productPriceSale}')
    # print(f'basePrice {productBasePrice}')

    # SECTION 6 - WRITE TO FILE LIKE CSV
    writeToCsv(date, merchantName, productName, productPriceSale, productBasePrice, productUrl)


  def processTops(self, url):
    print('processTops...')

    # SECTION - 1/1 http req to link
    # response = requests.get(url)
    # content = response.content

    # SECTION 1/2 - open browser and navigate to url wait then for page load
    content = openChrome(url)

    # SECTION 2 - parse content to beautifulsoup
    soup = BeautifulSoup(content, "html.parser")

    # SECTION 3 - write to file like html
    writeToFile("index-tops.html", soup.prettify())

    # SECTION 4 - process from html file or content
    soup = readContentFromFile("index-tops.html")

    # SECTION 5 - parse data
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    merchantName = MERCHANT["TOPS"]
    productName = ""
    productPriceSale = ""
    productBasePrice = ""
    productUrl = url

    elementProductDetailsCommonDescription = soup.find("div", class_="product-Details-common-description")
    productName = elementProductDetailsCommonDescription.find("div", class_="product-Details-left-block").find("div", class_="product-Details-name").find("h1").text.strip()
    productPriceSale = elementProductDetailsCommonDescription.find("div", class_="product-Details-right-block") .find("div", class_="product-Details-price-block").find("span", class_="product-Details-current-price").text.strip()
    productBasePrice = productPriceSale
    if elementProductDetailsCommonDescription.find("div", class_="product-Details-right-block").find("div", class_="product-Details-price-block").find("span", class_="product-Details-actual-price") != None:
      productBasePrice = elementProductDetailsCommonDescription.find("div", class_="product-Details-right-block") .find("div", class_="product-Details-price-block").find("span", class_="product-Details-actual-price").text.strip()


    # DEBUG
    # print("---------- DEBUG ----------")
    # print(f'name: {productName}')
    # print(f'price sale: {productPriceSale}')
    # print(f'basePrice {productBasePrice}')

    # SECTION 6 - WRITE TO FILE LIKE CSV
    writeToCsv(date, merchantName, productName, productPriceSale, productBasePrice, productUrl)

    
  def processLotuss(self, url):
    print('processLotuss...')

    # SECTION - 1/1 http req to link
    # response = requests.get(url)
    # content = response.content

    # SECTION 1/2 - open browser and navigate to url wait then for page load
    content = openChrome(url)

    # SECTION 2 - parse content to beautifulsoup
    soup = BeautifulSoup(content, "html.parser")

    # SECTION 3 - write to file like html
    writeToFile("index-lotuss.html", soup.prettify())

    # SECTION 4 - process from html file or content
    soup = readContentFromFile("index-lotuss.html")

    # SECTION 5 - parse data
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    merchantName = MERCHANT["LOTUSS"]
    productName = ""
    productPriceSale = ""
    productBasePrice = ""
    productUrl = url

    elementProductPanel = soup.find("button", {"id": "add-to-cart-btn-0"}).parent.parent.parent.parent
    productName = elementProductPanel.find_all("div")[0].find("h1").text.strip()
    productPriceSale = elementProductPanel.find_all("div")[2].find_all("div")[0].get_text(strip=True, separator="|").split("|")[1]
    productBasePrice = productPriceSale
    try:
      productBasePrice = elementProductPanel.find_all("div")[2].find_all("div")[1].get_text(strip=True).replace("฿", "")
    except:
      pass

    # DEBUG
    # print("---------- DEBUG ----------")
    # print(f'name: {productName}')
    # print(f'price sale: {productPriceSale}')
    # print(f'basePrice {productBasePrice}')

    # SECTION 6 - WRITE TO FILE LIKE CSV
    writeToCsv(date, merchantName, productName, productPriceSale, productBasePrice, productUrl)


  def processFreshket(self, url):
    print('processFreshket...')

    # SECTION - 1/1 http req to link
    # response = requests.get(url)
    # content = response.content

    # SECTION 1/2 - open browser and navigate to url wait then for page load
    content = openChrome(url)

    # SECTION 2 - parse content to beautifulsoup
    soup = BeautifulSoup(content, "html.parser")

    # SECTION 3 - write to file like html
    writeToFile("index-freshket.html", soup.prettify())

    # SECTION 4 - process from html file or content
    soup = readContentFromFile("index-freshket.html")

    # SECTION 5 - parse data
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    merchantName = MERCHANT['FRESHKET']
    productName = ""
    productPriceSale = ""
    productBasePrice = ""
    productUrl = url

    elementProductPanel = soup.find("div", attrs={"role": "main"}).find("div", attrs={"data-testid": "page-content-root"}).find("h1").parent
    productName = elementProductPanel.find("h1").text.strip()
    productPriceSale = elementProductPanel.find("h5", attrs={"id": "price-value"}).text.strip()
    productBasePrice = productPriceSale
    try:
      productBasePrice = elementProductPanel.find("span", attrs={"data-testid": "discount-original-price-label"}).get_text(strip=True, separator="|").split("|")[1]
    except:
      pass
    
    # DEBUG
    # print("---------- DEBUG ----------")
    # print(f'name: {productName}')
    # print(f'price sale: {productPriceSale}')
    # print(f'basePrice {productBasePrice}')

    # SECTION 6 - WRITE TO FILE LIKE CSV
    writeToCsv(date, merchantName, productName, productPriceSale, productBasePrice, productUrl)
