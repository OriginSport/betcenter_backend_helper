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


def split_three(str):
    #split data into three parts,
    l = []
    if len(str)==194:
        a = str[2:66]
        b = str[66:130]
        c = str[130:194]

        a = int('0x'+a,16) #math.pow(10,18)

        b = '0x' + b[24:]
        l = [a, b, c]

        return l


def num(x, y):
    return 10*x + y


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
        
        if str_l:
            game_id = reduce(num, str_l)
        else:
            game_id=''
        return game_id




def data():
    #找合约地址,合约不常变

    #contract_list = ['0x35BAB7165A301E99c75C3e59B48817856b4D5e5c']
    # 0xF70e44e803e66C40890AC4875E5036fDb55b5E81    06-22新合约地址

    contract_list = ['0xF70e44e803e66C40890AC4875E5036fDb55b5E81']

    for contract in contract_list:
        #url = 'http://api.etherscan.io/api?module=account&action=txlist&address=0xF70e44e803e66C40890AC4875E5036fDb55b5E81&startblock=0&endblock=99999999&sort=asc&apikey=YourApiKeyToken'
        url = 'https://api.etherscan.io/api?module=logs&action=getLogs&fromBlock=379224&toBlock=latest&address=0xF70e44e803e66C40890AC4875E5036fDb55b5E81'
        if url:
            r = requests.get(url, timeout=30)
            if r.status_code == 200:
                if r.json():
                    data = r.json()
                    status = data.get('status')
                    message = data.get('message')

                    tx_hash_list = []

                    tx_hash_game_id_dic = {}
                    if status=='1':
                        if message=='OK':
                            result = data.get('result')

                            for x in result:

                                #hash = x.get('hash')
                                hash = x.get('transactionHash')

                                tx_hash_list.append(hash)

                                data = x.get('data')


                                if data:

                                    if len(data) == 194:
                                        l = split_three(data)

                                        eth = l[0]
                                        addr = l[1]

                                        game_id = get_game_id(l[2])

                                        print('eth addr game_id*******************************************')
                                        print('eth',eth,'addr',addr,'game_id',game_id)

                                        tx_hash_game_id_dic.update({hash:game_id})
        print(tx_hash_list)
        contract_address_list = []

        contract_game_id_dic = {}
        main_contract_tx_contract_dic = {}

        for tx in tx_hash_list:
            new_url = 'https://api.etherscan.io/api?module=account&action=txlistinternal&txhash=%s&apikey=YourApiKeyToken' %tx

            if new_url:
                r = requests.get(new_url, timeout=50)
                if r.status_code == 200:
                    if r.json():
                        data = r.json()
                        status = data.get('status')
                        message = data.get('message')


                        if status == '1':
                            if message == 'OK':
                                result = data.get('result')

                                contract_address = result[0].get('contractAddress')
                                contract_address_list.append(contract_address)
                                contract_game_id_dic.update({contract_address:tx_hash_game_id_dic.get(tx)})
                                main_contract_tx_contract_dic.update({contract_address:tx})

        print('contract_address_list','======================')
        print(main_contract_tx_contract_dic)
        print(contract_address_list)
        for addr in contract_address_list:
            url = 'http://api.etherscan.io/api?module=account&action=txlist&address=%s&startblock=0&endblock=99999999&sort=asc&apikey=YourApiKeyToken' %addr
            if url:
                r = requests.get(url, timeout=30)
                if r.status_code == 200:
                    if r.json():
                        data = r.json()
                        status = data.get('status')
                        message = data.get('message')

                        if status == '1':
                            if message == 'OK':
                                result = data.get('result')

                                for x in result:

                                    address = x.get('from')
                                    to = x.get('to')
                                    value = x.get('value')
                                    block = x.get('blockNumber')
                                    tx_hash = x.get('hash')
                                    time_stamp = int(x.get('timeStamp'))

                                    time_datetime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time_stamp))
                                    #cn_time to utc_time

                                    date_time = datetime.datetime.strptime(time_datetime, '%Y-%m-%d %H:%M:%S')
                                    utc_time = date_time - datetime.timedelta(hours=8)
                                    utc_str = utc_time.strftime('%Y-%m-%d %H:%M:%S')

                                    value = int(value)/math.pow(10,18)
                                    game_id = contract_game_id_dic.get(addr)
                                    #print(utc_str)

                                    main_contract_txhash = main_contract_tx_contract_dic.get(addr)

                                    print('tx_hash',tx_hash,'address',address,'to',to,'value',value)
                                    print('contract',addr, 'game_id', game_id)
                                    print('main_contract_txhash',main_contract_tx_contract_dic.get(addr))

                                    input_url = 'https://www.etherchain.org/api/tx/%s' % tx_hash
                                    if input_url:
                                        r = requests.get(input_url, timeout=30)
                                        if r.status_code == 200:
                                            if r.json():
                                                data = r.json()
                                                data = data[0]
                                                input = data.get('input')
                                                if len(input) > 64:
                                                    input = input[-64:]
                                                    choice = int('0x' + input, 16)

                                                else:
                                                    choice = ''
                                    print('choice', choice)


                                    try:
                                        if value>0:
                                            if game_id:
                                                if BetRecord.objects.filter(tx_hash=tx_hash, address=address, to=to):
                                                    BetRecord.objects.filter(tx_hash=tx_hash, address=address, to=to).update(category='world_cup',
                                                    contract=addr,time_stamp=time_stamp,time=utc_str,game_id=game_id,
                                                    main_contract_txhash=main_contract_txhash, choice=choice)
                                                else:
                                                    BetRecord.objects.create(tx_hash=tx_hash,address=address, to=to, time=utc_str,
                                                    quantity=value,game_id=game_id, contract=addr,time_stamp=time_stamp,
                                                    main_contract_txhash=main_contract_txhash, choice=choice)


                                    except:
                                        pass







data()
