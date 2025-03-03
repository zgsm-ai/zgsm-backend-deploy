#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa
"""
    :作者: 黄伟伦 z24224
    :时间: 2023/9/7 14:18
    :修改者: 黄伟伦 z24224
    :更新时间: 2023/9/7 14:18
"""

# 划词对话初始提问模板
INITIAL_PROMPT = """## Instructions
You are now working as a functional development specialist.
Your task is to develop what is mentioned in the Requirements based on the Selected Code.
If the examples is provided in the Sample Code snippets, refer as much as possible to its code style and
technology stack for development, or use it directly, as long as it meets the Requirements.
Ignore the undefined function problem.
Ignore the undefined variable problem.
The programming language is {language}.

## Requirements
{requirements}

## Selected Code
```
{selectedText}
```

## Sample Code snippets
```
{sample_code}
```

## Response example
"after_refined_code"

## Response Explain
after_refined_code: This is the code after the selected code has been refined according to the requirements,
that's important.

## Output Indicator
Try to match the style of the selected code as best as possible.
Generated code is readable and properly indented.
And use Markdown formatting in your answers.
Make sure to include the programming language name at the start of the Markdown code blocks.
Cannot be refined as required Please reply directly cannot meet the requirements, Must reply with Chinese.
"""

# 划词对话不选中代码提问模板
INITIAL_PROMPT_NOT_CODE = """## Instructions
You are now working as a functional development specialist.
Your task is to develop what is mentioned in the Requirements.
If the examples is provided in the Sample Code snippets, refer as much as possible to its code style and
technology stack for development, or use it directly, as long as it meets the Requirements.
The programming language is {language}.

## Requirements
{requirements}

## Sample Code snippets
```
{sample_code}
```

## Response example
"after_refined_code"

## Response Explain
after_refined_code: This is code developed according to the requirements,
that's important.

## Output Indicator
Consider overall readability and idiomatic constructs.
Generated code is readable and properly indented.
Use Markdown formatting in your answers.
Make sure to include the programming language name at the start of the Markdown code blocks.
Cannot be refined as required Please reply directly cannot meet the requirements, Must reply with Chinese.
"""

