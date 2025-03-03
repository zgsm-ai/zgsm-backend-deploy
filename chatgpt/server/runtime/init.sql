-- api_rule 规则
INSERT INTO "public"."api_rule"("id", "deleted", "created_at", "update_at", "rule_type", "rule_info") VALUES (1, 'f', '2023-05-09 19:09:36', '2023-05-09 19:09:36', 'dept', '研发体系');


-- configuration 配置项
INSERT INTO "public"."configuration"("id", "deleted", "created_at", "update_at", "belong_type", "attribute_key", "attribute_value", "desc") VALUES (38, 'f', '2023-10-25 15:52:15', '2023-10-25 17:53:50.717441', 'prompt_template', 'simplifyCode', '```{language}
{selectedText}
```
Remove unnecessary code, like log statements and unused variables. Leave the rest of the code the same.', '精简代码');
INSERT INTO "public"."configuration"("id", "deleted", "created_at", "update_at", "belong_type", "attribute_key", "attribute_value", "desc") VALUES (37, 'f', '2023-10-26 10:44:08', '2023-10-26 10:44:08', 'prompt_template', 'scribe_merge_code', '## Instructions
You are now a senior front-end engineer.
The output consists of three parts: the requirements, the original code, and the developed code.
Background: The developed code is based on the original code and develops the content mentioned in the requirements
Your task can be summarized as follows:
1.Compare the original code and the developed code, and record the differences.
2.Identify the omission markers in the developed code.
3.Based on the omission markers, find the corresponding omitted code in the original code.
4.Copy the omitted code into the developed code.
5.Verify if the newly added code can produce the correct results.
6.Finally, complete the developed code is used as the output.
Let''s think step by step about the solution.
The programming language is {language}.
The output should be concise, professional, and in Markdown code block format (see output sample format).

## input
### requirements
{requirements}

### original code
{original_code}

### developed code
{developed_code}

## output sample format
```vue
code
```

## output', '划词对话-合并代码');
INSERT INTO "public"."configuration"("id", "deleted", "created_at", "update_at", "belong_type", "attribute_key", "attribute_value", "desc") VALUES (36, 'f', '2023-10-26 10:45:03', '2023-10-26 10:45:03', 'prompt_template', 'scribe_generate_code', '## Instructions
You are now a senior front-end engineer.
The input has three parts, the Requirements, the Selected Code, and the Code example snippets.
Your job is to read the requirements carefully and then generate code based on the requirements.
If there are selected code, first you need to understand it in depth, and second you need to develop requirements based on it;
otherwise, you can directly generate a new piece of code based on the requirements.
If the Code example snippets are provided, it is important to learn what they do and the technology stack they use,
and you need to refer to their style when generating the code.
The programming language is {language}.
Try to match the style of the selected code as closely as possible.
Don’t remove the original code easily.
Generated code is readable and properly indented.
The output needs to be concise and professional.
Please use the Markdown code block format in the output(Refer to the output example format).
Make sure to include the programming language name at the start of the Markdown code blocks.
Cannot generate the code according to the requirement please reply directly cannot meet the requirement,
must reply in Chinese.
Let''s think step by step with the Chain-of-Thought example.

## Chain-of-Thought example
### Requirements
为这个表单增加姓名、年薪、身高表单项
### Chain-of-Thought
首先找到当前选中代码中表单代码的位置，然后增加三个表单项，分别是姓名、年薪、身高

## Chain-of-Thought example
### Requirements
编写一个表单抽屉，表单内容是姓名、年龄、性别，支持提交表单并显示遮罩
### Chain-of-Thought
首先生成一个表单抽屉，然后编写三个表单项，分别是姓名、年龄、性别， 最后三个三个表单项都需要支持提交表单并显示遮罩

## input
### Requirements
{requirements}

### Selected Code
{selectedText}

### Code example snippets
{sample_code}

## output example format
```vue
xxx
```

## output', '划词对话-生成代码');
INSERT INTO "public"."configuration"("id", "deleted", "created_at", "update_at", "belong_type", "attribute_key", "attribute_value", "desc") VALUES (35, 'f', '2023-10-26 10:40:39', '2023-10-26 15:58:35.540552', 'prompt_template', 'scribe_filter_desc', '## Instructions
You are an experienced front-end engineer and natural language processing engineer.
Your task is to understand the semantics of [Requirements] and [Function Description Examples] at a high level,
Then, one by one, from the [Function Description Examples],
you select the examples that match the [Requirements] in meaning and semantics.
Provide output that contains only the serial numbers of the selected [Function Description Examples],
and select at least one.
If there are no similar examples at all, reply "No matching examples found".
Let''s think step by step with reference to the Chain-of-Thought.

## example
input:
[Requirements]
表格支持勾选，并能清除勾选
[Function Description Examples]
1、【表格】【勾选项】设置表格中指定的单个或者多个勾选项
2、【表格】【勾选项】【表格行】【表格数据】清除表格所有勾选项状态，将已勾选的表格行状态设置为未勾选；清除表格已勾选行；清除表格已勾选数据；清除表格勾选项
3、【表格】表格启禁用功能，可以批量操作，也可以单个操作
4、【表格】【删除功能】【批量删除】【单个删除】表格删除功能，包含批量删除和单个删除
5、【表格】【勾选项】【选中数据】【勾选的数据】判断表格中是否有勾选项；判断表格中是否有选中数据；是否有被勾选的数据否
[Chain-of-Thought]
首先Requirements中的主语是表格，然后提到的功能是既要支持勾选又要能清除勾选，所以选择2
output:
2

## example
input:
[Requirements]
在这个表单中增加一个带本地搜索的下拉选择器
[Function Description Examples]
1、【下拉选择器】【本地搜索】带本地搜索的下拉选择器
2、【下拉选择器】【全选功能】带全选功能的下拉选择器，可以实现全选功能
3、【下拉框】【地理信息】【地理数据信息】【IxTreeSelect树下拉框】【按钮】【parseLocalName】【地区名】一个数据为地理信息的下拉框，获取地理数据信息并用IxTreeSelect树下拉框展示，通过点击按钮触发parseLocalName获取选择的地区名
4、【下拉选择框】【日期选择器】带下拉选择框的日期选择器只允许选择当前之前的时间范围
5、【下拉选择器】【禁用】【全选功能】设置disabled 将带全选功能的下拉选择器禁用，将无法点开下拉框
[Chain-of-Thought]
首先Requirements中的主语是表单，然后提到的功能是增加一个带本地搜索的下拉选择器，所以选择1
output:
1

## example
input:
[Requirements]
为这个表格每一行最后一列增加编辑功能，点击编辑打开抽屉，抽屉内容是一个表单
[Function Description Examples]
1、【表格】【编辑功能】【抽屉】表格编辑功能，编辑后打开抽屉
2、【表格】【抽屉】表格新增功能，新增后打开抽屉
3、【表单】【抽屉】内容为表单的抽屉，点击抽屉底部的“取消”按钮，将关闭抽屉；关闭表单抽屉；关闭内容为表单的抽屉
4、【抽屉】【表单】【遮罩】打开一个抽屉，抽屉内容是表单，展示遮罩，可以点击非抽屉部分关闭抽屉；表单抽屉；内容为表单的抽屉
5、【表单】【抽屉】【回调函数】编辑表单抽屉点击确定按钮提交后，将触发editCallback.value函数；编辑表单抽屉回调函数处理
[Chain-of-Thought]
首先Requirements中的主语是表格，然后提到的功能是增加编辑功能，又提到打开抽屉及这个抽屉的内容是一个表单，所以选1、4
output:
1、4


## input
[Requirements]
{requirements}

[Function Description Examples]
{selectedText}

## output', '划词对话-过滤相似示例');
INSERT INTO "public"."configuration"("id", "deleted", "created_at", "update_at", "belong_type", "attribute_key", "attribute_value", "desc") VALUES (34, 'f', '2023-10-26 10:34:17', '2023-10-26 21:13:02.279627', 'prompt_template', 'scribe_add_tag', '## Instructions
You are an experienced front-end engineer and natural language processing engineer.
Your job is to decipher the meaning and semantics of the input,
Then the front-end component knowledge and key information related to the function are extracted as labels.
Let''s think step by step with reference to the Chain-of-Thought.

## example
input:
编写一个表单抽屉，表单内容是姓名、年龄、性别，支持提交表单并显示遮罩
Chain-of-Thought：
在这句话中，表单抽屉属于前端组件，提交表单和显示遮罩属于组件功能，姓名、年龄、性别属于业务信息应该忽略，所以提取出来的结果为【表单抽屉】【提交表单】【显示遮罩】。
output:
【表单抽屉】【提交表单】【显示遮罩】

## example
input:
去掉勾选列，新增port列，放在ip列后面
Chain-of-Thought：
在这句话中，勾选列属于前端组件，port列、ip列属于业务信息应该忽略，所以提取出来的结果为【表格】【勾选列】。
output:
【表格】【勾选列】

## example
input:
生成一个异步关闭的弹窗，弹窗名是新增，内部是一个form表单，表单项有域名，ip，描述
Chain-of-Thought：
在这句话中，弹窗、form表单属于前端组件，异步关闭属于组件功能，域名、ip、描述属于业务信息应该忽略，所以提取出来的结果为【异步关闭】【弹窗】【form表单】。
output:
【异步关闭】【弹窗】【form表单】

## input
{query}

## output', '划词对话-打标签');
INSERT INTO "public"."configuration"("id", "deleted", "created_at", "update_at", "belong_type", "attribute_key", "attribute_value", "desc") VALUES (33, 'f', '2023-10-25 15:51:45', '2023-10-25 17:53:04.11717', 'prompt_template', 'pickCommonFunc', '```{language}
{selectedText}
```
This code could be chunked into smaller functions and extracts the common function, which would look like:', '函数提取');
INSERT INTO "public"."configuration"("id", "deleted", "created_at", "update_at", "belong_type", "attribute_key", "attribute_value", "desc") VALUES (32, 'f', '2023-10-25 15:37:21', '2023-10-25 17:54:07.13688', 'prompt_template', 'optimize', '## Instructions
How could the readability of the code below be improved?
The programming language is {language}.
Consider overall readability and idiomatic constructs.
{custom_instructions}.

## Selected Code
```
{selectedText}
```

## Task
How could the readability of the code be improved?
The programming language is {language}.
Consider overall readability and idiomatic constructs.
Provide potential improvements suggestions where possible.
Consider that the code might be perfect and no improvements are possible.
Include code snippets (using Markdown) and examples where appropriate.
The code snippets must contain valid {language} code.
Must reply with Chinese.

## Readability Improvements', '千流AI：优化代码（旧）');
INSERT INTO "public"."configuration"("id", "deleted", "created_at", "update_at", "belong_type", "attribute_key", "attribute_value", "desc") VALUES (31, 'f', '2023-08-03 20:38:52', '2023-10-26 15:37:32.189368', 'prompt_template', 'review', '## Instructions
You are now working as a code review specialist.
Only check for obvious bugs, functional issues, performance issues, stability issues.
Ignore undefined function problems
Ignore problems with undefined methods
Ignore undefined variable issues

## Context
The selected code programming language is {language}.
{custom_instructions}

## Selected Code
{selectedText}

Only the following questions are addressed
Give a description of the problem,
Give solutions,
If have fix the code example, give fix code example.
Include code snippets (using Markdown) and examples where appropriate.
Must reply with Chinese.', '千流AI：代码Review（主动）');
INSERT INTO "public"."configuration"("id", "deleted", "created_at", "update_at", "belong_type", "attribute_key", "attribute_value", "desc") VALUES (29, 'f', '2023-10-25 15:40:52', '2023-10-26 14:22:19.840531', 'prompt_template', 'generateCodeByForm', '## Instructions
Now you are a Senior {language} Programmer.
Generate results based on the following requirements.
The results must use {language}.
{generation_type}
{output_requirements}
Using Markdown format, and identify its coding language to specify

## Requirement
{requirement_desc}
## results', '生成代码 表单');
INSERT INTO "public"."configuration"("id", "deleted", "created_at", "update_at", "belong_type", "attribute_key", "attribute_value", "desc") VALUES (28, 'f', '2023-10-25 15:43:45', '2023-10-25 17:52:21.803151', 'prompt_template', 'generateCodeByAsk', '## Instructions
Now you are a senior development engineer .
Generate code for the following Code .
{custom_instructions}
Must reply with Chinese and show me the code in your answer .

## Code
```
{code}
```', '生成代码（web）');
INSERT INTO "public"."configuration"("id", "deleted", "created_at", "update_at", "belong_type", "attribute_key", "attribute_value", "desc") VALUES (27, 'f', '2023-10-25 15:39:48', '2023-10-26 15:35:46.253129', 'prompt_template', 'generateCode', '## Instructions
Generate code for the following specification.
{custom_instructions}.

## Specification
{content}

## Instructions
Generate code for the specification.
Must reply with Chinese.

## Code', '生成代码');
INSERT INTO "public"."configuration"("id", "deleted", "created_at", "update_at", "belong_type", "attribute_key", "attribute_value", "desc") VALUES (26, 'f', '2023-10-25 15:33:00', '2023-10-25 17:24:12.543689', 'prompt_template', 'findProblems', '## Instructions
What could be wrong with the code below?
Only consider defects that would lead to incorrect behavior.
The programming language is {language}.
{custom_instructions}

## Selected Code
```
{selectedText}
```

## Task
Describe what could be wrong with the code?
Only consider defects that would lead to incorrect behavior.
Provide potential fix suggestions where possible.
Consider that there might not be any problems with the code."
Include code snippets (using Markdown) and examples where appropriate.
Must reply with Chinese.

## Analysis', '千流AI：查找bug（旧）');
INSERT INTO "public"."configuration"("id", "deleted", "created_at", "update_at", "belong_type", "attribute_key", "attribute_value", "desc") VALUES (25, 'f', '2023-10-25 15:38:51', '2023-10-25 17:30:40.914434', 'prompt_template', 'explain', '## Instructions
Summarize the code below (emphasizing its key functionality).
{custom_instructions}.

## Selected Code
```
{selectedText}
```

## Task
Summarize the code at a high level (including goal and purpose) with an emphasis on its key functionality.
Must reply with Chinese.

## Response', '千流AI：解释代码（旧）智能问答->解释代码（新）');
INSERT INTO "public"."configuration"("id", "deleted", "created_at", "update_at", "belong_type", "attribute_key", "attribute_value", "desc") VALUES (24, 'f', '2023-08-03 20:39:08', '2023-10-26 12:39:33.260368', 'prompt_template', 'auto_review', '## Instructions
You are now working as a code review specialist.
Only check for obvious bugs, functional issues, performance issues, stability issues.
Ignore undefined function problems
Ignore problems with undefined methods
Ignore undefined variable issues

## Context
The selected code programming language is #language#.
The following is the selected code snippet, the left is the code line number
## Selected Code
#select_code#

### Response example
{
"has_problem": true,
"error_start_line_number": 0,
"score": 0,
"review_content": "",
"fix_code_example": ""
}
## Response Explain
has_problem: Indicates whether the audit is faulty.             Optional values :true or false.
error_start_line_number: The number of lines of code where the problem occurred.
score: review problem severity score,On a scale of 0 to 10, 0 is the lowest and 10 is the highest, The score of package import type problem and specification type problem cannot exceed 5 points.
review_content: Only the following questions are addressed: Give a description of the problem;        Give the solution;          Give fix code example.
fix_code_example: If have fix the code example, write the code to this field.
## Output Indicator
Don''t output optimizations and suggestions.
Arguments or functions that you don''t know about can be ignored.
In the field review_content place include code snippets (using Markdown) and examples.
No problem please reply directly no problem.
Please simulate that the api only returns json strings.
The review_content field must be answered in Chinese.', '千流AI：代码Review（自动）');
INSERT INTO "public"."configuration"("id", "deleted", "created_at", "update_at", "belong_type", "attribute_key", "attribute_value", "desc") VALUES (23, 'f', '2023-10-25 15:34:13', '2023-10-25 17:29:59.561475', 'prompt_template', 'addTests', '## Instructions
Write a unit test for the code below.
{custom_instructions}

## Selected Code
```
{selectedText}
```

## Task
Write a unit test that contains test cases for the happy path and for all edge cases.
The programming language is {language}.
Must reply with Chinese.

## Unit Test', '千流AI：生成测试（旧）测试生成（新）');
INSERT INTO "public"."configuration"("id", "deleted", "created_at", "update_at", "belong_type", "attribute_key", "attribute_value", "desc") VALUES (22, 'f', '2023-10-25 15:48:55', '2023-10-25 17:27:20.684803', 'prompt_template', 'addStrongerCode', '```{language}
{selectedText}
```
Please make the above code more robust, covering more edge cases and handling errors.
Including but not limited to the following points:
1. Function input check supplement: function input check judgment
2. Function/Property call return value check Supplement: Function call or object property return value check
3. Add exception handling logic: Add exception handling logic, such as try cache
4. Do not change the business scenario of the original code

Requirements:
1. Return only one block of code, without any other explanation, using markdown
Output example:
```python
print(123)
```
Output:', '提升健壮性');
INSERT INTO "public"."configuration"("id", "deleted", "created_at", "update_at", "belong_type", "attribute_key", "attribute_value", "desc") VALUES (21, 'f', '2023-10-25 15:46:30', '2023-10-25 16:38:39.799457', 'prompt_template', 'addDebugCode', '```{language}
{selectedText}
```
Please make the above code easier to debug:
1. Add some log statements

Requirements:
1. Do not change the original code logic
2. Return only one block of code, using markdown
Output example:
```python
print(123)
```
Output:', '提升调试性');
INSERT INTO "public"."configuration"("id", "deleted", "created_at", "update_at", "belong_type", "attribute_key", "attribute_value", "desc") VALUES (20, 'f', '2023-10-25 15:49:22', '2023-10-26 09:52:48.162305', 'prompt_template', 'addComment', '```{language}
{selectedText}
```
Please add Chinese comments to the above code:
1. The comments of the function describe its function, parameters, return values, and examples
2. Include sensible comments at key points

Requirements:
1. Comments should follow the comment format of the language standard document
2. Return only one block of code, using markdown

Output example:
```python
print(123)
```
Output:', '添加注释');
INSERT INTO "public"."configuration"("id", "deleted", "created_at", "update_at", "belong_type", "attribute_key", "attribute_value", "desc") VALUES (19, 'f', '2023-10-26 10:58:57', '2023-10-27 10:33:11.817751', 'gpt', 'generate_code', '[
    {
        "language": "python",
        "prompt": "Python",
        "generation_type": [
        ]
    },
    {
        "language": "swagger",
        "prompt": "Swagger",
        "generation_type": [
            {
                "key": "api_interface",
                "name": "api接口",
                "desc": "生成api接口",
                "prompt": "api interface",
                "form_fields": [
                ]
            }
        ]
    },
    {
        "language": "c",
        "prompt": "C",
        "generation_type": [
            {
                "key": "func",
                "name": "函数",
                "desc": "生成函数",
                "prompt": "function",
                "form_fields": [
                    {
                        "type": "input",
                        "name": "入参",
                        "key": "input",
                        "desc": "入参",
                        "prompt": "input params: {value}\n"
                    },
                    {
                        "type": "textarea",
                        "name": "返回值",
                        "key": "output",
                        "desc": "返回值",
                        "prompt": "return value: {value}"
                    }
                ]
            },
            {
                "key": "struct",
                "name": "数据结构",
                "desc": "生成数据结构",
                "prompt": "data struct",
                "form_fields": [
                    {
                        "type": "select",
                        "name": "框架选择",
                        "desc": "框架选择",
                        "key": "frame",
                        "require": true,
                        "option": [
                            {
                                "key": "struct",
                                "name": "struct",
                                "desc": "struct框架",
                                "prompt": "The results must use {value} framework."
                            }
                        ]
                    }
                ]
            }
        ]
    },
    {
        "language": "c++",
        "prompt": "C++",
        "generation_type": [
            {
                "key": "func",
                "name": "函数",
                "desc": "生成函数",
                "prompt": "function",
                "form_fields": [
                    {
                        "type": "input",
                        "name": "入参",
                        "key": "input",
                        "desc": "入参",
                        "prompt": "input params: {value}\n"
                    },
                    {
                        "type": "textarea",
                        "name": "返回值",
                        "key": "output",
                        "desc": "返回值",
                        "prompt": "return value: {value}"
                    }
                ]
            },
            {
                "key": "struct",
                "name": "数据结构",
                "desc": "生成数据结构",
                "prompt": "data struct",
                "form_fields": [
                    {
                        "type": "select",
                        "name": "框架选择",
                        "desc": "框架选择",
                        "key": "frame",
                        "require": true,
                        "option": [
                            {
                                "key": "map",
                                "name": "map",
                                "desc": "map框架",
                                "prompt": "The results must use {value} framework."
                            }
                        ]
                    }
                ]
            }
        ]
    },
    {
        "language": "go",
        "prompt": "Go",
        "generation_type": [
            {
                "key": "func",
                "name": "函数",
                "desc": "生成函数",
                "prompt": "function",
                "form_fields": [
                    {
                        "type": "input",
                        "name": "入参",
                        "key": "input",
                        "desc": "入参",
                        "prompt": "input params: {value}\n"
                    },
                    {
                        "type": "textarea",
                        "name": "返回值",
                        "key": "output",
                        "desc": "返回值",
                        "prompt": "return value: {value}"
                    }
                ]
            },
            {
                "key": "api_interface",
                "name": "api接口",
                "desc": "生成api接口",
                "prompt": "api interface",
                "form_fields": [
                    {
                        "type": "select",
                        "name": "框架选择",
                        "desc": "框架选择",
                        "key": "frame",
                        "require": true,
                        "option": [
                            {
                                "key": "beego",
                                "name": "beego",
                                "desc": "beego框架",
                                "prompt": "The results must use {value} framework."
                            },
                            {
                                "key": "gin",
                                "name": "gin",
                                "desc": "gin框架",
                                "prompt": "The results must use {value} framework."
                            },
                            {
                                "key": "grpc1",
                                "name": "grpc",
                                "desc": "grpc框架",
                                "prompt": "The results must use {value} framework."
                            },
                            {
                                "key": "go-zero",
                                "name": "go-zero",
                                "desc": "go-zero框架",
                                "prompt": "The results must use {value} framework."
                            }
                        ]
                    }
                ]
            },
            {
                "key": "struct",
                "name": "数据结构",
                "desc": "生成数据结构",
                "prompt": "data struct",
                "form_fields": [
                    {
                        "type": "select",
                        "name": "框架选择",
                        "desc": "框架选择",
                        "key": "frame",
                        "require": true,
                        "option": [
                            {
                                "key": "struct",
                                "name": "struct",
                                "desc": "struct框架",
                                "prompt": "The results must use {value} framework."
                            },
                            {
                                "key": "map",
                                "name": "map",
                                "desc": "map框架",
                                "prompt": "The results must use {value} framework."
                            }
                        ]
                    }
                ]
            }
        ]
    },
    {
        "language": "java",
        "prompt": "Java",
        "generation_type": [
            {
                "key": "func",
                "name": "函数",
                "desc": "生成函数",
                "prompt": "function",
                "form_fields": [
                    {
                        "type": "input",
                        "name": "入参",
                        "key": "input",
                        "desc": "入参",
                        "prompt": "input params: {value}\n"
                    },
                    {
                        "type": "textarea",
                        "name": "返回值",
                        "key": "output",
                        "desc": "返回值",
                        "prompt": "return value: {value}"
                    }
                ]
            },
            {
                "key": "api_interface",
                "name": "api接口",
                "desc": "生成api接口",
                "prompt": "api interface",
                "form_fields": [
                    {
                        "type": "select",
                        "name": "框架选择",
                        "desc": "框架选择",
                        "key": "frame",
                        "require": true,
                        "option": [
                            {
                                "key": "sprintboot",
                                "name": "sprintboot",
                                "desc": "sprintboot框架",
                                "prompt": "The results must use {value} framework."
                            }
                        ]
                    }
                ]
            },
            {
                "key": "struct",
                "name": "数据结构",
                "desc": "生成数据结构",
                "prompt": "data struct",
                "form_fields": [
                    {
                        "type": "select",
                        "name": "框架选择",
                        "desc": "框架选择",
                        "key": "frame",
                        "require": true,
                        "option": [
                            {
                                "key": "struct",
                                "name": "struct",
                                "desc": "struct框架",
                                "prompt": "The results must use {value} framework."
                            },
                            {
                                "key": "map",
                                "name": "map",
                                "desc": "map框架",
                                "prompt": "The results must use {value} framework."
                            }
                        ]
                    }
                ]
            }
        ]
    },
    {
        "language": "shell",
        "prompt": "shell",
        "generation_type": [
            {
                "key": "func",
                "name": "函数",
                "desc": "生成函数",
                "prompt": "function",
                "form_fields": [
                    {
                        "type": "input",
                        "name": "入参",
                        "key": "input",
                        "desc": "入参",
                        "prompt": "input params: {value}\n"
                    },
                    {
                        "type": "textarea",
                        "name": "返回值",
                        "key": "output",
                        "desc": "返回值",
                        "prompt": "return value: {value}"
                    }
                ]
            }
        ]
    }
]', '自动生成代码的配置文件');
INSERT INTO "public"."configuration"("id", "deleted", "created_at", "update_at", "belong_type", "attribute_key", "attribute_value", "desc") VALUES (18, 'f', '2023-10-25 09:54:45', '2023-10-27 16:03:15.703895', 'permission', 'need_cause_department', '研发体系/用户体验驱动中心/UEDC', '划词对话 需要 拒绝原因 弹框的部门。多部门用 , 分隔');
INSERT INTO "public"."configuration"("id", "deleted", "created_at", "update_at", "belong_type", "attribute_key", "attribute_value", "desc") VALUES (13, 'f', '2023-08-14 16:56:22', '2023-08-14 16:56:22', 'code_completion', 'allow_department', 'UEDC,研发体系', '允许代码补全的部门，可简写。用 ,分割，区分大小写');
INSERT INTO "public"."configuration"("id", "deleted", "created_at", "update_at", "belong_type", "attribute_key", "attribute_value", "desc") VALUES (12, 'f', '2023-08-11 15:14:16', '2023-08-11 15:14:16', 'permission', 'allow_user_agent', 'node-fetch,qianliu-ai-jetbrains-plugin,cicd-service,qianliu-devops,qianliu-ai-lanjun', 'user-agent 允许白名单。多配置使用 , 分割');
INSERT INTO "public"."configuration"("id", "deleted", "created_at", "update_at", "belong_type", "attribute_key", "attribute_value", "desc") VALUES (8, 'f', '2023-07-06 16:23:16', '2023-07-06 16:23:16', 'review', 'review_max_review_num', '5', '');
INSERT INTO "public"."configuration"("id", "deleted", "created_at", "update_at", "belong_type", "attribute_key", "attribute_value", "desc") VALUES (7, 'f', '2023-06-05 10:07:50', '2023-06-05 10:07:50', 'ai_review', 'suffix_language_mapping', '{
        ".c": "C", ".cpp": "C++", ".cc": "C++", ".cxx": "C++", ".java": "Java", ".py": "Python",
        ".rb": "Ruby", ".js": "JavaScript", ".html": "HTML", ".htm": "HTML", ".css": "CSS",
        ".php": "PHP", ".pl": "Perl", ".swift": "Swift", ".go": "Go", ".rs": "Rust",
        ".kt": "Kotlin", ".dart": "Dart", ".scala": "Scala", ".lua": "Lua", ".m": "Objective-C",
        ".mm": "Objective-C++", ".h": "C/C++/Objective-C", ".hpp": "C/C++/Objective-C"
    }', '支持ai-review的语言类型');
INSERT INTO "public"."configuration"("id", "deleted", "created_at", "update_at", "belong_type", "attribute_key", "attribute_value", "desc") VALUES (6, 'f', '2023-05-26 14:58:44', '2023-05-26 14:58:44', 'plugin', 'users', '刘鹏|林凯鸿t43540', 'ide插件需要提示更新用户，值为用户（姓名+工号），多个用 “|” 隔开：刘鹏z10807|张三xxxx|李四xxxx');
INSERT INTO "public"."configuration"("id", "deleted", "created_at", "update_at", "belong_type", "attribute_key", "attribute_value", "desc") VALUES (5, 'f', '2023-05-25 16:37:42', '2023-05-25 16:37:42', 'qianliu_ad', 'on', '

---
## 为了更好的提升千流AI Copilot用户体验，将开展“千流AI copilot反馈有奖活动" !

**活动时间**：5.25-5.31

**活动对象**：研发人员

**活动内容**：
1. 使用千流AI Copilot代码生成，如发现任何BUG或新需求，提到：https://devops.atrust.sangfor.com/portal/feedback
2. 我们将根据反馈的缺陷或需求重要程度给予相应的奖励 ：马克杯、千流鼠标垫等。

**奖励发放**：奖品月底统一发放

**Copilot使用文档**：http://docs.sangfor.org/x/rNnHDw

**如有疑问，请联系：江帅20007  ！**
', '键：on为开；off为关。值：广告内容。只能写markdown格式，不要删除 ---  以及以上的内容。最好在测试环境验证一下');
INSERT INTO "public"."configuration"("id", "deleted", "created_at", "update_at", "belong_type", "attribute_key", "attribute_value", "desc") VALUES (3, 'f', '2023-05-16 10:59:56', '2023-10-27 09:16:52.803654', 'prompt', 'forbidden_word', 'sangfor|深信服|信服|sinfor|sangfor123|admin123|sangfor@123|qwe', 'sangfor|深信服|信服|sinfor|sangfor123|admin123|sangfor@123');
INSERT INTO "public"."configuration"("id", "deleted", "created_at", "update_at", "belong_type", "attribute_key", "attribute_value", "desc") VALUES (2, 'f', '2023-04-25 11:00:56', '2023-04-25 11:00:56', 'api_documentation', 'text', '### API端点

```
http://chatgpt.sangfor.com/api/v3/completion
```

### 请求方式

```
POST
```

### 请求头

| 参数         | 值               | 说明 |
| ------------ | ---------------- | ---- |
| Content-Type | application/json |      |
| app-id       | xxxx             |      |

### 请求体

描述API所需的参数及其类型。

| 参数                | 参数类型   | 默认值 | 是否必传 | 说明                   | 示例             |
| :------------------ | :--------- | :----- | :------- | :--------------------- | :--------------- |
| system_prompt       | array[str] |        | 否       | 系统预设               |                  |
| prompt              | str        |        | 是       | 问题                   |                  |
| stream              | bool       | false  | 否       | 是否流式响应           |                  |
| conversation_id     | str        |        | 否       | 一次记录会话的上下文id | 可使用自生成uuid |
| context_association | bool       | true   | 否       | 是否开启上下文         |                  |
| max_tokens          | int        |        | 否       | 回答最大token          |                  |

系统预设参考：

```
You are an intelligent answering robot. Please reply my questions in Chinese.
作为智能应答机器人回答问题

Draft an email or other piece of writing and respond in Chinese markdown format.
草拟一封电子邮件或者其他写作片段

Write Python code and respond in Chinese markdown format.
写Python代码

Answer questions about a set of documents and respond in Chinese markdown format.
围绕一系列文档来回答问题
```

### 响应

流式响应：application/text

```
content...
```

非流式响应：application/json

```json
{
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": "请问有什么可以帮助你的吗",
        "role": "assistant"
      }
    }
  ],
  "created": 1682494020,
  "id": "chatcmpl-79TqGhSqLOVdgDNbUzLUCRAKqSk9y",
  "model": "gpt-3.5-turbo-0301",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 92,
    "prompt_tokens": 135,
    "total_tokens": 227
  }
}
```



| 参数名            | 类型          | 描述     |
| ----------------- | ------------- | -------- |
| choices           | array[object] |          |
| finish_reason     | str           |          |
| index             | number        |          |
| message           | object        |          |
| content           | str           | 回答内容 |
| role              | str           |          |
| created           | number        |          |
| id                | str           |          |
| model             | str           | 使用模型 |
| object            | str           |          |
| usage             | object        |          |
| completion_tokens | number        |          |
| prompt_tokens     | number        |          |
| total_tokens      | number        |          |

#### 成功响应

```
HTTP/1.1 200 OK
Content-Type: application/text
```

#### 错误响应

```
HTTP/1.1 403 FORBIDDEN
Content-Type: application/json

