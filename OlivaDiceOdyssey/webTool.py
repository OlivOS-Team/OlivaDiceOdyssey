# -*- encoding: utf-8 -*-
'''
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/   
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___   
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/   

@File      :   webTool.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2022, OlivOS-Team
@Desc      :   None
'''

import OlivaDiceCore
import OlivaDiceOdyssey

import requests as req
from urllib.parse import urlencode
import json
import time
import threading

def getCnmodsReq(title = None, page = None):
    res = None
    tmp_res = None
    tmp_value = {}
    send_url = OlivaDiceOdyssey.cnmodsData.strCnmodsMain
    if title != None:
        tmp_value['title'] = str(title)
    if page != None:
        tmp_value['page'] = str(page)
    if title != None or page != None:
        send_url += '?' + urlencode(tmp_value)
    headers = {
        'User-Agent': OlivaDiceCore.data.bot_version_short_header
    }
    msg_res = req.request("GET", send_url, headers = headers, proxies = OlivaDiceCore.webTool.get_system_proxy())
    res_text = str(msg_res.text)
    try:
        tmp_res = json.loads(res_text)
        res = tmp_res
    except:
        pass
    return res

def getRulesReq(key:'str|None' = None, page = None, item_max = None):
    res = None
    tmp_res = None
    tmp_value = {}
    send_url = OlivaDiceOdyssey.cnmodsData.strRulesMain
    if key != None:
        tmp_value['key'] = str('%'.join(key))
    if page != None:
        tmp_value['page'] = str(page)
    if item_max != None:
        tmp_value['item_max'] = str(item_max)
    if key != None:
        send_url += '?' + urlencode(tmp_value)
    headers = {
        'User-Agent': OlivaDiceCore.data.bot_version_short_header
    }
    try:
        msg_res = req.request("GET", send_url, headers = headers, proxies = OlivaDiceCore.webTool.get_system_proxy())
        res_text = str(msg_res.text)
        tmp_res = json.loads(res_text)
        res = tmp_res
    except:
        pass
    return res


def sendKOOKBotMarketPulse(token:str):
    res = None
    tmp_res = None
    send_url = 'http://bot.gekj.net/api/v1/online.bot'
    headers = {
        'uuid': token,
        'User-Agent': OlivaDiceCore.data.bot_version_short_header
    }
    msg_res = req.request("GET", send_url, headers = headers, proxies = OlivaDiceCore.webTool.get_system_proxy())
    res_text = str(msg_res.text)
    try:
        tmp_res = json.loads(res_text)
        res = tmp_res
    except:
        pass
    return res



def sendKOOKBotMarketPulseThread(botDict:dict):
    dictTimerCount = {}
    checkF = 5
    while True:
        for botHash in botDict:
            flag_odysseyKOOKBotMarketPulseEnable = OlivaDiceCore.console.getConsoleSwitchByHash(
                'odysseyKOOKBotMarketPulseEnable',
                botHash
            )
            dictTimerCount.setdefault(botHash, 0)
            if 1 == flag_odysseyKOOKBotMarketPulseEnable \
            and botHash in OlivaDiceCore.msgCustom.dictStrCustomDict:
                dictStrCustom:dict = OlivaDiceCore.msgCustom.dictStrCustomDict[botHash]
                token_this = dictStrCustom.get('strOdysseyKOOKBotMarketPulseUUID', '-')
                if '-' != token_this:
                    if(dictTimerCount[botHash] <= 0):
                        res = OlivaDiceOdyssey.webTool.sendKOOKBotMarketPulse(token = token_this)
                        if res is not None:
                            dictTimerCount[botHash] = int(15 * 60)
                            OlivaDiceCore.msgReply.globalLog(
                                2,
                                'KOOK机器人服务平台心跳上报成功！',
                                [('OlivaDice', 'default'), ('KOOKBotMarket', 'default')]
                            )
                        else:
                            dictTimerCount[botHash] = 0
                            OlivaDiceCore.msgReply.globalLog(
                                3,
                                'KOOK机器人服务平台心跳上报失败！',
                                [('OlivaDice', 'default'), ('KOOKBotMarket', 'default')]
                            )
                    dictTimerCount[botHash] -= checkF
                else:
                    dictTimerCount[botHash] = 0
            else:
                dictTimerCount[botHash] = 0
        time.sleep(checkF)

def initKOOKBotMarketPulseThread(botDict:dict):
    threading.Thread(
        target = OlivaDiceOdyssey.webTool.sendKOOKBotMarketPulseThread,
        args = (botDict, )
    ).start()
