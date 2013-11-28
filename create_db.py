#!/usr/bin/env python2.7

import _mysql

print "*******Creating Table*******"

db = _mysql.connect('localhost', 'shaun', 'password', 'mtdb')

create_db = """
CREATE TABLE cards (
  ID         INT NOT NULL AUTO_INCREMENT,
  name       VARCHAR(100) NOT NULL,
  mana       VARCHAR(100),
  cmc        INT,
  types      VARCHAR(100),
  text       VARCHAR(256),
  flavor     VARCHAR(256),
  power      VARCHAR(4),
  toughness  VARCHAR(4),
  expansion  VARCHAR(100),
  rarity     VARCHAR(36),
  artist     VARCHAR(100),
  PRIMARY KEY (ID)
)"""

db.query(create_db)
print create_db

