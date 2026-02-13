# -*- encoding: utf-8 -*-
r"""
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/

@File      :   webTool.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2026, OlivOS-Team
@Desc      :   None
"""

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
import zipfile

gExtiverseDeck = {}


def releaseDir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def releaseToDirForFile(dir_path):
    tmp_path_list = dir_path.rstrip('/').split('/')
    if len(tmp_path_list) > 0:
        tmp_path_list = tmp_path_list[:-1]
    for tmp_path_list_index in range(len(tmp_path_list)):
        if tmp_path_list[tmp_path_list_index] != '':
            releaseDir('/'.join(tmp_path_list[: tmp_path_list_index + 1]))


def GETHttpFile(url, path):
    res = False
    send_url = url
    headers = {'User-Agent': 'OlivaDiceOdyssey/%s' % OlivaDiceOdyssey.data.OlivaDiceOdyssey_ver_short}
    try:
        msg_res = req.request('GET', send_url, headers=headers, proxies=OlivaDiceCore.webTool.get_system_proxy())
        releaseToDirForFile(path)
        with open(path, 'wb+') as tmp:
            tmp.write(msg_res.content)
        if msg_res.status_code in [200, 300]:
            res = True
        else:
            res = False
    except Exception:
        res = False
    return res


def getExtiverseDeckRemote():
    global gExtiverseDeck
    res = None
    tmp_res = None
    send_url = OlivaDiceOdyssey.cnmodsData.strExtiverseDeckMain
    headers = {'User-Agent': OlivaDiceCore.data.bot_version_short_header}
    msg_res = req.request('GET', send_url, headers=headers, proxies=OlivaDiceCore.webTool.get_system_proxy())
    res_text = str(msg_res.text)
    try:
        tmp_res = json.loads(res_text)
        res = tmp_res
        gExtiverseDeck = res
    except Exception:
        pass
    return res


def downloadExtiverseDeckRemote(name, botHash='unity'):
    res = False
    flag_hit = False
    res_text = None
    res_resource_list = None
    deck_type = 'deckclassic'
    for deck_meta_type in ['classic', 'yaml', 'excel']:
        if (
            type(gExtiverseDeck) is dict
            and deck_meta_type in gExtiverseDeck
            and type(gExtiverseDeck[deck_meta_type]) is list
        ):
            for item in gExtiverseDeck[deck_meta_type]:
                if (
                    type(item) is dict
                    and 'name' in item
                    and 'download_link' in item
                    and type(item['download_link']) is list
                    and item['name'] == name
                ):
                    if 'resource_link' in item:
                        res_resource_list = item['resource_link']
                    for send_url in item['download_link']:
                        headers = {'User-Agent': OlivaDiceCore.data.bot_version_short_header}
                        try:
                            msg_res = req.request(
                                'GET', send_url, headers=headers, proxies=OlivaDiceCore.webTool.get_system_proxy()
                            )
                            res_text = str(msg_res.text)
                            flag_hit = True
                        except Exception:
                            pass
                        if flag_hit:
                            res = True
                            deck_type = {'classic': 'deckclassic', 'yaml': 'deckyaml', 'excel': 'deckexcel'}[
                                deck_meta_type
                            ]
                            break
    # 这里要写入文件
    if flag_hit:
        checkDict = {'deckclassic': '.json', 'deckyaml': '.yaml', 'deckexcel': '.xlsx'}
        dfix = checkDict[deck_type]
        with open(
            os.path.join('plugin', 'data', 'OlivaDice', botHash, 'extend', deck_type, name + dfix),
            'w',
            encoding='utf-8',
        ) as f:
            f.write(res_text)
        # 这里下载并解压资源文件
        if res_resource_list is not None and type(res_resource_list) is list:
            for resource_url_this in res_resource_list:
                if type(resource_url_this) is str:
                    GETHttpFile(resource_url_this, 'plugin/data/OlivaDice/unity/update/tmp_deck_resource.zip')
                    with support_gbk(
                        zipfile.ZipFile(
                            'plugin/data/OlivaDice/unity/update/tmp_deck_resource.zip', 'r', zipfile.ZIP_DEFLATED
                        )
                    ) as resourceFile:
                        resourceFile_list = resourceFile.namelist()
                        for resourceFile_list_this in resourceFile_list:
                            try:
                                resourceFile.extract(resourceFile_list_this, 'data')
                            except Exception:
                                pass
    return res


