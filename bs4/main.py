from libs.bot.process import BotScaper
import json

'''
ELT
scraping got raw data write to csv
read csv to transform data add to database
query database to do awesome
'''

f = open('bs4/data.json')
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
    elif item['merchant'] == "LOTUSS":
      scaper.processLotuss(item['link'])
    elif item['merchant'] == "freshket.co":
      scaper.processFreshket(item['link'])
