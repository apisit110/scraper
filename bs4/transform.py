from libs.transform.main import Transform
from datetime import datetime

transfrom = Transform()
transfrom.transformProducts(datetime.now().strftime('%Y%m%d'))