def support_gbk(zip_file: zipfile.ZipFile):
    name_to_info = zip_file.NameToInfo
    # copy map first
    for name, info in name_to_info.copy().items():
        try:
            real_name = name.encode('cp437').decode('gbk')
        except Exception:
            real_name = name
        if real_name != name:
            info.filename = real_name
            del name_to_info[name]
            name_to_info[real_name] = info
    return zip_file


def getCnmodsReq(title=None, page=None, item_max=None, isRec=False, author=None):
    res = None
    tmp_res = None
    tmp_value = {}
    send_url = OlivaDiceOdyssey.cnmodsData.strCnmodsMain
    if title is not None:
        tmp_value['title'] = str(title)
    if page is not None:
        tmp_value['page'] = str(page)
    if item_max is not None:
        tmp_value['size'] = str(item_max)
    if isRec:
        tmp_value['isRec'] = 'true'
    if author is not None:
        tmp_value['article'] = str(author)
    if title is not None or page is not None or item_max is not None or isRec or author is not None:
        send_url += '?' + urlencode(tmp_value)
    headers = {'User-Agent': OlivaDiceCore.data.bot_version_short_header}
    msg_res = req.request('GET', send_url, headers=headers, proxies=OlivaDiceCore.webTool.get_system_proxy())
    res_text = str(msg_res.text)
    try:
        tmp_res = json.loads(res_text)
        res = tmp_res
    except Exception:
        pass
    return res


def getCnmodsDetailReq(keyId):
    """
    通过 keyId 获取模组详细信息
    """
    res = None
    tmp_res = None
    send_url = OlivaDiceOdyssey.cnmodsData.strCnmodsDetail
    if keyId is not None:
        tmp_value = {'keyId': str(keyId)}
        send_url += '?' + urlencode(tmp_value)
    headers = {'User-Agent': OlivaDiceCore.data.bot_version_short_header}
    try:
        msg_res = req.request('GET', send_url, headers=headers, proxies=OlivaDiceCore.webTool.get_system_proxy())
        res_text = str(msg_res.text)
        tmp_res = json.loads(res_text)
        res = tmp_res
    except Exception:
        pass
    return res


def getRulesReq(key: 'str|None' = None, page=None, item_max=None):
    res = None
    tmp_res = None
    tmp_value = {}
    send_url = OlivaDiceOdyssey.cnmodsData.strRulesMain
    if key is not None:
        tmp_value['key'] = str('%'.join(key))
    if page is not None:
        tmp_value['page'] = str(page)
    if item_max is not None:
        tmp_value['item_max'] = str(item_max)
    if key is not None:
        send_url += '?' + urlencode(tmp_value)
    headers = {'User-Agent': OlivaDiceCore.data.bot_version_short_header}
    try:
        msg_res = req.request('GET', send_url, headers=headers, proxies=OlivaDiceCore.webTool.get_system_proxy())
        res_text = str(msg_res.text)
        tmp_res = json.loads(res_text)
        res = tmp_res
    except Exception:
        pass
    return res


def sendKOOKBotMarketPulse(token: str):
    res = None
    tmp_res = None
    send_url = 'http://bot.gekj.net/api/v1/online.bot'
    headers = {'uuid': token, 'User-Agent': OlivaDiceCore.data.bot_version_short_header}
    msg_res = req.request('GET', send_url, headers=headers, proxies=OlivaDiceCore.webTool.get_system_proxy())
    res_text = str(msg_res.text)
    try:
        tmp_res = json.loads(res_text)
        res = tmp_res
    except Exception:
        pass
    return res


