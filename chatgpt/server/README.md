## 千流AI项目

### 一、功能列表


#### v2/completion接口
- 使用场景：ide / web生成代码
- action参数说明

| action             | 对应功能                                       | 备注                                     |
| :----------------- | :--------------------------------------------- | :--------------------------------------- |
| findProblems       | 千流AI：查找bug（旧）                          | 新版本已废弃                             |
| addTests           | 千流AI：生成测试（旧）测试生成（新）           |                                          |
| optimize           | 千流AI：优化代码（旧）                         | 新版本已废弃                             |
| explain            | 千流AI：解释代码（旧）智能问答->解释代码（新） |                                          |
| chat               | 智能问答                                       |                                          |
| generateCodeByForm | 生成代码                                       | 根据功能描述、技术栈等信息生成代码       |
| generateCodeByAsk  | 生成代码（web）                                | 代码生成页面生成代码后，继续追问优化代码 |
| review             | 代码review                                     | 包含主动reivew、自动review                                         |
| scribe             | 划词对话功能                                   |                                          |
| addDebugCode       | 提升调试性                                     |                                          |
| addStrongerCode    | 提升健壮性                                     |                                          |
| addComment         | 添加注释                                       |                                          |
| pickCommonFunc     | 函数提取                                       |                                          |
| simplifyCode       | 精简代码                                       |                                          |

对应docs文档地址：https://docs.atrust.sangfor.com/pages/viewpage.action?pageId=303557143

### 二 、环境依赖（语言版本，工具版本，额外依赖）
```
python==3.8.5
```

### 三 、项目说明（关键的目录结构，核心方案）

### 四 、环境部署

#### 开发部署
- 环境教程：https://docs.atrust.sangfor.com/pages/viewpage.action?pageId=304857376

测试部署

生产部署

五、使用方式

六、常见问题
