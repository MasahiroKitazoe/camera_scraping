# -*- coding: utf-8 -*-
from selenium import webdriver
import urllib
from bs4 import BeautifulSoup
import re

frame_match = {'中判サイズ': ['中判サイズFUJIFILM G Format43.8mm×32.9mmベイヤーCMOS', '中判サイズ32.9mm×43.8mmCMOS', '中判サイズ43.8mm×32.8mmCMOS', '中判サイズ53.4mm×40mmCMOS', '中判サイズ48mm×36mmCCD'], 'フルサイズ': ['35.9mm×24.0mm(フルサイズ) Exmor CMOSセンサー', '36mm×24mm(フルサイズ) CMOS', '35.8mm×23.9mm(フルサイズ) Exmor CMOSセンサー', 'フルサイズ35.6mm×23.8mmCMOS', 'フルサイズ36mm×24mmCMOS', 'フルサイズ35.9mm×24mmCMOS', 'フルサイズ35.8mm×23.9mmCMOS', 'フルサイズ35.9mm×24.0mmCMOS', 'フルサイズ35.9mm×23.9mmCMOS', 'フルサイズ36mm×23.9mmCMOS'], 'APS-C': ['23.5mm×15.7mm(APS-Cサイズ) 正方画素CMOS', '23.5mm×15.6mm(APS-Cサイズ) X-Trans CMOS III', '23.7mm×15.7mm(APS-Cサイズ)CMOS', '22.3mm×14.9mm(APS-Cサイズ)CMOS', '23.6mm×15.6mm(APS-Cサイズ) X-Trans CMOS II', '23.5mm×15.7mm(APS-Cサイズ)CMOS', 'APS-C型CMOS', 'APS-C22.3mm×14.9mmCMOS', 'APS-C23.5mm×15.6mmCMOS4', 'APS-C23.5mm×15.6mmCMOS', 'APS-C23.5mm×15.7mmCMOS', 'APS-C23.6mm×15.6mmCMOSIII', 'APS-C23.5mm×15.6mmCMOSIII', 'APS-C23.6mm×15.6mmCMOS', 'APS-C23.6mm×15.6mmCMOSII', 'APS-C23.4mm×15.5mmCMOS', 'APS-C23.6mm×15.7mmCMOS', 'APS-C22.4mm×15mmCMOS', 'APS-C22.5mm×15.0mmCMOS', 'APS-C23.7mm×15.7mmCMOS', 'APS-H26.7mm×17.9mmCMOS', '23.5mm×15.7mmCMOS X3'], '4/3型': ['4/3型(フォーサーズ)MOS', 'フォーサーズ4/3型LiveMOS'], '1型': ['1型CMOS', '1型CMOS(裏面照射型)', '1型MOS', '1/3.1型CMOS', '13.2mm×8.8mmCMOS'], '1/2.3型': ['1/2.3型CMOS(裏面照射型)', '1/2.3型MOS', '1/2.3型CCD', '1/2.3型CMOSx2', '1/2.3型CMOS', '1/2.33型CMOS(裏面照射型)', '1/2.33型CMOS', '1/2.33型CCD'], '1/3.1型': [], '1/1.7型': ['1/1.7型CMOS(裏面照射型)'], '1.5型': ['1.5型CMOS'], '1/10型': ['1/10型CMOS'], '1/5型': ['1/5型CMOS'], 'CMOSx2': ['CMOSx2'], 'CCD': ['CCD'], 'CMOS': ['CMOS'],}

def get_shooting_performance(shooting_num):
  if "○" not in shooting_num and "コマ" in shooting_num:
    shooting_num = shooting_num.replace('コマ', '')
    if '/秒' in shooting_num:
      shooting_num = shooting_num.replace('/秒', '')
    continuous_shooting_performance = float(shooting_num)
    return continuous_shooting_performance
  else:
    return ""

def get_max_shooting_num(shooting_num):
  max_shooting_num = shooting_num.replace('枚', '')
  return max_shooting_num

