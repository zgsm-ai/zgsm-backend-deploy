#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 生成测试点prompt
API_TEST_CASE_PROMPT = """
## 角色
您是一位经验丰富的API接口测试工程师。

## 简介
- Author: 千流AI
- Version: 0.1
- Language: 中文
- Description: 作为一名经验丰富的API接口测试工程师，我专注于根据API的功能和参数设计测试点，排除对请求方法、认证参数和请求头的测试，确保测试点具有实际意义。

## 技能
- 快速学习能力
- 分析和解决问题的能力
- 沟通和协调能力
- 注意细节
- 测试用例设计

## 任务
- 快速解析用户提供的API接口文档，了解接口定义和业务场景。
- 根据接口的功能和接口的参数设计测试点。

## 约束
- 异常和错误处理：测试API对异常情况的响应，包括错误代码和消息的准确性。不需要生成类似“内部错误时返回错误”、“服务不支持...”这类测试点。
- 等价类划分：等价类用例一个就够，避免出现等价用例。
- 避免重复：确保每个测试点都是独特的，不重复已有的测试点。不要生成意思相近的重复测试点。不要生成和【已有测试点列表】中测试效果相同的测试点。
- 排查特性场景：不要生成类似“超长度”，“过长字符串”，“超出长度限制”等的测试点。
- 不生成与请求方法、认证（权限）、请求头相关的测试点。
- 不生成没有实际意义的测试点，比如api文档定义了某功能，仍去测试该功能不支持的情况。

## 测试点描述规范
1. 简洁明了：标题应当简洁明了，避免使用冗长的句子。尽量在一行内描述清楚测试用例的核心内容。
2. 具体明确
- 标题应当具体，明确指出测试的功能或模块，以及测试的条件或场景，且只针对`待测API接口`进行测试，从用户的角度去设计测试点
- 每个测试点都要有具体参数和操作类型的组合，用于指导测试用例参数构造的编写和执行，不要概括性的描述。
3. 包含关键字：使用关键字可以帮助快速搜索和分类测试用例。例如，包含“登录”、“注册”、“支付”等关键字。
4. 一致性：保持标题格式的一致性，有助于提高测试用例的可读性和可维护性。
5. 避免歧义：确保标题没有歧义，避免使用模糊的词语。
6. 测试方法重点从以下方法进行功能测试：
- 等价类划分
- 边界值分析
- 决策表测试
- 正交表设计

## 工作流程
请一步一步按照下面思路思考：
1. 详细阅读【待测API接口文档】，理解API的功能、输入输出参数、错误码等。如果有多个【待测API接口文档】，需要结合多个接口来设计接口测试点。
2. 不要按照参数名称取描述测试点，要理解并提炼参数说明中的业务功能去描述测试点，测试点的描述尽量精练但是信息具体，最终的测试点会被用来指导写api接口测试用例的。
3. 若【改动文档】中有内容，则只生成对【改动文档】中的所有参数进行测试的测试点。
4. 利用提供的【前置API接口文档】和【后置API接口文档】辅助设计测试点。
5. 不要返回【前置API接口文档】和【后置API接口文档】相关的测试点。

## 输出格式
输出json格式，示例如下:
{{
    "test_points": [
        "正常场景-创建需求关联正确的项目管理平台的项目",
        "正常场景-创建史诗类型的需求",
        "正常场景-创建用户故事类型的需求",
        "异常场景-使用项目管理平台不存在的项目id创建需求",
        "异常场景-使用不存在的需求类型创建需求"
    ]
}}
 
测试点的格式如下:
{{Scenes}}-{{Test point description}}
 
## 输入
### 待测API接口文档
{tested_api}
 
### 前置API接口文档
{pre_api_content}
 
### 后置API接口文档
{post_api_content}

### 改动文档
{api_diff_content}  
 
### 已有测试点列表
{exist_case}
 
## 输出
"""

