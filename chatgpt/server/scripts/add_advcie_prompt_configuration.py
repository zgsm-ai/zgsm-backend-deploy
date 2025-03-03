# flake8: noqa
from peewee import fn
import json

from services.system.configuration_service import ConfigurationService

# pylint: disable
prompt_template = """
## Instructions
You play a senior front-end engineer. The following user input is the expression of requirements and existing code for front-end component code generation.
Your task is to think along the following lines, and finally guess and polish the user’s expression of requirements:
1. Understand user needs and identify whether user needs are related to front-end components.
2. If it has nothing to do with front-end components, the problem of clear expression of requirements will not be considered and the expression will be considered clear,and the "is_problem" field will be false.
3. If it is related to front-end components, further identify whether the requirements are clearly expressed.
3.1 If the requirements are not expressed clearly enough, please provide at least 3 polished results of the requirements.
3.2 If the requirements are already clearly expressed, there is no need to polish the requirements.
4. Unclear definition: the desired components are not clearly stated, and there is a problem with the grammar.
5. It is assumed that the technology stack used is already known, and the description of the technology stack is not considered when polishing.
Please think step by step.

## output field explanation
is_problem: 表达清晰为true，表达不清晰为false
result: 如果表达不清晰，则把结果放到result里面，否则为空数组
understand: 是否能理解用户需求
msg: 不能理解用户需求时返回给用户查看的提示

## example 1
### input
#### requirement
新增提示，操作成功
#### selected code
无
### 思考过程
需求跟前端组件相关，新增提示没有说明清楚提示的组件是什么，猜测可能是一个提示框，弹窗或者通知组件。所以对requirement的润色结果为result里面的内容，"is_problem": true。
### output
```json
{
    "is_problem": true,
    "result": [
        "在页面中添加一个提示框，提示框内容为“操作成功”",
        "在页面中添加一个弹窗，弹窗内容为“操作成功”",
        "在页面中添加一个通知，通知内容为“操作成功”"
    ],
    "understand": true,
    "msg": ""
}
```

## example 2
### input
#### requirement
在页面中添加一个提示框，提示框内容为“操作成功”。
#### selected code
无
### 思考过程
需求跟前端组件相关，已经说清楚了是添加一个提示框组件，生成一个提示框代码并提示操作成功，所以没有问题，"is_problem": false。
### output
```json
{
    "is_problem": false
    "result": [],
    "understand": true,
    "msg": ""
}
```

## example 3
### input
#### requirement
解释并给这段代码添加注释
#### selected code
print(12)
### 思考过程
需求跟前端组件无关，不考虑需求是否表达清晰，"is_problem": false
### output
```json
{
    "is_problem": false
    "result": [],
    "understand": true,
    "msg": ""
}
```

## example 4
### input
#### requirement
sdfsdfdsf
#### selected code
print(12)
### 思考过程
输入的内容无法理解, "understand": true
### output
```json
{
    "is_problem": false
    "result": [],
    "understand": false,
    "msg": "你描述的内容无法理解,请提供更明确的需求描述"
}
```

## input
### requirement
{user_prompt}
### selected code
{code}

## output
"""


class AddAdvicePrompt:

    @classmethod
    def run(cls):
        cls.insert_prompt_data()
        cls.insert_switch_data()

    @staticmethod
    def insert_prompt_data():
        """添加语言规范化的prompt"""
        prompt_data = {'deleted': False, 'belong_type': 'prompt_template', 'attribute_key': 'giveAdvice',
                       'attribute_value': prompt_template, 'desc': "用户描述语言规范化"}
        advice_prompt = ConfigurationService.get_configuration(
            prompt_data['belong_type'], prompt_data['attribute_key'])
        if advice_prompt:
            print("advice_prompt 配置已经存在")
        else:
            # 获取下一个可用的id
            max_id = ConfigurationService.dao.model.select(fn.MAX(ConfigurationService.dao.model.id)).scalar()
            next_id = max_id + 1 if max_id else 1
            prompt_data['id'] = next_id
            ConfigurationService.create(**prompt_data)
            print("advice_prompt 配置写入成功")

    @staticmethod
    def insert_switch_data():
        switch_data = {'deleted': False, 'belong_type': "permission", 'attribute_key': "advice_white_list_switch",
                       'attribute_value': json.dumps({"advice_switch": True, "dept_prefix": []}), 'desc': "问答语言规范化的开关"}

        advice_switch_json_str = ConfigurationService.get_configuration(
            switch_data['belong_type'], switch_data['attribute_key'])
        if advice_switch_json_str:
            print("advice_switch 配置已经存在")
        else:
            # 获取下一个可用的id
            max_id = ConfigurationService.dao.model.select(fn.MAX(ConfigurationService.dao.model.id)).scalar()
            next_id = max_id + 1 if max_id else 1
            switch_data['id'] = next_id
            ConfigurationService.create(**switch_data)
            print("advice_switch 配置写入成功")
