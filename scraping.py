# -*- coding: utf-8 -*-
import urllib
from bs4 import BeautifulSoup
import scraping_spec as ss
import pandas as pd
import time

def iter_rows(df):
  result_dict = {}
  for index, row in df.iterrows():
    result_dict[row[1]] = index + 1
  return result_dict

df_camera = pd.read_csv('datasets/cameras.csv', index_col=0)
df_makers = pd.read_csv('datasets/makers.csv')
df_frames = pd.read_csv('datasets/frames.csv')
df_finders = pd.read_csv('datasets/finders.csv')

makers_dict = iter_rows(df_makers)
frames_dict = iter_rows(df_frames)
finders_dict = iter_rows(df_finders)

dicts = [makers_dict, frames_dict, finders_dict]

makers = []
frames = []
finders = []

results = []
registered_model = []

urls = ['http://kakaku.com/camera/digital-camera/ranking_0050/', 'http://kakaku.com/camera/mirrorless-slr/ranking_V071/', 'http://kakaku.com/camera/digital-slr/ranking_V072/']

camera_type = 1

for url in urls:

  page_links =[url]

  while url is not None:
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    if soup.find(class_="next").find_next().get('href'):
      url = soup.find(class_="next").find_next().get('href')
      url = 'http://kakaku.com' + url
      page_links.append(url)
    else:
      url = None

  returned_links = []

  for url in page_links:
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    product_links = soup.find_all(class_="rkgBoxLink")
    for link in product_links:
      next_link = link.get('href') + 'spec/'
      result_dict, returned_link = ss.scrape_spec(next_link, dicts, returned_links)
      if returned_link is not None:
        result_dict['camera_type_id'] = camera_type
        results.append(result_dict)
        returned_links.append(returned_link)
      else:
        returned_link = ''
    time.sleep(1)

  camera_type += 1

print(len(results))

df = pd.io.json.json_normalize(results)
df_new = df_camera.append(df)[df_camera.columns.tolist()]
df_new = df_new.drop_duplicates(['name', 'maker_id'], keep='last')
df_new = df_new.reset_index(drop=True)
df_new.to_csv('datasets/cameras.csv')