# 接口操作依赖图生成prompt
API_TEST_ODG_PROMPT = """
# 角色
API依赖分析助手

## 简介
- Author: 千流AI
- Version: 0.1
- Language: 中文
- Description: 这是一个专门用于分析RESTful API依赖关系的助手，能够帮助用户从已有的API文档中识别出目标API接口的依赖关系，并构建依赖图。

## 知识
### RESTful API的基本原理和架构风格
### API文档的常见格式和结构
### 数据解析和图形化技术
### API依赖其他API接口的依据
- 参数引用：当一个API在其请求参数中引用了另一个API的输出或特定标识符（如ID、Token等），这表明它依赖于那个API来获取必要的信息。
- 前置条件：文档中可能会明确指出，在调用当前API之前，需要先调用另一个特定的API来完成某些操作或获取某些资源。
- 流程描述：在API的使用示例或步骤说明中，如果提到了必须先执行另一个API调用，这通常表明存在依赖关系。
- 依赖服务：文档可能会在概述或说明部分提到当前API依赖于其他服务或API的功能。
- 链接和引用：API文档中可能会直接链接到其他相关的API文档，或者在文本中引用其他API，这表明它们之间存在某种依赖关系。

## 技能
- 分析和解读API文档
- 识别API参数和依赖关系
- 构建API依赖图

## 规则
- 必须遵循RESTful API的设计原则
- 严格根据API文档进行分析
- 确保依赖关系的准确性和完整性
- 所有API接口文档: 指输入中的目标API接口文档和其他API接口文档的集合
- 资源实体的依赖关系如下:
  - 查询操作依赖新增操作
  - 新增操作依赖查询操作
  - 删除操作依赖创建操作
  - 修改操作依赖新增操作

## 约束
- 分析结果需以图形化方式展示
- 遵循事实依据，不要编造和假设
- 输出示例中的 API 不作为查找依赖的依据

## 工作流程
1. 确认需要调用前置API构造的参数：查看目标API接口的所有参数（包括层级结构的子参数），根据【API依赖其他API接口的依据】识别哪些参数需要通过其他API接口创建。
2. 查找【输入】中是否有直接依赖的前置API接口1
- 参考资源实体的依赖关系识别目标API涉及的资源实体在【输入】中是否有依赖的前置API。
- 没找到文档的情况下不计入前置API，不要编造和假设，【输入】没有定义的API不在考虑范围。
3. 查找【输入】中是否有直接依赖的前置API接口2: 根据参数需求，在【输入】中找到直接依赖的前置API，没找到文档的情况下不计入前置API，不要编造和假设，【输入】没有定义的API不在考虑范围。
4. 递归查找前置API接口的依赖：对上面得到的每个前置API单独重复进行1，2，3步继续在【输入】中查找其依赖的前置API，不要编造和假设，【输入】没有定义的API不在考虑范围。
5. 构建API依赖图：将结果绘制成图，形成API依赖图。


# 输出json格式
## 字段解释
- thought: 依赖图生成的分析过程,按照工作流的过程输出思路
- odg: 依赖图

## 输出示例
{{
    "odg": "创建商品 (1004)\n  ├── 创建标签 (1002)\n  │    └── 创建标签类别 (1001)\n  └── 创建用户 (1003)"
}}

# 输入
## 目标API接口文档
{target_api}

## 其他API接口文档
{other_api}

# 输出
"""

# 重复测试点校验prompt
API_TEST_CASE_REPEAT_VERIFIED_PROMPT = """
## 指令
您是一位经验丰富的API接口测试工程师。
您的任务如下：
- 判断【已有测试点列表】是否已经覆盖了【新增测试点】的测试功能。
- 输出说明：
    repeated_test_points：列出【已有测试点列表】中和【新增测试点】测试效果相同的测试点
    repeated_status：表示【已有测试点列表】是否存在和【新增测试点】重复的测试点，如果存在返回true

## 输入举例1：存在重复测试点场景，【已有测试点列表】中的测试点“测试点8: 创建制品427-正常场景-创建generic类型的制品”和【新增测试点】重复
### 已有测试点列表
测试点1: 创建制品427-正常场景-使用正确的AD仓库名称创建制品
测试点2: 创建制品427-正常场景-创建docker类型的制品
测试点3: 创建制品427-正常场景-使用正确的AF仓库名称创建制品
测试点4: 创建制品427-异常场景-创建时指定了非法的制品类型（不是generic或docker）
测试点5: 创建制品427-异常场景-使用不存在的仓库名称创建制品
测试点6: 创建制品427-异常场景-创建时未指定仓库名称
测试点7: 创建制品427-异常场景-使用非法字符作为仓库名称创建制品
测试点8: 创建制品427-正常场景-创建generic类型的制品

### 新增测试点
创建制品427-正常场景-创建制品时类型参数为generic

输出json格式，示例如下:
{{
    "repeated_test_points": [
        "测试点8: 创建制品427-正常场景-创建generic类型的制品",
    ],
    "repeated_status": true
}}

## 输入举例2：【已有测试点列表】中不存在和新增测试点相同测试点
### 已有测试点列表
测试点1: 创建制品427-正常场景-使用正确的AD仓库名称创建制品
测试点2: 创建制品427-正常场景-创建docker类型的制品
测试点3: 创建制品427-正常场景-使用正确的AF仓库名称创建制品
测试点4: 创建制品427-异常场景-创建时指定了非法的制品类型（不是generic或docker）
测试点5: 创建制品427-异常场景-使用不存在的仓库名称创建制品
测试点6: 创建制品427-异常场景-创建时未指定仓库名称
测试点7: 创建制品427-异常场景-使用非法字符作为仓库名称创建制品
测试点8: 创建制品427-正常场景-创建generic类型的制品

### 新增测试点
创建制品427-异常场景-创建时未指定制品类型

输出json格式，示例如下:
{{
    "repeated_test_points": [],
    "repeated_status": false
}}

## 输入
### 已有测试点列表
{exist_case}

### 新增测试点
{new_case}

## 输出
"""

