#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：范立伟33139
@Date    ：2024/3/29 14:58
"""

MOCK_STEP_NUM_ID_DICT = {
    0: 12,
    1: 23,
    2: 34
}

MOCK_PARAM_1 = {
    "param_type": "12",
    "param_key": "id",
    "param_info": [
        "step[0]['response']['data']['id']",
        "123",
        123
    ],
    "child_list": []
}
MOCK_PARAM_RES_1 = '[<response["12"]["data"]["id"]>,"123",123]'

MOCK_PARAM_2 = {
    "param_type": "12",
    "param_key": "id",
    "param_info": "step[0]['response']['data']['id']",
    "child_list": []
}
MOCK_PARAM_RES_2 = '<response["12"]["data"]["id"]>'

MOCK_PARAM_3 = {
    "param_type": "12",
    "param_key": "id",
    "param_info": "step[0]['params']['data']['id']",
    "child_list": []
}
MOCK_PARAM_RES_3 = '<requestBody["12"]["data"]["id"]>'

MOCK_PARAM_4 = {
    "param_type": "12",
    "param_key": "id",
    "param_info": "step[1]['url_param']['data']['id']",
    "child_list": []
}
MOCK_PARAM_RES_4 = '<queryParams["23"]["data"]["id"]>'

MOCK_PARAM_5 = {
    "param_type": "12",
    "param_key": "id",
    "param_info": "step[2]['restful_param']['data']['id']",
    "child_list": []
}
MOCK_PARAM_RES_5 = '<restParams["34"]["data"]["id"]>'

MOCK_PARAM_6 = {
    "param_type": "12",
    "param_key": "nameList",
    "param_info": "",
    "child_list": [
        {
            "param_type": "13",
            "param_key": "item[0]",
            "param_info": "",
            "is_arr_item": True,
            "child_list": [
                {
                    "param_type": "0",
                    "param_key": "",
                    "param_info": "step[0][\"params\"][\"name\"]",
                    "child_list": []
                },
                {
                    "param_type": "0",
                    "param_key": "",
                    "param_info": "123",
                    "child_list": []
                }
            ]}
    ]
}
MOCK_PARAM_RES_6 = '<requestBody["12"]["name"]>'
