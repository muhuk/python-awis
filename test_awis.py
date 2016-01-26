import os
from awis import AwisApi

ACCESS_ID = os.getenv('ACCESS_ID')
SECRET_ACCESS_KEY = os.getenv('SECRET_ACCESS_KEY')
assert ACCESS_ID is not None and SECRET_ACCESS_KEY is not None, \
  'Tests require ACCESS_ID and SECRET_ACCESS_KEY to be set in the environment'
  
def test_category_listings():
  api = AwisApi(ACCESS_ID, SECRET_ACCESS_KEY)
  tree = api.category_listings("Top/Business/Financial_Services")
  items = tree.findall(".//{%s}Count" % api.NS_PREFIXES["awis"])
  assert items[0].text > 0
  
def test_url_info():
  api = AwisApi(ACCESS_ID, SECRET_ACCESS_KEY)
  tree = api.url_info("www.domain.com", "Rank", "LinksInCount")
  elem = tree.find(".//{%s}StatusCode" % api.NS_PREFIXES["alexa"])
  assert elem.text == "Success"
