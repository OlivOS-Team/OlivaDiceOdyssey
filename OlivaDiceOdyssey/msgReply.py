# -*- encoding: utf-8 -*-
'''
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/   
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___   
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/   

@File      :   msgReply.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import OlivaDiceOdyssey
import OlivaDiceCore

import re
import html

def unity_init(plugin_event, Proc):
    pass

def data_init(plugin_event, Proc):
    OlivaDiceOdyssey.data.gProc = Proc
    OlivaDiceOdyssey.msgCustomManager.initMsgCustom(Proc.Proc_data['bot_info_dict'])
    if 'replyContextPrefixFliter' in OlivaDiceCore.crossHook.dictHookList:
        OlivaDiceCore.crossHook.dictHookList['replyContextPrefixFliter'].append('rules')
        OlivaDiceCore.crossHook.dictHookList['replyContextPrefixFliter'].append('rule')
    OlivaDiceOdyssey.webTool.initKOOKManageThread(Proc.Proc_data['bot_info_dict'])

def unity_reply(plugin_event, Proc):
    OlivaDiceCore.userConfig.setMsgCount()
    dictTValue = OlivaDiceCore.msgCustom.dictTValue.copy()
    dictTValue['tUserName'] = plugin_event.data.sender['name']
    dictTValue['tName'] = plugin_event.data.sender['name']
    dictStrCustom = OlivaDiceCore.msgCustom.dictStrCustomDict[plugin_event.bot_info.hash]
    dictGValue = OlivaDiceCore.msgCustom.dictGValue
    dictTValue.update(dictGValue)
    dictTValue = OlivaDiceCore.msgCustomManager.dictTValueInit(plugin_event, dictTValue)

    replyMsg = OlivaDiceCore.msgReply.replyMsg
    isMatchWordStart = OlivaDiceCore.msgReply.isMatchWordStart
    getMatchWordStartRight = OlivaDiceCore.msgReply.getMatchWordStartRight
    skipSpaceStart = OlivaDiceCore.msgReply.skipSpaceStart
    skipToRight = OlivaDiceCore.msgReply.skipToRight
    msgIsCommand = OlivaDiceCore.msgReply.msgIsCommand

    tmp_at_str = OlivOS.messageAPI.PARA.at(plugin_event.base_info['self_id']).CQ()
    tmp_id_str = str(plugin_event.base_info['self_id'])
    tmp_at_str_sub = None
    tmp_id_str_sub = None
    if 'sub_self_id' in plugin_event.data.extend:
        if plugin_event.data.extend['sub_self_id'] != None:
            tmp_at_str_sub = OlivOS.messageAPI.PARA.at(plugin_event.data.extend['sub_self_id']).CQ()
            tmp_id_str_sub = str(plugin_event.data.extend['sub_self_id'])
    tmp_command_str_1 = '.'
    tmp_command_str_2 = '。'
    tmp_command_str_3 = '/'
    tmp_reast_str = plugin_event.data.message
    flag_force_reply = False
    flag_is_command = False
    flag_is_from_host = False
    flag_is_from_group = False
    flag_is_from_group_admin = False
    flag_is_from_group_sub_admin = False
    flag_is_from_group_have_admin = False
    flag_is_from_master = False
    if isMatchWordStart(tmp_reast_str, '[CQ:reply,id='):
        tmp_reast_str = skipToRight(tmp_reast_str, ']')
        tmp_reast_str = tmp_reast_str[1:]
    if flag_force_reply is False:
        tmp_reast_str_old = tmp_reast_str
        tmp_reast_obj = OlivOS.messageAPI.Message_templet(
            'old_string',
            tmp_reast_str
        )
        tmp_at_list = []
        for tmp_reast_obj_this in tmp_reast_obj.data:
            tmp_para_str_this = tmp_reast_obj_this.CQ()
            if type(tmp_reast_obj_this) is OlivOS.messageAPI.PARA.at:
                tmp_at_list.append(str(tmp_reast_obj_this.data['id']))
                tmp_reast_str = tmp_reast_str.lstrip(tmp_para_str_this)
            elif type(tmp_reast_obj_this) is OlivOS.messageAPI.PARA.text:
                if tmp_para_str_this.strip(' ') == '':
                    tmp_reast_str = tmp_reast_str.lstrip(tmp_para_str_this)
                else:
                    break
            else:
                break
        if tmp_id_str in tmp_at_list:
            flag_force_reply = True
        if tmp_id_str_sub in tmp_at_list:
            flag_force_reply = True
        if 'all' in tmp_at_list:
            flag_force_reply = True
        if flag_force_reply is True:
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
        else:
            tmp_reast_str = tmp_reast_str_old
    [tmp_reast_str, flag_is_command] = msgIsCommand(
        tmp_reast_str,
        OlivaDiceCore.crossHook.dictHookList['prefix']
    )
    if flag_is_command:
        tmp_hagID = None
        if plugin_event.plugin_info['func_type'] == 'group_message':
            if plugin_event.data.host_id != None:
                flag_is_from_host = True
            flag_is_from_group = True
        elif plugin_event.plugin_info['func_type'] == 'private_message':
            flag_is_from_group = False
        if flag_is_from_group:
            if 'role' in plugin_event.data.sender:
                flag_is_from_group_have_admin = True
                if plugin_event.data.sender['role'] in ['owner', 'admin']:
                    flag_is_from_group_admin = True
                elif plugin_event.data.sender['role'] in ['sub_admin']:
                    flag_is_from_group_admin = True
                    flag_is_from_group_sub_admin = True
        if flag_is_from_host and flag_is_from_group:
            tmp_hagID = '%s|%s' % (str(plugin_event.data.host_id), str(plugin_event.data.group_id))
        elif flag_is_from_group:
            tmp_hagID = str(plugin_event.data.group_id)
        flag_hostEnable = True
        if flag_is_from_host:
            flag_hostEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                userId = plugin_event.data.host_id,
                userType = 'host',
                platform = plugin_event.platform['platform'],
                userConfigKey = 'hostEnable',
                botHash = plugin_event.bot_info.hash
            )
        flag_hostLocalEnable = True
        if flag_is_from_host:
            flag_hostLocalEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                userId = plugin_event.data.host_id,
                userType = 'host',
                platform = plugin_event.platform['platform'],
                userConfigKey = 'hostLocalEnable',
                botHash = plugin_event.bot_info.hash
            )
        flag_groupEnable = True
        if flag_is_from_group:
            if flag_is_from_host:
                if flag_hostEnable:
                    flag_groupEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                        userId = tmp_hagID,
                        userType = 'group',
                        platform = plugin_event.platform['platform'],
                        userConfigKey = 'groupEnable',
                        botHash = plugin_event.bot_info.hash
                    )
                else:
                    flag_groupEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                        userId = tmp_hagID,
                        userType = 'group',
                        platform = plugin_event.platform['platform'],
                        userConfigKey = 'groupWithHostEnable',
                        botHash = plugin_event.bot_info.hash
                    )
            else:
                flag_groupEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                    userId = tmp_hagID,
                    userType = 'group',
                    platform = plugin_event.platform['platform'],
                    userConfigKey = 'groupEnable',
                    botHash = plugin_event.bot_info.hash
                )
        #此频道关闭时中断处理
        if not flag_hostLocalEnable and not flag_force_reply:
            return
        #此群关闭时中断处理
        if not flag_groupEnable and not flag_force_reply:
            return
        if isMatchWordStart(tmp_reast_str, 'rules', isCommand = True) or isMatchWordStart(tmp_reast_str, 'rule', isCommand = True):
            OlivaDiceOdyssey.msgReply.replyRULES_command(
                plugin_event = plugin_event,
                Proc = Proc,
                tmp_reast_str = tmp_reast_str,
                isMatchWordStart = isMatchWordStart,
                getMatchWordStartRight = getMatchWordStartRight,
                skipSpaceStart = skipSpaceStart,
                dictStrCustom = dictStrCustom,
                dictTValue = dictTValue,
                replyMsg = replyMsg
            )
        elif isMatchWordStart(tmp_reast_str, ['cnmods','mdmz','modu'], isCommand = True):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, ['cnmods','mdmz','modu'])
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            tmp_reast_str = tmp_reast_str.rstrip(' ')
            if isMatchWordStart(tmp_reast_str, 'help'):
                OlivaDiceCore.msgReply.replyMsgLazyHelpByEvent(plugin_event, 'cnmods')
                return
            elif isMatchWordStart(tmp_reast_str, 'search'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, ['search', 'find'])
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_reast_str = tmp_reast_str.rstrip(' ')
                tmp_reast_str_list = tmp_reast_str.split(' ')
                tmp_reply_str = None
                tmp_title = None
                tmp_page = 1
                if len(tmp_reast_str_list) == 1:
                    tmp_title = tmp_reast_str_list[0]
                elif len(tmp_reast_str_list) >= 2:
                    tmp_title = tmp_reast_str_list[0]
                    if tmp_reast_str_list[-1].isdigit():
                        tmp_page = int(tmp_reast_str_list[-1])
                        tmp_title = ' '.join(tmp_reast_str_list[:-1])
                    else:
                        tmp_title = tmp_reast_str
                if tmp_title == None or tmp_title == '':
                    return
                tmp_res = OlivaDiceOdyssey.webTool.getCnmodsReq(title = tmp_title, page = tmp_page, item_max = 8, isRec = False, author = None)
                if tmp_res != None:
                    try:
                        tmp_reply_str = replyCnmodsList(tmp_res, 'search', plugin_event, replyMsg, dictStrCustom, dictTValue)
                        if tmp_reply_str:
                            OlivaDiceCore.userConfig.setUserConfigByKey(
                                userConfigKey = 'cnmodsTemp',
                                userConfigValue = tmp_res,
                                botHash = plugin_event.bot_info.hash,
                                userId = plugin_event.data.user_id,
                                userType = 'user',
                                platform = plugin_event.platform['platform']
                            )
                            OlivaDiceCore.userConfig.writeUserConfigByUserHash(
                                userHash = OlivaDiceCore.userConfig.getUserHash(
                                    userId = plugin_event.data.user_id,
                                    userType = 'user',
                                    platform = plugin_event.platform['platform']
                                )
                            )
                        else:
                            tmp_reply_str = dictStrCustom['strOdysseyCnmodsSearchNotFound']
                    except:
                        pass
                if tmp_reply_str != None:
                    replyMsg(plugin_event, tmp_reply_str)
            elif isMatchWordStart(tmp_reast_str, 'rec'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'rec')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_reast_str = tmp_reast_str.rstrip(' ')
                tmp_reast_str_list = tmp_reast_str.split(' ')
                tmp_reply_str = None
                tmp_title = None
                tmp_page = 1
                if len(tmp_reast_str_list) == 1:
                    tmp_title = tmp_reast_str_list[0]
                elif len(tmp_reast_str_list) >= 2:
                    tmp_title = tmp_reast_str_list[0]
                    if tmp_reast_str_list[-1].isdigit():
                        tmp_page = int(tmp_reast_str_list[-1])
                        tmp_title = ' '.join(tmp_reast_str_list[:-1])
                    else:
                        tmp_title = tmp_reast_str
                if tmp_title == None or tmp_title == '':
                    return
                tmp_res = OlivaDiceOdyssey.webTool.getCnmodsReq(title = tmp_title, page = tmp_page, item_max = 8, isRec = True, author = None)
                if tmp_res != None:
                    try:
                        tmp_reply_str = replyCnmodsList(tmp_res, 'rec', plugin_event, replyMsg, dictStrCustom, dictTValue)
                        if tmp_reply_str:
                            OlivaDiceCore.userConfig.setUserConfigByKey(
                                userConfigKey = 'cnmodsTemp',
                                userConfigValue = tmp_res,
                                botHash = plugin_event.bot_info.hash,
                                userId = plugin_event.data.user_id,
                                userType = 'user',
                                platform = plugin_event.platform['platform']
                            )
                            OlivaDiceCore.userConfig.writeUserConfigByUserHash(
                                userHash = OlivaDiceCore.userConfig.getUserHash(
                                    userId = plugin_event.data.user_id,
                                    userType = 'user',
                                    platform = plugin_event.platform['platform']
                                )
                            )
                        else:
                            tmp_reply_str = dictStrCustom['strOdysseyCnmodsRecNotFound']
                    except:
                        pass
                        pass
                if tmp_reply_str != None:
                    replyMsg(plugin_event, tmp_reply_str)
            elif isMatchWordStart(tmp_reast_str, 'author'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'author')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_reast_str = tmp_reast_str.rstrip(' ')
                tmp_reast_str_list = tmp_reast_str.split(' ')
                tmp_reply_str = None
                tmp_author = None
                tmp_page = 1
                if len(tmp_reast_str_list) == 1:
                    tmp_author = tmp_reast_str_list[0]
                elif len(tmp_reast_str_list) >= 2:
                    tmp_author = tmp_reast_str_list[0]
                    if tmp_reast_str_list[-1].isdigit():
                        tmp_page = int(tmp_reast_str_list[-1])
                        tmp_author = ' '.join(tmp_reast_str_list[:-1])
                    else:
                        tmp_author = tmp_reast_str
                if tmp_author == None or tmp_author == '':
                    return
                tmp_res = OlivaDiceOdyssey.webTool.getCnmodsReq(title = None, page = tmp_page, item_max = 8, isRec = False, author = tmp_author)
                if tmp_res != None:
                    try:
                        tmp_reply_str = replyCnmodsList(tmp_res, 'author', plugin_event, replyMsg, dictStrCustom, dictTValue)
                        if tmp_reply_str:
                            OlivaDiceCore.userConfig.setUserConfigByKey(
                                userConfigKey = 'cnmodsTemp',
                                userConfigValue = tmp_res,
                                botHash = plugin_event.bot_info.hash,
                                userId = plugin_event.data.user_id,
                                userType = 'user',
                                platform = plugin_event.platform['platform']
                            )
                            OlivaDiceCore.userConfig.writeUserConfigByUserHash(
                                userHash = OlivaDiceCore.userConfig.getUserHash(
                                    userId = plugin_event.data.user_id,
                                    userType = 'user',
                                    platform = plugin_event.platform['platform']
                                )
                            )
                        else:
                            tmp_reply_str = dictStrCustom['strOdysseyCnmodsAuthorNotFound']
                    except:
                        pass
                if tmp_reply_str != None:
                    replyMsg(plugin_event, tmp_reply_str)      
            elif isMatchWordStart(tmp_reast_str, 'luck'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'luck')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_reast_str = tmp_reast_str.rstrip(' ')
                tmp_reply_str = None
                tmp_page = 1
                if tmp_reast_str.isdigit():
                    tmp_page = int(tmp_reast_str)
                tmp_res = OlivaDiceOdyssey.webTool.getCnmodsReq(title = None, page = tmp_page, item_max = 8, isRec = True, author = None)
                if tmp_res != None:
                    try:
                        tmp_reply_str = replyCnmodsList(tmp_res, 'luck', plugin_event, replyMsg, dictStrCustom, dictTValue)
                        if tmp_reply_str:
                            OlivaDiceCore.userConfig.setUserConfigByKey(
                                userConfigKey = 'cnmodsTemp',
                                userConfigValue = tmp_res,
                                botHash = plugin_event.bot_info.hash,
                                userId = plugin_event.data.user_id,
                                userType = 'user',
                                platform = plugin_event.platform['platform']
                            )
                            OlivaDiceCore.userConfig.writeUserConfigByUserHash(
                                userHash = OlivaDiceCore.userConfig.getUserHash(
                                    userId = plugin_event.data.user_id,
                                    userType = 'user',
                                    platform = plugin_event.platform['platform']
                                )
                            )
                        else:
                            tmp_reply_str = dictStrCustom['strOdysseyCnmodsLuckNotFound']
                    except:
                        pass
                if tmp_reply_str != None:
                    replyMsg(plugin_event, tmp_reply_str)
            elif isMatchWordStart(tmp_reast_str, 'roll'):
                tmp_reply_str = None
                tmp_total_elements = 0
                # 获取总数
                tmp_res = OlivaDiceOdyssey.webTool.getCnmodsReq(title = None, page = 1, item_max = 1)
                if tmp_res != None:
                    try:
                        tmp_total_elements = tmp_res['data'].get('totalElements', 1)
                    except:
                        pass
                if tmp_total_elements > 0:
                    # 直接随机一个keyId
                    tmp_rd = OlivaDiceCore.onedice.RD('1D%s' % str(tmp_total_elements))
                    tmp_rd.roll()
                    if tmp_rd.resError == None:
                        tmp_keyId = tmp_rd.resInt
                        # 通过keyId获取详情
                        tmp_detail_res = OlivaDiceOdyssey.webTool.getCnmodsDetailReq(tmp_keyId)
                        if tmp_detail_res != None:
                            try:
                                if 'data' in tmp_detail_res and tmp_detail_res['data'] != None and 'module' in tmp_detail_res['data']:
                                    tmp_reply_str = replyCnmodsDetail(tmp_detail_res['data']['module'])
                                    replyMsg(plugin_event, tmp_reply_str)
                                    return
                            except:
                                pass
                if tmp_reply_str != None:
                    replyMsg(plugin_event, tmp_reply_str)
            elif isMatchWordStart(tmp_reast_str, 'find'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'find')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_reast_str = tmp_reast_str.rstrip(' ')
                tmp_reply_str = None
                # find命令只接受纯数字keyId
                if tmp_reast_str.isdigit():
                    tmp_keyId = int(tmp_reast_str)
                    # 通过keyId获取详情
                    tmp_detail_res = OlivaDiceOdyssey.webTool.getCnmodsDetailReq(tmp_keyId)
                    if tmp_detail_res != None:
                        try:
                            if 'data' in tmp_detail_res and tmp_detail_res['data'] != None and 'module' in tmp_detail_res['data']:
                                tmp_reply_str = replyCnmodsDetail(tmp_detail_res['data']['module'])
                            else:
                                dictTValue['tKeyId'] = str(tmp_keyId)
                                tmp_reply_str = dictStrCustom['strOdysseyCnmodsFindNotFound'].format(**dictTValue)
                        except:
                            tmp_reply_str = dictStrCustom['strOdysseyCnmodsFindError']
                    else:
                        tmp_reply_str = dictStrCustom['strOdysseyCnmodsFindErrorRetry']
                else:
                    tmp_reply_str = dictStrCustom['strOdysseyCnmodsFindOnlyNumber']
                if tmp_reply_str != None:
                    replyMsg(plugin_event, tmp_reply_str)
            elif isMatchWordStart(tmp_reast_str, 'get'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'get')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_reast_str = tmp_reast_str.rstrip(' ')
                tmp_reply_str = None
                # 获取缓存
                tmp_res = OlivaDiceCore.userConfig.getUserConfigByKey(
                    userId = plugin_event.data.user_id,
                    userType = 'user',
                    platform = plugin_event.platform['platform'],
                    userConfigKey = 'cnmodsTemp',
                    botHash = plugin_event.bot_info.hash
                )
                # 情况1: 无参数 - 显示缓存
                if tmp_reast_str == '':
                    if tmp_res != None and 'data' in tmp_res and 'list' in tmp_res['data'] and len(tmp_res['data']['list']) > 0:
                        tmp_reply_str = replyCnmodsList(tmp_res, 'get', plugin_event, replyMsg, dictStrCustom, dictTValue)
                    else:
                        tmp_reply_str = dictStrCustom['strOdysseyCnmodsGetCacheNotFound']
                # 情况2: 数字参数 - 从缓存获取指定序号
                elif tmp_reast_str.isdigit():
                    tmp_count_get = int(tmp_reast_str)
                    if tmp_res != None and 'data' in tmp_res and 'list' in tmp_res['data']:
                        if tmp_count_get >= 1 and tmp_count_get <= len(tmp_res['data']['list']):
                            tmp_get_res = tmp_res['data']['list'][tmp_count_get - 1]
                            tmp_reply_str = replyCnmodsDetail(tmp_get_res)
                            replyMsg(plugin_event, tmp_reply_str)
                            return
                        else:
                            dictTValue['tRange'] = str(len(tmp_res['data']['list']))
                            tmp_reply_str = dictStrCustom['strOdysseyCnmodsGetRangeError'].format(**dictTValue)
                    else:
                        tmp_reply_str = dictStrCustom['strOdysseyCnmodsGetCacheNotFound']
                # 情况3: 名称参数 - 搜索模组
                else:
                    tmp_search_res = OlivaDiceOdyssey.webTool.getCnmodsReq(title = tmp_reast_str, page = 1, item_max = 8, isRec = False, author = None)
                    if tmp_search_res != None and 'data' in tmp_search_res and 'list' in tmp_search_res['data']:
                        tmp_list = tmp_search_res['data']['list']
                        # 检查是否有完全匹配的结果
                        tmp_exact_match = None
                        for mod_this in tmp_list:
                            if mod_this.get('title', '') == tmp_reast_str:
                                tmp_exact_match = mod_this
                                break
                        # 如果有完全匹配,直接显示
                        if tmp_exact_match:
                            tmp_reply_str = replyCnmodsDetail(tmp_exact_match)
                            replyMsg(plugin_event, tmp_reply_str)
                            # 保存搜索结果到缓存
                            OlivaDiceCore.userConfig.setUserConfigByKey(
                                userConfigKey = 'cnmodsTemp',
                                userConfigValue = tmp_search_res,
                                botHash = plugin_event.bot_info.hash,
                                userId = plugin_event.data.user_id,
                                userType = 'user',
                                platform = plugin_event.platform['platform']
                            )
                            OlivaDiceCore.userConfig.writeUserConfigByUserHash(
                                userHash = OlivaDiceCore.userConfig.getUserHash(
                                    userId = plugin_event.data.user_id,
                                    userType = 'user',
                                    platform = plugin_event.platform['platform']
                                )
                            )
                            return
                        # 如果只有一个结果,直接显示
                        elif len(tmp_list) == 1:
                            tmp_reply_str = replyCnmodsDetail(tmp_list[0])
                            replyMsg(plugin_event, tmp_reply_str)
                            # 保存搜索结果到缓存
                            OlivaDiceCore.userConfig.setUserConfigByKey(
                                userConfigKey = 'cnmodsTemp',
                                userConfigValue = tmp_search_res,
                                botHash = plugin_event.bot_info.hash,
                                userId = plugin_event.data.user_id,
                                userType = 'user',
                                platform = plugin_event.platform['platform']
                            )
                            OlivaDiceCore.userConfig.writeUserConfigByUserHash(
                                userHash = OlivaDiceCore.userConfig.getUserHash(
                                    userId = plugin_event.data.user_id,
                                    userType = 'user',
                                    platform = plugin_event.platform['platform']
                                )
                            )
                            return
                        # 如果有多个结果,显示列表
                        elif len(tmp_list) > 1:
                            tmp_reply_str = replyCnmodsList(tmp_search_res, 'get_search', plugin_event, replyMsg, dictStrCustom, dictTValue)
                            # 保存搜索结果到缓存
                            OlivaDiceCore.userConfig.setUserConfigByKey(
                                userConfigKey = 'cnmodsTemp',
                                userConfigValue = tmp_search_res,
                                botHash = plugin_event.bot_info.hash,
                                userId = plugin_event.data.user_id,
                                userType = 'user',
                                platform = plugin_event.platform['platform']
                            )
                            OlivaDiceCore.userConfig.writeUserConfigByUserHash(
                                userHash = OlivaDiceCore.userConfig.getUserHash(
                                    userId = plugin_event.data.user_id,
                                    userType = 'user',
                                    platform = plugin_event.platform['platform']
                                )
                            )
                        else:
                            tmp_reply_str = dictStrCustom['strOdysseyCnmodsGetSearchNotFound']
                    else:
                        tmp_reply_str = dictStrCustom['strOdysseyCnmodsGetSearchError']
                
                if tmp_reply_str != None:
                    replyMsg(plugin_event, tmp_reply_str)
            else:
                OlivaDiceCore.msgReply.replyMsgLazyHelpByEvent(plugin_event, 'cnmods')
            return

def replyRULES_command(
    plugin_event,
    Proc,
    tmp_reast_str,
    isMatchWordStart,
    getMatchWordStartRight,
    skipSpaceStart,
    dictStrCustom,
    dictTValue,
    replyMsg
):
    tmp_hagID = None
    tmp_bothash = plugin_event.bot_info.hash
    tmp_userID = plugin_event.data.user_id
    if isMatchWordStart(tmp_reast_str, 'rules'):
        tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'rules')
        tmp_reast_str = skipSpaceStart(tmp_reast_str)
        tmp_reast_str = tmp_reast_str.rstrip(' ')
    elif isMatchWordStart(tmp_reast_str, 'rule'):
        tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'rule')
        tmp_reast_str = skipSpaceStart(tmp_reast_str)
        tmp_reast_str = tmp_reast_str.rstrip(' ')
    
    [tmp_keyword, tmp_page] = OlivaDiceCore.msgReply.getNumberPara(tmp_reast_str, reverse = True)
    if tmp_page == '' or not tmp_page.isdigit():
        tmp_page = 1
    else:
        tmp_page = int(tmp_page)
    if tmp_page < 1:
        tmp_page = 1
    tmp_keyword = tmp_keyword.rstrip(' ')
    tmp_item_max = 8
    tmp_item_max = OlivaDiceCore.console.getConsoleSwitchByHash(
        'odysseyRulesItemLimit',
        tmp_bothash
    )
    if not type(tmp_item_max) == int:
        tmp_item_max = 8
    if tmp_item_max < 1:
        tmp_item_max = 8
    tmp_total_page = 0
    if tmp_keyword != '':
        tmp_res = OlivaDiceOdyssey.webTool.getRulesReq(key = tmp_keyword, page = tmp_page - 1, item_max = tmp_item_max)
        if (
            type(tmp_res) == dict and 'code' in tmp_res and 'status' in tmp_res
        ) and (
            tmp_res['code'] == 0 and tmp_res['status'] == 200
        ):
            if 'data' in tmp_res and 'result' in tmp_res['data'] and type(tmp_res['data']['result']) == list:
                if 'total' in tmp_res['data'] and type(tmp_res['data']['total']) == int:
                    tmp_total_page = int(tmp_res['data']['total'] / tmp_item_max) + 1
                if len(tmp_res['data']['result']) == 0:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strOdysseyRulesNone'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                elif len(tmp_res['data']['result']) == 1:
                    data_this = tmp_res['data']['result'][0]
                    replyRULES_command_getResult(
                        data_this = data_this,
                        plugin_event = plugin_event,
                        dictStrCustom = dictStrCustom,
                        dictTValue = dictTValue,
                        replyMsg = replyMsg
                    )
                elif len(tmp_res['data']['result']) > 1:
                    data_list = tmp_res['data']['result']
                    if len(data_list) > tmp_item_max:
                        data_list = data_list[:tmp_item_max]
                    result_list = []
                    count = 1
                    for data_list_this in data_list:
                        tmp_data_list_this_rule = 'N/A'
                        tmp_data_list_this_keyword = 'N/A'
                        tmp_data_list_this_content = 'N/A'
                        if type(data_list_this) == dict and 'rule' in data_list_this and 'keyword' in data_list_this and 'content' in data_list_this:
                            tmp_data_list_this_rule = data_list_this['rule']
                            tmp_data_list_this_keyword = data_list_this['keyword']
                            tmp_data_list_this_content = data_list_this['content']
                        result_list.append(
                            '%d. [%s]%s' % (
                                count,
                                tmp_data_list_this_rule,
                                tmp_data_list_this_keyword
                            )
                        )
                        count += 1
                    dictTValue['tResult'] = '%s\n====[第%d/%d页]====' % (
                        OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strOdysseyRulesSplit'], dictTValue).join(result_list),
                        tmp_page,
                        tmp_total_page
                    )
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strOdysseyRulesList'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                    tmp_select:str = OlivaDiceCore.msgReplyModel.replyCONTEXT_regWait(
                        plugin_event = plugin_event,
                        flagBlock = 'allowCommand',
                        hash = OlivaDiceCore.msgReplyModel.contextRegHash([None, tmp_userID])
                    )
                    if tmp_select == None:
                        pass
                    elif type(tmp_select) == str:
                        if tmp_select.isdigit():
                            tmp_select = int(tmp_select)
                            if tmp_select >= 1 and tmp_select <= 8:
                                data_this = tmp_res['data']['result'][tmp_select - 1]
                                replyRULES_command_getResult(
                                    data_this = data_this,
                                    plugin_event = plugin_event,
                                    dictStrCustom = dictStrCustom,
                                    dictTValue = dictTValue,
                                    replyMsg = replyMsg
                                )
                            else:
                                dictTValue['tResult'] = '超出范围'
                                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strOdysseyRulesError'], dictTValue)
                                replyMsg(plugin_event, tmp_reply_str)
                        else:
                            dictTValue['tResult'] = '请输入数字'
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strOdysseyRulesError'], dictTValue)
                            replyMsg(plugin_event, tmp_reply_str)
        else:
            dictTValue['tResult'] = 'API连接失败'
            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strOdysseyRulesError'], dictTValue)
            replyMsg(plugin_event, tmp_reply_str)

def replyRULES_command_getResult(
    data_this,
    plugin_event,
    dictStrCustom,
    dictTValue,
    replyMsg
):
    if type(data_this) == dict and 'rule' in data_this and 'keyword' in data_this and 'content' in data_this:
        dictTValue['tResult'] = '[%s] - %s\n%s' % (
            data_this['rule'],
            data_this['keyword'],
            data_this['content']
        )
        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strOdysseyRulesShow'], dictTValue)
        replyMsg(plugin_event, tmp_reply_str)

def replyCnmodsList(mod_list_data, list_type, plugin_event, replyMsg, dictStrCustom, dictTValue):
    """
    统一处理cnmods列表显示
    """
    tmp_reply_str = None
    if mod_list_data != None and 'data' in mod_list_data and 'list' in mod_list_data['data'] and len(mod_list_data['data']['list']) > 0:
        tmp_res_list = []
        tmp_count = 0
        for mod_this in mod_list_data['data']['list']:
            tmp_count += 1
            tmp_res_list.append(
                '%d. [%s]%s' % (
                    tmp_count,
                    str(mod_this.get('keyId', 'N/A')),
                    mod_this.get('title', 'N/A')
                )
            )
        tmp_page_max = mod_list_data['data'].get('totalPages', 1)
        tmp_total_elements = mod_list_data['data'].get('totalElements', 0)
        tmp_page_now = mod_list_data['data'].get('page', 1)
        # 根据类型设置不同的页码标记
        if list_type == 'search':
            page_marker = '---[第%s/%s页 共%s项]---'
            dictTValue['tCnmodsResult'] = '%s\n%s' % (
                '\n'.join(tmp_res_list),
                page_marker % (str(tmp_page_now), str(tmp_page_max), str(tmp_total_elements))
            )
            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strOdysseyCnmodsSearch'], dictTValue)
        elif list_type == 'rec':
            page_marker = '---[第%s/%s页 共%s项 编辑推荐]---'
            dictTValue['tCnmodsResult'] = '%s\n%s' % (
                '\n'.join(tmp_res_list),
                page_marker % (str(tmp_page_now), str(tmp_page_max), str(tmp_total_elements))
            )
            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strOdysseyCnmodsRec'], dictTValue)
        elif list_type == 'author':
            page_marker = '---[第%s/%s页 共%s项 作者搜索]---'
            dictTValue['tCnmodsResult'] = '%s\n%s' % (
                '\n'.join(tmp_res_list),
                page_marker % (str(tmp_page_now), str(tmp_page_max), str(tmp_total_elements))
            )
            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strOdysseyCnmodsAuthor'], dictTValue)
        elif list_type == 'get':
            page_marker = '---[共%s项]---'
            dictTValue['tCnmodsResult'] = '%s\n%s' % (
                '\n'.join(tmp_res_list),
                page_marker % str(min(tmp_total_elements, 10))
            )
            tmp_reply_str = dictTValue['tCnmodsResult']
        elif list_type == 'get_search':
            page_marker = '---[第%s/%s页 共%s项]---'
            dictTValue['tCount'] = str(len(mod_list_data['data']['list']))
            dictTValue['tCnmodsResult'] = '%s\n%s' % (
                '\n'.join(tmp_res_list),
                page_marker % (str(tmp_page_now), str(tmp_page_max), str(tmp_total_elements))
            )
            tmp_reply_str = dictStrCustom['strOdysseyCnmodsGetMultiMatch'].format(**dictTValue)
        elif list_type == 'luck':
            page_marker = '---[第%s/%s页 共%s项 编辑推荐]---'
            dictTValue['tCnmodsResult'] = '%s\n%s' % (
                '\n'.join(tmp_res_list),
                page_marker % (str(tmp_page_now), str(tmp_page_max), str(tmp_total_elements))
            )
            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strOdysseyCnmodsLuck'], dictTValue)
    return tmp_reply_str

def replyCnmodsDetail(mod_data):
    """生成单个模组的详细信息字符串"""
    # 基础信息 
    tmp_header = '[%s]《%s》\n' % (str(mod_data.get('keyId', 'N/A')), mod_data.get('title', 'N/A'))
    # 标签信息
    tmp_tag_list = []
    for key_this in ['moduleType', 'moduleVersion', 'moduleAge', 'occurrencePlace', 'structure']:
        if key_this in mod_data and mod_data[key_this] != '':
            tmp_tag_list.append(mod_data[key_this])
    tmp_tags = ''
    if len(tmp_tag_list) > 0:
        tmp_tags = '%s\n' % ' - '.join(tmp_tag_list)
    # 作者信息
    tmp_author = '作者: %s\n' % mod_data.get('article', '')
    if not tmp_author:
        tmp_author = ''
    # 规模信息
    tmp_min_amount = mod_data.get('minAmount', 0)
    tmp_max_amount = mod_data.get('maxAmount', 0)
    tmp_min_duration = mod_data.get('minDuration', 0)
    tmp_max_duration = mod_data.get('maxDuration', 0)
    tmp_scale = ''
    if tmp_min_amount > 0 or tmp_max_amount > 0:
        tmp_scale = '规模: %d-%d人, %d-%d时\n' % (tmp_min_amount, tmp_max_amount, tmp_min_duration, tmp_max_duration)
    # 原创信息
    tmp_original = '原创: %s\n' % ('是' if mod_data.get('original', False) else '否')
    # 发布日期
    tmp_date = ''
    tmp_release_date = mod_data.get('releaseDate', '')
    if tmp_release_date:
        tmp_date = '发布日期: %s\n' % tmp_release_date
    # 简介
    tmp_intro = '简介: %s\n' % html.unescape(re.sub('\\</{0,1}(.+?)\\>', '', mod_data.get('opinion', '')))
    # 链接信息
    url_index = OlivaDiceOdyssey.cnmodsData.strCnmodsIndex
    url_index_mobile = OlivaDiceOdyssey.cnmodsData.strCnmodsIndexMobile
    tmp_key_id = str(mod_data.get('keyId', 'N/A'))
    tmp_pc_link = 'PC端链接: %s\n' % (url_index + tmp_key_id)
    tmp_mobile_link = '移动端链接: %s\n' % (url_index_mobile + tmp_key_id)
    # 下载地址
    tmp_download = ''
    tmp_download_url = mod_data.get('url', '')
    if tmp_download_url:
        tmp_download = '模组下载地址: %s' % tmp_download_url
    # 组装最终字符串
    tmp_cnmods_str = '%s%s%s%s%s%s%s%s%s%s' % (
        tmp_header,      # [编号]《标题》
        tmp_tags,        # 标签
        tmp_author,      # 作者: xxx
        tmp_scale,       # 规模: xxx
        tmp_original,    # 原创: xxx
        tmp_date,        # 发布日期: xxx
        tmp_intro,       # 简介: xxx
        tmp_pc_link,     # PC端链接: xxx
        tmp_mobile_link, # 移动端链接: xxx
        tmp_download,    # 下载地址: xxx
    )
    return tmp_cnmods_str