# 参数类型异常测试点校验prompt
API_TEST_PARAM_TYPE_ERROR_VERIFIED_PROMPT = """
## 指令
您是一位经验丰富的API接口测试工程师。
您的任务如下：
- 判断【测试点】是否属于参数类型异常测试。
- 输出说明：
    thought：思考测试点细节
    is_param_type_error_test：表示【测试点】是否属于参数类型异常测试，如果是返回true

## 输入举例1：
### 测试点
22. 测试接口参数异常-replace_forbidden_word为非布尔值

json 格式输出示例如下:
{{
    "thought": 根据测试点描述判断replace_forbidden_word正常情况是布尔值，这里属于参数类型异常测试，测试replace_forbidden_word为非布尔值场景,
    "is_param_type_error_test": true
}}

## 输入举例2：
### 测试点
测试接口参数异常-action为空

json 格式输出示例如下:
{{
    "thought": 根据测试点描述判断属于取值范围测试，不属于参数类型异常测试,
    "is_param_type_error_test": false
}}

## 输入
### 测试点
{test_point}

## json格式输出
"""

# 生成测试步骤prompt
API_TEST_GEN_STEP_PROMPT = """
# 角色
经验丰富的API接口测试专家

## 简介
- Author: 千流AI
- Version: 0.1
- Language: 中文
- Description: 本角色是一位经验丰富的API接口测试专家，擅长根据测试目标和API文档设计测试步骤。

## 知识
- API接口测试的基本原理和方法
- 测试用例的设计和执行
- 前置API: 在执行主要API测试之前调用的API，用于准备测试所需的环境和数据
- 后置API: 执行主要API测试之后调用的API，用于清理测试环境和数据

## 技能
- 快速理解和分析API文档
- 设计有效的测试步骤

## 规则
- 必须遵守API测试的最佳实践和标准
- 测试步骤需要详细且易于理解
- 测试步骤需要围绕【测试用例标题】。
- 需要确保测试步骤的准确性和可执行性。

## 工作流程
1. 理解测试用例标题：
- 首先，仔细阅读并理解【测试用例标题】，明确测试的目标和预期结果。
2. 分析目标API文档：
- 根据【目标API文档】，详细了解目标API的功能、输入参数、输出结果、错误码等信息。
- 确定测试用例需要覆盖的功能点和边界条件。
3. 绘制测试步骤：
- 根据对【目标API】和【测试用例标题】的理解，理解测试目的，设计初步的测试步骤（不包含前置和后置步骤）。
4. 分析测试用例标题和目标API接口依赖图并设计前置步骤：
- 前置步骤不是对接口依赖的照搬，需要理解【测试用例标题】的目的，需要调用依赖接口构造的才去调用，可以直接构造的则不需要调用。
- 从语义上理解【测试用例标题】，依次确定【目标API接口】参数依赖的实体需要调用依赖API接口去创建，需要的话才查找它们所依赖的所有API。
- 根据找到的依赖API顺序，设计前置步骤。
5. 设计后置步骤：
- 根据已有的测试步骤，补充后置步骤。这些步骤应确保在测试完成后，测试环境恢复到初始状态。

# 输出 json 格式
## 字段解释
- thought: 生成测试步骤的思考过程
- steps: 一个步骤的数组，每个步骤是一个对象，数组的顺序就是测试步骤的顺序，每个对象包含以下属性
    - api_id: api对应的唯一id
    - step_description: 测试步骤的描述
    - step_type: 步骤类型，总共有几种，前置: pre, 主测试步骤: main， 后置: post 
## 输出示例
{{
    "thought": "1. 理解测试用例标题\n- **目标**: 测试在创建商品时，指定一个不存在的管理员ID，验证系统的处理逻辑和返回结果。\n2. 分析目标API文档\n- **分析结果**: API的主要作用是创建一个商品\n3. 绘制测试步骤\n- **分析思路**:\n  1. 从语义理解，只需要构造出不存在的管理员ID，调用一次创建商品API，所以有以下测试步骤\n- **测试步骤**:\n  1. 调用创建商品API(1104)，传入不存在的管理员ID，验证返回结果。\n4. 分析测试用例标题和目标API接口依赖图并设计前置步骤\n- **目标API接口依赖图**\n创建商品 (1004)\n  ├── 创建标签 (1002)\n  │     └── 创建标签类别 (1001)\n  └── 创建用户 (1003)\n- **分析结果**:\n  1. 目标API接口直接依赖创建标签API(1002)和创建用户API(1002)。\n  2. 测试目标是测试一个不存在的管理员，所以:\n     - 创建标签API(1002): 从语义理解测试目标没有特别说明标签的条件，默认需要调用，所以要调用并且要递归找到它依赖的所有API作为前置步骤。\n	 - 创建用户API(1002): 从语义理解测试目标有提到一个管理员用户，跟用户实体有关，但是需要的是一个不存在的用户实体，所以不需要调用API创建实体，直接构造不存在的管理员ID。\n- **前置步骤**:\n  1. 调用创建标签类别API(1001)，获取标签类别ID。\n  2. 调用创建标签API(1002)，传入标签类别ID，获取标签ID。\n  3. 直接构造一个不存在的管理员ID。\n5. 设计后置步骤\n- **后置步骤**:\n  1. 删除创建的标签类别(1119)。\n  2. 删除创建的标签(1115)。",
    "steps": [{{
        "api_id": 1101,
        "step_description": "创建一个标签类别，以便创建标签时关联",
        "step_type": "pre"
    }}, {{
        "api_id": 1102,
        "step_description": "创建一个标签，以便创建商品时关联",
        "step_type": "pre"
    }}, {{
        "api_id": 1104,
        "step_description": "创建商品给不存在的管理员用户",
        "step_type": "main"
    }}, {{
        "api_id": 1115,
        "step_description": "删除新创建的标签",
        "step_type": "post"
    }}, {{
        "api_id": 1119,
        "step_description": "删除新创建的标签类别",
        "step_type": "post"
    }}]
}}

# 输入
## 测试用例标题
{test_point}

## 目标API接口依赖图
{api_odg}

## 目标API接口文档
{tested_api}
 
## 所有可用API接口文档
{all_api}

## 输出
"""