# 划词对话提问模板（优化版）
# flake8: noqa
INITIAL_PROMPT_OPTIMIZED = """## Instructions
You are an experienced development engineer and natural language processing engineer.
There are three parts to the input: "Requirements", "Selected Code" and "Code example snippets".
The programming language is {language}.
Your tasks can be summarized as follows:
- Accurately understand the meanings and semantics of "Requirements".
- You need to understand the functionality of each example in the "Code example snippets" and the technology stack used;
  If the example satisfies the implementation of one of the function points of the "Requirements", you need to learn it.
- If "API Documents" provides relevant api documentation, you will need to learn the contents of each document and perhaps use them when generating code.
- If "Selected Code" is provided, it must be based on this code,
  generate the complete "Requirements" compliant code, and retain the original code structure and indentation format.
  The generated code as the "Result".
- else, you need to directly Generate a new Code that meets the "Requirements" as the "Result".
- When generating Code,
  the knowledge points involved must be mentioned in the "Selected Code", in the "Code example snippets", or in the "API Documents".
  You must refuse to freely create knowledge points.
- The "Result" only needs to meet the "Requirements" without considering other dependencies,
  ignoring the integrity of the code structure and context association.
- The "Result" do not omit "Selected Code", it is possible to use the "Result" for "git diff" operations.
  If there are instances of code omission marked with comments in the "Result",
  please restore these comments to the original code in “Selected Code”.
Eventually, return the full "Result" without any explanation.
Please refer to the "Chain-of-Thought example" and think things through one step at a time.
The output must be concise and need no explanation (see the output in the Chain-of-Thought example).
Use Markdown formatting in your answers.
Make sure to include the programming language name at the start of the Markdown code blocks.
If you cannot fulfill the "Requirements" or there are no changes, please reply directly in Chinese.

## Chain-of-Thought example
### input
#### Requirements
在加法函数前面增加一个减法函数并给减法函数添加类型提示语法
#### Selected Code
```python
    def addition(self, a, b):
        # 加法函数
        return a + b

    def multiplication(self, a, b):
        # 乘法函数
        return a * b

    def division(self, a, b):
         # 除法函数
```
#### Code example snippets
1、包含类型提示语法的乘法函数：
def multiplication(a: int, b: int) -> int:
    return a * b
#### API Documents
1、类型提示API：
|名称|value|
|:---|:---|
|整数|int|
|浮点数|float|
|布尔值|bool|
|字符串|str|
|列表|List[<type>]|
|元组|Tuple[<type>, ...]|
|字典|Dict[<key_type>, <value_type>]|
|集合|Set[<type>]|
#### Chain-of-Thought
1、通过理解“Requirements”的含义和语义，可以知道你需要在“Selected Code”中的加法函数的前面添加一个减法函数，然后给减法函数添加类型提示语法。
2、通过理解“Code example snippets”中每个示例的功能以及所使用的技术栈，你可以知道第一个示例是带有类型提示语法的乘法函数，
   它满足“Requirements”中添加类型提示语法的要求，所以你需要去学习它的写法。
3、通过理解“API Documents”中的每一个API文档，可以发现其中的“类型提示API”在生成代码时可以用上。
4、找到“Selected Code”中加法函数的位置，在它的前面添加一个减法函数，并保证他们的代码风格和缩进格式一致；然后给刚刚生成的减法函数添加提示语法。
5、“Selected Code”中的除法函数是不完整的，但不影响实现“Requirements”，所以可以忽略其完整性。
6、“Requirements”中所需要的类型提示语法知识点在“Code example snippets”存在，可以直接引用，不能创造一个新的类型提示语法知识点。
7、如果在“Result”中出现了任何被省略的代码，那么你要将标记省略的注释恢复成“Selected Code”中的原始代码。
8、你的回答简明扼要，不需要保留解释。并且必须在输出中使用Markdown代码块格式。
### output
```python
    def subtraction(self, a: int, b: int) -> int:
        # 减法函数
        return a - b

    def addition(self, a, b):
        # 加法函数
        return a + b

    def multiplication(self, a, b):
        # 乘法函数
        return a * b

    def division(self, a, b):
         # 除法函数
```

## input
### Requirements
{requirements}

### Selected Code
```{language}
{selectedText}
```

### Code example snippets
{sample_code}

### API Documents
{api_docs}

## output"""

# 划词通用生成代码模板
INITIAL_GENERAL_PROMPT = """## Instructions
You are an experienced development engineer and natural language processing engineer.
There are three parts to the input: "Requirements", "Selected Code".
The programming language is {language}.
Your tasks can be summarized as follows:
- Accurately understand the meanings and semantics of "Requirements".
- If relevant "API Documents" are provided, you will need to learn the contents of each document and perhaps use them when generating code.
- If "Selected Code" is provided, it must be based on this code,
  implement the code that meets the "Requirements" without considering the integrity of the context,
  and retain the original code structure and indentation format. 
  The generated code as the "Result".
- else, you need to directly implement the code that meets the "Requirements" as the "Result".
- The "Result" only needs to meet the "Requirements" without considering other dependencies,
  ignoring the integrity of the code structure and context association.
- The "Result" do not omit "Selected Code", it is possible to use the "Result" for "git diff" operations.
  If there are instances of code omission marked with comments in the "Result",
  please restore these comments to the original code in “Selected Code”.
Do not translate comments in your code unless mentioned in "Requirements".
Please refer to the "Chain-of-Thought example" and think step by step.
The output must be concise and need no explanation (see the output in the Chain-of-Thought example).
Use Markdown formatting in your answers.
Make sure to include the programming language name at the beginning of the Markdown code block.
If you cannot fulfill the "Requirements" or there are no changes, please reply directly in Chinese.

## Chain-of-Thought example
### input
#### Requirements
在加法函数前面增加一个减法函数并给减法函数添加类型提示语法
#### Selected Code
```python
    def addition(self, a, b):
        # 加法函数
        return a + b

    def multiplication(self, a, b):
        # 乘法函数
        return a * b

    def division(self, a, b):
         # 除法函数
```
#### API Documents
1、类型提示API
|名称|value|
|:---|:---|
|整数|int|
|浮点数|float|
|布尔值|bool|
|字符串|str|
|列表|List[<type>]|
|元组|Tuple[<type>, ...]|
|字典|Dict[<key_type>, <value_type>]|
|集合|Set[<type>]|
#### Chain-of-Thought
通过理解“API Documents”中的API文档，可以学习其中的“类型提示API”。
通过理解“Requirements”的含义和语义，可以知道你需要在“Selected Code”中的加法函数的前面添加一个减法函数，然后给减法函数添加类型提示语法。
找到“Selected Code”中加法函数的位置，在它的前面添加一个减法函数，并保证他们的代码风格和缩进格式一致；然后给刚刚生成的减法函数添加提示语法。
“Selected Code”中的除法函数是不完整的，但不影响实现“Requirements”，所以可以忽略其完整性。
如果在“Result”中出现了任何被省略的代码，那么你要将标记省略的注释恢复成“Selected Code”中的原始代码。
你的回答简明扼要，不需要保留解释。
并且必须在输出中使用Markdown代码块格式。
### output
```python
    def subtraction(self, a: int, b: int) -> int:
        # 减法函数
        return a - b

    def addition(self, a, b):
        # 加法函数
        return a + b

    def multiplication(self, a, b):
        # 乘法函数
        return a * b

    def division(self, a, b):
         # 除法函数
```

## input
### Requirements
{requirements}

### Selected Code
```{language}
{selectedText}
```

### API Documents
{api_docs}

## output"""

