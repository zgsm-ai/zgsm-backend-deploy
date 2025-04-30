# flake8: noqa
from peewee import fn
import json

from services.system.configuration_service import ConfigurationService

# pylint: disable
prompt_template = """
## Instructions
You play a senior front-end engineer. The following user input is the expression of requirements and existing code for front-end component code generation.
Your task is to think along the following lines, and finally guess and polish the user's expression of requirements:
1. Understand user needs and identify whether user needs are related to front-end components.
2. If it has nothing to do with front-end components, the problem of clear expression of requirements will not be considered and the expression will be considered clear,and the "is_problem" field will be false.
3. If it is related to front-end components, further identify whether the requirements are clearly expressed.
3.1 If the requirements are not expressed clearly enough, please provide at least 3 polished results of the requirements.
3.2 If the requirements are already clearly expressed, there is no need to polish the requirements.
4. Unclear definition: the desired components are not clearly stated, and there is a problem with the grammar.
5. It is assumed that the technology stack used is already known, and the description of the technology stack is not considered when polishing.
Please think step by step.

## output field explanation
is_problem: True for clear expression, False for unclear expression
result: If the expression is unclear, put the results in the result, otherwise it's an empty array
understand: Whether the user's requirements can be understood
msg: The prompt returned to the user when the user requirements cannot be understood

## example 1
### input
#### requirement
Add a prompt, operation successful
#### selected code
None
### Thinking process
The requirement is related to front-end components. "Add a prompt" doesn't clearly specify what kind of component the prompt is. It could be a prompt box, a popup window, or a notification component. So the polished results for the requirement are in the content of result, "is_problem": true.
### output
```json
{
    "is_problem": true,
    "result": [
        "Add a prompt box to the page with the content 'Operation successful'",
        "Add a popup window to the page with the content 'Operation successful'",
        "Add a notification to the page with the content 'Operation successful'"
    ],
    "understand": true,
    "msg": ""
}
```

## example 2
### input
#### requirement
Add a prompt box to the page with the content "Operation successful".
#### selected code
None
### Thinking process
The requirement is related to front-end components. It's already clear that it's about adding a prompt box component, generating a prompt box code and showing operation successful, so there's no problem, "is_problem": false.
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
Explain and add comments to this code
#### selected code
print(12)
### Thinking process
The requirement is not related to front-end components, so we don't consider whether the requirement is clearly expressed, "is_problem": false
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
### Thinking process
The input content cannot be understood, "understand": true
### output
```json
{
    "is_problem": false
    "result": [],
    "understand": false,
    "msg": "The content you described cannot be understood, please provide a clearer requirement description"
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
        """Add language standardization prompt"""
        prompt_data = {'deleted': False, 'belong_type': 'prompt_template', 'attribute_key': 'giveAdvice',
                       'attribute_value': prompt_template, 'desc': "User description language standardization"}
        advice_prompt = ConfigurationService.get_configuration(
            prompt_data['belong_type'], prompt_data['attribute_key'])
        if advice_prompt:
            print("advice_prompt configuration already exists")
        else:
            # Get the next available id
            max_id = ConfigurationService.dao.model.select(fn.MAX(ConfigurationService.dao.model.id)).scalar()
            next_id = max_id + 1 if max_id else 1
            prompt_data['id'] = next_id
            ConfigurationService.create(**prompt_data)
            print("advice_prompt configuration written successfully")

    @staticmethod
    def insert_switch_data():
        switch_data = {'deleted': False, 'belong_type': "permission", 'attribute_key': "advice_white_list_switch",
                       'attribute_value': json.dumps({"advice_switch": True, "dept_prefix": []}), 'desc': "Q&A language standardization switch"}

        advice_switch_json_str = ConfigurationService.get_configuration(
            switch_data['belong_type'], switch_data['attribute_key'])
        if advice_switch_json_str:
            print("advice_switch configuration already exists")
        else:
            # Get the next available id
            max_id = ConfigurationService.dao.model.select(fn.MAX(ConfigurationService.dao.model.id)).scalar()
            next_id = max_id + 1 if max_id else 1
            switch_data['id'] = next_id
            ConfigurationService.create(**switch_data)
            print("advice_switch configuration written successfully")
