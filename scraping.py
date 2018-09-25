# -*- coding: utf-8 -*-
from selenium import webdriver
import urllib
from bs4 import BeautifulSoup
import scraping_spec as ss
import pandas as pd

urls = ['http://kakaku.com/camera/digital-camera/ranking_0050/', 'http://kakaku.com/camera/mirrorless-slr/ranking_V071/', 'http://kakaku.com/camera/digital-slr/ranking_V072/']

for url in urls:

  html = urllib.request.urlopen(url)
  soup = BeautifulSoup(html, "html.parser")

  product_links = soup.find_all(class_="rkgBoxLink")
  for link in product_links:
    next_link = link.get('href') + 'spec/'
    ss.scrape_spec(next_link)

  time.sleep(1)
