# coding=utf-8
import requests
from bs4 import BeautifulSoup
import re
import os
import time
import sys
import io
import datetime
import time
import math
from functools import reduce


abs_path = os.path.abspath(__file__)
project_path = '/'.join(abs_path.split('/')[:-3])
sys.path.insert(0, project_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "betcenter_backend_helper.settings")
import django
django.setup()

from betcenter_backend_helper.bet.models import BetItem
from betcenter_backend_helper.bet_record.models import BetRecord
from betcenter_backend_helper.bet_detail.models import BetDetail



def fun(str):
    if len(str)==64:
        return int('0x'+str,16)


def num(x, y):
    return 10*x + y

def str_category(b):
    if len(b)==64:
        l = []
        for i in range(0,60):
            if b[i]==b[i+1]==b[i+2]:
                l.append(i)

        if l[0]%2==0:
            b = b[0:l[0]]

        else:

            b = b[0:l[1]]

        L = []
        for x in range(int(len(b) / 2)):
            L.append(b[2 * x:2 * x + 2])

        str_l = []

        for x in L:
            m_ = int('0x' + x, 16)
            str_l.append(chr(m_))

        category = ''
        for x in str_l:
            category = category + x


        return category


def get_game_id(b):
    if len(b)==64:
        l = []
        for i in range(0,60):
            if b[i]==b[i+1]==b[i+2]:
                l.append(i)

        if l[0]%2==0:
            b = b[0:l[0]]

        else:

            b = b[0:l[1]]
        L = []
        for x in range(int(len(b) / 2)):
            L.append(b[2 * x:2 * x + 2])

        str_l = []

        for x in L:
            m_ = int('0x' + x, 16)
            str_l.append(chr(m_))


        for i in range(len(str_l)):
            str_l[i] = int(str_l[i])

        game_id = reduce(num, str_l)
        return game_id



def data():
    tx_hash_list = []
    con_url = 'https://api.etherscan.io/api?module=logs&action=getLogs&fromBlock=379224&toBlock=latest&address=0xF70e44e803e66C40890AC4875E5036fDb55b5E81'
    if con_url:
        r = requests.get(con_url, timeout=30)
        if r.status_code == 200:
            if r.json():
                data = r.json()
                data = data['result']
                for x in data:
                    
                    tx_hash_list.append(x.get('transactionHash'))


    #tx_hash_list = ['https://www.etherchain.org/api/tx/0x0dba00f8ed18aa78ab6ea65301fdfafac46ed26fe46094a0763e584c2c2b50de']
    for tx in tx_hash_list:
        url = 'https://www.etherchain.org/api/tx/%s'%tx
        print(url)
        if url:
            r = requests.get(url, timeout=30)
            if r.status_code == 200:
                if r.json():
                    data = r.json()

                    for x in data:
                        if x.get('type')=='tx':
                            if len(x.get('input'))>630:
                                a = x.get('input')
                                b9 = a[-64:]
                                b8 = a[-128:-64]
                                b7 = a[-192:-128]
                                b6 = a[-256:-192]
                                b5 = a[-320:-256]
                                b4 = a[-384:-320]
                                b3 = a[-448:-384]
                                b2 = a[-512:-448]
                                b1 = a[-576:-512]
                                b0 = a[-640:-576]

                                print(b0,b1,b2,b3,b4,b5,b6,b7,b8,b9)

                                creater_address = '0x' + x.get('from')
                                creater_address = creater_address if len(creater_address)>40 else ''

                                new_url = 'https://api.etherscan.io/api?module=account&action=txlistinternal&txhash=%s&apikey=YourApiKeyToken' %tx
                                if new_url:
                                    r = requests.get(new_url, timeout=30)
                                    if r.status_code == 200:
                                        if r.json():
                                            data = r.json()
                                            status = data.get('status')
                                            message = data.get('message')

                                            if status == '1':
                                                if message == 'OK':
                                                    result = data.get('result')
                                                    contract_address = result[0].get('contractAddress')
                                
                                try:
                                    category = str_category(b0)
                                    game_id = get_game_id(b1)
                                    minimumbet = fun(b2)
                                    spread = fun(b3)
                                    left_odds = fun(b4)
                                    middle_odds = fun(b5)
                                    right_odds = fun(b6)
                                    flag = fun(b7)
                                    starttime = fun(b8)
                                    confirmations = fun(b9)


                                    print(category,game_id,minimumbet,spread,left_odds,middle_odds,right_odds,flag,starttime,confirmations, contract_address)
                                
                                    if BetDetail.objects.filter(tx_hash=tx):
                                        BetDetail.objects.filter(tx_hash=tx).update(creater_address=creater_address,contract=contract_address)
                                    else:
                                        BetDetail.objects.create(tx_hash=tx,category=category,game_id=game_id,minimumbet=minimumbet,
                                                             spread=spread,left_odds=left_odds,middle_odds=middle_odds,
                                                             right_odds=right_odds,flag=flag,time_stamp=starttime,
                                                             confirmations=confirmations,creater_address=creater_address,contract=contract_address)
                                


                                except:
                                    pass


                                        
                                        

                                        
                                        
                                        
                                        
                                        
                                        
data()
