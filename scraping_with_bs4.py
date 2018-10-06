# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd
import time
from camera_name_dict import make_dict

portal_sites = ['kakaku.com',
'www.yodobashi.com',
'biccamera.com',
'amazon.co.jp',
'mapcamera.com',
'rakuten.co.jp',
'shopping.yahoo.co.jp',
'sony.jp',
'shop.kitamura.jp',
'yamada-denkiweb.com',
'nojima.co.jp',
'joshinweb.jp',
'kojima.net',
'edion.com'
]

name_check_list = make_dict()

df_target_cameras = pd.read_csv('datasets/target_cameras.csv')
cam_names_list = df_target_cameras['name']

cam_list_del_id = 0

driver = webdriver.Chrome('./chromedriver')

driver_reset = 1

for model in cam_names_list:

  if driver_reset > 3:
    driver.quit()
    driver = webdriver.Chrome('./chromedriver')
    driver_reset = 1

  results =[]
  driver.implicitly_wait(5)
  driver.get('https://www.google.co.jp/search?q=' + model + 'レビュー')
  driver.implicitly_wait(5)

  try:
    while True:
      html = driver.page_source
      soup = BeautifulSoup(html, "html.parser")

      all_search = soup.find_all(class_='rc')

      for data in all_search:
        url = data.find('a').get('href')
        for pt_site in portal_sites:
          exit_flag = False
          if pt_site in url:
            exit_flag = True
          else:
            title = data.find('h3').string
            dis_element = data.find(class_='st')
            if dis_element is None:
              dis = ''
            else:
              dis = dis_element.string
            result = [title, dis, url]
            results.append(result)
            exit_flag = True
          if exit_flag is True:
            break

      driver.find_element_by_id('pnnext').click()

  except NoSuchElementException:
      print('最後のページまできたよ')

  index_of_results = 0
  del_list = []

  for item in results:
    dele = True
    stop_loop = False
    for check_words in name_check_list:
      if stop_loop is True:
        stop_loop = False
        break
      for check_word in check_words:
        if check_word in item[0]:
          dele = False
          stop_loop = True
          break
        else:
          pass
    if dele is True:
      results.pop(index_of_results)
    index_of_results += 1

  print(model)
  print(str(len(results)) + '件のデータが取れたよ')

  if len(results) ==0:
    print('スクレイピング失敗！処理を終えます！')
    driver.quit()
    break

  df_review = pd.read_csv('datasets/reviews.csv', index_col=0 )
  df_inter_table = pd.read_csv('datasets/camera_reviews.csv', index_col=0)

  if len(df_inter_table) == 0:
    last_cam_id = 0
  else:
    camera_ids = df_inter_table['camera_id']
    table_len = len(camera_ids)
    last_cam_id = int(camera_ids[table_len - 1])

  if len(df_review) == 0:
    review_index = 1
  else:
    review_index = len(df_review) + 1

  for result in results:
    df_result = pd.DataFrame()
    df_result['title'] = [result[0]]
    df_result['body'] = [result[1]]
    df_result['url'] = [result[2]]
    df_review = pd.concat([df_review, df_result])

    df_cam_rev = pd.DataFrame()
    df_cam_rev['camera_id'] = [last_cam_id + 1]
    df_cam_rev['review_id'] = [review_index]
    df_inter_table = pd.concat([df_inter_table, df_cam_rev])
    review_index += 1

  df_review = df_review.reset_index(drop=True)
  df_inter_table = df_inter_table.reset_index(drop=True)
  df_review.to_csv('datasets/reviews.csv')
  df_inter_table.to_csv('datasets/camera_reviews.csv')

  cam_names_list = cam_names_list.drop(cam_list_del_id)
  df_update_cameras = pd.DataFrame()
  df_update_cameras['name'] = cam_names_list
  df_update_cameras.to_csv('datasets/target_cameras.csv')
  cam_list_del_id += 1

  driver_reset += 1

