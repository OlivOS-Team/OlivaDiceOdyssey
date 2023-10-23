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

import OlivOS
import OlivaDiceCore
import OlivaDiceOdyssey

import requests as req
from urllib.parse import urlencode
import json
import time
import threading
import hashlib
import os

gExtiverseDeck = {}

def getExtiverseDeckRemote():
    global gExtiverseDeck
    res = None
    tmp_res = None
    send_url = OlivaDiceOdyssey.cnmodsData.strExtiverseDeckMain
    headers = {
        'User-Agent': OlivaDiceCore.data.bot_version_short_header
    }
    msg_res = req.request("GET", send_url, headers = headers, proxies = OlivaDiceCore.webTool.get_system_proxy())
    res_text = str(msg_res.text)
    try:
        tmp_res = json.loads(res_text)
        res = tmp_res
        gExtiverseDeck = res
    except:
        pass
    return res

def downloadExtiverseDeckRemote(name, botHash = 'unity'):
    global gExtiverseDeck
    res = False
    flag_hit = False
    res_text = None
    deck_type = 'deckclassic'
    if type(gExtiverseDeck) is dict \
    and 'classic' in gExtiverseDeck \
    and type(gExtiverseDeck['classic']) is list:
        for item in gExtiverseDeck['classic']:
            if type(item) is dict \
            and 'name' in item \
            and 'download_link' in item \
            and type(item['download_link']) is list \
            and item['name'] == name:
                for send_url in item['download_link']:
                    headers = {
                        'User-Agent': OlivaDiceCore.data.bot_version_short_header
                    }
                    try:
                        msg_res = req.request("GET", send_url, headers = headers, proxies = OlivaDiceCore.webTool.get_system_proxy())
                        res_text = str(msg_res.text)
                        flag_hit = True
                    except:
                        pass
                    if flag_hit:
                        res = True
                        deck_type = 'deckclassic'
                        break
    # 这里要写入文件
    if flag_hit:
        with open(os.path.join('plugin', 'data', 'OlivaDice', botHash, 'extend', deck_type, name + '.json'), 'w', encoding = 'utf-8') as f:
            f.write(res_text)
    return res

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



