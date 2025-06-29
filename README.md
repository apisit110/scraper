เปรียบเทียบราคาสินค้า

- สินค้าตัวเดียวกัน แต่ร้านไหนขายถูกสุด

โจทย์

- สินค้าตัวเดียวกันซื้อจากที่ไหนถูกที่สุด

How to know current price

- [x] lookup from website direct merchan
- [ ] lookup at store

How it work

- search product price from source like website, application
- save raw data to csv or any format
- transform raw data to new format like match the same product but different merchants
- save it, and ready to use
- do something e.g. send notification to someone that follow when price in target

# Source

- BigC
  - [x] Web
  - [ ] Android
- MakroPro
  - [x] Web
  - [ ] Android
- Watsons
  - [ ] Web
- Tops
  - [x] Web
- Lotuss
  - [x] Web
- Freshket
  - [x] Web
- All ONLINE
  - [x] Web
- Multybeauty
  - [ ] Web
- Shopee
  - [ ] Web

> fix error packages requests openssl
> https://stackoverflow.com/questions/76187256/importerror-urllib3-v2-0-only-supports-openssl-1-1-1-currently-the-ssl-modu
> python3 -m pipenv install urllib3==1.26.6

ETL (Extract – Transform – Load)

- Extract
- Transform
- Load

ELT (Extract – Load – Transform)

- Extract
- Load
- Transform

> Landing Zone = pos, web site, sensor, file, cloud
> Staging = raw data store in database

---

- Extract อ่านข้อมูลจาก Source เช่น Web, App
- Load เก็บไว้ใน Data lake หรือเก็บในเครื่องตัวเองก่อนใช้สำหรับทดสอบเท่านั้น
- Transform ดึงข้อมูลที่เก็บไว้มาแปลงให้เป็น format ที่ต้องการแต่ละ Web จะได้ข้อมูลไม่เหมือนกัน แต่เราอยากรู้ว่าสินค้าแต่ละชิ้น ชื่ออะไร ราคาเท่าไหร่

---

use pyenv to manage python version

```bash
# create env
pyenv virtualenv 3.12.9 scraper

# use env
pyenv local scraper

# install pacakge
pip install -r requirements.txt

# start program - Extract and Load
make start
```

---

### BigC - Web

เขียนด้วย: Next.js + RestAPI

- หน้า product detail เป็น ssr เราสามารถใช้ http get ได้เลยไม่ต้องเข้าถึง ui element ข้อมูลจะอยู่ใน tags script id คือ `__NEXT_DATA__` และต้องยิง api เส้น get product detail เพื่อดูรายละเอียดสินค้า

#### Columns

- product_id = props.pageProps.productDetail.product_id
- price_sales = props.pageProps.productDetail.price_sales
- volume = props.pageProps.productDetail.volume
- name = props.pageProps.productDetail.name
- sku = props.pageProps.productDetail.sku
- price_base = props.pageProps.productDetail.price_base
- main_barcode = props.pageProps.productDetail.attributes.main_barcode
- department_name = props.pageProps.productDetail.attributes.department_name
- brand = props.pageProps.productDetail.attributes.brand

### Makro - Web

เขียนด้วย: Next.js + GraphQL

- หน้า product detail เป็น ssr เราสามารถใช้ http get ได้เลยไม่ต้องเข้าถึง ui element ข้อมูลจะอยู่ใน tags script id คือ `__NEXT_DATA__`

#### Columns

- title = props.pageProps.product.title
- brand = props.pageProps.product.brand
- size = props.pageProps.product.size
- displayPrice = props.pageProps.product.displayPrice
- originPrice = props.pageProps.product.originPrice
- sku = props.pageProps.product.sku
- totalInventory = props.pageProps.product.totalInventory
- slabPriceTiers = props.pageProps.product.slabPrices.slabPriceTiers <!-- array -->
- productId = props.pageProps.productId
- buildId = buildId

### Watsons - Web

เขียนด้วย: Angular

- หน้า product detail มีข้อมูลอยู่ใน tags script id คือ `wtcth-state`

### Tops

เขียนด้วย Java?

- หน้า product detail เข้าถึง ui element เพื่อดึงข้อมูล

#### Columns

- name
- brand
- sku
- productPriceSale
- productBasePrice
- imageUrl
- stockStatus

### Lotuss

เขียนด้วย Java? + rest api

- หน้า product detail เราสามารถใช้ http get ได้เลยไม่ต้องเข้าถึง ui element ยิง api เส้น get product detail เพื่อดูรายละเอียดสินค้า

#### Columns

- id
- sku
- name
- brand
- regularPricePerUOW
- finalPricePerUOW
- stockStatus

### Freshket

เขียนด้วย: Next.js + GraphQL

- หน้า product detail เป็น ssr เราสามารถใช้ http get ได้เลยไม่ต้องเข้าถึง ui element ข้อมูลจะอยู่ใน tags script id คือ `__NEXT_DATA__`

#### Columns

- guid
- name
- originalPrice
- price

---

### สิ่งที่อยากได้

ตารางที่ 1 โดยรวม

| Id  | Date       | Name | BIG_C | MAKRO_PRO | WATSONS | TOPS | LOTUSS | ALLONLINE |
| --- | ---------- | ---- | ----- | --------- | ------- | ---- | ------ | --------- |
| 1   | 2025-06-28 | น้ำ  | 60    | 59        |         |      |        |           |
| 2   | 2025-06-28 | ข้าว | 112   | 110       |         |      |        |           |

<!-- ตารางที่ 2 แสดงแต่ละรายการ

| Id  | Date       | Name | Merchant  | Price | Original Price | Price Tiers |
| --- | ---------- | ---- | --------- | ----- | -------------- | ----------- |
| 1   | 2025-06-28 | น้ำ  | MAKRO_PRO | 0     | 0              |             | -->
