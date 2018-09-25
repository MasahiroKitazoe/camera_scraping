# -*- coding: utf-8 -*-
from selenium import webdriver
import urllib
from bs4 import BeautifulSoup

def scrape_spec(url):
  html = urllib.request.urlopen(url)
  soup = BeautifulSoup(html, "html.parser")

  name = soup.find(itemprop="name").text

