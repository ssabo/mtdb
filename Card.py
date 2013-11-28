from bs4 import BeautifulSoup
import urllib2
import _mysql
import unicodedata

class Card:

  #Base for URL to fetch cards from
  __BASE_URL = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid='

  # HTML Object IDs
  __name_id   = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_nameRow'
  __mana_id   = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_manaRow'
  __cmc_id    = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cmcRow'
  __types_id  = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_typeRow'
  __text_id   = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_textRow'
  __flavor_id = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_flavorRow'
  __p_t_id    = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ptRow'
  __set_id    = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_setRow'
  __rarity_id = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rarityRow'
  __artist_id = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_artistRow'
  __card_id   = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_numberRow'

  def __init__(self,gatherer_id, db_connection = None):
    self.db        = db_connection 
    self.unique_id = gatherer_id

    URL = self.__BASE_URL + gatherer_id
    self.soup      = BeautifulSoup(urllib2.urlopen(URL))

    self.name      = self.__extract_content(self.__name_id)
    self.mana      = self.__extract_mana(self.__mana_id)
    self.cmc       = self.__extract_content(self.__cmc_id)
    self.types     = self.__extract_content(self.__types_id)
    self.text      = self.__extract_content(self.__text_id,'\n')
    self.flavor    = self.__extract_content(self.__flavor_id)
    self.power     = self.__extract_power(self.__p_t_id)
    self.toughness = self.__extract_toughness(self.__p_t_id)
    self.expansion = self.__extract_text(self.__set_id)
    self.rarity    = self.__extract_content(self.__rarity_id)
    self.card_id   = self.__extract_content(self.__card_id)
    self.artist    = self.__extract_content(self.__artist_id)

  def __str__(self):
    return self.name

  def __extract_items(self,content_id):
    bs4content = self.soup.find(id=content_id)
    if bs4content != None:
      bs4value = bs4content.find('div',class_='value')
      return bs4value
    else:
      return
  
  # extracts and formats regular content with or without images
  def __extract_content(self,content_id, delim = ' '):
    bs4content = self.__extract_items(content_id)
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
        
    return self.__normalize_string(content)


  def __normalize_string(self, string):
    if not all(ord(c) < 128 for c in string):
      return string.strip()
    else:
      return string.strip()
  
  # extracts raw text from content ignoring images
  def __extract_text(self,content_id):
    bs4content = self.__extract_items(content_id)
    bs4strings = bs4content.stripped_strings
    return self.__normalize_string(' '.join(string for string in bs4strings))
  
  # extracts mana values from contents
  def __extract_mana(self,content_id):
    bs4content = self.__extract_items(content_id)
    if bs4content is not None:
      bs4images = bs4content.find_all('img')
      if bs4images is not None:
        return self.__normalize_string(','.join('['+image['alt']+']' for image in bs4images))
    return ''

  def __extract_power(self,content_id):
    bs4content = self.__extract_items(content_id)
    if bs4content is not None:
      return self.__normalize_string(bs4content.string.strip().split('/')[0])
    return ''

  def __extract_toughness(self,content_id):
    bs4content = self.__extract_items(content_id)
    if bs4content is not None:
      return self.__normalize_string(bs4content.string.strip().split('/')[1])
    return ''

  def save_card(self):
    values = [self.unique_id, self.name, self.mana, self.cmc, self.types, self.text, self.flavor,
self.power, self.toughness, self.expansion, self.rarity, self.card_id, self.artist]

    for (i,value) in enumerate(values):
      values[i] = value.replace("'", "\\'")

    create_card_query = u"""
INSERT INTO cards (
ID, name, mana, cmc, types, text, flavor,
power, toughness, expansion, rarity, card_id, artist
) VALUES (
'%s', '%s', '%s', '%s', '%s', '%s', '%s',
'%s', '%s', '%s', '%s', '%s', '%s'
)""" % tuple(values)
    create_card_query = create_card_query.encode('utf-8')
    self.db.query(create_card_query)

  def print_card(self):
    print "Name      :    %s"      % self.name
    print "Mana      :    %s"      % self.mana
    print "CMC       :    %s"      % self.cmc
    print "Types     :    %s"      % self.types
    print "Text      :    %s"      % self.text
    print "Flavor    :    %s"      % self.flavor
    print "P/T       :    %s / %s" % (self.power, self.toughness)
    print "Expansion :    %s"      % self.expansion
    print "Rarity    :    %s"      % self.rarity
    print "Card ID   :    %s"      % self.card_id
    print "Artist    :    %s"      % self.artist
