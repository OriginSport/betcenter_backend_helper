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

from betcenter_backend_helper.dice.models import Refund


def split_data(str):
    #split data
    l = []
    if len(str)==66:
        amount = str[2:66]
        amount = int('0x' + amount,16) #amount

        l = [amount]

        return l


def data(network_id):

    contract_config = {
        1: {
            'address': ['0x5085c5356129ee11bffb523e3166d7153ac13c75'],
            'url': 'https://api.etherscan.io/api?module=logs&action=getLogs&fromBlock=6578592&toBlock=latest&address=%s&topic0=%s'
        },
        3: {
            'address': ['0xd43bee68a9ae0ca71257bdddd8ff89a836f57e95', '0x7bcf2c682d8e5dd9ca9ad046e3a431ccbf03a76a'],
            'url': 'https://api-ropsten.etherscan.io/api?module=logs&action=getLogs&fromBlock=379224&toBlock=latest&address=%s&topic0=%s'
        }
    }
    addresses = contract_config[network_id]['address']

    topic0 = '0xb6c0eca8138e097d71e2dd31e19a1266487f0553f170b7260ffe68bcbe9ff8a7'
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

                        if len(data) == 66:
                            l = split_data(data)
                            amount = l[0]


                        timestamp = int(x.get('timeStamp'), 16)
                        time_ = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
                        address_from = '0x' + x.get('topics')[1][26:]

                        print(network_id, address_from, time_, timestamp, amount, contract_address, address_to)

                        if Refund.objects.filter(transactionHash=transactionHash):
                            pass

                            

                        else:
                            Refund.objects.create(transactionHash=transactionHash, network_id=network_id,
                                                      contract_address=contract_address,
                                                      address_to=address_to, address_from=address_from, time=time_,
                                                      time_stamp=timestamp, amount=amount)





if __name__ == "__main__":
    data(1)
    data(3)






































