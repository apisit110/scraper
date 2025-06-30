import os
from datetime import datetime
import pandas as pd
import json
from libs.bot.process import generateRawFileName, generateProductFileName
from table_products import tableProducts

class Transform:
  def __init__(self):
    pass

  def transformProducts(self, date):
    _path = os.path.join('bs4', 'libs', 'constants', 'merchant.json')
    f = open(_path, 'r')
    MERCHANTS = json.load(f)
    f.close()

    mapBigCSkuToId = {}
    mapMakroProSkuToId = {}
    # mapWatsonsSkuToId = {}
    mapTopsSkuToId = {}
    mapLotussSkuToId = {}
    # mapFreshketSkuToId = {}
    mapAllOnlineSkuToId = {}
    for product in tableProducts:
      if (product['big_c_sku'] != ''): mapBigCSkuToId[product['big_c_sku']] = product['id']
      if (product['makro_pro_sku'] != ''):  mapMakroProSkuToId[product['makro_pro_sku']] = product['id']
      # if (product['watsons_sku'] != ''):  mapWatsonsSkuToId[product['watsons_sku']] = product['id']
      if (product['tops_sku'] != ''):  mapTopsSkuToId[product['tops_sku']] = product['id']
      if (product['lotuss_sku'] != ''):  mapLotussSkuToId[product['lotuss_sku']] = product['id']
      # if (product['freshket_sku'] != ''):  mapFreshketSkuToId[product['freshket_sku']] = product['id']
      if (product['allonline_sku'] != ''):  mapAllOnlineSkuToId[product['allonline_sku']] = product['id']

    bigCFilePath = os.path.join('RawZone', generateRawFileName(MERCHANTS['BIG_C'], date))
    f = open(bigCFilePath, 'r')
    bigCData = pd.read_csv(f)
    f.close()

    makroProFilePath = os.path.join('RawZone', generateRawFileName(MERCHANTS['MAKRO_PRO'], date))
    f = open(makroProFilePath, 'r')
    makroProData = pd.read_csv(f)
    f.close()

    # watson...

    topsFilePath = os.path.join('RawZone', generateRawFileName(MERCHANTS['TOPS'], date))
    f = open(topsFilePath, 'r')
    topsData = pd.read_csv(f)
    f.close()

    lotussFilePath = os.path.join('RawZone', generateRawFileName(MERCHANTS['LOTUSS'], date))
    f = open(lotussFilePath, 'r')
    lotussData = pd.read_csv(f) 
    f.close()

    # freshket...

    allOnlineFilePath = os.path.join('RawZone', generateRawFileName(MERCHANTS['ALLONLINE'], date))
    f = open(allOnlineFilePath, 'r')
    allOnlineData = pd.read_csv(f)
    f.close()
    
    result = {}
    for index, row in bigCData.iterrows():
      sku = str(row['sku'])
      if sku in mapBigCSkuToId:
        id = mapBigCSkuToId[sku]
        if id not in result:
          result[id] = {
            'Id': id,
            'Date': datetime.now().strftime('%Y-%m-%d'),
            'Name': row['name'],
            'BIG_C': row['price_sales'],
            'MAKRO_PRO': '',
            'WATSONS': '',
            'TOPS': '',
            'LOTUSS': '',
            'FRESHKET': '',
            'ALLONLINE': ''
          }
        else:
          result[id]['BIG_C'] = row['price_sales']
      else:
        print('please add sku to tableProducts for big_c_sku:', sku)

    for index, row in makroProData.iterrows():
      sku = str(row['sku'])
      if sku in mapMakroProSkuToId:
        id = mapMakroProSkuToId[sku]
        if id not in result:
          result[id] = {
            'Id': id,
            'Date': datetime.now().strftime('%Y-%m-%d'),
            'Name': row['title'],
            'BIG_C': '',
            'MAKRO_PRO': row['displayPrice'],
            'WATSONS': '',
            'TOPS': '',
            'LOTUSS': '',
            'FRESHKET': '',
            'ALLONLINE': ''
          }
        else:
          result[id]['MAKRO_PRO'] = row['displayPrice']
      else:
        print('please add sku to tableProducts for makro_pro_sku:', sku)

    # watson...

    for index, row in topsData.iterrows():
      sku = str(row['sku'])
      if sku in mapTopsSkuToId:
        id = mapTopsSkuToId[sku]
        if id not in result:
          result[id] = {
            'Id': id,
            'Date': datetime.now().strftime('%Y-%m-%d'),
            'Name': row['name'],
            'BIG_C': '',
            'MAKRO_PRO': '',
            'WATSONS': '',
            'TOPS': row['productPriceSale'],
            'LOTUSS': '',
            'FRESHKET': '',
            'ALLONLINE': ''
          }
        else:
          result[id]['TOPS'] = row['productPriceSale']
      else:
        print('please add sku to tableProducts for tops_sku:', sku)

    for index, row in lotussData.iterrows():
      sku = str(row['sku'])
      if sku in mapLotussSkuToId:
        id = mapLotussSkuToId[sku]
        if id not in result:
          result[id] = {
            'Id': id,
            'Date': datetime.now().strftime('%Y-%m-%d'),
            'Name': row['name'],
            'BIG_C': '',
            'MAKRO_PRO': '',
            'WATSONS': '',
            'TOPS': '',
            'LOTUSS': row['regularPricePerUOW'],
            'FRESHKET': '',
            'ALLONLINE': ''
          }
        else:
          result[id]['LOTUSS'] = row['regularPricePerUOW']
      else:
        print('please add sku to tableProducts for lotuss_sku:', sku)

    # freshket...

    for index, row in allOnlineData.iterrows():
      sku = str(row['sku'])
      if sku in mapAllOnlineSkuToId:
        id = mapAllOnlineSkuToId[sku]
        if id not in result:
          result[id] = {
            'Id': id,
            'Date': datetime.now().strftime('%Y-%m-%d'),
            'Name': row['name'],
            'BIG_C': '',
            'MAKRO_PRO': '',
            'WATSONS': '',
            'TOPS': '',
            'LOTUSS': '',
            'FRESHKET': '',
            'ALLONLINE': row['productPriceSale']
          }
        else:
          result[id]['ALLONLINE'] = row['productPriceSale']
      else:
        print('please add sku to tableProducts for allonline_sku:', sku)
    
    with open(generateProductFileName(date, '000'), 'w') as f:
      f.write('Id,Date,Name,BIG_C,MAKRO_PRO,WATSONS,TOPS,LOTUSS,ALLONLINE\n')
      for id, data in result.items():
        f.write(f"{data['Id']},{data['Date']},{data['Name']},{data['BIG_C']},{data['MAKRO_PRO']},{data['WATSONS']},{data['TOPS']},{data['LOTUSS']},{data['ALLONLINE']}\n")
  pass

  def transformProductDetail(self, date):
    # This function is not implemented in the original code
    pass