# 划词打标签模板
# flake8: noqa
INITIAL_TAG_PROMPT = """## Instructions
You are an experienced front-end engineer and natural language processing engineer.
Your tasks can be summarized as follows:
- First, ensure that you fully understand the meaning and semantics of the "input" content provided.
- Next, analyze the front-end development concepts mentioned in the "input" content,
  and identify the directly related custom components and their respective functionalities.
- Record the functionalities and relevant key information of each component using tags.
- Finally, group the components based on their functionalities,
  which contributes to retrieve relevant examples of each component functionality.
  Business-specific information (such as regular table columns and form items) should be ignored.
Please refer to the "Chain-of-Thought example" and think things through one step at a time.
The output must be concise and impersonal (see the output in the Chain-of-Thought example).

## Chain-of-Thought example
### input
去掉勾选列，新增port列，放在ip列后面
### output
1、【表格】【基本使用】

## Chain-of-Thought example
### input
在下面代码中，添加一个必填的表单项，表单项内容为分支单选组件
### output
1、【表单项】【必填】
2、【分支单选】【基本使用】

## Chain-of-Thought example
### input
在下面表单项代码中添加一个选择用户弹窗
### output
1、【选择用户弹窗】【基本使用】

## Chain-of-Thought example
### input
生成一个异步关闭的IxModal组件，其内部是一个form表单，表单项有域名，ip，描述
### output
1、【IxModal】【异步关闭】
2、【form表单】【基本使用】

## Chain-of-Thought example
### input
生成一个tabs容器
### output
1、【tabs容器】【基本使用】

## Chain-of-Thought example
### input
设置快速选择为最近24小时
### output
1、【时间选择器】【快速选择】

## Chain-of-Thought example
### input
给表格添加操作列，操作列有一个删除按钮，点击删除按钮携带该行的uuid，发送POST请求'api/v1/delete'，接口成功后消息提示
### output
1、【表格】【删除功能】
2、【接口请求】【POST】
2、【消息提示】【接口成功】

## Chain-of-Thought example
### input
将该抽屉的footer的按钮组使用间距组件包裹
### output
1、【间距】【基本使用】

## Chain-of-Thought example
### input
在第一个表单子项中添加一个tab，tab项有：待审批，已通过，已拒绝
### output
1、【tab】【基本使用】

## Chain-of-Thought example
### input
在页面中添加一个tag标签页组件，包含待审批、已通过、已拒绝三个选项卡
### output
1、【tag标签页】【基本使用】

## Chain-of-Thought example
### input
在表单的最后添加一个行号输入框，错误信息的属性值为errors，该输入框的值为macAddress， 当formData.excludeSwitchMac等于status.value.disable时禁用该输入框
### output
1、【行号输入框】【基本使用】

## Chain-of-Thought example
### input
在下面代码中，添加一个用户/部门选择穿梭框的自定义搜索项
### output
1、【用户/部门选择穿梭框】【基本使用】

## Chain-of-Thought example
### input
在表格和抽屉的中间添加一个分页器组件，并绑定pagination的所有数据，页数的值为pagination.pageIndex,分页器大小为pagination.pageSize
### output
1、【分页器】【基本使用】
2、【分页器】【绑定pagination】

## Chain-of-Thought example
### input
在当前文件生成一个表格，有如下功能：1.表格里的操作栏有新增按钮和刷新按钮，其中点击新增需要打开一个弹框，弹框内容是一些基础表单；2.表格里的操作栏有详情按钮，点击可以打开一个详情抽屉；3.表格支持配置列显示隐藏；4.表格里的工具栏支持更多筛选
### output
1、【表格】【基本使用】
2、【表格】【新增功能】【打开弹框】
3、【表格】【刷新功能】
4、【表单】【基本使用】
5、【表格】【详情功能】【详情抽屉】
6、【表格】【列配置】【显示隐藏】
7、【表格】【工具栏】【筛选】

## Chain-of-Thought example
### input
判断是国内用户时，隐藏按钮
### output
1、【判断】【国内用户】

## input
{query}

## output"""

