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


# listData = [
#   # ---------- SECTION WATSONS ----------
#   # ---------- SECTION WATSONS ----------
#   # ---------- SECTION WATSONS ----------
#   # {
#   #   "merchant": "WATSONS",
#   #   "name": "วาสลีน เฮลธี้ ไบรท์ กลูต้า-ไฮยา เซรั่ม เบิสท์ โลชั่น สมูทติ้ง เพอร์เฟคเตอร์ 300 มล.",
#   #   "description": "ลดราคา",
#   #   "link": "https://www.watsons.co.th/th/วาสลีน-เฮลธี้-ไบรท์-กลูต้า-ไฮยา-เซรั่ม-เบิสท์-โลชั่น-สมูทติ้ง-เพอร์เฟคเตอร์-300-มล./p/BP_309104"
#   # },

#   # ---------- SECTION freshket.co ----------
#   # ---------- SECTION freshket.co ----------
#   # {
#   #   "merchant": "freshket.co",
#   #   "name": "ข้าวหอมมะลิ 100% ตราเบญจรงค์",
#   #   "description": "",
#   #   "link": "https://freshket.co/product/detail/ข้าวหอมมะลิ-100-ตราเบญจรงค์/d5e57636-7181-4843-a41f-1eb52eb324de"
#   # },
# ]

# print(listData)

f = open('bs4/data.json')
listData = json.load(f)
f.close()

# for x in listData:
for x in listData:
  # print(x['merchant'])
  # print(x['link'])

  if x['link']:
    scaper = BotScaper()

    if x['merchant'] == "BIG_C":
      scaper.processBigC(x['link'])
      # pass
    elif x['merchant'] == "MAKRO_PRO":
      scaper.processMakroPro(x['link'])
      # pass
    elif x['merchant'] == "WATSONS":
      scaper.processWatsons(x['link'])
      # pass
    elif x['merchant'] == "TOPS":
      scaper.processTops(x['link'])
      # pass
    elif x['merchant'] == "LOTOSS":
      scaper.processLotoss(x['link'])
      # pass
    # elif x['merchant'] == "freshket.co":
    #   scaper.processFreshket(x['link'])
    #   pass
