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
    msg_res = req.request("GET", send_url, headers = headers)
    res_text = str(msg_res.text)
    try:
        tmp_res = json.loads(res_text)
        res = tmp_res
    except:
        pass
    return res
