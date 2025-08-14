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
MERCHANTS = json.load(f)
f.close()

def generateRawFileName(merchant, date, runningNumber='000'):
  if merchant == MERCHANTS['BIG_C']:
    return f'big_c_product_detail_{date}_{runningNumber}.csv'
  elif merchant == MERCHANTS['MAKRO_PRO']:
    return f'makro_product_detail_{date}_{runningNumber}.csv'
  elif merchant == MERCHANTS['WATSONS']:
    return f'watsons_product_detail_{date}_{runningNumber}.csv'
  elif merchant == MERCHANTS['TOPS']:
    return f'tops_product_detail_{date}_{runningNumber}.csv'
  elif merchant == MERCHANTS['LOTUSS']:
    return f'lotuss_product_detail_{date}_{runningNumber}.csv'
  elif merchant == MERCHANTS['FRESHKET']:
    return f'freshket_product_detail_{date}_{runningNumber}.csv'
  elif merchant == MERCHANTS['ALLONLINE']:
    return f'allonline_product_detail_{date}_{runningNumber}.csv'

def generateProductFileName(date, runningNumber='000'):
  return f'products_{date}_{runningNumber}.csv'

def escapeComma(value):
  if "," in value:
    return '"' + value + '"'
  return value

def getNested(d, keys, default=None):
  for key in keys:
    if isinstance(d, dict):
      d = d.get(key, default)
    else:
      return default
  return d

