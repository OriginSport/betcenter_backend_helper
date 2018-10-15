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
        choice = str[2:66]
        reveal = str[66:130]
        result = str[130:194]
        amount = str[194:258]
        win_amount = str[258:322]
        choice = int('0x' + choice,16) #choice
        reveal = '0x' + reveal #reveal
        result = int('0x' + result,16) #result
        amount = int('0x' + amount,16) #amount
        win_amount = int('0x' + win_amount,16) #winAmount
        l = [choice, reveal, result, amount, win_amount]

        return l


def data(network_id):

    contract_config = {
        1: {
            'address': ['0x5085c5356129ee11bffb523e3166d7153ac13c75'],
            'url': 'https://api.etherscan.io/api?module=logs&action=getLogs&fromBlock=379224&toBlock=latest&address=%s&topic0=%s'
        },
        3: {
            'address': ['0xd43bee68a9ae0ca71257bdddd8ff89a836f57e95', '0x7bcf2c682d8e5dd9ca9ad046e3a431ccbf03a76a'],
            'url': 'https://api-ropsten.etherscan.io/api?module=logs&action=getLogs&fromBlock=379224&toBlock=latest&address=%s&topic0=%s'
        }
    }
    addresses = contract_config[network_id]['address']

    topic0 = '0x0b69c882106d473936244e69933a842887f623d0eb2bb247dcb75215d461bd7b'
    for address in addresses:
        url = contract_config[network_id]['url'] % (address, topic0)
        address_to = address
        contract_address = address

        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            if r.json():
                data = r.json()
                status = data.get('status')
                message = data.get('message')

                if status == '1' and message == 'OK':
                    result = data.get('result')
                    for x in result:
                        transactionHash = x.get('transactionHash')
                        data = x.get('data')

                        if len(data) == 322:
                            l = split_five(data)
                            choice = l[0]
                            reveal = l[1]
                            result = l[2]
                            amount = l[3]
                            jackpot_payment = l[4]  # win_amount

                        timestamp = int(x.get('timeStamp'), 16)
                        time_ = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
                        modulo = int(x.get('topics')[2], 16)
                        address_from = '0x' + x.get('topics')[1][26:]

                        print(network_id, choice, result, reveal, address_to, time_, timestamp, modulo, jackpot_payment, amount)

                        if DiceRecord.objects.filter(transactionHash=transactionHash):
                            pass

                            '''
                            DiceRecord.objects.filter(transactionHash=transactionHash).update(network_id=network_id, choice=choice,
                                                                              result=result, reveal=reveal,
                                                                              contract_address=contract_address,
                                                                              address_to=address_to,
                                                                              address_from=address_from, time=time_,
                                                                              time_stamp=timestamp,
                                                                              modulo=modulo,
                                                                              jackpot_payment=jackpot_payment,
                                                                              amount=amount)
                            '''

                        else:
                            DiceRecord.objects.create(transactionHash=transactionHash, network_id=network_id, choice=choice,
                                                      result=result, reveal=reveal,
                                                      contract_address=contract_address,
                                                      address_to=address_to, address_from=address_from, time=time_,
                                                      time_stamp=timestamp,
                                                      modulo=modulo, jackpot_payment=jackpot_payment, amount=amount)





if __name__ == "__main__":
    data(1)
    data(3)






































