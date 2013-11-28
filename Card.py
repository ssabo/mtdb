from bs4 import BeautifulSoup
import urllib2

BASE_URL = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid='

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

class Card:

  def __init__(self,gatherer_id):
    URL = BASE_URL + gatherer_id
    self.soup      = BeautifulSoup(urllib2.urlopen(URL))
    self.name      = self.extract_content(name_id)
    self.mana      = self.extract_mana(mana_id)
    self.cmc       = self.extract_content(cmc_id)
    self.types     = self.extract_content(types_id)
    self.text      = self.extract_content(text_id,'\n')
    self.flavor    = self.extract_content(flavor_id)
    self.p_t       = self.extract_content(p_t_id)
    self.expansion = self.extract_text(set_id)
    self.rarity    = self.extract_content(rarity_id)
    self.card_id   = self.extract_content(card_id)
    self.artist    = self.extract_content(artist_id)

  def __str__(self):
    return self.name

  def print_card(self):
    print "Name      :    %s" % self.name
    print "Mana      :    %s" % self.mana
    print "CMC       :    %s" % self.cmc
    print "Types     :    %s" % self.types
    print "Text      :    %s" % self.text
    print "Flavor    :    %s" % self.flavor
    print "P/T       :    %s" % self.p_t
    print "Expansion :    %s" % self.expansion
    print "Rarity    :    %s" % self.rarity
    print "Card ID   :    %s" % self.card_id
    print "Artist    :    %s" % self.artist
    
  def extract_items(self,content_id):
    bs4content = self.soup.find(id=content_id)
    if bs4content != None:
      bs4value = bs4content.find('div',class_='value')
      return bs4value
    else:
      return
  
  # extracts and formats regular content with or without images
  def extract_content(self,content_id, delim = ' '):
    bs4content = self.extract_items(content_id)
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
  def extract_text(self,content_id):
    bs4content = self.extract_items(content_id)
    bs4strings = bs4content.stripped_strings
    return ' '.join(string for string in bs4strings).strip()
  
  # extracts mana values from contents
  def extract_mana(self,content_id):
    bs4content = self.extract_items(content_id)
    bs4images = bs4content.find_all('img')
    return ' '.join(image['alt'] for image in bs4images).strip()
  
