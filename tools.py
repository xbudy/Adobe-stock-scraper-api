import requests
from bs4 import BeautifulSoup
import pandas as pd

def parse_id(id):
  headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
      'Accept': '*/*',
      'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
      'X-Request-Id': 'cac83afb1ae95a9f8b140c7c2910fae7',
      'X-Requested-With': 'XMLHttpRequest',
      'Connection': 'keep-alive',
      'Referer': 'https://stock.adobe.com/search/free?filters%5Bcontent_type%3Aphoto%5D=1&filters%5Bcontent_type%3Aillustration%5D=1&filters%5Bcontent_type%3Azip_vector%5D=1&filters%5Bfree_collection%5D=1&filters%5Bcontent_type%3Aimage%5D=1&k=python&order=relevance&safe_search=1&limit=100&search_page=1&search_type=usertyped&acp=&aco=python&get_facets=1&asset_id=275146416',
      'TE': 'Trailers',
  }


  response = requests.get('https://stock.adobe.com/Ajax/MediaData/{}?full=1'.format(id), headers=headers)
  keys=response.json()['keywords']
  description=response.json()['meta_description']
  file_type=response.json()['content_type']
  return keys,description,file_type



def searcher(keyword):
  headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
      'Accept': '*/*',
      'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
      'X-Request-Id': 'cac83afb1ae95a9f8b140c7c2910fae7-1625233468943',
      'X-Requested-With': 'XMLHttpRequest',
      'Connection': 'keep-alive',
      'Referer': 'https://stock.adobe.com/search/free?load_type=search&native_visual_search=&similar_content_id=&is_recent_search=&search_type=usertyped&k=python',
      'TE': 'Trailers',
  }

  params = (
      ('filters[content_type:photo]', '1'),
      ('filters[content_type:illustration]', '1'),
      ('filters[content_type:zip_vector]', '1'),
      ('filters[free_collection]', '1'),
      ('filters[content_type:image]', '1'),
      ('k', keyword),
      ('order', 'relevance'),
      ('safe_search', '1'),
      ('limit', '100'),
      ('search_page', '1'),
      ('search_type', 'usertyped'),
      ('acp', ''),
      ('get_facets', '1'),
  )

  response = requests.get('https://stock.adobe.com/Ajax/Search', headers=headers, params=params)
  data=response.json()
  master_data=[]
  if data['total_items']!=0:
    products_id=list(data['items'].keys())
    for id in products_id:
      product={}
      item=data['items'][id]
      product['title']=item['title']
      product['image_source']=item['thumbnail_url']
      product['file_type']=item['asset_type']
      product['permalink']=item['content_url']
      product['similar_keys'],product['description'],product['file_type']=parse_id(id)
      master_data.append(product)
  return master_data

def getData(keyword):
  data=searcher(keyword)
  df=pd.DataFrame(data)
  l=df.to_csv(index=False)
  return l
