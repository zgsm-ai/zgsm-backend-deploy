#!/usr/bin/env python
# -*- coding: UTF-8 -*-

mock_manual_case_data_no_post = {
    "display_name": "Fan Liwei",
    "case_code": "WeakPWD_Func_Default_01_001_os",
    "case_id": 2798507,
    "case_name": "Default Weak Password Setting Test",
    "case_pre_step": "1. AF device running normally;",
    "case_step": "1. Create a new web application protection template P1, only enable password protection;   <br>2. Check the default configuration of password protection options in advanced configuration;   <br>3. Add a new security protection policy, only enable web application protection, use template P1   <br>4. PC accesses web services through AF, enter account password to log in, the password is 8 digits of pure letters   <br>5. Change the system time to 10 minutes later, check the weak password log information in the security log;",
    "case_expect": "2. All web password protection settings are checked  <br>5. WEB login plaintext transmission detection log information can be found in the security log;",
    "case_post_step": "",
    "case_remark": "[AT_GIT_URL][Lin Xianjie11956] Default Weak Password Setting Test.robot  <br>1. Default weak password setting;",
    "case_level": "BVT",
    "case_module": "Baseline/01-New Architecture Case Baseline/002-Security Capability[bvt986,manual475-UI172]/04-Strategy(Strategy)/02-Basic Security Capability-Jiang Shiqi/01-WAF(Zhou Mengyuan)/01-Traditional Protection/01-Basic Protection Capability/04-Password Protection/02-WEB Login Weak Password Detection/02-Functional Effect/01-Password Setting Method Test/01-Default Weak Password Setting/Default Weak Password Setting Test",
    "product_id": 17,
    "product_name": "AF"
}

mock_no_post_expect_result = """
*** Settings ***
Resource    resource/common/keywords.robot
Test Setup     _setup

*** Test Cases ***
BVT-Default Weak Password Setting Test
    [Tags]    Level-BVT    ID-WeakPWD_Func_Default_01_001_os    Status-Not Debugged    Topology-To Be Added    Author-Qianliu AI    SystemID-2798507

    #@step   1. Create a new web application protection template P1, only enable password protection;
    Add WEB Application Protection Template    TemplateName=P1    ApplicationHiding=No    PasswordProtection=Yes    AccessControl=No    DataLeakageProtection=No    HTTPAnomalyDetection=No    VulnerabilityProtection=No    ExpectedResult=Success

    #@step   2. Check the default configuration of password protection options in advanced configuration;
    #@expect 2. All web password protection settings are checked
    Check WEB Application Protection Template Configuration    TemplateName=P1    PasswordProtection=Yes    ExpectedResult=Success

    #@step   3. Add a new security protection policy, only enable web application protection, use template P1
    Add Security Policy    Name=web_protection    Type=server    SourceZone=lan    DestinationZone=wan    WEBApplicationProtection=Yes    WEBApplicationProtectionTemplate=P1    Action=permit    ExpectedResult=Success
    Wait    Time=5

    #@step   4. PC accesses web services through AF, enter account password to log in, the password is 8 digits of pure letters
    Login Console with Account Password    GatewayIP=${AF_IP}    Username=admin    Password=abcdefgh    ExpectedResult=Success

    #@step   5. Change the system time to 10 minutes later, check the weak password log information in the security log;
    #@expect 5. WEB login plaintext transmission detection log information can be found in the security log;
    CLI    DeviceName=dut1    Command=config; clock time ${10MinutesLaterTime}; clock date ${CurrentDate}
    Check Syslog    DeviceName=${DeviceName}    LogType=WEB Application Protection    QueryResultCheckPoint=WEB Login Plaintext Transmission Detection    CheckTimes=5    ExpectedResult=Success

*** Keywords ***
_setup
    #@step   1. AF device running normally;
    Check AF Device Status    DeviceName=${DeviceName}    ExpectedResult=Success
"""


mock_manual_case_data_no_pre = {
    "display_name": "Fan Liwei",
    "case_code": "WeakPWD_Func_Default_01_001_os",
    "case_id": 2798507,
    "case_name": "Default Weak Password Setting Test",
    "case_pre_step": "",
    "case_step": "1. Create a new web application protection template P1, only enable password protection;   <br>2. Check the default configuration of password protection options in advanced configuration;   <br>3. Add a new security protection policy, only enable web application protection, use template P1   <br>4. PC accesses web services through AF, enter account password to log in, the password is 8 digits of pure letters   <br>5. Change the system time to 10 minutes later, check the weak password log information in the security log;",
    "case_expect": "2. All web password protection settings are checked  <br>5. WEB login plaintext transmission detection log information can be found in the security log;",
    "case_post_step": "1. Delete web application protection template P1",
    "case_remark": "[AT_GIT_URL][Lin Xianjie11956] Default Weak Password Setting Test.robot  <br>1. Default weak password setting;",
    "case_level": "BVT",
    "case_module": "Baseline/01-New Architecture Case Baseline/002-Security Capability[bvt986,manual475-UI172]/04-Strategy(Strategy)/02-Basic Security Capability-Jiang Shiqi/01-WAF(Zhou Mengyuan)/01-Traditional Protection/01-Basic Protection Capability/04-Password Protection/02-WEB Login Weak Password Detection/02-Functional Effect/01-Password Setting Method Test/01-Default Weak Password Setting/Default Weak Password Setting Test",
    "product_id": 17,
    "product_name": "AF"
}

