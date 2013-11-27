#!/usr/bin/env python2.7

import urllib2
from bs4 import BeautifulSoup

# global objects
URL = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=31790'
soup = BeautifulSoup(urllib2.urlopen(URL))

# HTML Object IDs
name_id   = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_nameRow'
mana_id   = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_manaRow'
cmc_id    = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cmcRow'
types_id  = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_typeRow'
text_id   = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_textRow'
flavor_id = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_flavorRow'
p_t_id    = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ptRow'
set_id    = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_setRow'
rarity_id = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rarityRow'
artist_id = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_artistRow'
card_id   = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_numberRow'

# extracts the value items from the specified section
def extract_items(soup,content_id):
  bs4content = soup.find(id=content_id)
  if bs4content != None:
    bs4value = bs4content.find('div',class_='value')
    return bs4value
  else:
    return

# extracts and formats regular content with or without images
def extract_content(soup,content_id, delim = ' '):
  bs4content = extract_items(soup,content_id)
  if bs4content == None:
    return ''
  bs4items = bs4content.descendants
  content = ''
  last_item = ''
  for item in bs4items:
    item_type = item.name 

    if last_item == 'img' or item_type == 'img':
      content = content.strip() + " "
    else:
      content = content.strip() + delim

    if item_type == 'img':
      content = content + '[' + item['alt'] + ']'
      last_item = 'img'
    elif item_type == None:
      content = content + item.strip()
      last_item = 'text'
      
  return content.strip()

# extracts raw text from content ignoring images
def extract_text(soup,content_id):
  bs4content = extract_items(soup,content_id)
  bs4strings = bs4content.stripped_strings
  return ' '.join(string for string in bs4strings).strip()

# extracts mana values from contents
def extract_mana(soup,content_id):
  bs4content = extract_items(soup,content_id)
  bs4images = bs4content.find_all('img')
  return ' '.join(image['alt'] for image in bs4images).strip()

print "Name      :    %s" % extract_content(soup,name_id)
print "Mana      :    %s" % extract_mana(soup,mana_id)
print "CMC       :    %s" % extract_content(soup,cmc_id)
print "Types     :    %s" % extract_content(soup,types_id)
print "Text      :    %s" % extract_content(soup,text_id,'\n')
print "Flavor    :    %s" % extract_content(soup,flavor_id)
print "P/T       :    %s" % extract_content(soup,p_t_id)
print "Expansion :    %s" % extract_text(soup,set_id)
print "Rarity    :    %s" % extract_content(soup,rarity_id)
print "Card ID   :    %s" % extract_content(soup,card_id)
print "Artist    :    %s" % extract_content(soup,artist_id)
