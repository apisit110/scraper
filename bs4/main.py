# makro -> https://www.makro.co.th/
# BigC -> https://www.bigc.co.th/
# watsons -> https://www.watsons.co.th/
# tops -> https://www.tops.co.th/
# Lotus -> https://www.lotuss.com/th
# multybeauty -> https://www.multybeauty.com

from libs.bot.process import BotScaper
import json

'''
ELT
scraping got raw data write to csv
read csv to transform data add to database
query database to do awesome
'''

f = open('bs4/dev_data.json')
listData = json.load(f)
f.close()

for item in listData:
  if item['link']:
    scaper = BotScaper()

    if item['merchant'] == "BIG_C":
      scaper.processBigC(item['link'])
    elif item['merchant'] == "MAKRO_PRO":
      scaper.processMakroPro(item['link'])
    # elif item['merchant'] == "WATSONS":
    #   scaper.processWatsons(item['link'])
    elif item['merchant'] == "TOPS":
      scaper.processTops(item['link'])
    elif item['merchant'] == "LOTOSS":
      scaper.processLotoss(item['link'])
    elif item['merchant'] == "freshket.co":
      scaper.processFreshket(item['link'])
