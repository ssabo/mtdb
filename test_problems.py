#!/usr/bin/env python2.7

from Card import *
import _mysql

db = _mysql.connect('localhost', 'shaun', 'password', 'mtdb')

print "-------------------------------"
cards = [Card('31790',db),
         Card('10677',db),
         Card('366416',db),
         Card('154408',db),
         Card('28669',db),
         Card('4957',db)]
for card in cards:
  card.print_card()
  card.save_card()
  print "-------------------------------"