# 划词选择相似示例描述模板
INITIAL_SELECT_PROMPT = """## Instructions
You are an experienced front-end engineer and natural language processing engineer.
Among them, there are three parts of the input: Requirements, Component function tags, and Function description examples.
Background: Requirements refer to the functionalities that need to be implemented,
which may involve the functionalities of some front-end components.
Component function tags are key information extracted after grouping the component functionalities mentioned
in the Requirements.
Function description examples are summaries of the implementation process of a functionality,
each example with a serial number.
You need to understand the grouping and tagging meanings in the Component function tags,
and then select the examples serial number from the Function description examples that match
the component functionalities mentioned in the requirements as references for implementing the requirements.
Your tasks can be summarized as follows:
- Accurately understand the meanings and semantics of the Requirements and the Function description examples.
- Interpret the meanings of grouping and tagging in the Component function tags.
- Then, based on the functionalities inferred from the Requirements and Component function tags,
  select the examples serial number from the Function description examples that have meanings and
  semantics matching the functional points.
  Select at least one for each functional point, unless they are unrelated. This is important.
The output must be concise and need no explanation (see Output in the example).
Let's think step by step with reference to the Chain-of-Thought example.

## Chain-of-Thought example
### input
#### Requirements
表格支持勾选，并能清除勾选
#### Component function tags
1、【表格】【勾选功能】
2、【表格】【清除勾选功能】
#### Functional description examples
1、【表格删除功能】【批量删除】【单个删除】表格删除功能，包含批量删除和单个删除
2、【表格】【勾选项】设置表格中指定的单个或者多个勾选项
3、【表格】【启禁用功能】【批量操作】【单个操作】表格启禁用功能，可以批量操作，也可以单个操作
4、【表格】【勾选项】【表格行】【表格数据】清除表格所有勾选项状态，将已勾选的表格行状态设置为未勾选；清除表格已勾选行；清除表格已勾选数据；清除表格勾选项
### Chain-of-Thought
通过理解需求和功能描述示例的含义和语义以及对组件功能标签中分组和标签的解读；在这个需求中，涉及到了前端的表格组件的勾选功能，可以支持勾选也可以清除勾选；
在功能描述示例中，第2条和第4条都符合表格的勾选功能，但是第4条能支持清除勾选，更合适，所以选择4。
### output
4

## Chain-of-Thought example
### input
#### Requirements
在表格的操作列中，添加编辑和删除两个按钮；在状态列中，添加状态启禁用功能
#### Component function tags
1、【表格】【编辑功能】
2、【表格】【删除功能】
3、【表格】【启禁用功能】
#### Functional description examples
1、【表格】【勾选项】【表格行】【表格数据】清除表格所有勾选项状态，将已勾选的表格行状态设置为未勾选；清除表格已勾选行；清除表格已勾选数据；清除表格勾选项
2、【表格】【新增功能】【抽屉】表格新增功能，新增后打开抽屉
3、【表格编辑】【抽屉】表格编辑功能，编辑后打开抽屉
4、【表格】【搜索功能】表格搜索功能
5、【表格】【启禁用功能】【批量操作】【单个操作】表格启禁用功能，可以批量操作，也可以单个操作
6、【表格删除功能】【批量删除】【单个删除】表格删除功能，包含批量删除和单个删除
### Chain-of-Thought
通过理解需求和功能描述示例的含义和语义以及对组件功能标签中分组和标签的解读；在这个需求中，涉及到了表格组件的编辑、删除、启禁用三个功能点；
在功能描述示例中，第3条满足表格的编辑功能，第5条满足表格的启禁用功能，第6条满足表格的删除功能，所以选3、5、6。
### output
3、5、6

## Chain-of-Thought example
### input
#### Requirements
抽屉支持编辑和详情状态，点击编辑展示表单，点击取消展示详情内容
#### Component function tags
1、【抽屉】【编辑状态】
2、【抽屉】【详情状态】
3、【基础表单】
4、【抽屉】【取消操作】
#### Functional description examples
1、【基础表格】可展开表格
2、【表格】【新增功能】【抽屉】表格新增功能，新增后打开抽屉
3、【表单】基本使用
4、【表格编辑】【抽屉】表格编辑功能，编辑后打开抽屉
5、【基础表格】表头分组
6、【表单抽屉】【关闭抽屉】内容为表单的抽屉，点击抽屉底部的“取消”按钮，将关闭抽屉；关闭表单抽屉；关闭内容为表单的抽屉
7、【抽屉】表单抽屉
8、【抽屉】【编辑】【表单】【取消】【文本详情】【状态】一个可以改变状态的抽屉，点击编辑，抽屉展示表单内容，点击取消，抽屉隐藏表单内容，展示文本详情内容切换状态后抽屉的title也会发生变化；可改变状态的抽屉；改变抽屉的状态
### Chain-of-Thought
通过理解需求和功能描述示例的含义和语义以及对组件功能标签中分组和标签的解读；在这个需求中，涉及到了抽屉组件的支持编辑和详情状态两个功能点以及基础的表单组件；
在功能描述示例中，第3条满足基础的表单组件，第8条直接就能满足表单的支持编辑和详情状态这些功能，所以选3、8。
### output
3、8


## input
### Requirements
{requirements}

### Component function tags
{tags}

### Functional description examples
{selectedText}

## output"""