def sendKOOKManageThread(botDict: dict):
    dictTimerCount = {}
    dictPlayGameReg = {}
    listPlayGameMusicSoftware = ['cloudmusic', 'qqmusic', 'kugou']
    checkF = 5
    while True:
        for botHash in botDict:
            # KOOKBotMarketPulse
            flag_odysseyKOOKBotMarketPulseEnable = OlivaDiceCore.console.getConsoleSwitchByHash(
                'odysseyKOOKBotMarketPulseEnable', botHash
            )
            dictTimerCount.setdefault(botHash, 0)
            if 1 == flag_odysseyKOOKBotMarketPulseEnable and botHash in OlivaDiceCore.msgCustom.dictStrCustomDict:
                dictStrCustom: dict = OlivaDiceCore.msgCustom.dictStrCustomDict[botHash]
                token_this = dictStrCustom.get('strOdysseyKOOKBotMarketPulseUUID', '-')
                if '-' != token_this:
                    if dictTimerCount[botHash] <= 0:
                        res = OlivaDiceOdyssey.webTool.sendKOOKBotMarketPulse(token=token_this)
                        if res is not None:
                            dictTimerCount[botHash] = int(15 * 60)
                            OlivaDiceCore.msgReply.globalLog(
                                2,
                                'KOOK机器人服务平台心跳上报成功！',
                                [('OlivaDice', 'default'), ('KOOKBotMarket', 'default')],
                            )
                        else:
                            dictTimerCount[botHash] = 0
                            OlivaDiceCore.msgReply.globalLog(
                                3,
                                'KOOK机器人服务平台心跳上报失败！',
                                [('OlivaDice', 'default'), ('KOOKBotMarket', 'default')],
                            )
                    dictTimerCount[botHash] -= checkF
                else:
                    dictTimerCount[botHash] = 0
            else:
                dictTimerCount[botHash] = 0

            # KOOK在玩游戏/听音乐状态
            flag_odysseyKOOKPlayGameMode = OlivaDiceCore.console.getConsoleSwitchByHash(
                'odysseyKOOKPlayGameMode', botHash
            )
            str_strOdysseyKOOKPlayGameMusicName = OlivaDiceCore.msgCustom.dictStrCustomDict.get(botHash, {}).get(
                'strOdysseyKOOKPlayGameMusicName', '听啥咧'
            )
            str_strOdysseyKOOKPlayGameMusicSinger = OlivaDiceCore.msgCustom.dictStrCustomDict.get(botHash, {}).get(
                'strOdysseyKOOKPlayGameMusicSinger', '谁唱的'
            )
            flag_odysseyKOOKPlayGameMusicSoftware = OlivaDiceCore.console.getConsoleSwitchByHash(
                'odysseyKOOKPlayGameMusicSoftware', botHash
            )
            str_strOdysseyKOOKPlayGameMusicSoftware = listPlayGameMusicSoftware[0]
            if (
                flag_odysseyKOOKPlayGameMusicSoftware < len(listPlayGameMusicSoftware)
                and flag_odysseyKOOKPlayGameMusicSoftware >= 0
            ):
                str_strOdysseyKOOKPlayGameMusicSoftware = listPlayGameMusicSoftware[
                    flag_odysseyKOOKPlayGameMusicSoftware
                ]
            str_strOdysseyKOOKPlayGameID = OlivaDiceCore.msgCustom.dictStrCustomDict.get(botHash, {}).get(
                'strOdysseyKOOKPlayGameID', '0'
            )
            int_strOdysseyKOOKPlayGameID = 1521178
            try:
                int_strOdysseyKOOKPlayGameID = int(str_strOdysseyKOOKPlayGameID)
            except Exception:
                pass
            dictPlayGameReg.setdefault(
                botHash, {'data_type': -1, 'id': -1, 'music_name': None, 'singer': None, 'software': None}
            )
            hash_playgame_old_obj = hashlib.new('md5')
            for key in dictPlayGameReg[botHash]:
                hash_playgame_old_obj.update(
                    ('|' + key + ':' + str(dictPlayGameReg[botHash][key]) + '|').encode('utf-8')
                )
            hash_playgame_old = hash_playgame_old_obj.hexdigest()
            if 0 == flag_odysseyKOOKPlayGameMode:
                dictPlayGameReg[botHash].update({
                    'data_type': 0,
                    'id': -1,
                    'music_name': None,
                    'singer': None,
                    'software': None,
                })
            elif 1 == flag_odysseyKOOKPlayGameMode:
                dictPlayGameReg[botHash].update({
                    'data_type': 1,
                    'id': 1521178,
                    'music_name': None,
                    'singer': None,
                    'software': None,
                })
            elif 2 == flag_odysseyKOOKPlayGameMode:
                dictPlayGameReg[botHash].update({
                    'data_type': 2,
                    'id': -1,
                    'music_name': str_strOdysseyKOOKPlayGameMusicName,
                    'singer': str_strOdysseyKOOKPlayGameMusicSinger,
                    'software': str_strOdysseyKOOKPlayGameMusicSoftware,
                })
            elif 3 == flag_odysseyKOOKPlayGameMode:
                dictPlayGameReg[botHash].update({
                    'data_type': 1,
                    'id': int_strOdysseyKOOKPlayGameID,
                    'music_name': None,
                    'singer': None,
                    'software': None,
                })
            hash_playgame_new_obj = hashlib.new('md5')
            for key in dictPlayGameReg[botHash]:
                hash_playgame_new_obj.update(
                    ('|' + key + ':' + str(dictPlayGameReg[botHash][key]) + '|').encode('utf-8')
                )
            hash_playgame_new = hash_playgame_new_obj.hexdigest()
            if hash_playgame_old != hash_playgame_new:
                if 0 == flag_odysseyKOOKPlayGameMode:
                    fake_plugin_event = OlivOS.API.Event(
                        OlivOS.contentAPI.fake_sdk_event(
                            bot_info=OlivaDiceOdyssey.data.gProc.Proc_data['bot_info_dict'][botHash],
                            fakename='OlivaDice高阶模块',
                        ),
                        OlivaDiceOdyssey.data.gProc.log,
                    )
                    try:
                        if fake_plugin_event.indeAPI.hasAPI('set_playgame_delete_activity_all'):
                            fake_plugin_event.indeAPI.set_playgame_delete_activity_all()
                    except Exception:
                        pass
                elif 1 == flag_odysseyKOOKPlayGameMode:
                    fake_plugin_event = OlivOS.API.Event(
                        OlivOS.contentAPI.fake_sdk_event(
                            bot_info=OlivaDiceOdyssey.data.gProc.Proc_data['bot_info_dict'][botHash],
                            fakename='OlivaDice高阶模块',
                        ),
                        OlivaDiceOdyssey.data.gProc.log,
                    )
                    try:
                        if fake_plugin_event.indeAPI.hasAPI('set_playgame_activity_game'):
                            fake_plugin_event.indeAPI.set_playgame_activity_game(1521178)
                    except Exception:
                        pass
                elif 2 == flag_odysseyKOOKPlayGameMode:
                    fake_plugin_event = OlivOS.API.Event(
                        OlivOS.contentAPI.fake_sdk_event(
                            bot_info=OlivaDiceOdyssey.data.gProc.Proc_data['bot_info_dict'][botHash],
                            fakename='OlivaDice高阶模块',
                        ),
                        OlivaDiceOdyssey.data.gProc.log,
                    )
                    try:
                        if fake_plugin_event.indeAPI.hasAPI('set_playgame_activity_music'):
                            fake_plugin_event.indeAPI.set_playgame_activity_music(
                                str_strOdysseyKOOKPlayGameMusicName,
                                str_strOdysseyKOOKPlayGameMusicSinger,
                                str_strOdysseyKOOKPlayGameMusicSoftware,
                            )
                    except Exception:
                        pass
                elif 3 == flag_odysseyKOOKPlayGameMode:
                    fake_plugin_event = OlivOS.API.Event(
                        OlivOS.contentAPI.fake_sdk_event(
                            bot_info=OlivaDiceOdyssey.data.gProc.Proc_data['bot_info_dict'][botHash],
                            fakename='OlivaDice高阶模块',
                        ),
                        OlivaDiceOdyssey.data.gProc.log,
                    )
                    try:
                        if fake_plugin_event.indeAPI.hasAPI('set_playgame_activity_game'):
                            fake_plugin_event.indeAPI.set_playgame_activity_game(int_strOdysseyKOOKPlayGameID)
                    except Exception:
                        pass
        time.sleep(checkF)


def initKOOKManageThread(botDict: dict):
    threading.Thread(target=OlivaDiceOdyssey.webTool.sendKOOKManageThread, args=(botDict,)).start()
