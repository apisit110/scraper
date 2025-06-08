from libs.bot.process import BotScaper
import json
import os

'''
ELT
scraping got raw data write to csv
read csv to transform data add to database
query database to do awesome
'''

_path = os.path.join('bs4', 'libs', 'constants', 'merchant.json')
f = open(_path, 'r')
MERCHANT = json.load(f)
f.close()

f = open('bs4/data.json')
listData = json.load(f)
f.close()

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

# ----- MAKRO_PRO -----
f = open('bs4/source_makro_pro_product_detail_pages.json')
makroProductDetailPages = json.load(f)
f.close()
for page in makroProductDetailPages:
  scaper = BotScaper()
  url = page['url']
  scaper.processMakroPro(url)

# for item in listData:
#   if item['link']:
#     scaper = BotScaper()

#     # if item['merchant'] == MERCHANT['BIG_C']:
#     #   scaper.processBigC(item['link'])
    
#     # elif item['merchant'] == MERCHANT['WATSONS']:
#     #   scaper.processWatsons(item['link'])
#     # elif item['merchant'] == MERCHANT['TOPS']:
#     #   scaper.processTops(item['link'])
#     # elif item['merchant'] == MERCHANT['LOTUSS']:
#     #   scaper.processLotuss(item['link'])
#     # elif item['merchant'] == MERCHANT['FRESHKET']:
#     #   scaper.processFreshket(item['link'])