{
  "data": null,
  "error_code": 130001,
  "message": "[prompt] ：该输入项不允许为空",
  "success": false
}
```

### 注意事项1:

默认使用 gpt-3.5，即存在 4096 token 上限. 可通过 response 中的 usage 判断使用的 token 长度.
若超过 4096 则会被服务端进行截断（最早的信息会被丢弃）

### 注意事项2:

使用频率 <40次/min ,请勿频率过大，导致整个服务不可用. 另外请勿分享给其他人使用, 如有发现，会做封号处理.

### 示例1

#### 请求

```
POST https://chat.sangfor.com/api/v3/completion
```

#### 请求体

```json
{
    "prompt": "计时器"
}
```

#### 响应

HTTP/1.1 200 OK
Content-Type: application/text

```
计时器是一种用于测量时间间隔的工具。它可以在一定时间内计算时间的流逝，通常用于测量运动员的比赛时间、烹饪时间、实验时间等。计时器可以是机械式的，也可以是电子式的，现在还有很多手机和电脑上都内置了计时器功能。在使用计时器时，需要设置起始时间和结束时间，计时器会自动计算时间间隔并显示出来。
```

### 示例2

#### 请求

```
POST https://chat.sangfor.com/api/v3/completion
```

#### 请求体

```json
{
    "system_prompt": ["Write Python code and respond in Chinese markdown format."],
    "prompt": "计时器",
    "stream": true
}
```

#### 响应

HTTP/1.1 200 OK
Content-Type: application/text

```
​```python
import time

start_time = time.time() # 记录开始时间

# 执行需要计时的代码

end_time = time.time() # 记录结束时间

elapsed_time = end_time - start_time # 计算时间差

print(f"程序执行时间为：{elapsed_time}秒")
​```

