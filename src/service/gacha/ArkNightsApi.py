from functools import lru_cache
import json
from typing import Dict, Tuple

import requests

from .model import *

def basic(token: str) -> Doctor:
    data = json.dumps({
        "appId": 1,
        "channelMasterId": 1,
        "channelToken": {
            "token": token
        }
    })
    with requests.post('https://as.hypergryph.com/u8/user/info/v1/basic', data=data) as response:
        obj = json.loads(response.text)
        obj = obj['data']
        return Doctor(token=token,**obj)


paths = ["gacha", "diamond", "recent"]
def recent(token: str, page: int):
    with requests.post("https://as.hypergryph.com/u8/pay/v1/recent", json.dumps({
        "appId": 1,
        "channelMasterId": 1,
        "channelToken": {
            "token": token,
        }
    })) as response:
        res_json = json.loads(response.text)
        try:
            return res_json['data']
        except KeyError:
            print((token, page, res_json))
            return []


def inquiry(token: str, page: int, path: str = "gacha"):
    if path == "recent":
        return recent(token=token, page=page)
    params = {
        'token': token,
        'page': page
    }
    try:
        with requests.get(f'https://ak.hypergryph.com/user/api/inquiry/{path}', params=params) as response:
            res_json = json.loads(response.text)
            return res_json['data']['list']
    except KeyError:
        print((token, page, response.text))
    except requests.exceptions.ChunkedEncodingError:
        print((token, page, response.text))
    except json.decoder.JSONDecodeError:
        print((token, page, response.text))
    return []

def inquiry2iter(token: str, path: str = "gacha"):
    for page in range(1, 11):
        gs = inquiry(token=token, page=page, path=path)
        for g in gs:
            try:
                if 'payTime' in g.keys():
                    g['ts'] = g['payTime']
            except AttributeError as e:
                print({
                    'function:': f'inquiry2iter(token: str = {token}, path: str = {path}):',
                    'e': e,
                    'g': g,
                    'type(g)': type(g),
                })
                return
            yield g
        if len(gs) != 10:
            break

def __gacha(token:str, page:int, doctor: Doctor=None)->Tuple[List[Gacha],bool]:
    '''
    token
    page 1~10
    uid for build a object
    :return gachas hasNext
    '''
    if not doctor:
        doctor = basic(token)
    with requests.get(url="https://ak.hypergryph.com/user/api/inquiry/gacha", params={
        'token': token,
        'page': page,
        'channelId': 1,
    }) as response:
        dic = json.loads(response.text)
        data = dic['data']
        gachas = [Gacha(uid=doctor.uid,**gacha) for gacha in data['list']]
        pagination:Dict = data['pagination']
        return gachas, (pagination['current']*10<pagination['total'])


def gachaiter(token:str, doctor:Doctor=None):
    if not doctor:
        doctor = basic(token)
    for page in range(1,11):
        gachas,hasNext = __gacha(token=token,page=page,doctor=doctor)
        for gacha in gachas:yield gacha
        if not hasNext:break



if __name__ == '__main__':
    t = "nehYrmDhGg+kArnCb/YbXjmF"
    #
    for gacha in gachaiter(t):
        print(gacha)
    # print(diamond("qe/AxGCo1//WCzsOKZ18bD8C", 1))
    # for d in inquiry2iter(t, "recent"):
    #     print(d)

    