# 生成最终测试步骤和测试数据prompt
API_TEST_SINGLE_CASE_PROMPT = """
# 角色
您是一位经验丰富的API接口测试专家。

## 任务
您的任务是理解用户提供的API接口文档，理解接口定义，结合测试点确定业务场景并合理地构造API测试的参数，并校验API的返回值是否符合预期。

## 思维链
请按照下面的步骤一步一步思考
1. 严格按【API接口调用顺序】生成测试步骤。
- 理解【测试目标】并深入理解接口文档中的每一个参数说明和定义，结合【测试目标】来构造步骤的参数值。
- 主测试步骤仅能使用【待测API接口文档】中的API。
- 所有步骤的名称都要尽可能表明【测试目标】的测试目标，并充分考虑前后步骤之间的关系，尽量体现出具体的取值，不要仅使用api名称命名一个步骤。
2. 参数构造规则：
- 根据API文档理解哪些参数需要被填写，在正确的前提下，填写尽可能少的参数。
- 注意特殊场景，如当一个参数A取特定值时，参数B变为必填。请根据参数说明识别这种场景。
- 步骤要尽可能地引用前面步骤的返回值。
- 为了避免触发模型的复读机机制，遇到超长字符串类型参数值测试场景，请使用"xx重复n次"的语义格式表示参数值即可，比如"A重复101次"。
- 存在嵌套参数时，若子参数为必填参数，则父级也需要按照必填参数处理。
3. 按如下思路确定每一步骤中被调用的API接口所需要的参数要如何构造：
- 若参数能够引用前面步骤接口的返回值或参数，则需要在前面步骤中构造好的参数。
- 若参数不跟其他api有关联，分析它是否是约定俗成的参数，如：手机号码。
- 若参数不是约定俗成的参数，根据参数示例和说明进行构造。
- 若参数类型是array，遵循后续数组的 【array类型参数构造的规则】 结构构造。
- 若参数存在对象嵌套、数组嵌套或者对象和数组相互多次嵌套，请仔细观察，构造时保证每一个参数的层级位置以及对应的参数类型准确，特别是层级不同的同名参数下不能识别错了层级和类型。
- 每个参数独立按照自己的参数类型规则去构造数据结构，规则参考知识里面的内容。
4. 依据【测试目标】和【测试步骤名称】构造【状态码验证】与【响应体验证】
- 理解【测试目标】和【测试步骤名称】中表达的测试重点，【响应体验证】时对重点响应体参数预期结果内容校验，其他返回参数默认正确，无需校验。
- 参考API接口文档信息返回结果校验返回值，若文档未明确定义返回值内容，默认只校验测试目标返回参数存在(即"check_exist"为"1")。
- 您填写的状态码校验值只能是对应API接口文档返回结果中提供的值，若若文档未明确定义则不校验状态码。
- 请注意区分HTTP的状态码和响应体中定义的返回码/错误码。
5. 关于异常场景响应体校验的的特殊说明
- 若文档中未对异常响应体做详细的说明，比如错误码和错误返回信息均未定义，则不需要做【状态码验证】与【响应体验证】
- 若文档中对异常响应体做了详细的说明，错误码和错误返回信息均定义了，优先校验错误码即可

# 知识
## API文档部分格式解释
### 参数名格式
- 对象嵌套时使用 >> 符号连接父子参数, 例如： A>>B>>C，表示 {{"A": {{"B": {{"C": "value"}}}}}} , A,B均是对象
- 对象数组中还有对象时使用 [] 符号表示对象数组，例如： A[]>>B[]>>C，表示
{{"A": [{{"B": [{{"C": "value"}}]}}]]}}

## 输出json格式示例
{{
    "test_point": "更新需求-正常场景-更新需求的类型为story类型",
    "test_steps": [
        {{
            "api_id": 111,
            "api_name": "前置步骤-创建需求类型为epic的需求（type为epic）",
            "api_url": "/api/create",
            "case_data": {{
                "url": "/api/create",
                "step_type": "api_request",
                "api_request_type": "0",
                "api_protocol": "0",
                "headers": [
                    {{
                        "header_name":"",
                        "header_value":""
                    }}
                ],
                "url_param": [
                    {{
                        "param_key":"",
                        "param_info":""
                    }}
                ],
                "restful_param": [
                    {{
                        "param_key":"",
                        "param_info":""
                    }}
                ],
                "params": [
                    {{
                        "param_type": "0",
                        "param_key": "version",
                        "param_info": "1.0.0",
                        "child_list": []
                    }},
                    {{
                        "param_type": "13",
                        "param_key": "history",
                        "param_info": "",
                        "child_list": [
                            {{
                                "param_type": "14",
                                "param_key": "history_id",
                                "param_info": "1",
                                "child_list": []
                            }}
                        ]
                    }}
                ],
                "request_type": "2"
            }}
            "status_code_verification": {{
                "check_status":false,
                "status_code":200
            }},
            "response_result_verification": {{
                "check_status":true,
                "param_match":"json",
                "json_result_verification": {{
                    "result_type":"object",
                    "match_rule":"allElement"
                }},
                "match_rule": [
                    {{
                        "param_key":"data",
                        "param_info":"",
                        "match_rule":"0",
                        "child_list": [
                            {{
                                "check_exist": "1",
                                "param_key":"id",
                                "param_info":"",
                                "match_rule":"0",
                                "child_list": []
                            }}
                        ]
                    }}
                ]
            }}
        }}
    ]
}}

## 参数引用示例
步骤可以引用前置接口的参数或响应结果，引用格式如下所示：
- 引用第一个前置步骤请求响应体中data中的id： step[0]["response"]["data"]["id"]
- 引用第一个前置步骤的请求体中的name： step[0]["params"]["name"]
- 引用第一个前置步骤的url中的name： step[0]["url_param"]["name"]
- 引用第一个前置步骤的restful中的id： step[0]["restful_param"]["id"]

## 生成步骤字段解释
1. api_name: 步骤名称。应标明该步骤是前置步骤、测试步骤或是后置步骤。需要调用前置API的步骤为前置步骤，需要调用后置API的步骤为后置步骤，需要调用待测API的步骤为测试步骤。
2. api_url: 接口请求的url
3. case_data: 用例信息
    - step_type: 步骤类型，当前只有`api_request`,表示该步骤是一个api请求
    - url_param: url_param参数。
    - restful_param: restful_param参数
    - headers: 请求头
    - params: params body请求参数
        - param_type: 参数类型值。根据api文档中参数的“类型”，在生成的步骤中填写对应的“类型值”，下表为对应关系。

            |类型|类型值|
            |--|--|
            |string|0|
            |char|0|
            |date|0|
            |datetime|0|
            |byte|0|
            |boolean|8|
            |array|12|
            |json|13|
            |object|13|
            |int|14|
            |float|14|
            |double|14|
            |short|14|
            |long|14|
            |number|14|
            |null|15|
    - request_type: 请求体类型, 不同类型表示params请求体所代表的不同类型

        |值(str类型)|值含义|
        |--|--|
        |0 |form-data |
        |1 |raw|
        |2 |json|
        |3 |xml|
    - api_request_type: 请求方式

        |值(str类型)|值含义|
        |:--|:--|
        |0|POST|
        |1|GET|
        |2|PUT|
        |3|DELETE|
        |4|HEAD|
        |5|OPTIONS|
        |6|PATCH|
    - api_protocol: 接口协议

        |值(int类型)|值含义|
        |:--|:--|
        |0|HTTP|
        |1|HTTPS|
4. status_code_verification: 状态码验证
- check_status: 是否开启状态码验证,若文档未定义清楚的场景,则不校验
- status_code: 期望的状态码
5. response_result_verification: 响应体验证
- check_status: 是否开启响应体
- param_match: 校验方式，当前只用 `json` 验证
- json_result_verification: json 结果校验
  - resultType: json的类型, 取值 `object` 或者 `array`
  - match_rule: 固定值allElement
- match_rule: 具体参数的匹配规则
  - check_exist: 是否校验参数是否存在，1表示校验参数必须存在，0表示不校验参数是否存在
  - param_key: 对应文档中的参数名
  - child_list: array或object类型参数的子级参数信息
  - param_info: 预期结果
  - match_rule: 内容校验规则, 校验参数和预期结果的关系

        |值(str类型)|值含义|
        |--|--|
        |0 | 不校验 []              |
        |1 | 值-等于 [value =]      |
        |2 | 值-不等于 [value !=]   |
        |3 | 值-大于 [value >]      |
        |4 | 值-小于 [value <]      |
        |5 | 正则匹配 [Reg =]       |
        |6 | 长度-等于 [length =]   |
        |7 | 长度-不等于 [length !=]|
        |8 | 长度-大于 [length >]   |
        |9 | 长度-小于 [length <]   |
        |10    | 值-包含 [ include =]   |
        |11    | 值-大于等于 [value >=] |
        |12    | 值-小于等于 [value <=] |
        |13    | 值-不包含 [ include !=]|
  - child_list: 子参数校验规则列表

## 关于array类型参数构造的规则:
请先区分这个array类型参数是在构造params请求参数时遇到的或是在构造响应体验证的参数匹配规则时遇到的！
### 当需要构造params请求参数中的array类型参数时
**该规则只适用于params请求参数,请不要在响应体验证的match_rule中使用！！！**
**该规则只适用于params请求参数,请不要在响应体验证的match_rule中使用！！！**
**该规则只适用于params请求参数,请不要在响应体验证的match_rule中使用！！！**
1. 数组元素表示：
- 当参数为 array 类型时，构造参数时需要在 child_list 字段中每个元素的 param_key 以 item[n] 的形式表示下标，其中 n 是数组的索引。
2. 区分对象数组和普通数组：
- 如果 array 类型参数还有子参数，则为对象数组。
- 如果 array 类型参数没有子参数，则为普通数组。
3. 对象数组构造规则：
- 用 item[n] 表示数组中的一个对象元素的 param_key ，这时 item[n] 对应的 param_type 为 object（13），每个对象包含多个子参数。
- 子参数构造放在 item[n] 对象下的 child_list 字段中。
- 多组参数则有多个 item 对象。
- 示例:
(此例子中personInfo是在构造params请求参数时遇到的array类型参数)
{{
    "param_type": "12",
    "param_key": "personInfo",
    "param_info": "",
    "child_list": [
        {{
            "param_type": "13",
            "param_key": "item[0]",
            "param_info": "",
            "is_arr_item": true,
            "child_list": [
                {{
                    "param_type": "0",
                    "param_key": "name",
                    "param_info": "张三",
                    "child_list": []
                }},
                {{
                    "param_type": "14",
                    "param_key": "age",
                    "param_info": "11",
                    "child_list": []
                }}
            ]
        }},
        {{
            "param_type": "13",
            "param_key": "item[1]",
            "param_info": "",
            "is_arr_item": true,
            "child_list": [
                {{
                    "param_type": "0",
                    "param_key": "name",
                    "param_info": "李四",
                    "child_list": []
                }},
                {{
                    "param_type": "14",
                    "param_key": "age",
                    "param_info": "19",
                    "child_list": []
                }}
            ]
        }}
    ]
}}
4. 普通数组构造规则：
- 用 item[n] 表示数组中的一个基本类型元素（如字符串或数字）。
- 参数值直接放到 param_key 为 item[n] 的结构体的 param_info 中。
- 示例
(此例子中nameList是在构造params请求参数时遇到的array类型参数)
{{
    "param_type": "12",
    "param_key": "nameList",
    "param_info": "",
    "child_list": [
        {{
            "param_type": "0",
            "param_key": "item[0]",
            "param_info": "张三",
            "is_arr_item": true
        }},
        {{
            "param_type": "0",
            "param_key": "item[1]",
            "param_info": "李四",
            "is_arr_item": true
        }}
    ]
}}
5. 因数组参数而构造出的 param_key 为 item[n] 的对象需要补充这个字段 "is_arr_item": true。

### 当需要构造响应体验证中array参数匹配规则时
- 与在params中的array参数不同，此处不需要在childlist中用items[n]来表示不同子元素
- 示例
（此例子中data参数为响应体验证中需要构造参数匹配规则时遇到的array类型参数）
{{
    "param_key":"data",
    "param_info":"",
    "match_rule":"0",
    "child_list": [
        {{
            "check_exist": "1",
            "param_key": "data_1",
            "param_info": "",
            "match_rule": "1",
            "child_list": []
        }},
        {{
            "check_exist": "1",
            "param_key": "data_2",
            "param_info": "0",
            "match_rule": "1",
            "child_list": []
        }}
    ]
}}

# 输入
## 测试目标
{test_point}

## API接口调用顺序
{test_steps}

## 待测API接口文档
{tested_api}

## 前置api接口文档
{pre_api_content}

## 后置api接口文档
{post_api_content}

# 输出
"""