def sendKOOKManageThread(botDict:dict):
    dictTimerCount = {}
    dictPlayGameReg = {}
    listPlayGameMusicSoftware = ['cloudmusic', 'qqmusic', 'kugou']
    checkF = 5
    while True:
        for botHash in botDict:
            # KOOKBotMarketPulse
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

            # KOOK在玩游戏/听音乐状态
            flag_odysseyKOOKPlayGameMode = OlivaDiceCore.console.getConsoleSwitchByHash(
                'odysseyKOOKPlayGameMode',
                botHash
            )
            str_strOdysseyKOOKPlayGameMusicName = OlivaDiceCore.msgCustom.dictStrCustomDict.get(botHash, {}).get('strOdysseyKOOKPlayGameMusicName', '听啥咧')
            str_strOdysseyKOOKPlayGameMusicSinger = OlivaDiceCore.msgCustom.dictStrCustomDict.get(botHash, {}).get('strOdysseyKOOKPlayGameMusicSinger', '谁唱的')
            flag_odysseyKOOKPlayGameMusicSoftware = OlivaDiceCore.console.getConsoleSwitchByHash(
                'odysseyKOOKPlayGameMusicSoftware',
                botHash
            )
            str_strOdysseyKOOKPlayGameMusicSoftware = listPlayGameMusicSoftware[0]
            if flag_odysseyKOOKPlayGameMusicSoftware < len(listPlayGameMusicSoftware) \
            and flag_odysseyKOOKPlayGameMusicSoftware >= 0:
                str_strOdysseyKOOKPlayGameMusicSoftware = listPlayGameMusicSoftware[flag_odysseyKOOKPlayGameMusicSoftware]
            str_strOdysseyKOOKPlayGameID = OlivaDiceCore.msgCustom.dictStrCustomDict.get(botHash, {}).get('strOdysseyKOOKPlayGameID', '0')
            int_strOdysseyKOOKPlayGameID = 1521178
            try:
                int_strOdysseyKOOKPlayGameID = int(str_strOdysseyKOOKPlayGameID)
            except:
                pass
            dictPlayGameReg.setdefault(botHash, {
                'data_type': -1,
                'id': -1,
                'music_name': None,
                'singer': None,
                'software': None
            })
            hash_playgame_old_obj = hashlib.new('md5')
            for key in dictPlayGameReg[botHash]:
                hash_playgame_old_obj.update(('|' + key + ':' + str(dictPlayGameReg[botHash][key]) + '|').encode('utf-8'))
            hash_playgame_old = hash_playgame_old_obj.hexdigest()
            if 0 == flag_odysseyKOOKPlayGameMode:
                dictPlayGameReg[botHash].update({
                    'data_type': 0,
                    'id': -1,
                    'music_name': None,
                    'singer': None,
                    'software': None
                })
            elif 1 == flag_odysseyKOOKPlayGameMode:
                dictPlayGameReg[botHash].update({
                    'data_type': 1,
                    'id': 1521178,
                    'music_name': None,
                    'singer': None,
                    'software': None
                })
            elif 2 == flag_odysseyKOOKPlayGameMode:
                dictPlayGameReg[botHash].update({
                    'data_type': 2,
                    'id': -1,
                    'music_name': str_strOdysseyKOOKPlayGameMusicName,
                    'singer': str_strOdysseyKOOKPlayGameMusicSinger,
                    'software': str_strOdysseyKOOKPlayGameMusicSoftware
                })
            elif 3 == flag_odysseyKOOKPlayGameMode:
                dictPlayGameReg[botHash].update({
                    'data_type': 1,
                    'id': int_strOdysseyKOOKPlayGameID,
                    'music_name': None,
                    'singer': None,
                    'software': None
                })
            hash_playgame_new_obj = hashlib.new('md5')
            for key in dictPlayGameReg[botHash]:
                hash_playgame_new_obj.update(('|' + key + ':' + str(dictPlayGameReg[botHash][key]) + '|').encode('utf-8'))
            hash_playgame_new = hash_playgame_new_obj.hexdigest()
            if hash_playgame_old != hash_playgame_new:
                if 0 == flag_odysseyKOOKPlayGameMode:
                    fake_plugin_event = OlivOS.API.Event(
                        OlivOS.contentAPI.fake_sdk_event(
                            bot_info = OlivaDiceOdyssey.data.gProc.Proc_data['bot_info_dict'][botHash],
                            fakename = 'OlivaDice高阶模块'
                        ),
                        OlivaDiceOdyssey.data.gProc.log
                    )
                    try:
                        if fake_plugin_event.indeAPI.hasAPI('set_playgame_delete_activity_all'):
                            fake_plugin_event.indeAPI.set_playgame_delete_activity_all()
                    except:
                        pass
                elif 1 == flag_odysseyKOOKPlayGameMode:
                    fake_plugin_event = OlivOS.API.Event(
                        OlivOS.contentAPI.fake_sdk_event(
                            bot_info = OlivaDiceOdyssey.data.gProc.Proc_data['bot_info_dict'][botHash],
                            fakename = 'OlivaDice高阶模块'
                        ),
                        OlivaDiceOdyssey.data.gProc.log
                    )
                    try:
                        if fake_plugin_event.indeAPI.hasAPI('set_playgame_activity_game'):
                            fake_plugin_event.indeAPI.set_playgame_activity_game(1521178)
                    except:
                        pass
                elif 2 == flag_odysseyKOOKPlayGameMode:
                    fake_plugin_event = OlivOS.API.Event(
                        OlivOS.contentAPI.fake_sdk_event(
                            bot_info = OlivaDiceOdyssey.data.gProc.Proc_data['bot_info_dict'][botHash],
                            fakename = 'OlivaDice高阶模块'
                        ),
                        OlivaDiceOdyssey.data.gProc.log
                    )
                    try:
                        if fake_plugin_event.indeAPI.hasAPI('set_playgame_activity_music'):
                            fake_plugin_event.indeAPI.set_playgame_activity_music(
                                str_strOdysseyKOOKPlayGameMusicName,
                                str_strOdysseyKOOKPlayGameMusicSinger,
                                str_strOdysseyKOOKPlayGameMusicSoftware
                            )
                    except:
                        pass
                elif 3 == flag_odysseyKOOKPlayGameMode:
                    fake_plugin_event = OlivOS.API.Event(
                        OlivOS.contentAPI.fake_sdk_event(
                            bot_info = OlivaDiceOdyssey.data.gProc.Proc_data['bot_info_dict'][botHash],
                            fakename = 'OlivaDice高阶模块'
                        ),
                        OlivaDiceOdyssey.data.gProc.log
                    )
                    try:
                        if fake_plugin_event.indeAPI.hasAPI('set_playgame_activity_game'):
                            fake_plugin_event.indeAPI.set_playgame_activity_game(int_strOdysseyKOOKPlayGameID)
                    except:
                        pass
        time.sleep(checkF)

def initKOOKManageThread(botDict:dict):
    threading.Thread(
        target = OlivaDiceOdyssey.webTool.sendKOOKManageThread,
        args = (botDict, )
    ).start()
