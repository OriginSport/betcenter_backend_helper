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
from betcenter_backend_helper.dice.models import DiceRecord



def split_five(str):
    #split data into five parts,
    l = []
    if len(str)==322:
        a = str[2:66]
        b = str[66:130]
        c = str[130:194]
        d = str[194:258]
        e = str[258:322]

        a = int('0x'+a,16) #choice

        b = '0x' + b #reveal

        c = int('0x'+c,16) #result

        d = int('0x'+d,16) #amount

        e = int('0x'+e,16) #winAmount

        l = [a, b, c, d, e]

        return l

'''
def split_eight(str):
    # split data into eight parts,
    l = []
    if len(str) == 514:
        a = str[2:66]
        b = str[66:130]
        c = str[130:194]
        d = str[194:258]
        e = str[258:322]
        f = str[322:386]
        g = str[386:450]
        h = str[450:514]

        a = int('0x' + a, 16)  #

        b = int('0x' + b, 16)  #

        c = int('0x' + c, 16)  #

        d = int('0x' + d, 16)  #

        e = int('0x' + e, 16)  #

        l = [a, b, c, d, e]

        return l
'''

def data(network_id):
    for i in range(0,1):
        for y in range(0,1):
            if network_id==1:
                main_contract_txhash = ''
                contract_url = ''
            elif network_id==3:
                main_contract_txhash = '0xd43bee68a9ae0ca71257bdddd8ff89a836f57e95'
                contract_url ='https://api-ropsten.etherscan.io/api?module=logs&action=getLogs&fromBlock=379224&toBlock=latest&address=0xd43bee68a9ae0ca71257bdddd8ff89a836f57e95&topic0=0x0b69c882106d473936244e69933a842887f623d0eb2bb247dcb75215d461bd7b'
                address_to = '0xD43BeE68A9ae0ca71257BdddD8ff89a836f57e95'
            if contract_url:
                r = requests.get(contract_url, timeout=30)
                if r.status_code == 200:
                    if r.json():
                        data = r.json()
                        status = data.get('status')
                        message = data.get('message')

                        tx_hash_list = []

                        if status == '1':
                            if message == 'OK':
                                result = data.get('result')

                                for x in result:
                                    hash = x.get('transactionHash')

                                    tx_hash_list.append(hash)

                                    data = x.get('data')

                                    if len(data)==322:
                                        l = split_five(data)

                                        choice = l[0]
                                        reveal = l[1]
                                        result = l[2]
                                        amount = int(l[3])
                                        jackpot_payment = int(l[4]) #winamount

                                    timestamp = int(x.get('timeStamp'),16)
                                    time_ = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))

                                    modulo = int(x.get('topics')[2], 16)

                                    address_from = '0x' + x.get('topics')[1][26:]

                                    print(address_from, hash, modulo, time_, timestamp, choice, reveal, result, amount, jackpot_payment, type(amount), type(jackpot_payment))

                                    if DiceRecord.objects.filter(tx_hash=hash):
                                        DiceRecord.objects.filter(tx_hash=hash).update(network_id=3, choice=choice, result=result, reveal=reveal,
                                        main_contract_txhash=main_contract_txhash, address_to=address_to,
                                        address_from=address_from, time=time_, time_stamp=timestamp, modulo=modulo,
                                        jackpot_payment=jackpot_payment, amount=amount)
                                        print('22222222222222222222222')
                                    else:
                                        DiceRecord.objects.create(network_id=3, choice=choice, result=result, reveal=reveal,
                                        tx_hash=hash, main_contract_txhash=main_contract_txhash, address_to=address_to,
                                        address_from=address_from)

                                    '''
                                    if network_id==1:
                                        tx_url = ''
                                    elif network_id==3:
                                        tx_url = 'https://api.infura.io/v1/jsonrpc/ropsten/eth_getTransactionReceipt?params=[%22%s%22]' %hash

                                    if tx_url:
                                        r = requests.get(tx_url, timeout=30)
                                        if r.status_code == 200:
                                            if r.json():
                                                data = r.json()
                                                data = data['result']
                                                
                                    '''




data(3)









































