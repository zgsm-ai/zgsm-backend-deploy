#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：范立伟33139
@Date    ：2024/8/27 20:37
"""

mock_manual_case_data_no_post = {
    "display_name": "范立伟33139",
    "case_code": "WeakPWD_Func_Default_01_001_os",
    "case_id": 2798507,
    "case_name": "默认弱口令设置测试",
    "case_pre_step": "1.AF设备运行正常；",
    "case_step": "1. 新建web应用防护模板P1，仅启用口令防护；   <br>2. 检查高级配置中口令防护选项默认配置；   <br>3. 新增安全防护策略，仅启用web应用防护，引用模板为P1   <br>4. PC通过AF访问web服务，输入账号密码登录，密码为8位纯字母   <br>5.修改系统时间为10分钟后，在安全日志查看弱口令日志信息；",
    "case_expect": "2.web口令防护设置全勾选  <br>5.在安全日志中能查看到WEB登录明文传输检测日志信息；",
    "case_post_step": "",
    "case_remark": "[AT_GIT_URL][林贤杰11956] 默认弱口令设置测试.robot  <br>1.默认弱口令设置；",
    "case_level": "BVT",
    "case_module": "基线/01-新架构用例基线/002-安全能力[bvt986,手动475-UI172]/04-策略(Strategy)/02-安全基础能力-蒋世齐/01-WAF(周梦园)/01-传统防护/01-基础防护能力/04-口令防护/02-WEB登录弱口令检测/02-功能效果/01-口令设置方式测试/01-默认弱口令设置/默认弱口令设置测试",
    "product_id": 17,
    "product_name": "AF"
}

mock_no_post_expect_result = """
*** Settings ***
Resource    resource/common/keywords.robot
Test Setup     _setup

*** Test Cases ***
BVT-默认弱口令设置测试
    [Tags]    级别-BVT    ID-WeakPWD_Func_Default_01_001_os    状态-未调试    拓扑-待补充    作者-千流AI    系统ID-2798507

    #@step   1. 新建web应用防护模板P1，仅启用口令防护；
    新增WEB应用防护模板    模板名称=P1    应用隐藏=否    口令防护=是    权限控制=否    数据泄密防护=否    HTTP异常检测=否    漏洞防扫描=否    期望结果=成功

    #@step   2. 检查高级配置中口令防护选项默认配置；
    #@expect 2.web口令防护设置全勾选
    检查WEB应用防护模板配置    模板名称=P1    口令防护=是    期望结果=成功

    #@step   3. 新增安全防护策略，仅启用web应用防护，引用模板为P1
    新增安全策略    名称=web_protection    类型=server    源区域=lan    目的区域=wan    WEB应用防护=是    WEB应用防护模版=P1    动作=permit    期望结果=成功
    等待    时间=5

    #@step   4. PC通过AF访问web服务，输入账号密码登录，密码为8位纯字母
    账号密码登录控制台    网关IP=${AF_IP}    用户名=admin    密码=abcdefgh    期望结果=成功

    #@step   5.修改系统时间为10分钟后，在安全日志查看弱口令日志信息；
    #@expect 5.在安全日志中能查看到WEB登录明文传输检测日志信息；
    CLI    设备名称=dut1    命令=config; clock time ${10分钟后时间}; clock date ${当前日期}
    syslog日志检查    设备名称=${DeviceName}    日志类型=WEB应用防护    查询结果检查点=WEB登录明文传输检测    检查次数=5    期望结果=成功

*** Keywords ***
_setup
    #@step   1.AF设备运行正常；
    检查AF设备状态    设备名称=${DeviceName}    期望结果=成功
"""


mock_manual_case_data_no_pre = {
    "display_name": "范立伟33139",
    "case_code": "WeakPWD_Func_Default_01_001_os",
    "case_id": 2798507,
    "case_name": "默认弱口令设置测试",
    "case_pre_step": "",
    "case_step": "1. 新建web应用防护模板P1，仅启用口令防护；   <br>2. 检查高级配置中口令防护选项默认配置；   <br>3. 新增安全防护策略，仅启用web应用防护，引用模板为P1   <br>4. PC通过AF访问web服务，输入账号密码登录，密码为8位纯字母   <br>5.修改系统时间为10分钟后，在安全日志查看弱口令日志信息；",
    "case_expect": "2.web口令防护设置全勾选  <br>5.在安全日志中能查看到WEB登录明文传输检测日志信息；",
    "case_post_step": "1.删除web应用防护模板P1",
    "case_remark": "[AT_GIT_URL][林贤杰11956] 默认弱口令设置测试.robot  <br>1.默认弱口令设置；",
    "case_level": "BVT",
    "case_module": "基线/01-新架构用例基线/002-安全能力[bvt986,手动475-UI172]/04-策略(Strategy)/02-安全基础能力-蒋世齐/01-WAF(周梦园)/01-传统防护/01-基础防护能力/04-口令防护/02-WEB登录弱口令检测/02-功能效果/01-口令设置方式测试/01-默认弱口令设置/默认弱口令设置测试",
    "product_id": 17,
    "product_name": "AF"
}

mock_no_pre_expect_result = """
*** Settings ***
Resource    resource/common/keywords.robot
Test Teardown    _teardown

