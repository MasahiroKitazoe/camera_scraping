import pandas as pd
import re

def make_dict():
  stop_words = ['EOS', 'サイバーショット', 'COOLPIX', 'FUJIFILM', 'OLYMPUS', 'PowerShot', 'LUMIX', 'EXILIM', 'RICOH', 'PENTAX', 'キット', 'ソニー', 'SONY', 'Kiss', 'PEN', 'ライカ', 'LEICA', 'RICOH', 'リコー', 'オリンパス', 'パナソニック', 'ボディ', 'Canon', 'Nikon', 'キャノン', 'ニコン']

  stop_words_for_make_name_list =['キット', 'ボディ', 'レンズ']

  df = pd.read_csv('./datasets/cameras.csv')
  df = df.iloc[:, :2]

  name_check_list = []

  for index, val in df.iterrows():
    word_list = val['name'].split(' ')
    for word in word_list:
      for stop_word in stop_words:
        if stop_word in word:
          word_list.remove(word)
          break
        else:
          try:
            int(word)
            word_list.remove(word)
            break
          except ValueError:
            pass
    name_check_list.append(word_list)

# 全部いっぺんにスクレイピングすると、Bot判定されるので、手動で機種名を配列に入れて指定することにする。
  # cam_names_list = []

  # camera_list = df['name']
  # for camera in camera_list:
  #   cam_elements = camera.split(' ')
  #   for stop_word in stop_words_for_make_name_list:
  #     for element in cam_elements:
  #       if stop_word in element:
  #         cam_elements.remove(element)

  #   result = ' '.join(cam_elements)
  #   cam_names_list.append(result)

  return name_check_list