mock_no_pre_expect_result = """
*** Settings ***
Resource    resource/common/keywords.robot
Test Teardown    _teardown

*** Test Cases ***
BVT-Default Weak Password Setting Test
    [Tags]    Level-BVT    ID-WeakPWD_Func_Default_01_001_os    Status-Not Debugged    Topology-To Be Added    Author-Qianliu AI    SystemID-2798507

    #@step   1. Create a new web application protection template P1, only enable password protection;
    Add WEB Application Protection Template    TemplateName=P1    ApplicationHiding=No    PasswordProtection=Yes    AccessControl=No    DataLeakageProtection=No    HTTPAnomalyDetection=No    VulnerabilityProtection=No    ExpectedResult=Success

    #@step   2. Check the default configuration of password protection options in advanced configuration;
    #@expect 2. All web password protection settings are checked
    Check WEB Application Protection Template Configuration    TemplateName=P1    PasswordProtection=Yes    ExpectedResult=Success

    #@step   3. Add a new security protection policy, only enable web application protection, use template P1
    Add Security Policy    Name=web_protection    Type=server    SourceZone=lan    DestinationZone=wan    WEBApplicationProtection=Yes    WEBApplicationProtectionTemplate=P1    Action=permit    ExpectedResult=Success
    Wait    Time=5

    #@step   4. PC accesses web services through AF, enter account password to log in, the password is 8 digits of pure letters
    Login Console with Account Password    GatewayIP=${AF_IP}    Username=admin    Password=abcdefgh    ExpectedResult=Success

    #@step   5. Change the system time to 10 minutes later, check the weak password log information in the security log;
    #@expect 5. WEB login plaintext transmission detection log information can be found in the security log;
    CLI    DeviceName=dut1    Command=config; clock time ${10MinutesLaterTime}; clock date ${CurrentDate}
    Check Syslog    DeviceName=${DeviceName}    LogType=WEB Application Protection    QueryResultCheckPoint=WEB Login Plaintext Transmission Detection    CheckTimes=5    ExpectedResult=Success

*** Keywords ***
_teardown
    #@step   1. Delete web application protection template P1
    Delete WEB Application Protection Template    TemplateName=P1    ExpectedResult=Success
"""

mock_robot_case = """
*** Settings ***
Resource    resource/common/keywords.robot
Test Setup     _setup
Test Teardown    _teardown

*** Test Cases ***
BVT-Default Weak Password Setting Test
    [Tags]    Level-BVT    ID-WeakPWD_Func_Default_01_001_os    Status-Not Debugged    Topology-To Be Added    Author-Qianliu AI    SystemID-2798507

    #@step   1. Create a new web application protection template P1, only enable password protection
    Add WEB Application Protection Template    TemplateName=P1    ApplicationHiding=No    PasswordProtection=Yes    AccessControl=No    DataLeakageProtection=No    HTTPAnomalyDetection=No    VulnerabilityProtection=No    ExpectedResult=Success

    #@step   2. Check the default configuration of password protection options in advanced configuration
    Check WEB Application Protection Template Configuration    TemplateName=P1    PasswordProtection=Yes    ExpectedResult=Success

    #@step   3. Add a new security protection policy, only enable web application protection, use template P1
    Add Security Policy    Name=web_protection    Type=server    SourceZone=lan    DestinationZone=wan    WEBApplicationProtection=Yes    WEBApplicationProtectionTemplate=P1    Action=permit    ExpectedResult=Success
    Wait    Time=5

    #@step   4. PC accesses web services through AF, enter account password to log in, the password is 8 digits of pure letters
    #@expect
    Login Console with Account Password    GatewayIP=${AF_IP}    Username=admin    Password=abcdefgh    ExpectedResult=Success

    #@step   5. Change the system time to 10 minutes later, check the weak password log information in the security log
    #@expect 5. WEB login plaintext transmission detection log information can be found in the security log
    CLI    DeviceName=dut1    Command=config; clock time ${10MinutesLaterTime}; clock date ${CurrentDate}
    Check Syslog    DeviceName=${DeviceName}    LogType=WEB Application Protection    QueryResultCheckPoint=WEB Login Plaintext Transmission Detection    CheckTimes=5    ExpectedResult=Success

*** Keywords ***
_setup
    #@step   1. AF device running normally123
    Check AF Device Status    DeviceName=${DeviceName}    ExpectedResult=Success

_teardown
    #@step   1. Delete web application protection template P1 123
    Delete WEB Application Protection Template    TemplateName=P1    ExpectedResult=Success
"""

mock_step_map_expect = [
    [0, ""],
    [1, 0],
    [2, ""],
    [3, ""],
    [4, 1],
]
