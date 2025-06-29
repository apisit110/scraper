from libs.bot.process import BotScaper
import json
import os

'''
ELT
scraping got raw data write to csv
read csv to transform data add to database
query database to do awesome
'''

class Extractor:
  def __init__(self):
    pass

  _path = os.path.join('bs4', 'libs', 'constants', 'merchant.json')
  f = open(_path, 'r')
  MERCHANT = json.load(f)
  f.close()

  f = open('bs4/data.json')
  listData = json.load(f)
  f.close()

  def extractBigC(self):
    # ----- BIG_C -----
    index = 0
    f = open('bs4/source_big_c_product_detail_pages.json')
    bigcProductDetailPages = json.load(f)
    f.close()
    for page in bigcProductDetailPages:
      isFirstLoop = index == 0
      index += 1

      scaper = BotScaper()
      url = page['url']
      scaper.processBigC(url, isFirstLoop)
    pass

  def extractMakroPro(self):
    # ----- MAKRO_PRO -----
    f = open('bs4/source_makro_pro_product_detail_pages.json')
    makroProductDetailPages = json.load(f)
    f.close()
    for page in makroProductDetailPages:
      scaper = BotScaper()
      url = page['url']
      scaper.processMakroPro(url)
    pass

  def extractWatsons(self):
    # ----- Watsons -----
    # processWatsons...
    pass

  def extractTops(self):
    # ----- TOPS -----
    f = open('bs4/source_tops_product_detail_pages.json')
    topsProductDetailPages = json.load(f)
    f.close()
    for page in topsProductDetailPages:
      scaper = BotScaper()
      url = page['url']
      scaper.processTops(url)
    pass

  def extractLotuss(self):
    # ----- Lotuss -----
    f = open('bs4/source_lotuss_product_detail_pages.json')
    lotussProductDetailPages = json.load(f)
    f.close()
    for page in lotussProductDetailPages:
      scaper = BotScaper()
      url = page['url']
      scaper.processLotuss(url)
    pass

  def extractFreshket(self):
    # ----- Freshket -----
    f = open('bs4/source_freshket_product_detail_pages.json')
    lotussProductDetailPages = json.load(f)
    f.close()
    for page in lotussProductDetailPages:
      scaper = BotScaper()
      url = page['url']
      scaper.processFreshket(url)
    pass

  def extractAllOnline(self):
    # ----- All ONLINE -----
    f = open('bs4/source_allonline_product_detail_pages.json')
    allonlineProductDetailPages = json.load(f)
    f.close()
    for page in allonlineProductDetailPages:
      scaper = BotScaper()
      url = page['url']
      scaper.processAllOnline(url)
    pass
