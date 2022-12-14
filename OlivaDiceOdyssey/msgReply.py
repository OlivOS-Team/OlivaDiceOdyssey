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
    OlivaDiceOdyssey.msgCustomManager.initMsgCustom(Proc.Proc_data['bot_info_dict'])
    if 'replyContextFliter' in OlivaDiceCore.crossHook.dictHookList:
        OlivaDiceCore.crossHook.dictHookList['replyContextFliter'].append('rules')
        OlivaDiceCore.crossHook.dictHookList['replyContextFliter'].append('rule')

def unity_reply(plugin_event, Proc):
    OlivaDiceCore.userConfig.setMsgCount()
    dictTValue = OlivaDiceCore.msgCustom.dictTValue.copy()
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
    tmp_at_str_sub = None
    if 'sub_self_id' in plugin_event.data.extend:
        if plugin_event.data.extend['sub_self_id'] != None:
            tmp_at_str_sub = OlivOS.messageAPI.PARA.at(plugin_event.data.extend['sub_self_id']).CQ()
    tmp_command_str_1 = '.'
    tmp_command_str_2 = '。'
    tmp_command_str_3 = '/'
    tmp_reast_str = plugin_event.data.message
    flag_force_reply = False
    flag_is_command = False
    flag_is_from_host = False
    flag_is_from_group = False
    flag_is_from_group_admin = False
    flag_is_from_group_have_admin = False
    flag_is_from_master = False
    if isMatchWordStart(tmp_reast_str, '[CQ:reply,id='):
        tmp_reast_str = skipToRight(tmp_reast_str, ']')
        tmp_reast_str = tmp_reast_str[1:]
        if isMatchWordStart(tmp_reast_str, tmp_at_str):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, tmp_at_str)
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            flag_force_reply = True
    if isMatchWordStart(tmp_reast_str, tmp_at_str):
        tmp_reast_str = getMatchWordStartRight(tmp_reast_str, tmp_at_str)
        tmp_reast_str = skipSpaceStart(tmp_reast_str)
        flag_force_reply = True
    if tmp_at_str_sub != None:
        if isMatchWordStart(tmp_reast_str, tmp_at_str_sub):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, tmp_at_str_sub)
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            flag_force_reply = True
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
        elif isMatchWordStart(tmp_reast_str, 'cnmods', isCommand = True) or isMatchWordStart(tmp_reast_str, 'mdmz', isCommand = True) or isMatchWordStart(tmp_reast_str, 'modu', isCommand = True):
            if isMatchWordStart(tmp_reast_str, 'cnmods'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'cnmods')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_reast_str = tmp_reast_str.rstrip(' ')
            elif isMatchWordStart(tmp_reast_str, 'mdmz'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'mdmz')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_reast_str = tmp_reast_str.rstrip(' ')
            elif isMatchWordStart(tmp_reast_str, 'modu'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'modu')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_reast_str = tmp_reast_str.rstrip(' ')
            if isMatchWordStart(tmp_reast_str, 'search'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'search')
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
                    tmp_page = tmp_reast_str_list[-1]
                if tmp_title == None:
                    return
                tmp_res = OlivaDiceOdyssey.webTool.getCnmodsReq(title = tmp_title, page = tmp_page)
                if tmp_res != None:
                    try:
                        tmp_res_list = []
                        tmp_count = 0
                        tmp_page_max = 1
                        tmp_page_now = 1
                        if len(tmp_res['data']['list']) > 0:
                            for mod_this in tmp_res['data']['list']:
                                tmp_count += 1
                                tmp_res_list.append(
                                    '[%s] %s' % (
                                        str(tmp_count),
                                        mod_this['title']
                                    )
                                )
                            tmp_page_max = tmp_res['data']['totalPages']
                            tmp_page_now = tmp_page
                            dictTValue['tCnmodsResult'] = '%s\n---[第%s/%s页]---' % (
                                '\n'.join(tmp_res_list),
                                str(tmp_page_now),
                                str(tmp_page_max)
                            )
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strOdysseyCnmodsSearch'], dictTValue)
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
                            tmp_reply_str = '未找到相关魔都模组搜索结果'
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
                tmp_res = OlivaDiceOdyssey.webTool.getCnmodsReq(title = None, page = tmp_page)
                if tmp_res != None:
                    try:
                        tmp_res_list = []
                        tmp_count = 0
                        tmp_page_max = 1
                        tmp_page_now = 1
                        if len(tmp_res['data']['list']) > 0:
                            for mod_this in tmp_res['data']['list']:
                                tmp_count += 1
                                tmp_res_list.append(
                                    '[%s] %s' % (
                                        str(tmp_count),
                                        mod_this['title']
                                    )
                                )
                            tmp_page_max = tmp_res['data']['totalPages']
                            tmp_page_now = tmp_page
                            dictTValue['tCnmodsResult'] = '%s\n---[第%s/%s页]---' % (
                                '\n'.join(tmp_res_list),
                                str(tmp_page_now),
                                str(tmp_page_max)
                            )
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strOdysseyCnmodsLuck'], dictTValue)
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
                            tmp_reply_str = '未找到魔都模组推荐结果'
                    except:
                        pass
                if tmp_reply_str != None:
                    replyMsg(plugin_event, tmp_reply_str)
            elif isMatchWordStart(tmp_reast_str, 'roll'):
                tmp_reply_str = None
                tmp_page_count = None
                tmp_page = 1
                tmp_res = OlivaDiceOdyssey.webTool.getCnmodsReq(title = None, page = 1)
                if tmp_res != None:
                    try:
                        tmp_page_count = tmp_res['data']['totalPages']
                    except:
                        pass
                if tmp_page_count != None:
                    tmp_rd = OlivaDiceCore.onedice.RD(
                        '1D%s' % str(tmp_page_count)
                    )
                    tmp_rd.roll()
                    if tmp_rd.resError == None:
                        tmp_page = tmp_rd.resInt
                        tmp_res = OlivaDiceOdyssey.webTool.getCnmodsReq(title = None, page = tmp_page)
                        if tmp_res != None:
                            try:
                                tmp_rd_1 = OlivaDiceCore.onedice.RD(
                                    '1D%s' % str(len(tmp_res['data']['list']))
                                )
                                tmp_rd_1.roll()
                                if tmp_rd_1.resError == None:
                                    if tmp_rd_1.resInt > 0:
                                        tmp_get_res = tmp_res['data']['list'][tmp_rd_1.resInt - 1]
                                        tmp_tag_list = []
                                        tmp_tag_str = ''
                                        for key_this in [
                                            'moduleType',
                                            'moduleVersion',
                                            'moduleAge',
                                            'occurrencePlace',
                                            'structure'
                                        ]:
                                            if key_this in tmp_get_res:
                                                if tmp_get_res[key_this] != '':
                                                    tmp_tag_list.append(tmp_get_res[key_this])
                                        if len(tmp_tag_list) > 0:
                                            tmp_tag_str = '%s\n' % ' - '.join(tmp_tag_list)
                                        url_index = OlivaDiceOdyssey.cnmodsData.strCnmodsIndex
                                        tmp_cnmods_str = '《%s》\n%s%s\n链接：%s' % (
                                            tmp_get_res['title'],
                                            tmp_tag_str,
                                            html.unescape(re.sub('\\</{0,1}(.+?)\\>', '', tmp_get_res['opinion'])),
                                            url_index + str(tmp_get_res['keyId'])
                                        )
                                        tmp_reply_str = tmp_cnmods_str
                            except:
                                pass
                if tmp_reply_str != None:
                    replyMsg(plugin_event, tmp_reply_str)
            elif isMatchWordStart(tmp_reast_str, 'get'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'get')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_reast_str = tmp_reast_str.rstrip(' ')
                tmp_reply_str = None
                tmp_count_get = 1
                tmp_not_hit = '未找到所取魔都模组条目\n或许你应当先试试查找模组'
                tmp_res = OlivaDiceCore.userConfig.getUserConfigByKey(
                    userId = plugin_event.data.user_id,
                    userType = 'user',
                    platform = plugin_event.platform['platform'],
                    userConfigKey = 'cnmodsTemp',
                    botHash = plugin_event.bot_info.hash
                )
                if tmp_reast_str.isdigit():
                    tmp_count_get = int(tmp_reast_str)
                if tmp_count_get != None:
                    try:
                        if tmp_res != None:
                            if tmp_count_get >= 1 and tmp_count_get <= len(tmp_res['data']['list']):
                                tmp_get_res = tmp_res['data']['list'][tmp_count_get - 1]
                                tmp_tag_list = []
                                tmp_tag_str = ''
                                for key_this in [
                                    'moduleType',
                                    'moduleVersion',
                                    'moduleAge',
                                    'occurrencePlace',
                                    'structure'
                                ]:
                                    if key_this in tmp_get_res:
                                        if tmp_get_res[key_this] != '':
                                            tmp_tag_list.append(tmp_get_res[key_this])
                                if len(tmp_tag_list) > 0:
                                    tmp_tag_str = '%s\n' % ' - '.join(tmp_tag_list)
                                url_index = OlivaDiceOdyssey.cnmodsData.strCnmodsIndex
                                tmp_cnmods_str = '《%s》\n%s%s\n链接：%s' % (
                                    tmp_get_res['title'],
                                    tmp_tag_str,
                                    html.unescape(re.sub('\\</{0,1}(.+?)\\>', '', tmp_get_res['opinion'])),
                                    url_index + str(tmp_get_res['keyId'])
                                )
                                tmp_reply_str = tmp_cnmods_str
                            else:
                                tmp_reply_str = tmp_not_hit
                        else:
                            tmp_reply_str = tmp_not_hit
                    except:
                        pass
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
