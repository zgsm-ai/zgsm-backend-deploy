#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa
"""
    :Author: Huang Weilian z24224
    :Time: 2023/9/7 14:18
    :Modifier: Huang Weilian z24224
    :UpdateTime: 2023/9/7 14:18
"""

# Initial question template for highlighting word dialogue
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

# Question template for highlighting word dialogue without selecting code
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

# Question template for highlighting word dialogue (optimized version)
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
Add a subtraction function before the addition function and add type hint syntax to the subtraction function
#### Selected Code
```python
    def addition(self, a, b):
        # Addition function
        return a + b

    def multiplication(self, a, b):
        # Multiplication function
        return a * b

    def division(self, a, b):
         # Division function
```
#### Code example snippets
1、Multiplication function containing type hint syntax:
def multiplication(a: int, b: int) -> int:
    return a * b
#### API Documents
1、Type hint API：
|Name|value|
|:---|:---|
|Integer|int|
|Float|float|
|Boolean|bool|
|String|str|
|List|List[<type>]|
|Tuple|Tuple[<type>, ...]|
|Dictionary|Dict[<key_type>, <value_type>]|
|Set|Set[<type>]|
#### Chain-of-Thought
1.  By understanding the meaning and semantics of "Requirements", you can know that you need to add a subtraction function before the addition function in "Selected Code", and then add type hint syntax to the subtraction function.
2.  By understanding the functionality of each example in "Code example snippets" and the technology stack used, you can know that the first example is a multiplication function with type hint syntax,
    which meets the requirement of adding type hint syntax in "Requirements", so you need to learn its writing style.
3.  By understanding each API document in "API Documents", you can find that the "Type hint API" can be used when generating code.
4.  Find the position of the addition function in "Selected Code", add a subtraction function before it, and ensure that their code style and indentation format are consistent; then add the hint syntax to the newly generated subtraction function.
5.  The division function in "Selected Code" is incomplete, but it does not affect the implementation of "Requirements", so its integrity can be ignored.
6.  The type hint syntax knowledge points required in "Requirements" exist in "Code example snippets" and can be directly cited without creating a new type hint syntax knowledge point.
7.  If any omitted code appears in the "Result", you need to restore the comments marked as omitted to the original code in "Selected Code".
8.  Your answer should be concise and without explanation. And you must use Markdown code block format in the output.
### output
```python
    def subtraction(self, a: int, b: int) -> int:
        # Subtraction function
        return a - b

    def addition(self, a, b):
        # Addition function
        return a + b

    def multiplication(self, a, b):
        # Multiplication function
        return a * b

    def division(self, a, b):
         # Division function
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

# General code generation template for highlighting word dialogue
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
Add a subtraction function before the addition function and add type hint syntax to the subtraction function
#### Selected Code
```python
    def addition(self, a, b):
        # Addition function
        return a + b

    def multiplication(self, a, b):
        # Multiplication function
        return a * b

    def division(self, a, b):
         # Division function
```
#### API Documents
1、Type hint API
|Name|value|
|:---|:---|
|Integer|int|
|Float|float|
|Boolean|bool|
|String|str|
|List|List[<type>]|
|Tuple|Tuple[<type>, ...]|
|Dictionary|Dict[<key_type>, <value_type>]|
|Set|Set[<type>]|
#### Chain-of-Thought
By understanding the API documents in "API Documents", you can learn the "Type hint API".
By understanding the meaning and semantics of "Requirements", you can know that you need to add a subtraction function before the addition function in "Selected Code", and then add type hint syntax to the subtraction function.
Find the position of the addition function in "Selected Code", add a subtraction function before it, and ensure that their code style and indentation format are consistent; then add the hint syntax to the newly generated subtraction function.
The division function in "Selected Code" is incomplete, but it does not affect the implementation of "Requirements", so its integrity can be ignored.
If any omitted code appears in the "Result", you need to restore the comments marked as omitted to the original code in "Selected Code".
Your answer should be concise and without explanation.
And you must use Markdown code block format in the output.
### output
```python
    def subtraction(self, a: int, b: int) -> int:
        # Subtraction function
        return a - b

    def addition(self, a, b):
        # Addition function
        return a + b

    def multiplication(self, a, b):
        # Multiplication function
        return a * b

    def division(self, a, b):
         # Division function
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