# 划词sase项目迁移通用模板
INITIAL_REPLACE_PROMPT = """## Instructions
You are an experienced development engineer and natural language processing engineer.
There are two parts to the input: "Requirements" and "Selected Code".
The programming language is {language}.
Your tasks can be summarized as follows:
- Accurately understand the meaning and semantics of "Requirements" and the implementation steps involved.
- You must be based on "Selected Code",
  then follow the steps in Requirements and step by step implement the code that satisfies the meaning of the steps,
  and retain the original code structure and indentation format. 
  The generated code as the "Result".
- When generating code,
  the knowledge points involved must already exist or be covered in selected code.
  You must refuse to freely create knowledge points.
- The "Result" do not omit "Selected Code", it is possible to use the "Result" for "git diff" operations.
  If there are instances of code omission marked with comments in the "Result",
  please restore these comments to the original code in “Selected Code”.
Eventually, return the full "Result" without any explanation.
Please refer to the "Chain-of-Thought example" and think step by step.
The output must be concise and need no explanation (see the output in the Chain-of-Thought example).
Use Markdown formatting in your answers.
Make sure to include the programming language name at the start of the Markdown code blocks.
If you cannot fulfill the "Requirements" or there are no changes, please reply directly in Chinese.

## Chain-of-Thought example
### input
#### Requirements
请按照以下规则顺序执行替换和引入程序：1.在加法函数前面增加一个减法函数；2.再给所有函数添加类型提示语法；3.补全除法函数的代码
#### Selected Code
```python
    def addition(self, a, b):
        # 加法函数
        return a + b

    def multiplication(self, a, b):
        # 乘法函数
        return a * b

    def division(self, a, b):
         # 除法函数
```
#### Chain-of-Thought
确理解“需求”的含义和语义以及所涉及的实现步骤。
通过理解“Requirements”的含义和语义以及所涉及的实现步骤，你可以准确的知道有3个步骤；
1.找到“Selected Code”中加法函数的位置，在它的前面添加一个减法函数，并保证他们的代码风格和缩进格式一致；
2.根据“Instructions”中提到的开发语言“python”，根据其类型提示语法给4个函数添加上；
3.然后参考其他函数的代码风格补全除法函数的代码。
如果在“Result”中出现了任何被省略的代码，那么你要将标记省略的注释恢复成“Selected Code”中的原始代码。
你的回答简明扼要，不需要保留解释。
并且必须在输出中使用Markdown代码块格式。
### output
```python
    def subtraction(self, a: int, b: int) -> int:
        # 减法函数
        return a - b

    def addition(self, a: int, b: int) -> int:
        # 加法函数
        return a + b

    def multiplication(self, a: int, b: int) -> int:
        # 乘法函数
        return a * b

    def division(self, a: int, b: int) -> float:
        # 除法函数
        if b == 0:
            raise ValueError("除数不能为0")
        return a / b
```

## input
### Requirements
{requirements}

### Selected Code
```{language}
{selectedText}
```

## output"""

