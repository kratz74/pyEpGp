#!/usr/bin/python3

import boto3, botocore
import os, sys

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
enc_print('    <title>List of Players</title>')
enc_print('  </head>')
enc_print('  <body>')
enc_print('    <h1>Guild Characters</h1>')

dynamodb = boto3.resource('dynamodb', region_name="us-west-2",
    aws_access_key_id='epgp', aws_secret_access_key='EpGpAccessKey', endpoint_url="http://172.31.20.228:8000")

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

enc_print('  </body>')
enc_print('</html>')
