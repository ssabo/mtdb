#!/usr/bin/env python2.7

from Card import *
import _mysql
import random
import time
import threading

db = _mysql.connect('localhost', 'shaun', 'password', 'mtdb')

threads = 5
print_lines_mod = 100
start = 1

working_list = []

def add_card(item_id,tmp):
  card = Card(item_id, db)
  if not card.name == '':
    card.save_card()
  working_list.remove(item_id)

for item_id in range(start, 10000000):
  submitable = False
  while not submitable:
    if len(working_list) >= threads:
      continue
    else:
      submitable = True
  if item_id % 300 == 0:
    while len(working_list) !=0:
      continue
    db = _mysql.connect('localhost', 'shaun', 'password', 'mtdb')

  if item_id % print_lines_mod == 0:
    print "%04d-%02d-%02dT%02d:%02d:%02d - %s" % (time.localtime().tm_year,
      time.localtime().tm_mon,
      time.localtime().tm_mday,
      time.localtime().tm_hour,
      time.localtime().tm_min,
      time.localtime().tm_sec, item_id)
  tmp = 1
  t = threading.Thread(target=add_card, args=(item_id,tmp))
  working_list.append(item_id)
  t.start()
