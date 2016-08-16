#!/usr/bin/env python

import argparse
import time
import json
from selenium import webdriver

# parse args
description = 'Bulk Export Activity from Garmin Connect'
epilog = ('*Original activity files (.fit) are downloaded from each '
          'activity page in the range from `first` to `last`.')
parser = argparse.ArgumentParser(description=description, epilog=epilog)

parser.add_argument('username', help='Garmin account username')
parser.add_argument('password', help='Garmin account password')
parser.add_argument('first', type=int, help='first activity page*')
parser.add_argument('last', type=int, help='last activity page*')
parser.add_argument('-v', action='version', version='%(prog)s 0.1')
args = parser.parse_args()

first = args.first
last = args.last
usr = args.username
pwd = args.password

login_url = ("https://sso.garmin.com/sso/login?"
             "service=https%3A%2F%2Fconnect.garmin.com%2Fpost-auth%2Flogin&amp;"
             "source=https%3A%2F%2Fconnect.garmin.com%2Fen-US%2Fsignin&amp;"
             "redirectAfterAccountLoginUrl=https%3A%2F%2Fconnect.garmin.com%2F"
             "post-auth%2Flogin&amp")
json_url = ("https://connect.garmin.com/proxy/activity-search-service-1.0/json/"
            "activities?currentPage={}")
download_url = ("https://connect.garmin.com/modern/proxy/download-service/"
                "files/activity/{}")

driver = webdriver.Chrome()
driver.get(login_url)

usr_box = driver.find_element_by_id('username')
pwd_box = driver.find_element_by_id('password')
login_btn = driver.find_element_by_id('login-btn-signin')

usr_box.send_keys(usr)
pwd_box.send_keys(pwd)
login_btn.click()

pages = []
for i in range(first, last + 1):
  print('Parsing page: {}'.format(i))
  driver.get(json_url.format(i))
  body = driver.find_element_by_tag_name('body')
  pages.append(json.loads(body.get_attribute('textContent')))
  time.sleep(3)

act_ids = []
for page in pages:
  for activity in page['results']['activities']:
    act_ids.append(activity['activity']['activityId'])

downloads = [download_url.format(act_id) for act_id in act_ids]

for i, download in enumerate(downloads):
  print('Downloading activity: {}'.format(act_ids[i]))
  driver.get(download)
  time.sleep(3)

driver.quit()