# Tagging template for highlighting words
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
Remove the checked column, add the port column, and place it after the ip column
### output
1.  【Table】【Basic Usage】

## Chain-of-Thought example
### input
In the following code, add a required form item, and the form item content is a branch radio component
### output
1.  【Form Item】【Required】
2.  【Branch Radio】【Basic Usage】

## Chain-of-Thought example
### input
Add a select user pop-up window in the following form item code
### output
1.  【Select User Pop-up】【Basic Usage】

## Chain-of-Thought example
### input
Generate an asynchronous IxModal component, which internally is a form form, and the form items include domain name, ip, and description
### output
1.  【IxModal】【Asynchronous Close】
2.  【Form Form】【Basic Usage】

## Chain-of-Thought example
### input
Generate a tabs container
### output
1.  【Tabs Container】【Basic Usage】

## Chain-of-Thought example
### input
Set the quick selection to the last 24 hours
### output
1.  【Time Selector】【Quick Selection】

## Chain-of-Thought example
### input
Add an operation column to the table, the operation column has a delete button, clicking the delete button carries the uuid of the row, sends a POST request 'api/v1/delete', and displays a message after the interface is successful
### output
1.  【Table】【Delete Function】
2.  【Interface Request】【POST】
3.  【Message Prompt】【Interface Successful】

## Chain-of-Thought example
### input
Wrap the footer button group of the drawer with a spacing component
### output
1.  【Spacing】【Basic Usage】

## Chain-of-Thought example
### input
Add a tab to the first form subitem, and the tab items include: pending approval, approved, and rejected
### output
1.  【Tab】【Basic Usage】

## Chain-of-Thought example
### input
Add a tag tab component to the page, including three tabs: pending approval, approved, and rejected
### output
1.  【Tag Tab】【Basic Usage】

## Chain-of-Thought example
### input
Add a line number input box to the end of the form, the attribute value of the error message is errors, the value of the input box is macAddress, and the input box is disabled when formData.excludeSwitchMac equals status.value.disable
### output
1.  【Line Number Input Box】【Basic Usage】

## Chain-of-Thought example
### input
In the following code, add a custom search item for the user/department selection shuttle box
### output
1.  【User/Department Selection Shuttle Box】【Basic Usage】

## Chain-of-Thought example
### input
Add a pager component between the table and the drawer, and bind all the data of pagination, the page number value is pagination.pageIndex, and the pager size is pagination.pageSize
### output
1.  【Pager】【Basic Usage】
2.  【Pager】【Bind Pagination】

## Chain-of-Thought example
### input
Generate a table in the current file with the following functions: 1. The operation bar in the table has an add button and a refresh button, where clicking add needs to open a pop-up window, and the pop-up window content is some basic forms; 2. The operation bar in the table has a detail button, clicking can open a detail drawer; 3. The table supports configuring column display and hiding; 4. The toolbar in the table supports more filtering
### output
1.  【Table】【Basic Usage】
2.  【Table】【Add Function】【Open Pop-up Window】
3.  【Table】【Refresh Function】
4.  【Form】【Basic Usage】
5.  【Table】【Detail Function】【Detail Drawer】
6.  【Table】【Column Configuration】【Show and Hide】
7.  【Table】【Toolbar】【Filter】

## Chain-of-Thought example
### input
Hide the button when judging that it is a domestic user
### output
1.  【Judgment】【Domestic User】

## input
{query}

## output"""

