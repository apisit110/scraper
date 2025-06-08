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

def escapeComma(value):
  if "," in value:
    return '"' + value + '"'
  return value

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

def appendToFile(fileName, header, content):
  filePath = os.path.join("RawZone", fileName)
  if Path(filePath).is_file() == False:
    f = open(filePath, "w")
    f.write(header)
    f.close()

  with open(filePath, "a") as f:
    f.write(content)


class BotScaper:
  # def __init__(self) -> None:
  #   pass
  def __init__(self):
    pass

  def processBigC(self, url, isFirstLoop):
    print('processBigC...')
    
    isDebugFromExistingHTMLFile = False
    if (isDebugFromExistingHTMLFile == False):
      # SECTION - 1/1 http req to link
      if (isFirstLoop):
        payload = {}
        headers = {
          'User-Agent': 'curl/7.81.0', # requests.utils.default_user_agent()
        }
        response = requests.get(url, headers=headers, data=payload)
        content = response.content

        # SECTION 1/2 - open browser and navigate to url wait then for page load
        # content = openChrome(url)

        # SECTION 2 - parse content to beautifulsoup
        soup = BeautifulSoup(content, "html.parser")

        # SECTION 3 - write to file like html
        writeToFile("big-c-product-detail.html", soup.prettify())

    # SECTION 4 - process from html file or content
    soup = readContentFromFile("big-c-product-detail.html")

    # SECTION 5 - EXTRACT
    next_data_script = soup.find('script', id='__NEXT_DATA__')
    if next_data_script:
      json_data_str = next_data_script.string
      try:
        next_data_object = json.loads(json_data_str)
        buildId = str(next_data_object['buildId'])
        canonical = "/product/" + url.rsplit("/", 1)[-1] # str(next_data_object['props']['pageProps']['seoData']['canonical']) # if not firstLoop will use oldhtmldata

        craftUrlApiGetProductDetail = "https://www.bigc.co.th/_next/data/" + buildId + canonical + ".json"
        payload = {}
        headers = {
          'User-Agent': 'curl/7.81.0', # requests.utils.default_user_agent()
        }
        response = requests.get(craftUrlApiGetProductDetail, headers=headers, data=payload)
        data = json.loads(response.text)
        thumbnail_image = escapeComma(str(data['pageProps']['productDetail']['thumbnail_image']))
        sku = escapeComma(str(data['pageProps']['productDetail']['sku']))
        name = escapeComma(str(data['pageProps']['productDetail']['name']))
        image = escapeComma(str(data['pageProps']['productDetail']['image']))
        brand = escapeComma(str(data['pageProps']['productDetail']['attributes']['brand']))
        department_name = escapeComma(str(data['pageProps']['productDetail']['attributes']['department_name']))
        main_barcode = escapeComma(str(data['pageProps']['productDetail']['attributes']['main_barcode']))
        division_name = escapeComma(str(data['pageProps']['productDetail']['attributes']['division_name']))
        price_sales = escapeComma(str(data['pageProps']['productDetail']['price_sales']))
        price_base = escapeComma(str(data['pageProps']['productDetail']['price_base']))
        special_from_date = escapeComma(str(data['pageProps']['productDetail']['special_from_date']))
        special_to_date = escapeComma(str(data['pageProps']['productDetail']['special_to_date']))
        product_id = escapeComma(str(data['pageProps']['productDetail']['product_id']))

        # SECTION 6 Load
        fileName = "big_c_product_detail" + datetime.now().strftime("%Y%m%d") + "_000" + ".csv"
        header = ','.join(
          [
            'created_at',
            'thumbnail_image',
            'sku',
            'name',
            'image',
            'brand',
            'department_name',
            'main_barcode',
            'division_name',
            'price_sales',
            'price_base',
            'special_from_date',
            'special_to_date',
            'product_id'
          ]
        ) + '\n'
        content = ','.join(
          [
            datetime.now().isoformat(),
            thumbnail_image,
            sku,
            name,
            image,
            brand,
            department_name,
            main_barcode,
            division_name,
            price_sales,
            price_base,
            special_from_date,
            special_to_date,
            product_id
          ]
        ) + '\n'
        appendToFile(fileName, header, content)
      except Exception as e:
        print(f'An error occurred: ${e}')
    else:
      print("JSON script tag not found using regex.")





  def processMakroPro(self, url):
    print('processMakroPro...')

    isDebugFromExistingHTMLFile = False
    if (isDebugFromExistingHTMLFile == False):
      # SECTION - 1/1 http req to link
      response = requests.get(url)
      content = response.content

      # SECTION 1/2 - open browser and navigate to url wait then for page load
      # content = openChrome(url)

      # SECTION 2 - parse content to beautifulsoup
      soup = BeautifulSoup(content, "html.parser")

      # SECTION 3 - write to file like html
      writeToFile("makro-pro-product-detail.html", soup.prettify())

    # SECTION 4 - process from html file or content
    soup = readContentFromFile("makro-pro-product-detail.html")

    # SECTION 5 - EXTRACT
    next_data_script = soup.find('script', id='__NEXT_DATA__')
    if next_data_script:
      json_data_str = next_data_script.string

      try:
        next_data_object = json.loads(json_data_str)
        title = str(next_data_object['props']['pageProps']['product']['title'])
        # description = str(next_data_object['props']['pageProps']['product']['description'])
        brand = str(next_data_object['props']['pageProps']['product']['brand'])
        size = str(next_data_object['props']['pageProps']['product']['size'])
        displayPrice = str(next_data_object['props']['pageProps']['product']['displayPrice'])
        originPrice = str(next_data_object['props']['pageProps']['product']['originPrice'])
        priceUnit = str(next_data_object['props']['pageProps']['product']['priceUnit'])
        sku = str(next_data_object['props']['pageProps']['product']['sku'])
        imageUrls = str(next_data_object['props']['pageProps']['product']['imageUrls'])

        # SECTION 6 Load
        fileName = "makro_product_detail" + datetime.now().strftime("%Y%m%d") + "_000" + ".csv"
        header = ','.join(
          [
            'createdAt',
            'title',
            'brand',
            'size',
            'displayPrice',
            'originPrice',
            'priceUnit',
            'sku',
            'imageUrls'
          ]
        ) + '\n'
        content = ','.join(
          [
            datetime.now().isoformat(),
            title,
            brand,
            size,
            displayPrice,
            originPrice,
            priceUnit,
            sku,
            imageUrls
          ]
        ) + '\n'
        appendToFile(fileName, header, content)
      except Exception as e:
        print(f'An error occurred: ${e}')
    else:
      print("JSON script tag not found using regex.")





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

    isDebugFromExistingHTMLFile = False
    if (isDebugFromExistingHTMLFile == False):
      # SECTION - 1/1 http req to link
      # response = requests.get(url)
      # content = response.content

      # SECTION 1/2 - open browser and navigate to url wait then for page load
      content = openChrome(url)

      # SECTION 2 - parse content to beautifulsoup
      soup = BeautifulSoup(content, "html.parser")

      # SECTION 3 - write to file like html
      writeToFile("tops-product-detail.html", soup.prettify())

    # SECTION 4 - process from html file or content
    soup = readContentFromFile("tops-product-detail.html")

    # SECTION 5 - EXTRACT
    elementProductDetailsCommonDescription = soup.find("div", class_="product-Details-common-description")
    productName = elementProductDetailsCommonDescription.find("div", class_="product-Details-left-block").find("div", class_="product-Details-name").find("h1").text.strip()
    productPriceSale = elementProductDetailsCommonDescription.find("div", class_="product-Details-right-block") .find("div", class_="product-Details-price-block").find("span", class_="product-Details-current-price").text.strip()
    productBasePrice = productPriceSale
    if elementProductDetailsCommonDescription.find("div", class_="product-Details-right-block").find("div", class_="product-Details-price-block").find("span", class_="product-Details-actual-price") != None:
      productBasePrice = elementProductDetailsCommonDescription.find("div", class_="product-Details-right-block") .find("div", class_="product-Details-price-block").find("span", class_="product-Details-actual-price").text.strip()

    # SECTION 6 Load
    fileName = "tops_product_detail" + datetime.now().strftime("%Y%m%d") + "_000" + ".csv"
    header = ','.join(
      [
        'createdAt',
        'productName',
        'productPriceSale',
        'productBasePrice',
        'url'
      ]
    ) + '\n'
    content = ','.join(
      [
        datetime.now().isoformat(),
        productName,
        productPriceSale,
        productBasePrice,
        url
      ]
    ) + '\n'
    appendToFile(fileName, header, content)





  def processLotuss(self, url):
    print('processLotuss...')

    # SECTION - 1/1 http req to link
    sku = url.rsplit("/", 1)[-1]
    craftUrlApiGetProductDetail = "https://api-o2o.lotuss.com/lotuss-mobile-bff/product/v4/product?slug=" + sku
    response = requests.get(craftUrlApiGetProductDetail)
    # content = response.content

    # SECTION 1/2 - open browser and navigate to url wait then for page load
    # content = openChrome(url)

    # SECTION 2 - parse content to beautifulsoup
    # soup = BeautifulSoup(content, "html.parser")

    # SECTION 3 - write to file like html
    # writeToFile("lotuss-product-detail.html", soup.prettify())

    # SECTION 4 - process from html file or content
    # soup = readContentFromFile("lotuss-product-detail.html")

    # SECTION 5 - EXTRACT
    data = json.loads(response.text)
    id = escapeComma(str(data['data']['id']))
    sku = escapeComma(str(data['data']['sku']))
    name = escapeComma(str(data['data']['name']))
    brand = escapeComma(str(data['data']['links']['brand']['name']))
    regularPricePerUOW = escapeComma(str(data['data']['regularPricePerUOW']))
    finalPricePerUOW = escapeComma(str(data['data']['finalPricePerUOW']))

    # SECTION 6 Load
    fileName = "lotuss_product_detail" + datetime.now().strftime("%Y%m%d") + "_000" + ".csv"
    header = ','.join(
      [
        'createdAt',
        'id',
        'sku',
        'name',
        'brand',
        'regularPricePerUOW',
        'finalPricePerUOW',
        'url'
      ]
    ) + '\n'
    content = ','.join(
      [
        datetime.now().isoformat(),
        id,
        sku,
        name,
        brand,
        regularPricePerUOW,
        finalPricePerUOW,
        url
      ]
    ) + '\n'
    appendToFile(fileName, header, content)





  def processFreshket(self, url):
    print('processFreshket...')

    isDebugFromExistingHTMLFile = False
    if (isDebugFromExistingHTMLFile == False):
      # SECTION - 1/1 http req to link
      response = requests.get(url)
      content = response.content

      # SECTION 1/2 - open browser and navigate to url wait then for page load
      # content = openChrome(url)

      # SECTION 2 - parse content to beautifulsoup
      soup = BeautifulSoup(content, "html.parser")

      # SECTION 3 - write to file like html
      writeToFile("freshket-product-detail.html", soup.prettify())

    # SECTION 4 - process from html file or content
    soup = readContentFromFile("freshket-product-detail.html")

    # SECTION 5 - EXTRACT
    next_data_script = soup.find('script', id='__NEXT_DATA__')
    if next_data_script:
      json_data_str = next_data_script.string
      try:
        next_data_object = json.loads(json_data_str)
        guid = escapeComma(str(next_data_object['props']['pageProps']['detail']['guid']))
        name = escapeComma(str(next_data_object['props']['pageProps']['detail']['name']))
        originalPrice = escapeComma(str(next_data_object['props']['pageProps']['detail']['sellingPrice']['originalPrice']))
        price = escapeComma(str(next_data_object['props']['pageProps']['detail']['sellingPrice']['price']))

        # SECTION 6 Load
        fileName = "freshket_product_detail" + datetime.now().strftime("%Y%m%d") + "_000" + ".csv"
        header = ','.join(
          [
            'createdAt',
            'guid',
            'name',
            'originalPrice',
            'price',
            'url'
          ]
        ) + '\n'
        content = ','.join(
          [
            datetime.now().isoformat(),
            guid,
            name,
            originalPrice,
            price,
            url
          ]
        ) + '\n'
        appendToFile(fileName, header, content)
      except Exception as e:
        print(f'An error occurred: ${e}')
    else:
      print("JSON script tag not found using regex.")