# 校验API文档是否包含异常场景测试点详细响应描述
API_TEST_POINT_DOC_INSPECTOR_PROMPT = """
# 角色
API文档分析助手

## 简介
- Author: 千流AI
- Version: 0.1
- Language: 中文
- Description: 分析API文档，检查测试点是否被覆盖，并提供优化建议。

## 背景
- 你是一名API文档分析助手，你的任务是分析用户提供的API文档，检查文档是否包含了用户指定测试点的响应体说明，并给出优化建议。

## 上下文
### API文档信息
{tested_api}

### 测试点描述
{test_point}

## 目标
- 分析API文档中的响应体描述，确定是否覆盖了用户指定的测试点。

## 技能
- 深入理解API文档结构和响应体描述。
- 能够识别文档中是否覆盖了测试点的响应描述。

## 知识库
- HTTP API文档的标准格式。
- 常见的API测试点和异常场景。


## 工作流
1. 读取并分析用户提供的API文档。
2. 确定用户指定的测试点是否被覆盖。

## 输出json格式，示例如下
{{
    "why": "xxx",
    "cover": true,
    "suggestions": "xxx"
}}

# 请提供json回复
"""

# 更新旧用例步骤和测试参数
API_TEST_CASE_MODIFY_PROMPT = """
## 指令
您是一位经验丰富的API接口测试专家。
您的任务是理解用户提供的API接口文档，理解接口定义,分析API接口参数的的说明结合测试点来确定业务场景并构造合理api调用的参数。
## 思考过程
请按照下面的步骤一步一步思考
1. 请修改【旧测试步骤】的内容，生成新的测试步骤。
1.1 由于部分API的文档已经改动，因此【旧测试步骤】的参数可能已经过时，您的任务是基于【旧测试步骤】生成新的步骤，以适应这些API改动
1.2 【api改动文档】中包含了api新增、修改参数的信息，请根据 api_id 字段对应地修改【旧测试步骤】。
1.3 【api删除文档】中包含了api被删除的参数，请您从旧测试步骤中删除掉这些参数。
1.4 保留【旧测试步骤】中checkbox字段的值。若参数应填写但其不在【旧测试步骤】中，对于必填的，标记checkbox为true，非必填的标记checkbox为false。
1.5 不要生成既不在【旧测试步骤】也不在【api改动文档】中的参数。即使它们出现在API文档中，他们也不需要被生成。注意：对于这些参数，不是标记checkbox为false，而是不要生成。
2. 必须填写【api改动文档】中的必填参数，填写规则如下
2.1 如果参数和【前置API接口文档】有关联,则需要调用前置步骤中构造好的参数。
2.2 如果参数不跟其他api有关联，则分析是否是约定俗成的参数，比如：手机号码，默认构造正常场景时需要按照中国的手机号11位数进行构造。
2.3 如果也不是约定俗成的参数，则参考api文档对于该参数的详细定义，借鉴示例，进行构造。
2.4 要能充分根据字段类型来识别特殊情况，例如：参数类型是 string，示例是一个数组[ a, b, c], 这个意思很可能就是指参数从其中一个值选一个。
2.5 请求api调用时必填字段不能缺失。即API文档中【必填】栏为【是】的参数，测试步骤test_steps里面的case_data必须包含所有的必填参数项，且param_info不能为空。
3. 参考【api接口文档】，构造新测试步骤所需要的参数。
4. 您生成的新测试步骤中，API调用顺序以及测试步骤名称必须与【旧测试步骤】保持一致。
5. 请根据【api接口文档】，正确填写新测试步骤中的参数类型。


## 输出json格式示例
{{
    "test_point": "更新需求-正常场景-更新需求的类型为story类型",
    "test_steps_title": [
        {{
            "api_id": 111,
            "step_name": "前置步骤-创建类型为epic的需求"
        }},
        {{
            "api_id": 222,
            "step_name": "主测试步骤-更新需求的类型为story类型"
        }},
        {{
            "api_id": 333,
            "step_name": "后置步骤-删除创建的需求"
        }}
    ],
    "test_steps": [
        {{
            "conn_id": 10000,
            "api_id": 111,
            "api_name": "前置步骤-创建需求类型为epic的需求",
            "api_url": "/api/create",
            "api_protocol": 0,
            "case_data": {{
                "url": "/api/create",
                "step_type": "api_request",
                "api_request_type": "0",
                "headers": [
                    {{
                        "header_name":"",
                        "header_value":""
                    }}
                ],
                "url_param": [
                    {{
                        "param_key":"page",
                        "param_info":"1"
                    }}
                ],
                "restful_param": [
                    {{
                        "param_key":"his_id",
                        "param_info":"1"
                    }}
                ],
                "params": [
                    {{
                        "param_type": "0",
                        "param_key": "version",
                        "param_info": "1.0.0",
                        "child_list": []
                    }},
                    {{
                        "param_type": "13",
                        "param_key": "history",
                        "param_info": "",
                        "child_list": [
                            {{
                                "param_type": "14",
                                "param_key": "history_id",
                                "param_info": "1",
                                "child_list": []
                            }}
                        ]
                    }},
                    {{
                        "param_type": "12",
                        "param_key": "historyList",
                        "param_info": "",
                        "child_list": [
                            {{
                                "param_type": "13",
                                "param_key": "item[0]",
                                "param_info": "",
                                "is_arr_item": true,
                                "child_list": [
                                    {{
                                        "param_type": "14",
                                        "param_key": "history_id",
                                        "param_info": "1",
                                        "child_list": []
                                    }},
                                    {{
                                        "param_type": "0",
                                        "param_key": "history_name",
                                        "param_info": "change_name2024",
                                        "child_list": []
                                    }},
                                    {{
                                        "param_type": "12",
                                        "param_key": "hobby",
                                        "param_info": "",
                                        "child_list": [
                                            {{
                                                "param_type": "0",
                                                "param_key": "item[0]",
                                                "param_info": "football",
                                                "is_arr_item": true,
                                                "child_list": []
                                            }},
                                            {{
                                                "param_type": "0",
                                                "param_key": "item[1]",
                                                "param_info": "basketball",
                                                "is_arr_item": true,
                                                "child_list": []
                                            }},
                                        ]
                                    }}
                                ]
                            }}
                        ]
                    }}
                ],
            }}
            "status_code_verification": {{
                "check_status":true,
                "status_code":200
            }},
            "response_result_verification": {{
                "check_status":true,
                "param_match":"json",
                "json_result_verification": {{
                    "result_type":"object",
                    "match_rule":"allElement"
                }},
                "match_rule": [
                    {{
                        "param_key":"",
                        "param_info":"",
                        "match_rule":"0",
                        "child_list": [
                            {{
                                "param_key":"id",
                                "param_info":"",
                                "match_rule":"0",
                                "child_list": []
                            }}
                        ]
                    }}
                ]
            }}
        }}
    ]
}}

** 字段解释 **
1. api_name: 步骤名称, 前缀可以是【前置步骤】【主测试步骤】【后置步骤】三个中的一个。
2. conn_id: 步骤 id，请按【旧测试步骤】中的conn_id对应地填写该字段。
3. api_url: 步骤请求的url
4. step_type: 步骤类型，当前只有`api_request`,表示该步骤是一个api请求
5. url_param: url_param参数
6. restful_param: restful_param参数
7. headers: 请求头
8. params: params请求参数
param_info表示实际测试的参数值
param_type表示参数的类型

9. 允许的 param_type 取值
|值(str类型)|值含义|
|--|--|
|0 |string|
|0 |char|
|0 |date|
|0 |datetime|
|0 |byte|
|8 |boolean|
|12|array|
|13|json|
|13|object|
|14|int|
|14|float|
|14|double|
|14|short|
|14|long|
|14|number|
|15|null|

10. request_type: 请求体类型, 不同类型表示params请求体所代表的不同类型
|值(str类型)|值含义|
|--|--|
|0 |form-data |
|1 |raw|
|2 |json|
|3 |xml|

11. api_protocol: 接口协议
|值(int类型)|值含义|
|:--|:--|
|0|HTTP|
|1|HTTPS|

12. api_request_type: 请求方式
|值(str类型)|值含义|
|:--|:--|
|0|POST|
|1|GET|
|2|PUT|
|3|DELETE|
|4|HEAD|
|5|OPTIONS|
|6|PATCH|

13. status_code_verification: 状态码验证
- check_status: 是否开启该校验
- status_code: 期望的状态码

14. response_result_verification: 响应体验证
- check_status: 是否开启该校验
- param_match: 校验方式，当前只用 `json` 验证
- json_result_verification: json 结果校验
  - resultType: json的类型, 取值 `object` 或者 `array`
  - match_rule: 固定值allElement
- match_rule: 具体参数的匹配规则
  - param_key: 参数名,如果参数是 aaa>>bbb 格式，需要把 bbb 作为子参数放到 child_list 字段中中
  - param_info: 预期结果
  - match_rule: 内容校验规则, 校验参数和预期结果的关系
|值(str类型)|值含义|
|--|--|
|0 | 不校验 []              |
|1 | 值-等于 [value =]      |
|2 | 值-不等于 [value !=]   |
|3 | 值-大于 [value >]      |
|4 | 值-小于 [value <]      |
|5 | 正则匹配 [Reg =]       |
|6 | 长度-等于 [length =]   |
|7 | 长度-不等于 [length !=]|
|8 | 长度-大于 [length >]   |
|9 | 长度-小于 [length <]   |
|10    | 值-包含 [ include =]   |
|11    | 值-大于等于 [value >=] |
|12    | 值-小于等于 [value <=] |
|13    | 值-不包含 [ include !=]|
  - child_list: 子参数校验规则列表
  
## 输入
 
### 测试点
{test_point}
 
### API调用顺序
{test_steps}

### 旧测试步骤
{old_test_steps} 
  
### api接口文档
{tested_api}
 
### api改动文档
{api_diff_content}
 
### api参数删除文档
{api_del_content}
  
## 输出
"""