# Highlight word selection similar example description template
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
The table supports checking and can clear the check
#### Component function tags
1.  【Table】【Check Function】
2.  【Table】【Clear Check Function】
#### Functional description examples
1.  【Table Delete Function】【Batch Delete】【Single Delete】Table delete function, including batch delete and single delete
2.  【Table】【Check Item】Set the specified single or multiple check items in the table
3.  【Table】【Enable and Disable Function】【Batch Operation】【Single Operation】Table enable and disable function, can be batch operated or single operated
4.  【Table】【Check Item】【Table Row】【Table Data】Clear all check item states in the table, set the checked table row state to unchecked; clear the checked table rows; clear the checked table data; clear the table check items
### Chain-of-Thought
By understanding the meaning and semantics of the requirements and function description examples, and interpreting the grouping and tags in the component function tags; in this requirement, it involves the check function of the front-end table component, which can support checking and clearing the check;
In the function description examples, items 2 and 4 both meet the check function of the table, but item 4 can support clearing the check, which is more suitable, so select 4.
### output
4

## Chain-of-Thought example
### input
#### Requirements
Add two buttons, edit and delete, in the operation column of the table; add enable and disable function in the status column
#### Component function tags
1.  【Table】【Edit Function】
2.  【Table】【Delete Function】
3.  【Table】【Enable and Disable Function】
#### Functional description examples
1.  【Table】【Check Item】【Table Row】【Table Data】Clear all check item states in the table, set the checked table row state to unchecked; clear the checked table rows; clear the checked table data; clear the table check items
2.  【Table】【Add Function】【Drawer】Table add function, open the drawer after adding
3.  【Table Edit】【Drawer】Table edit function, open the drawer after editing
4.  【Table】【Search Function】Table search function
5.  【Table】【Enable and Disable Function】【Batch Operation】【Single Operation】Table enable and disable function, can be batch operated or single operated
6.  【Table Delete Function】【Batch Delete】【Single Delete】Table delete function, including batch delete and single delete
### Chain-of-Thought
By understanding the meaning and semantics of the requirements and function description examples, and interpreting the grouping and tags in the component function tags; in this requirement, it involves three function points of the table component: edit, delete, and enable/disable;
In the function description examples, item 3 meets the edit function of the table, item 5 meets the enable/disable function of the table, and item 6 meets the delete function of the table, so select 3, 5, and 6.
### output
3、5、6

## Chain-of-Thought example
### input
#### Requirements
The drawer supports edit and detail states, clicking edit displays the form, clicking cancel displays the detail content
#### Component function tags
1.  【Drawer】【Edit State】
2.  【Drawer】【Detail State】
3.  【Basic Form】
4.  【Drawer】【Cancel Operation】
#### Functional description examples
1.  【Basic Table】Expandable table
2.  【Table】【Add Function】【Drawer】Table add function, open the drawer after adding
3.  【Form】Basic Usage
4.  【Table Edit】【Drawer】Table edit function, open the drawer after editing
5.  【Basic Table】Table header grouping
6.  【Form Drawer】【Close Drawer】The content is a drawer of the form, clicking the "Cancel" button at the bottom of the drawer will close the drawer; close the form drawer; close the drawer whose content is a form
7.  【Drawer】Form Drawer
8.  【Drawer】【Edit】【Form】【Cancel】【Text Detail】【State】A drawer that can change the state, clicking edit, the drawer displays the form content, clicking cancel, the drawer hides the form content and displays the text detail content, the title of the drawer will also change after switching the state; a drawer that can change the state; change the state of the drawer
### Chain-of-Thought
By understanding the meaning and semantics of the requirements and function description examples, and interpreting the grouping and tags in the component function tags; in this requirement, it involves two function points of the drawer component: support for edit and detail states, as well as the basic form component;
In the function description examples, item 3 meets the basic form component, and item 8 directly meets the function of supporting edit and detail states of the form, so select 3 and 8.
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