*** Test Cases ***
BVT-默认弱口令设置测试
    [Tags]    级别-BVT    ID-WeakPWD_Func_Default_01_001_os    状态-未调试    拓扑-待补充    作者-千流AI    系统ID-2798507

    #@step   1. 新建web应用防护模板P1，仅启用口令防护；
    新增WEB应用防护模板    模板名称=P1    应用隐藏=否    口令防护=是    权限控制=否    数据泄密防护=否    HTTP异常检测=否    漏洞防扫描=否    期望结果=成功

    #@step   2. 检查高级配置中口令防护选项默认配置；
    #@expect 2.web口令防护设置全勾选
    检查WEB应用防护模板配置    模板名称=P1    口令防护=是    期望结果=成功

    #@step   3. 新增安全防护策略，仅启用web应用防护，引用模板为P1
    新增安全策略    名称=web_protection    类型=server    源区域=lan    目的区域=wan    WEB应用防护=是    WEB应用防护模版=P1    动作=permit    期望结果=成功
    等待    时间=5

    #@step   4. PC通过AF访问web服务，输入账号密码登录，密码为8位纯字母
    账号密码登录控制台    网关IP=${AF_IP}    用户名=admin    密码=abcdefgh    期望结果=成功

    #@step   5.修改系统时间为10分钟后，在安全日志查看弱口令日志信息；
    #@expect 5.在安全日志中能查看到WEB登录明文传输检测日志信息；
    CLI    设备名称=dut1    命令=config; clock time ${10分钟后时间}; clock date ${当前日期}
    syslog日志检查    设备名称=${DeviceName}    日志类型=WEB应用防护    查询结果检查点=WEB登录明文传输检测    检查次数=5    期望结果=成功

*** Keywords ***
_teardown
    #@step   1.删除web应用防护模板P1
    删除WEB应用防护模板    模板名称=P1    期望结果=成功
"""

mock_robot_case = """
*** Settings ***
Resource    resource/common/keywords.robot
Test Setup     _setup
Test Teardown    _teardown

*** Test Cases ***
BVT-默认弱口令设置测试
    [Tags]    级别-BVT    ID-WeakPWD_Func_Default_01_001_os    状态-未调试    拓扑-待补充    作者-千流AI    系统ID-2798507

    #@step   1. 新建web应用防护模板P1，仅启用口令防护
    新增WEB应用防护模板    模板名称=P1    应用隐藏=否    口令防护=是    权限控制=否    数据泄密防护=否    HTTP异常检测=否    漏洞防扫描=否    期望结果=成功

    #@step   2. 检查高级配置中口令防护选项默认配置
    检查WEB应用防护模板配置    模板名称=P1    口令防护=是    期望结果=成功

    #@step   3. 新增安全防护策略，仅启用web应用防护，引用模板为P1
    新增安全策略    名称=web_protection    类型=server    源区域=lan    目的区域=wan    WEB应用防护=是    WEB应用防护模版=P1    动作=permit    期望结果=成功
    等待    时间=5

    #@step   4. PC通过AF访问web服务，输入账号密码登录，密码为8位纯字母
    #@expect
    账号密码登录控制台    网关IP=${AF_IP}    用户名=admin    密码=abcdefgh    期望结果=成功

    #@step   5. 修改系统时间为10分钟后，在安全日志查看弱口令日志信息
    #@expect 5. 在安全日志中能查看到WEB登录明文传输检测日志信息
    CLI    设备名称=dut1    命令=config; clock time ${10分钟后时间}; clock date ${当前日期}
    syslog日志检查    设备名称=${DeviceName}    日志类型=WEB应用防护    查询结果检查点=WEB登录明文传输检测    检查次数=5    期望结果=成功

*** Keywords ***
_setup
    #@step   1. AF设备运行正常123
    检查AF设备状态    设备名称=${DeviceName}    期望结果=成功

_teardown
    #@step   1. 删除web应用防护模板P1 123
    删除WEB应用防护模板    模板名称=P1    期望结果=成功
"""

mock_step_map_expect = [
    [0, ""],
    [1, 0],
    [2, ""],
    [3, ""],
    [4, 1],
]
