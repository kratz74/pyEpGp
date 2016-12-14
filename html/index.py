#!/usr/bin/python3

import boto3, botocore
import os, sys
import datetime

def enc_print(*strings):
    for string in strings:
        if type(string) == str:
            sys.stdout.buffer.write(string.encode('UTF-8'))
        else:
            sys.stdout.buffer.write(str(string).encode('UTF-8'))
    sys.stdout.buffer.write(b'\n')

enc_print("Content-Type: text/html; charset=utf-8")
enc_print()
enc_print('<!DOCTYPE html>')
enc_print('<html>')
enc_print('  <head>')
enc_print('    <meta charset="utf-8">')
enc_print('    <link rel="stylesheet" href="styles.css"/>')
enc_print('    <title>Guild EP/GP Status</title>')
enc_print('  </head>')
enc_print('  <body>')

dynamodb = boto3.resource('dynamodb', region_name="us-west-2",
    aws_access_key_id='epgp', aws_secret_access_key='EpGpAccessKey', endpoint_url="http://172.31.20.228:8000")

enc_print('    <h1>Guild EP/GP Status</h1>')

guildTab = dynamodb.Table('guild')
guildResp = guildTab.scan()
if 'Items' in guildResp:
    enc_print('    <h2>Guild info</h2>')
    guildItems = guildResp['Items']
    enc_print('    <table>')
    for item in guildItems:
        tsStr = datetime.datetime.fromtimestamp(int(item['timestamp'])).strftime('%d.%m.%Y %H:%M:%S')
        enc_print('     <tr>')
        enc_print('     <tr>')
        enc_print('      <th align="left">Name:</td>')
        enc_print('      <td align="left">', item['name'], '</td>')
        enc_print('     </tr>')
        enc_print('     <tr>')
        enc_print('      <th align="left">Realm:</td>')
        enc_print('      <td align="left">', item['realm'], ':', item['region'], '</td>')
        enc_print('     </tr>')
        enc_print('     <tr>')
        enc_print('      <th align="left">Min EP:</td>')
        enc_print('      <td align="left">', item['min_ep'], '</td>')
        enc_print('     </tr>')
        enc_print('     <tr>')
        enc_print('      <th align="left">Base GP:</td>')
        enc_print('      <td align="left">', item['base_gp'], '</td>')
        enc_print('     </tr>')
        enc_print('     <tr>')
        enc_print('      <th align="left">Decay [%]:</td>')
        enc_print('      <td align="left">', item['decay_p'], '</td>')
        enc_print('     </tr>')
        enc_print('     <tr>')
        enc_print('      <th align="left">Last Update:</td>')
        enc_print('      <td align="left">', tsStr, '</td>')
        enc_print('     </tr>')
    enc_print('    </table>')

enc_print('    <h2>Guild Characters</h2>')


enc_print('    <table>')
enc_print('     <tr>')
enc_print('      <th align="left">Character Name</td>')
enc_print('      <th align="left">Effort Points</td>')
enc_print('      <th align="left">Gear Points</td>')
enc_print('     </tr>')

charTab = dynamodb.Table('characters')
charResp = charTab.scan()
if 'Items' in charResp:
    charItems = charResp['Items']
    for item in charItems:
        enc_print('     <tr>')
        enc_print('       <td align="left">', item['name'], '</td>')
        enc_print('       <td align="left">', item['ep'], '</td>')
        enc_print('       <td align="left">', item['gp'], '</td>')
        enc_print('     </tr>')

enc_print('    </table>')

enc_print('    <h2>Loot Log</h2>')
enc_print('    <table>')
enc_print('     <tr>')
enc_print('      <th align="left">Date:</td>')
enc_print('      <th align="left">Name:</td>')
enc_print('      <th align="left">Item:</td>')
enc_print('      <th align="left">Gear Points:</td>')
enc_print('     </tr>')

lootTab = dynamodb.Table('loot')
lootResp = lootTab.scan()
if 'Items' in lootResp:
    lootItems = lootResp['Items']
    for item in lootItems:
        tsStr = datetime.datetime.fromtimestamp(int(item['timestamp'])).strftime('%d.%m.%Y %H:%M:%S')
        enc_print('     <tr>')
        enc_print('       <td align="left">', tsStr, '</td>')
        enc_print('       <td align="left">', item['name'], '</td>')
        enc_print('       <td align="left">', item['item'], '</td>')
        enc_print('       <td align="left">', item['gp'], '</td>')
        enc_print('     </tr>')

enc_print('    </table>')

enc_print('  </body>')
enc_print('</html>')
