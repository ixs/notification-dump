#!/usr/bin/env python3

""" MacOS Notification Database Dumper

This simple python script dumps all notification items from the MacOS Notification
database to stdout.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.

"""

__author__ = "Andreas Thienemann"
__copyright__ = "Copyright 2018-2019, Andreas Thienemann"

import sqlite3
from platform import mac_ver
from sqlite3 import Error
import subprocess
import os
import biplist
import pprint
import datetime


def mac_epoch_to_datetime(input):
  '''Returns a datetime object for a MacOS epoch timestamp'''
  epoch_base =  datetime.datetime.strptime("01-01-2001", "%m-%d-%Y")
  timedelta = datetime.timedelta(seconds=data['date'])
  return epoch_base + timedelta


darwin_user_dir = subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_DIR']).rstrip()
nc_db = os.path.join(darwin_user_dir, b'com.apple.notificationcenter/db2/db')

conn = sqlite3.connect(nc_db)
conn.row_factory = sqlite3.Row
cursor = conn.execute("SELECT data from record");

notifications = []

for row in cursor:
  plist = biplist.readPlistFromString(row[0])
  try:
    data = {'app': plist.get('app', 'Unknown'),
            'date': plist.get('date', plist['req'].get('trig', {}).get('date', 'Unknown')),
            'title': plist.get('req', {}).get('titl', 'None'),
            'body': plist.get('req', {}).get('body', 'None')}
  except KeyError:
    pprint.pprint(plist)
  data.update({'date': mac_epoch_to_datetime(data['date'])})
  notifications.append(data)

for n in notifications:
  print(n['date'].strftime('%x %X'), n['title'], n['body'][0:80].replace('\n', ' - ') + '...')
