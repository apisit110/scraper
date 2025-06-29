from typing import Union
from fastapi import FastAPI
from libs.extractor.main import Extractor
from datetime import datetime
from libs.transform.main import Transform

'''
ELT
scraping got raw data write to csv
read csv to transform data add to database
query database to do awesome
'''

app = FastAPI()

@app.get("/")
def read_root():
  return {"Hello": "World"}

@app.get("/extract")
def extract():
  extractor = Extractor()
  extractor.extractBigC()
  extractor.extractMakroPro()
  extractor.extractWatsons()
  extractor.extractTops()
  extractor.extractLotuss()
  extractor.extractFreshket()
  extractor.extractAllOnline()
  return {"message": "Extraction logic goes here"}

@app.get("/transform")
def transform():
  transform = Transform()
  transform.transformProducts(datetime.now().strftime('%Y%m%d'))
  return {"message": "Transformation logic completed"}