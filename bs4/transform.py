import os
import json
import re

_path = os.path.join('bs4', 'libs', 'constants', 'merchant.json')
f = open(_path, 'r')
MERCHANT = json.load(f)
f.close()


def mapColumn(row, columnIndex):
  try:
    return row.split(',')[columnIndex]
  except:
    return ''
  
def checkDiscount(priceSale, basePrice):
  discountPercentage = (100 - ((priceSale / basePrice) * 100))
  return format(discountPercentage, '.2f')
  
def processEachRow(fileData, groupData):
  for idx, row in enumerate(fileData.split('\n')):
    if idx == 0: continue
    if not row: continue
    
    date = mapColumn(row, 0)
    merchant = mapColumn(row, 1)
    name = mapColumn(row, 2)
    priceSale = float(mapColumn(row, 3))
    basePrice = priceSale
    if mapColumn(row, 4) != '': basePrice = float(mapColumn(row, 4))
    url = mapColumn(row, 5)

    discountPercentage = float(checkDiscount(priceSale, basePrice))
    message = ''
    prefix = ''
    percentage = ''

    if discountPercentage > 0:
      percentage = f'-{discountPercentage}% '
    
    if discountPercentage > 10:
      prefix = '[hot] '
      pass
    
    message += f'{prefix}{percentage}{name} {url}'
    if discountPercentage > 10: print(message)

    if merchant == MERCHANT['BIG_C']:
      pass
    elif merchant == MERCHANT['MAKRO_PRO']:
      if re.search('คริสตัล น้ำดื่ม 1.5 ล. x 6', name):
        groupData['pd1']['MAKRO_PRO']['priceSale'] = priceSale
        groupData['pd1']['MAKRO_PRO']['basePrice'] = basePrice
      pass
    elif merchant == MERCHANT['TOPS']:
      pass
    elif merchant == MERCHANT['LOTUSS']:
      if re.search('คริสตัล น้ำดื่ม 1500 มล. แพ็ค 6', name):
        groupData['pd1']['LOTUSS']['priceSale'] = priceSale
        groupData['pd1']['LOTUSS']['basePrice'] = basePrice
      pass
    elif merchant == MERCHANT['FRESHKET']:
      pass

arr = os.listdir(os.path.join('RawZone'))

for item in sorted(arr, reverse=True):
  # print(f'process file :: {item}')

  groupData = {
    'pd1': {
      'MAKRO_PRO': {
        'priceSale': '',
        'basePrice': ''
      },
      'LOTUSS': {
        'priceSale': '',
        'basePrice': ''
      },
    }
  }

  _path = os.path.join('RawZone', item)
  f = open(_path, 'r')
  processEachRow(f.read(), groupData)
  f.close()

  # print(groupData)
  break