# 筛选组件及hook
INITIAL_PROMPT_COMPONENT = """## Instructions
You are an experienced development engineer and natural language processing engineer.
There are two parts to the input: "Requirements" and "Components".
Your tasks can be summarized as follows:
- Accurately understand the meanings and semantics of "Requirements".
- Select components that are directly related to the "Requirements" from the "Components" one by one.
- Results are separated by commas.
Please refer to the "Chain-of-Thought example" and think things through one step at a time.
The output must be concise and need no explanation (see the output in the Chain-of-Thought example).

## Chain-of-Thought example
### input
#### Requirements
在下面表单项代码中添加一个分支选择器组件，最大选择数量为2048，需要从props参数中获取选项值，并且判断是否开启分权分域，是否添加只读状态
#### Components
IxForm,IxFormItem,IxInput,IxIcon,IxCheckbox,IxButton,IxRow,IxCol,IxBranchGroupSelect,IxBranchSelectModal,sf-form-item
### output
IxBranchGroupSelect

## Chain-of-Thought example
### input
#### Requirements
编写一个空状态组件，描述内容为“没有数据”并展示一个操作按钮
#### Components
IxSpace,IxButton,IxCopy,IxProTable,empty,IxDateRange
### output
IxButton,empty

## Chain-of-Thought example
### input
#### Requirements
在表格头部处增加刷新表格功能 
#### Components
IxProTable,IxHeader,IxSpace,IxButton,IxAlert,useIduxTable,valueAddUnit 
### output
IxProTable,IxHeader,useIduxTable

## Chain-of-Thought example
### input
#### Requirements
在这个表格的操作列中，添加编辑和删除两个按钮；在状态列中，添加状态启禁用功能 
#### Components
IxProTable,IxSpace,IxButton,ViewOrEditDrawer,IxSaseToolbar,status-drop-down-menu,single-layout,useIduxTable,DrawerState,useIduxTableSelect,useModal,useMessage 
### output
IxButton,useIduxTable,useIduxTableSelect

## Chain-of-Thought example
### input
#### Requirements
在IxModal组件上添加visible属性，值为props中的visible 
#### Components
IxModal,IxProTable,IxButton,ref,reactive,withDefaults,TablePagination,ProTableColumn,$i,useVModel 
### output
IxModal

## Chain-of-Thought example
### input
#### Requirements
在single-layout组件的title插槽中添加一个开关组件，尺寸为sm，加载属性使用loading值 
#### Components
IxSpace,IxConfirmSwitch,IxButton,single-layout,IxAlert,IxCard,IxProTable,IxHeader,IxTooltip,IxInput,IxEmpty,TextRender,TextRenderItem,StatusDropDownMenu,AppDrawer,DrawerState,useIduxTable,useMessage,useModal 
### output
IxConfirmSwitch

## Chain-of-Thought example
### input
#### Requirements
为输入框添加进行强度检查，不显示强度进度条，包含3个校验配置：1. 10-30个字符，2. 至少包含以下二项：大写字母、小写字母、数字和特殊字符如_@？+等，3. 不能包含用户名、常用字符组合 
#### Components
IxSpace,IxHeader,IxInput,HintStrength,IxButton,HintItem 
### output
HintStrength,HintItem

## Chain-of-Thought example
### input
#### Requirements
在第一个表单子项中添加一个输入框，输入框控制器为name
#### Components
IxForm,IxFormItem,IxInput,IxIcon,IxCheckbox,IxButton,IxRow,IxCol,IxSaseToolbar,IxModal,UserGroupSelect,Validators,useFormGroup 
### output
IxInput


## input
### Requirements
{requirements}

### Components
{components}

## output"""