以上代码实现了一个简单的计时器，可以用来计算程序的执行时间。在代码执行前记录开始时间，执行完后记录结束时间，两者相减即可得到程序执行时间。

当然，我们也可以将上面的代码封装成一个函数，方便在其他地方调用。以下是封装后的代码：

​```python
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time() # 记录开始时间
        result = func(*args, **kwargs) # 执行函数
        end_time = time.time() # 记录结束时间
        elapsed_time = end_time - start_time # 计算时间差
        print(f"程序执行时间为：{elapsed_time}秒")
        return result
    return wrapper
​```
```



', '');
INSERT INTO "public"."configuration"("id", "deleted", "created_at", "update_at", "belong_type", "attribute_key", "attribute_value", "desc") VALUES (1, 'f', '2023-04-25 11:00:28', '2023-04-25 11:00:28', 'banner', 'text', '【通知】千流 Copilot 全面开放使用，欢迎大家安装使用！ 使用文档：http://docs.sangfor.org/x/rNnHDw', '1.由于每次提问都有费用支出，请勿用于工作无关的问题 ; 2. API已提供申请入口(广场->应用广场->申请)，请勿私自爬取API使用，一经发现，将封号处理！');


--组件库映射配置
--INSERT INTO "public"."components_map"("id", "deleted", "created_at", "update_at", "team", "git_repos", "inline_chat_components", "fauxpilot_components") VALUES (2, 'f', '2023-10-23 20:22:11', '2023-10-24 10:38:02.358202', 'other', 'just_test', 'test', '');
--INSERT INTO "public"."components_map"("id", "deleted", "created_at", "update_at", "team", "git_repos", "inline_chat_components", "fauxpilot_components") VALUES (3, 'f', '2023-10-24 10:47:21', '2023-10-26 17:44:30.912257', 'mss', 'git@mq.code.sangfor.org:SS/SOC/soc_workflow_webui.git', 'ss-business,ss-components', 'ss-components');
--INSERT INTO "public"."components_map"("id", "deleted", "created_at", "update_at", "team", "git_repos", "inline_chat_components", "fauxpilot_components") VALUES (1, 'f', '2023-10-23 20:12:45', '2023-10-26 19:00:32.772076', 'sase', 'git@mq.code.sangfor.org:UED/SAAS/sase-platform.git', 'sase,idux', 'sf-vue;;<sf-[a-z]+,idux');


--设置更新 开始自增id
SELECT setval('api_rule_id_seq', (SELECT MAX(id) FROM api_rule));
SELECT setval('configuration_id_seq', (SELECT MAX(id) FROM configuration));
--SELECT setval('components_map_id_seq', (SELECT MAX(id) FROM components_map));