# General template for migrating sase projects with highlighting words
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
Please execute the replacement and import program in the following order: 1. Add a subtraction function before the addition function; 2. Add type hint syntax to all functions; 3. Complete the code of the division function
#### Selected Code
```python
    def addition(self, a, b):
        # Addition function
        return a + b

    def multiplication(self, a, b):
        # Multiplication function
        return a * b

    def division(self, a, b):
         # Division function
```
#### Chain-of-Thought
Accurately understand the meaning and semantics of "Requirements" and the implementation steps involved.
By understanding the meaning and semantics of "Requirements" and the implementation steps involved, you can accurately know that there are 3 steps;
1. Find the position of the addition function in "Selected Code", add a subtraction function before it, and ensure that their code style and indentation format are consistent;
2. According to the development language "python" mentioned in "Instructions", add type hints to the 4 functions according to its type hint syntax;
3. Then refer to the code style of other functions to complete the code of the division function.
If any omitted code appears in the "Result", you need to restore the comments marked as omitted to the original code in "Selected Code".
Your answer should be concise and without explanation.
And you must use Markdown code block format in the output.
### output
```python
    def subtraction(self, a: int, b: int) -> int:
        # Subtraction function
        return a - b

    def addition(self, a, b):
        # Addition function
        return a + b

    def multiplication(self, a, b):
        # Multiplication function
        return a * b

    def division(self, a: int, b: int) -> float:
        # Division function
        if b == 0:
            raise ValueError("Divisor cannot be 0")
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

# Filter components and hooks
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
Add a branch selector component to the following form item code, the maximum selection quantity is 2048, need to get the option value from the props parameter, and judge whether to enable power decentralization, whether to add read-only status
#### Components
IxForm,IxFormItem,IxInput,IxIcon,IxCheckbox,IxButton,IxRow,IxCol,IxBranchGroupSelect,IxBranchSelectModal,sf-form-item
### output
IxBranchGroupSelect

## Chain-of-Thought example
### input
#### Requirements
Write an empty state component, the description content is "No data" and display an operation button
#### Components
IxSpace,IxButton,IxCopy,IxProTable,empty,IxDateRange
### output
IxButton,empty

## Chain-of-Thought example
### input
#### Requirements
Add a refresh table function at the head of the table
#### Components
IxProTable,IxHeader,IxSpace,IxButton,IxAlert,useIduxTable,valueAddUnit
### output
IxProTable,IxHeader,useIduxTable

## Chain-of-Thought example
### input
#### Requirements
Add two buttons, edit and delete, in the operation column of this table; add status enable/disable function in the status column
#### Components
IxProTable,IxSpace,IxButton,ViewOrEditDrawer,IxSaseToolbar,status-drop-down-menu,single-layout,useIduxTable,DrawerState,useIduxTableSelect,useModal,useMessage
### output
IxButton,useIduxTable,useIduxTableSelect

## Chain-of-Thought example
### input
#### Requirements
Add the visible attribute to the IxModal component, the value is visible in the props
#### Components
IxModal,IxProTable,IxButton,ref,reactive,withDefaults,TablePagination,ProTableColumn,$i,useVModel
### output
IxModal

## Chain-of-Thought example
### input
#### Requirements
Add a switch component to the title slot of the single-layout component, the size is sm, and the loading attribute uses the loading value
#### Components
IxSpace,IxConfirmSwitch,IxButton,single-layout,IxAlert,IxCard,IxProTable,IxHeader,IxTooltip,IxInput,IxEmpty,TextRender,TextRenderItem,StatusDropDownMenu,AppDrawer,DrawerState,useIduxTable,useMessage,useModal
### output
IxConfirmSwitch

## Chain-of-Thought example
### input
#### Requirements
Add a strength check to the input box, do not display the strength progress bar, including 3 verification configurations: 1. 10-30 characters, 2. At least include two of the following: uppercase letters, lowercase letters, numbers and special characters such as _@?+ etc., 3. Cannot include usernames, common character combinations
#### Components
IxSpace,IxHeader,IxInput,HintStrength,IxButton,HintItem
### output
HintStrength,HintItem

## Chain-of-Thought example
### input
#### Requirements
Add an input box to the first form subitem, the input box controller is name
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
