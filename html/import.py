#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from __future__ import print_function 
import cgi, cgitb
import json
import io
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

def open_table(db, name):
    table = db.Table(name)
    try:
        crTs = table.creation_date_time
        charactersMissing = False
    except botocore.exceptions.ClientError:
        charactersMissing = True
    if charactersMissing == True:
        table = dynamodb.create_table(
            TableName=name,
            KeySchema=[{'AttributeName': 'name', 'KeyType': 'HASH'}],
            AttributeDefinitions=[
                {'AttributeName': 'name', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            })
    return table

def open_loot_table(db, name):
    table = db.Table(name)
    #table.delete()
    try:
        crTs = table.creation_date_time
        charactersMissing = False
    except botocore.exceptions.ClientError:
        charactersMissing = True
    if charactersMissing == True:
        table = dynamodb.create_table(
            TableName=name,
            KeySchema=[{'AttributeName': 'name', 'KeyType': 'HASH'},
                {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}],
            AttributeDefinitions=[
                {'AttributeName': 'name', 'AttributeType': 'S'},
                {'AttributeName': 'timestamp', 'AttributeType': 'N'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            })
    return table

cgitb.enable()

enc_print("Content-Type: text/html; charset=utf-8")
enc_print()
enc_print('<!DOCTYPE html>')
enc_print('<html>')
enc_print('  <head>')
enc_print('    <meta charset="utf-8">')
enc_print('    <link rel="stylesheet" href="styles.css"/>')
enc_print('    <title>EP/GP Addon Data Import Log</title>')
enc_print('  </head>')
enc_print('  <body>')

#enc_print(os.environ)
#boto3.set_stream_logger('botocore', level='DEBUG')

# AWS http://54.200.238.145:8000
# Google http://db:8000
dynamodb = boto3.resource('dynamodb', region_name="us-west-2",
    aws_access_key_id='epgp', aws_secret_access_key='EpGpAccessKey', endpoint_url="http://db:8000")

guildTab = open_table(dynamodb, 'guild')
lootTab = open_loot_table(dynamodb, 'loot')
charTab = open_table(dynamodb, 'characters')

form = cgi.FieldStorage()
fileitem = form["data"]
if not fileitem.file:
    enc_print('Form data is not file!')

reader = io.BufferedReader(fileitem.file)
wrapper = io.TextIOWrapper(reader)

data = json.load(wrapper)

guildTab.put_item(Item={
    'name': data['guild'], 'realm': data['realm'], 'region': data['region'],
    'min_ep': data['min_ep'], 'base_gp': data['base_gp'], 'decay_p': data['decay_p'],
    'extras_p': data['extras_p'], 'timestamp': data['timestamp']})

enc_print('    <h1>EP/GP Addon Data Import Log</h1>')
enc_print('    <h2>Stored Guild</h2>')
enc_print('    <table>')
enc_print('     <tr>')
enc_print('      <th align="left">Name</td>')
enc_print('      <td align="left">', data['guild'], '</td>')
enc_print('     </tr>')
enc_print('     <tr>')
enc_print('      <th align="left">Realm</td>')
enc_print('      <td align="left">', data['realm'], ':', data['region'], '</td>')
enc_print('     </tr>')
enc_print('     <tr>')
enc_print('      <th align="left">Min EP</td>')
enc_print('      <td align="left">', data['min_ep'], '</td>')
enc_print('     </tr>')
enc_print('     <tr>')
enc_print('      <th align="left">Base GP</td>')
enc_print('      <td align="left">', data['base_gp'], '</td>')
enc_print('     </tr>')
enc_print('     <tr>')
enc_print('      <th align="left">Decay [%]</td>')
enc_print('      <td align="left">', data['decay_p'], '</td>')
enc_print('     </tr>')
enc_print('    </table>')

enc_print('    <h2>Stored Characters</h2>')
enc_print('    <table>')
enc_print('     <tr>')
enc_print('      <th align="left">Character Name</td>')
enc_print('      <th align="left">Effort Points</td>')
enc_print('      <th align="left">Gear Points</td>')
enc_print('     </tr>')
for person in data['roster']:
    charTab.put_item(Item={'name': person[0], 'guild': data['guild'], 'ep': person[1], 'gp': person[2]})
    enc_print('     <tr>')
    enc_print('       <td align="left">', person[0], '</td>')
    enc_print('       <td align="left">', person[1], '</td>')
    enc_print('       <td align="left">', person[2], '</td>')
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
for loot in data['loot']:
    lootTab.put_item(Item={'name': loot[1], 'item': loot[2], 'gp': loot[3], 'timestamp': loot[0]})
    tsStr = datetime.datetime.fromtimestamp(int(loot[0])).strftime('%d.%m.%Y %H:%M:%S')
    enc_print('     <tr>')
    enc_print('       <td align="left">', tsStr, '</td>')
    enc_print('       <td align="left">', loot[1], '</td>')
    enc_print('       <td align="left">', loot[2], '</td>')
    enc_print('       <td align="left">', loot[3], '</td>') 
    enc_print('     </tr>')

enc_print('    </table>')

enc_print('  </body>')
enc_print('</html>')
