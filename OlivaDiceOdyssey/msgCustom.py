# -*- encoding: utf-8 -*-
'''
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/   
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___   
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/   

@File      :   msgCustom.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import OlivaDiceCore
import OlivaDiceOdyssey

dictConsoleSwitchTemplate = {
    'default' : {
        'odysseyRulesItemLimit': 8,
        'odysseyKOOKBotMarketPulseEnable': 0,
        'odysseyKOOKPlayGameMode': 1,
        'odysseyKOOKPlayGameMusicSoftware': 0
    }
}

dictStrCustomDict = {}

dictStrCustom = {
    'strOdysseyCnmodsSearch': '魔都模组搜索结果如下:\n{tCnmodsResult}',
    'strOdysseyCnmodsRec': '魔都模组编辑推荐结果如下:\n{tCnmodsResult}',
    'strOdysseyCnmodsAuthor': '作者模组搜索结果如下:\n{tCnmodsResult}',
    'strOdysseyCnmodsLuck': '魔都模组随机如下:\n{tCnmodsResult}',
    'strOdysseyCnmodsSearchNotFound': '未找到相关魔都模组搜索结果',
    'strOdysseyCnmodsRecNotFound': '未找到相关魔都模组编辑推荐结果',
    'strOdysseyCnmodsAuthorNotFound': '未找到该作者的魔都模组',
    'strOdysseyCnmodsLuckNotFound': '未找到魔都模组推荐结果',
    'strOdysseyCnmodsFindNotFound': '未找到该模组(keyId: {tKeyId})',
    'strOdysseyCnmodsFindError': '获取模组详情失败',
    'strOdysseyCnmodsFindErrorRetry': '获取模组详情失败，请稍后再试',
    'strOdysseyCnmodsFindOnlyNumber': 'find命令只接受纯数字keyId\n例如: .cnmods find 12345',
    'strOdysseyCnmodsGetCacheNotFound': '未找到缓存的模组列表\n或许你应当先试试查找模组',
    'strOdysseyCnmodsGetRangeError': '序号超出范围(1-{tRange})\n或许你应当先试试查找模组',
    'strOdysseyCnmodsGetSearchNotFound': '未找到相关魔都模组',
    'strOdysseyCnmodsGetSearchError': '搜索失败，请稍后再试',
    'strOdysseyCnmodsGetMultiMatch': '找到[{tCount}]个匹配的模组:\n{tCnmodsResult}',
    'strOdysseyRulesNone': '没有找到合适的规则',
    'strOdysseyRulesShow': '规则速查结果如下:\n{tResult}',
    'strOdysseyRulesList': '规则速查找到如下待选结果:\n{tResult}\n输入序号以查看对应结果',
    'strOdysseyRulesSplit': '\n',
    'strOdysseyRulesError': '规则速查发生错误:\n{tResult}',
    'strOdysseyKOOKBotMarketPulseUUID': '-',
    'strOdysseyKOOKPlayGameMusicName': '-',
    'strOdysseyKOOKPlayGameMusicSinger': '-',
    'strOdysseyKOOKPlayGameID': '6',
}

dictStrConst = {
}

dictGValue = {
}

dictTValue = {
    'tCnmodsResult': 'N/A'
}

dictHelpDocTemp = {
    'cnmods': '''魔都模组模块:
[.cnmods roll]    在线抽取一个模组
[.cnmods luck ([页码])]    查看魔都推荐
[.cnmods search [关键字] ([页码])]    在线查找模组
[.cnmods rec [关键字] ([页码])]    搜索编辑推荐
[.cnmods author [作者名] ([页码])]    搜索指定作者
[.cnmods find [编号]]    通过编号直接查找模组详情
[.cnmods get [序号/名称]]    获取对应模组
本模块所实现功能已获魔都模组官方授权，未经允许不得擅自用于二次发布''',

    'OlivaDiceOdyssey': '''[OlivaDiceOdyssey]
OlivaDice高阶模块
本模块为青果跑团掷骰机器人(OlivaDice)高阶模块，集成与跑团相关但不是必须的或是版权受限的功能。
核心开发者: lunzhiPenxil仑质
[.help OlivaDiceOdyssey更新] 查看本模块更新日志
注: 本模块为可选模块。''',

    'OlivaDiceOdyssey更新': '''[OlivaDiceOdyssey]
3.0.2: 支持新版OlivOS
3.0.0: 初始化项目''',

    '魔都模组': '&cnmods',
}

dictUserConfigNoteDefault = {
    'cnmodsTemp': None
}
