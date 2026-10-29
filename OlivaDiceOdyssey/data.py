# -*- encoding: utf-8 -*-
r"""
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/

@File      :   data.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2026, OlivOS-Team
@Desc      :   None
"""

OlivaDiceOdyssey_ver = '3.0.19'
OlivaDiceOdyssey_svn = 20
OlivaDiceOdyssey_ver_short = '%s(%s)' % (str(OlivaDiceOdyssey_ver), str(OlivaDiceOdyssey_svn))

# 牌堆资源包的临时下载文件（相对 OlivaDiceCore.data.dataDirRoot）
deckResourceTmpFile = '/unity/update/tmp_deck_resource.zip'
# 牌堆资源包解压到 OlivOS 的资源目录（图片等）
deckResourceExtractDir = './data'

gProc = None
