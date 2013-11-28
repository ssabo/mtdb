#!/usr/bin/env python2.7

import _mysql

print "*******Creating Table*******"

db = _mysql.connect('localhost', 'shaun', 'password', 'mtdb')

create_db = """
CREATE TABLE cards (
  ID    INT NOT NULL AUTO_INCREMENT,
  name  VARCHAR(100) NOT NULL,
  text  VARCHAR(256),
  PRIMARY KEY (ID)
)"""

db.query(create_db)