def openChrome(url, isHeadless):
  options = webdriver.ChromeOptions()
  if isHeadless == True:
    options.add_argument('--headless')  # If you want to run Chrome in headless mode
    options.add_argument('--disable-gpu')  # Required for headless mode to work on Windows
  # options.add_argument("--enable-javascript")
  driver = webdriver.Chrome(options=options) # driver = webdriver.Chrome()
  driver.get(url)
  time.sleep(5)
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
    print(f'processBigC: {url}')
    
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
        # content = openChrome(url, True)

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
        product_id = escapeComma(str(getNested(data, ['pageProps', 'productDetail', 'product_id'], default='')))
        price_sales = escapeComma(str(getNested(data, ['pageProps', 'productDetail', 'price_sales'], default='')))
        volume = escapeComma(str(getNested(data, ['pageProps', 'productDetail', 'volume'], default='')))
        name = escapeComma(str(getNested(data, ['pageProps', 'productDetail', 'name'], default='')))
        sku = escapeComma(str(getNested(data, ['pageProps', 'productDetail', 'sku'], default='')))
        price_base = escapeComma(str(getNested(data, ['pageProps', 'productDetail', 'price_base'], default='')))
        main_barcode = escapeComma(str(getNested(data, ['pageProps', 'productDetail', 'attributes', 'main_barcode'], default='')))
        department_name = escapeComma(str(getNested(data, ['pageProps', 'productDetail', 'attributes', 'department_name'], default='')))
        brand = escapeComma(str(getNested(data, ['pageProps', 'productDetail', 'attributes', 'brand'], default='')))

        # SECTION 6 Load
        fileName = "big_c_product_detail_" + datetime.now().strftime("%Y%m%d") + "_000" + ".csv"
        header = ','.join(
          [
            'created_at',
            'product_id',
            'price_sales',
            'price_base',
            'volume',
            'name',
            'sku',
            'main_barcode',
            'department_name',
            'brand',
            'url'
          ]
        ) + '\n'
        content = ','.join(
          [
            datetime.now().isoformat(),
            product_id,
            price_sales,
            price_base,
            volume,
            name,
            sku,
            main_barcode,
            department_name,
            brand,
            url
          ]
        ) + '\n'
        appendToFile(fileName, header, content)
      except Exception as e:
        print(f'An error occurred: ${e}')
    else:
      print("JSON script tag not found using regex.")





  def processMakroPro(self, url):
    print(f'processMakroPro: {url}')

    isDebugFromExistingHTMLFile = False
    if (isDebugFromExistingHTMLFile == False):
      # SECTION - 1/1 http req to link
      response = requests.get(url)
      content = response.content

      # SECTION 1/2 - open browser and navigate to url wait then for page load
      # content = openChrome(url, True)

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
        title = escapeComma(str(getNested(next_data_object, ['props', 'pageProps', 'product', 'title'], default='')))
        brand = escapeComma(str(getNested(next_data_object, ['props', 'pageProps', 'product', 'brand'], default='')))
        size = escapeComma(str(getNested(next_data_object, ['props', 'pageProps', 'product', 'size'], default='')))
        displayPrice = escapeComma(str(getNested(next_data_object, ['props', 'pageProps', 'product', 'displayPrice'], default='')))
        originPrice = escapeComma(str(getNested(next_data_object, ['props', 'pageProps', 'product', 'originPrice'], default='')))
        sku = escapeComma(str(getNested(next_data_object, ['props', 'pageProps', 'product', 'sku'], default='')))
        totalInventory = escapeComma(str(getNested(next_data_object, ['props', 'pageProps', 'product', 'totalInventory'], default='')))
        slabPriceTiers = escapeComma(str(getNested(next_data_object, ['props', 'pageProps', 'product', 'slabPrices', 'slabPriceTiers'], default=''))) # array
        productId = escapeComma(str(getNested(next_data_object, ['props', 'pageProps', 'productId'], default='')))
        buildId = escapeComma(str(getNested(next_data_object, ['buildId'], default='')))

        # SECTION 6 Load
        fileName = "makro_product_detail_" + datetime.now().strftime("%Y%m%d") + "_000" + ".csv"
        header = ','.join(
          [
            'createdAt',
            'title',
            'brand',
            'size',
            'displayPrice',
            'originPrice',
            'sku',
            'totalInventory',
            'slabPriceTiers',
            'productId',
            'buildId',
            'url'
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
            sku,
            totalInventory,
            slabPriceTiers,
            productId,
            buildId,
            url
          ]
        ) + '\n'
        appendToFile(fileName, header, content)
      except Exception as e:
        print(f'An error occurred: ${e}')
    else:
      print("JSON script tag not found using regex.")





  def processWatsons(self, url):
    print(f'processWatsons: {url}')

    # SECTION - 1/1 http req to link
    # response = requests.get(url)
    # content = response.content

    # SECTION 1/2 - open browser and navigate to url wait then for page load
    content = openChrome(url, True)

    # SECTION 2 - parse content to beautifulsoup
    soup = BeautifulSoup(content, "html.parser")

    # SECTION 3 - write to file like html
    writeToFile("index-watsons.html", soup.prettify())

    # SECTION 4 - process from html file or content
    soup = readContentFromFile("index-watsons.html")

    # SECTION 5 - parse data
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    merchantName = MERCHANTS['WATSONS']
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
    print(f'processTops: {url}')

    isDebugFromExistingHTMLFile = False
    if (isDebugFromExistingHTMLFile == False):
      # SECTION - 1/1 http req to link
      # response = requests.get(url)
      # content = response.content

      # SECTION 1/2 - open browser and navigate to url wait then for page load
      content = openChrome(url, False)

      # SECTION 2 - parse content to beautifulsoup
      soup = BeautifulSoup(content, "html.parser")

      # SECTION 3 - write to file like html
      writeToFile("tops-product-detail.html", soup.prettify())

    # SECTION 4 - process from html file or content
    soup = readContentFromFile("tops-product-detail.html")

    # SECTION 5 - EXTRACT
    next_data_script = soup.find('script', id='__NEXT_DATA__')
    if next_data_script:
      json_data_str = next_data_script.string
      try:
        next_data_object = json.loads(json_data_str)
        sku = escapeComma(str(next_data_object['props']['pageProps']['productData']['sku']))
        brand = escapeComma(str(next_data_object['props']['pageProps']['productData']['brand']))
        imageUrl = 'https://assets.tops.co.th/' + str(next_data_object['props']['pageProps']['productData']['images'][0]['url'])
        name = escapeComma(str(next_data_object['props']['pageProps']['productData']['name']))
        productPriceSale = escapeComma(str(next_data_object['props']['pageProps']['productData']['price']))
        productBasePrice = getattr(next_data_object['props']['pageProps']['productData'], 'originalPrice', "")
        stockStatus = escapeComma(str(next_data_object['props']['pageProps']['productData']['stockAvail']))

        # SECTION 6 Load
        fileName = "tops_product_detail_" + datetime.now().strftime("%Y%m%d") + "_000" + ".csv"
        header = ','.join(
          [
            'createdAt',
            'name',
            'brand',
            'sku',
            'productPriceSale',
            'productBasePrice',
            'imageUrl',
            'stockStatus',
            'url'
          ]
        ) + '\n'
        content = ','.join(
          [
            datetime.now().isoformat(),
            name,
            brand,
            sku,
            productPriceSale,
            productBasePrice,
            imageUrl,
            stockStatus,
            url
          ]
        ) + '\n'
        appendToFile(fileName, header, content)
      except Exception as e:
        print(f'An error occurred: ${e}')
    else:
      print("JSON script tag not found using regex.")





  def processLotuss(self, url):
    print(f'processLotuss: {url}')

    # SECTION - 1/1 http req to link
    sku = url.rsplit("/", 1)[-1]
    craftUrlApiGetProductDetail = "https://api-o2o.lotuss.com/lotuss-mobile-bff/product/v4/product?slug=" + sku
    response = requests.get(craftUrlApiGetProductDetail)
    # content = response.content

    # SECTION 1/2 - open browser and navigate to url wait then for page load
    # content = openChrome(url, True)

    # SECTION 2 - parse content to beautifulsoup
    # soup = BeautifulSoup(content, "html.parser")

    # SECTION 3 - write to file like html
    # writeToFile("lotuss-product-detail.html", soup.prettify())

    # SECTION 4 - process from html file or content
    # soup = readContentFromFile("lotuss-product-detail.html")

    # SECTION 5 - EXTRACT
    data = json.loads(response.text)
    id = escapeComma(str(getNested(data, ['data', 'id'], default='')))
    sku = escapeComma(str(getNested(data, ['data', 'sku'], default='')))
    name = escapeComma(str(getNested(data, ['data', 'name'], default='')))
    brand = escapeComma(str(getNested(data, ['data', 'links', 'brand', 'name'], default='')))
    regularPricePerUOW = escapeComma(str(getNested(data, ['data', 'regularPricePerUOW'], default='')))
    finalPricePerUOW = escapeComma(str(getNested(data, ['data', 'finalPricePerUOW'], default='')))
    stockStatus =  escapeComma(str(getNested(data, ['data', 'stockStatus'], default='')))

    # SECTION 6 Load
    fileName = "lotuss_product_detail_" + datetime.now().strftime("%Y%m%d") + "_000" + ".csv"
    header = ','.join(
      [
        'createdAt',
        'id',
        'sku',
        'name',
        'brand',
        'regularPricePerUOW',
        'finalPricePerUOW',
        'stockStatus',
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
        stockStatus,
        url
      ]
    ) + '\n'
    appendToFile(fileName, header, content)





  def processFreshket(self, url):
    print(f'processFreshket: {url}')

    isDebugFromExistingHTMLFile = False
    if (isDebugFromExistingHTMLFile == False):
      # SECTION - 1/1 http req to link
      response = requests.get(url)
      content = response.content

      # SECTION 1/2 - open browser and navigate to url wait then for page load
      # content = openChrome(url, True)

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
        fileName = "freshket_product_detail_" + datetime.now().strftime("%Y%m%d") + "_000" + ".csv"
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





  def processAllOnline(selt, url):
    print(f'processAllOnline: {url}')

    isDebugFromExistingHTMLFile = False
    if (isDebugFromExistingHTMLFile == False):
      # SECTION - 1/1 http req to link
      response = requests.get(url)
      content = response.content

      # SECTION 1/2 - open browser and navigate to url wait then for page load
      # content = openChrome(url, True)

      # SECTION 2 - parse content to beautifulsoup
      soup = BeautifulSoup(content, "html.parser")

      # SECTION 3 - write to file like html
      writeToFile("allonline-product-detail.html", soup.prettify())

    # SECTION 4 - process from html file or content
    soup = readContentFromFile("allonline-product-detail.html")

    # SECTION 5 - EXTRACT
    name = ""
    brand = ""
    sku = ""
    productPriceSale = ""
    productBasePrice = ""
    imageUrl = ""
    stockStatus = ""

    name = soup.find("h1", attrs={"id": "title-product"}).text.strip()
    brand = soup.find("meta", {"itemprop": "name"})["content"]
    sku = soup.find("span", {"itemprop": "sku"}).text.strip()
    productPriceSale = soup.find("div", attrs={"class": "price"}).find("span", attrs={"class": "currentPrice"}).text.replace("฿", "").strip()
    productBasePrice = soup.find("div", attrs={"class": "price"}).find("strike").text.replace("฿", "").strip()
    imageUrl = soup.find("div", attrs={"class": "main-image"}).select_one('img[src]:not([src=""])')["src"]
    stockStatus = soup.find("div", attrs={"class": "order-count-wrapper"}).find("div", attrs={"class": "available"}).text.strip()

    # SECTION 6 Load
    fileName = "allonline_product_detail_" + datetime.now().strftime("%Y%m%d") + "_000" + ".csv"
    header = ','.join(
      [
        'createdAt',
        'name',
        'brand',
        'sku',
        'productPriceSale',
        'productBasePrice',
        'imageUrl',
        'stockStatus',
        'url'
      ]
    ) + '\n'
    content = ','.join(
      [
        datetime.now().isoformat(),
        name,
        brand,
        sku,
        productPriceSale,
        productBasePrice,
        imageUrl,
        stockStatus,
        url
      ]
    ) + '\n'
    appendToFile(fileName, header, content)