def scrape_spec(url, dicts, registered_links):
  makers_dict = dicts[0]
  frames_dict = dicts[1]
  finders_dict = dicts[2]

  html = urllib.request.urlopen(url)
  soup = BeautifulSoup(html, "html.parser")

  pattern = r"(.+)spec\/"
  matchOB = re.search(pattern, url)
  if matchOB:
    url_for_body = matchOB.group(1)

  if soup.find(class_="variSpec") is not None:
    variSpecs = soup.find(class_="specSelect").children
    for child in variSpecs:
      # print(child)
      # print(child.string)
      # print(type(child))
      # print('----------------------')
      if child.string is not None:
        if '本体' in child.string:
          target_info = child.children
          for info in target_info:
            if info.get('href') is not None:
              url_for_body = info.get('href')

  if url_for_body in registered_links:
    return None, None
  else:
    new_url = url_for_body + 'spec/'
    new_html = urllib.request.urlopen(new_url)
    soup = BeautifulSoup(new_html, "html.parser")

  name = soup.find(itemprop="name").text
  print(name)

  if soup.find(id="subInfoRow2") is not None:
    date_text = soup.find(id="subInfoRow2").text
    pattern = r"発売日：(\d+)年 ?(\d+)月"
    matchOB = re.search(pattern, date_text)
    if matchOB:
      open_year = int(matchOB.group(1))
      open_month = int(matchOB.group(2))
    else:
      open_year = ""
      open_month = ""
  else:
    open_year = ""
    open_month = ""

  maker = soup.find(class_="digestMakerName").text
  maker_id = makers_dict[maker]

  elements = {}

  ths = soup.find_all(class_="itemviewColor03b")
  for th in ths:
    elements[th.text] = th.find_next_sibling().text

  if soup.find(id="minPrice") is not None:
    price = soup.find(id="minPrice").find_next().text
  else:
    text = soup.find(id="minUesdPrice").text
    pattern = r"中古価格帯（税込）：(¥[\d,]+)"
    matchOB = re.search(pattern, text)
    if matchOB:
      price = matchOB.group(1)
    else:
      price = ""

  price = price.replace('¥', '').replace(',', '')
  if price != "":
    price = int(price)

  pattern = r"(\w\w\w\w?)万画素.有効画素."
  text = elements['画素数']
  matchOB = re.search(pattern, text)
  if matchOB:
    pixel = matchOB.group(1)
  else:
    pixel = ""

  pattern = r"通常.ISO(\w+).(\d+)"
  text = elements['撮影感度']
  matchOB = re.search(pattern, text)
  if matchOB:
    min_iso = matchOB.group(1)
    max_iso = matchOB.group(2)
  else:
    min_iso = ""
    max_iso = ""

  if '拡張' in text:
    pattern = r"(\d+)..?$"
    matchOB = re.search(pattern, text)
    if matchOB:
      max_iso = matchOB.group(1)

  if '連写撮影' in elements:
    shooting_num = elements['連写撮影']
    continuous_shooting_performance = get_shooting_performance(shooting_num)
  else:
    shooting_num = elements['連写撮影/秒']
    continuous_shooting_performance = get_shooting_performance(shooting_num)

  shutter_speed = elements['シャッタースピード']

  pattern = r"^(\d+\.?\d?)インチ(\d+\.?\d?).+"
  text = elements['液晶モニター']
  matchOB = re.search(pattern, text)
  if matchOB:
    monitor_size = float(matchOB.group(1))
    monitor_pixel = float(matchOB.group(2))
  else:
    monitor_size = ""
    monitor_pixel = ""

  if '撮影枚数\xa0' in elements:
    shooting_num = elements['撮影枚数\xa0']
    max_shooting_num = get_max_shooting_num(shooting_num)
  else:
    shooting_num = elements['撮影枚数']
    max_shooting_num = get_max_shooting_num(shooting_num)

  if 'ファインダー使用時' in max_shooting_num:
    pattern_f = r"ファインダー使用時：(\d+)"
    pattern_m = r"モニタ使用時：(\d+)"
    matchOB = re.search(pattern_f, max_shooting_num)
    if matchOB:
      max_num_of_shooting_with_finder = int(matchOB.group(1))
    else:
      max_num_of_shooting_with_finder = ""
    matchOB = re.search(pattern_m, max_shooting_num)
    if matchOB:
      max_num_of_shooting = int(matchOB.group(1))
    else:
      max_num_of_shooting = ""
  else:
    if "液晶モニタ使用時：" in max_shooting_num:
      max_shooting_num = max_shooting_num.replace('液晶モニタ使用時：', '')
      max_num_of_shooting_with_finder = ""
      if "\u3000" in max_shooting_num:
        max_num_of_shooting = ""
      if max_shooting_num != "":
        max_num_of_shooting = int(max_shooting_num)
    else:
      max_num_of_shooting_with_finder = ""
      if max_shooting_num != "":
        max_num_of_shooting = max_shooting_num
      else:
        max_num_of_shooting = ""

  if '4K対応\xa0' in elements:
    four_k = elements['4K対応\xa0']
  else:
    four_k = elements['4K対応']

  if "○" in four_k:
    four_k = True
  else:
    four_k = False

  if 'Wi-Fi\xa0' in elements:
    wifi = elements['Wi-Fi\xa0']
  else:
    wifi = elements['Wi-Fi']

  if "○" in wifi:
    wifi = True
  else:
    wifi = False

  if 'Bluetooth対応(常時接続)' in elements:
    bluetooth = elements['Bluetooth対応(常時接続)']
  else:
    bluetooth = elements['Bluetooth']

  if "焦点距離\xa0" in elements:
    focus_range = elements['焦点距離\xa0']
    if "〜" in focus_range:
      pattern = r"(\d+.?\d?)mm〜(\d+.?\d?)mm"
      matchOB = re.search(pattern, focus_range)
      if matchOB:
        min_focus = matchOB.group(1)
        max_focus = matchOB.group(2)
      else:
        min_focus = ""
        max_focus = ""
    elif 'mm' in focus_range:
      focus_range = focus_range.replace('mm', '')
      focus_range = float(focus_range)
      min_focus = round(focus_range)
      max_focus = round(focus_range)
    else:
      min_focus = ""
      max_focus = ""
  else:
    min_focus = ""
    max_focus = ""

  if "光学ズーム\xa0" in elements:
    zoom = elements['光学ズーム\xa0']
    if "倍" in zoom:
      zoom = zoom.replace('倍', '')
      zoom = round(float(zoom))
    else:
      zoom = ""
  else:
    zoom = ""

  if "可動式モニタ" in elements:
    move_panel = elements['可動式モニタ']
  else:
    move_panel = ""

  if "チルト液晶\xa0" in elements:
    if "○" in elements['チルト液晶\xa0']:
      move_panel = "チルト液晶"

  if "バリアングル液晶\xa0" in elements:
    if "○" in elements['バリアングル液晶\xa0']:
      move_panel = "バリアングル液晶"

  if "○" in elements["自分撮り機能\xa0"]:
    selfie = True
  else:
    selfie = False

  if "総重量" in elements['重量']:
    pattern = r"総重量：(\d+.?\d?)g"
    matchOB = re.search(pattern, elements['重量'])
    if matchOB:
      weight = round(float(matchOB.group(1)))
    else:
      weight = ""
  elif '本体' in elements['重量']:
    weight = elements['重量'].replace('本体：', '').replace('g', '')
    weight = round(float(weight))
  else:
    if 'g' in elements['重量']:
      weight = elements['重量'].replace('g', '')
      weight = round(float(weight))
    else:
      weight = None

  size = elements['幅x高さx奥行き']
  if 'x' in elements['幅x高さx奥行き']:
    size_list = size.split('x')
    width = float(size_list[0])
    height = float(size_list[1])
    depth = size_list[2]
    depth = float(depth.replace(' mm', ''))
  else:
    width = ""
    height = ""
    depth = ""

  if "防水性能" in elements:
    waterproof = elements['防水性能']
  else:
    waterproof = elements['防塵・防滴\xa0']

  if 'GPS機能\xa0' in elements:
    if "○" in elements['GPS機能\xa0']:
      gps = True
    else:
      gps = False
  else:
    if "○" in elements['GPS\xa0']:
      gps = True
    else:
      gps = False

  if "最短撮影距離" in elements:
    nearest_shot_str = elements['最短撮影距離']
    pattern_n = r"(\d+)cm\(標準\)"
    pattern_m = r"(\d+)cm\(マクロ\)"
    matchOB_n = re.search(pattern_n, nearest_shot_str)
    if matchOB_n:
      nearest_shot = matchOB_n.group(1)
      nearest_shot = float(nearest_shot)
    else:
      nearest_shot = ""
    matchOB_m = re.search(pattern_m, nearest_shot_str)
    if matchOB_m:
      nearest_shot_with_macro_mode = matchOB_m.group(1)
      nearest_shot_with_macro_mode = float(nearest_shot_with_macro_mode)
    else:
      nearest_shot_with_macro_mode = ""
  else:
    nearest_shot = ""
    nearest_shot_with_macro_mode = ""

  if '手ブレ補正機構\xa0' in elements:
    anti_shake = elements['手ブレ補正機構\xa0']

  if "5軸手ブレ補正" in elements:
    if "○" in elements['5軸手ブレ補正']:
      five_axis_anti_shake = True
    else:
      five_axis_anti_shake = False
  else:
    five_axis_anti_shake = ""

  if "F値\xa0" in elements:
    f_value = elements['F値\xa0']
    if "〜" in  f_value:
      pattern = r"F(\d.?\d?)〜F(\d.?\d?)"
      matchOB = re.search(pattern, f_value)
      if matchOB:
        f_value = matchOB.group(1)
        f_value_wide = matchOB.group(2)
      else:
        f_value = ""
        f_value_wide = ""
    else:
      f_value = f_value.replace('F', '')
      f_value_wide = f_value
  else:
    f_value = ""
    f_value_wide = ""

  frame_id = 14
  if '撮像素子\xa0' in elements:
    frame = elements['撮像素子\xa0']
    for key , val in frame_match.items():
      if frame in val:
        frame_id = frames_dict[key]

  if "ファインダー" in elements:
    finder = elements['ファインダー']
  else:
    finder = elements['ファインダー形式\xa0']

  if finder in finders_dict:
    finder_id = finders_dict[finder]
  else:
    finder_id = 2

  if '360度カメラ\xa0' in elements:
    if elements['360度カメラ\xa0'] == "○":
      super_wide = True
    else:
      super_wide = False
  else:
    super_wide = False

  if 'タッチパネル' in elements:
    if "○" in elements['タッチパネル']:
      touch_panel = True
    else:
      touch_panel = False
  elif 'タッチパネル\xa0':
    if "○" in elements['タッチパネル\xa0']:
      touch_panel = True
    else:
      touch_panel = False
  else:
    touch_panel = False

  results = {'name': name, 'maker_id': maker_id, 'price': price, 'pixel': pixel, 'min_iso': min_iso, 'max_iso': max_iso, 'continuous_shooting_performance': continuous_shooting_performance, 'shutter_speed': shutter_speed, 'monitor_size': monitor_size, 'monitor_pixel': monitor_pixel, 'max_num_of_shooting': max_num_of_shooting, 'max_num_of_shooting_with_finder': max_num_of_shooting_with_finder, 'four_k': four_k, 'wifi': wifi, 'bluetooth': bluetooth, 'min_focus': min_focus, 'max_focus': max_focus, 'zoom': zoom, 'move_panel': move_panel, 'selfie': selfie, 'weight': weight, 'width': width, 'height': height, 'depth': depth, 'gps': gps, 'nearest_shot': nearest_shot, 'nearest_shot_with_macro_mode': nearest_shot_with_macro_mode, 'anti_shake': anti_shake, 'five_axis_anti_shake': five_axis_anti_shake, 'f_value': f_value, 'f_value_wide': f_value_wide, 'frame_id': frame_id, 'finder_id': finder_id, 'super_wide': super_wide, 'open_year': open_year, 'open_month': open_month, 'touch_panel': touch_panel, 'waterproof': waterproof}
  return results, url_for_body
