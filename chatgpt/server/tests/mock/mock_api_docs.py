# 测试点
test_points = [
    "查询应用分类授权-正常场景-验证接口在提供正确的name、fieldMode、sortBy、entityType、pageIndex和pageSize时，能够成功返回应用分类授权信息。"
]

# 被测api文档
tested_api = """
#### 查询应用分类授权-基于名称
##### 接口信息

**API Path**
/api/v3/resourceGroupAssign/queryByName

**请求协议**
HTTP

**请求方法**
POST

**请求参数**Json
Object

| 参数名 | 说明 | 必填 | 类型 | 值可能性 |  限制 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|name|应用分类名称 ，基于名称请求时为必传字段|是|[string]| | |SSL内部应用|
|fieldMode|返回字段模式，取值范围：["all", "lite"]，<br />分别表示”返回所有字段“，”返回精简后的字段“|是|[string]| | |all|
|sortBy|排序方式，默认为："default"|是|[string]| | |default|
|entityType|实体类型，取值范围：["group", "band", "user"]，<br />分别表示组织架构，角色，用户，传空数组或不传表示查询所有实体类型|是|[object]| | |["user", "group", "band"]|
|pageIndex|页码编号|是|[number]| | | |
|pageSize|每页显示的数量上限|是|[number]| | | |

**响应内容**：

**返回结果**
>成功 (200)
Json
Object

| 参数名  | 说明 | 必填 | 类型 | 值可能性 | 限制 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|code|错误码|是|[string]| ||OK|
|data|响应数据|是|[object]| || |
|data>>count|查询结果总数|是|[number]| ||4|
|data>>pageCount|总页数|是|[number]| ||1|
|data>>pageSize|分页大小|是|[number]| ||20|
|data>>pageIndex|当前页码|是|[number]| ||1|
|data>>data|应用授权详情|是|[array]| ||[{"id":"5141600b-f276-4919-93a0-162be255f2ce","name":"/","displayName":"","entityType":"group","userDirectoryId":"6c97c0d0-db08-11ee-9cc7-6f7f82e11f93","path":"","bandType":0,"isDeleted":0,"serverName":"custom_dir","dataType":"externalUserGroup","effectiveTime":"0","expireTime":"0","description":"","authorisedStatus":1},{"id":"0fccfc00-dc5f-11ee-931f-a9e941254445","name":"本地角色","displayName":"","entityType":"band","userDirectoryId":"1","path":"","bandType":0,"isDeleted":0,"serverName":"本地用户目录","dataType":"localUserBand","effectiveTime":"0","expireTime":"0","description":"","authorisedStatus":1},{"id":"3e12e620-daf6-11ee-99c1-ad5ce62be579","name":"hzm","displayName":"hzm","entityType":"user","userDirectoryId":"1","path":"/","bandType":0,"isDeleted":0,"serverName":"本地用户目录","dataType":"localUser","effectiveTime":"1709222400000","expireTime":"1709395199999","description":"","authorisedStatus":3},{"id":"12b3eb60-dbc7-11ee-8fa8-035bfe34954c","name":"张三","displayName":"张三","entityType":"user","userDirectoryId":"1","path":"/","bandType":0,"isDeleted":0,"serverName":"本地用户目录","dataType":"localUser","effectiveTime":"1709740800000","expireTime":"1709805540999","description":"","authorisedStatus":2}]|
|data>>data>>id|授权对象id|是|[string]| ||5141600b-f276-4919-93a0-162be255f2ce|
|data>>data>>name|授权对象名称|是|[string]| ||/|
|data>>data>>displayName|授权对象显示名称|是|[string]| || |
|data>>data>>entityType|group: 组织架构<br />band：角色<br />user: 用户|是|[string]| ||group|
|data>>data>>userDirectoryId|用户目录id|是|[string]| ||6c97c0d0-db08-11ee-9cc7-6f7f82e11f93|
|data>>data>>isDeleted|外部已删除， 0 未删除 ，1 已删除|是|[number]| ||0|
|data>>data>>serverName|所属用户目录名称|是|[string]| ||custom_dir|
|data>>data>>dataType|数据类型，例如：<br />externalUserGroup：外部组织架构<br />localUserBand：本地角色<br />localUser：本地用户|是|[string]| ||externalUserGroup|
|data>>data>>effectiveTime|生效时间戳，例 1709222400000|是|[string]| ||0|
|data>>data>>expireTime|过期时间戳，例 1709222400000|是|[string]| ||0|
|data>>data>>description|描述信息|是|[string]| || |
|data>>data>>authorisedStatus|授权状态<br />1： 永不过期；<br />2： 即将过期；<br />3：已过期|是|[number]| ||1|
|msg|描述信息|是|[string]| ||请求成功|
|traceId|链路请求的标识|是|[string]| ||00bf58d2f1b31b0c|

"""

# 前置api文档
pre_api_content = """
#### 新增应用分类
##### 接口信息

**API Path**
/api/v1/resource/createResourceGroup

**请求协议**
HTTPS

**请求方法**
POST

**请求头部**：
| 头部标签 | 必填 | 说明 | 类型 | 值可能性 | 限制 | 头部内容 | 示例 | 
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|Content-Type|是||[string]|||application/json|application/json|

**请求参数**Json
Object

| 参数名 | 说明 | 必填 | 类型 | 值可能性 |  限制 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|name|应用分类名字|是|[string]|:| | |
|description|应用分类的描述|否|[string]|:| | |

**响应内容**：

**返回结果**
>成功 (200)
Json
Object

| 参数名  | 说明 | 必填 | 类型 | 值可能性 | 限制 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|code|错误码，非0表示错误，具体含义请参考错误码定义|是|[number]| || |
|data|返回内容|是|[object]| || |
|data>>id|应用分类ID|是|[string]| || |
|msg|描述信息|是|[string]| || |


**详细说明**：
接口描述：
请求示例
{
    &quot;name&quot;: &quot;第一分类&quot;,
    &quot;description&quot;: &quot;这是应用分类&quot;
}

错误信息



错误提示
错误码




参数检查失败
10000001


方法入参不能为空
10000001


应用分类名（%s）已存在
77200005


创建失败
10000000


#### 新增用户
##### 接口信息

**API Path**
/api/v3/user/create

**请求协议**
HTTPS

**请求方法**
POST

**请求头部**：
| 头部标签 | 必填 | 说明 | 类型 | 值可能性 | 限制 | 头部内容 | 示例 | 
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|Content-Type|是||[string]|||application/json|application/json|

**请求参数**Json
Object

| 参数名 | 说明 | 必填 | 类型 | 值可能性 |  限制 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|directoryDomain| |是|[string]| | | |
|name|用户名|是|[string]| | | |
|group|所属组|是|[object]| | | |
|group>>op| |是|[string]| | |set|
|group>>key| |是|[string]| | |id、externalId、path|
|group>>data| |是|[string]| | | |
|password|密码|否|[string]| | | |
|externalId|用户外部ID|否|[string]| | | |
|displayName|显示名|否|[string]| | | |
|inheritGroup|继承所属组的应用授权：0不继承，1继承|否|[number]|1:,0:| | |
|status|启用状态：0禁用，1启用|否|[number]|0:,1:| | |
|description|描述|否|[string]| | | |
|phone|手机号码|否|[string]| | | |
|email|电子邮件|否|[string]| | | |
|expiredTime|过期时间，13位长度的Unix时间戳，'0'表示永不过期|否|[string]|0:| | |
|pwdModel|密码加密算法类型：'clear'明文，'rsa'非对称加密|否|[string]|clear:,rsa:| | |
|DataSource| |否|[object]| | | |
|DataSource>>status| |否|[string]| | |local|
|DataSource>>displayName| |否|[string]| | |local|
|DataSource>>email| |否|[string]| | |local|
|DataSource>>description| |否|[string]| | |local|
|DataSource>>phone| |否|[string]| | |local|
|DataSource>>expiredTime| |否|[string]| | |local|

**响应内容**：

**返回结果**
>成功 (200)
Json
Object

| 参数名  | 说明 | 必填 | 类型 | 值可能性 | 限制 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|code|返回码，0 返回成功|是|[string]|OK;|| |
|data|用户ID|是|[array]| || |
|msg|返回提示信息，与返回码对应|是|[string]| || |


**详细说明**：
接口描述：参数groupID所属组ID，必须参数，根组ID为'root'。如果需要将用户关联到其他组织架构，可先用组织架构的查询接口(queryGroupByPath)获取ID。参数password密码，为了在数据传输过程中（数据从浏览器/客户端到服务端的过程）保障密码数据的安全，强烈建议使用RSA算法对密码字段进行加密后的密码（将pwdModel参数设置为'rsa'）。加密方式参考详见demo中public模块的encrypt函数，以及handle_rsa.js。如果您不想对密码字段进行加密（强烈不建议如此），可以在请求中不传pwdModel参数或者将pwdModel参数设置为'clear'。认证策略ID，authComposeId获取方式，用“开发者工具”过滤请求 authComposeId/queryAll，在控制台“业务管理”-&gt;“认证管理”-&gt;“认证策略”页面中打开您新增用户所属的用户目录，找到所属用户目录的认证策略查询接口，查看响应体数据获取对应的认证策略ID用户策略ID，userPolicyId获取方式，用“开发者工具”过滤请求 userPolicy/queryUserPolicy，进入控制台“业务管理”-&gt;“策略管理”-&gt;“用户策略”页面，查看响应体数据获取所需策略的ID请求示例{
    "status": 1,
    "name": "testUser",
    "description": "",
    "password": "22033431e0eb565d3fdbfa9b4f124798cbbd48bb9ab34c4bb9d97bce7d12a8c218b0ad677e3d6de5162fad14245e942755b3db3ae822a9e49fa633498382a720a41b11a7fafe13bc09225444983f3974ede2824f6b195186ef32d8184fbf2af67c3f7a3dbcabc89c3d560d6f4044a8f15d3acec043d6c7fccba3681f44da239451a2eba0701121839cf6c771b3e67b5c9a8174bc9b117aba74aea0c3b8e736c1976751153a38826f3af80169586530fa3ee2f414aed46ec0c6f8ac90deed08203fe22e09123f5fcfce9eeb58ced1f92715e7b003e19142eaa0f97cded5f2a97cb3c0aee6585a62db60977d9af60f7d7d2e0d021fca704fc0b4076c39297c3ea9",
    "email": "",
    "phone": "",
    "groupId": "root",
    "expiredTime": "0",
    "inheritGroup": 1,
    "roleIdList": [
        "23c916f0-5583-11eb-880a-913383f106f2"
    ]
}错误信息错误提示错误码用户或组织架构最多关联1000个应用10000000密码不能属于常见弱密码10000001暂时不支持批量功能10000001外部ID重复，请重新输入10000000密码不能包含用户名10000000用户名（%s）已存在77200005组织架构不存在77200004认证策略不存在77200004用户策略不存在77200004角色不存在或已被删除77200004超级管理员角色不允许被分配10000001SYSTEM管理员为系统内置管理员，请使用其他名字10000001管理员角色不存在77200005操作失败10000000


#### 新增组织架构
##### 接口信息

**API Path**
/api/v3/group/create

**请求协议**
HTTPS

**请求方法**
POST 

**请求头部**：
| 头部标签 | 必填 | 说明 | 类型 | 值可能性 | 限制 | 头部内容 | 示例 | 
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|Content-Type|是||[string]|||application/json|application/json|

**请求参数**Json
Object

| 参数名 | 说明 | 必填 | 类型 | 值可能性 |  限制 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|directoryDomain|所属用户目录域|是|[string]| | | |
|name|组织架构名字|是|[string]| | | |
|group| |是|[object]| | | |
|group>>op| |是|[string]| | | |
|group>>key| |是|[string]| | | |
|group>>data| |是|[string]| | | |
|description|描述|否|[string]| | | |
|externalId|外部ID|否|[string]| | | |

**响应内容**：

**返回结果**
>成功 (200)
Json
Object

| 参数名  | 说明 | 必填 | 类型 | 值可能性 | 限制 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|code|错误码，非0表示错误，具体含义请参考错误码定义|是|[number]| || |
|data|本地组织架构ID|是|[object]| || |
|data>>id| |是|[array]| || |
|msg|描述信息|是|[string]| || |

**详细说明**：
接口描述：部分参数，如关联对象ID，需要通过在控制台手动获取，以Chrome浏览器为例，获取方式为F12打开“开发者工具”，在Network中找到对应对象的查询接口手动获取该对象的ID用户目录ID，userDirectoryId获取方式，用“开发者工具”过滤请求 userDirectory/queryAll，打开控制台“业务管理”-&gt;“用户管理”页面，查看响应体数据获取对应用户目录的ID，也可以通过用户目录查询接口获取ID认证策略ID，authComposeId获取方式，用“开发者工具”过滤请求 authComposeId/queryAll，在控制台“业务管理”-&gt;“认证管理”-&gt;“认证策略”页面中打开您新增用户所属的用户目录，找到所属用户目录的认证策略查询接口，查看响应体数据获取对应的认证策略ID用户策略ID，userPolicyId获取方式，用“开发者工具”过滤请求 userPolicy/queryUserPolicy，进入控制台“业务管理”-&gt;“策略管理”-&gt;“用户策略”页面，查看响应体数据获取所需策略的ID请求示例{
	"userDirectoryId": "d36ccb20-596a-11eb-a393-bbd9cb089321",
	"name": "外部分组1",
	"description": "1111",
	"path": "/",
	"authComposeId": "d36ccb20-596a-11eb-a393-bbd9cb0893d1",
	"roleIdEditWay": "append",
	"roleIdList": [ "7759f620-5583-11eb-880a-913383f106f2", "6559f620-5583-11eb-880a-913383f106f2"],
	"userPolicyId": "default"
}错误信息错误提示错误码参数检查失败10000001组织架构名称错误，不能存在/77200005所属组织架构路径层级不能超过32级10000001用户目录不存在77200004用户组织架构名（%s）已存在77200005用户最多关联1000个应用77200007保存失败，关联的应用不存在或已被删除77200004保存失败，关联的应用分类不存在或已被删除77200004操作失败10000000


#### 新增角色
##### 接口信息

**API Path**
/api/v3/role/create

**请求协议**
HTTPS

**请求方法**
POST

**请求头部**：
| 头部标签 | 必填 | 说明 | 类型 | 值可能性 | 限制 | 头部内容 | 示例 | 
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|Content-Type|是||[string]|||application/json|application/json|

**请求参数**Json
Object

| 参数名 | 说明 | 必填 | 类型 | 值可能性 |  限制 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|directoryDomain| |是|[string]| | | |
|name|用户名|是|[string]| | | |
|externalId|用户外部ID|否|[string]| | | |
|description|描述|否|[string]| | | |

**响应内容**：

**返回结果**
>成功 (200)
Json
Object

| 参数名  | 说明 | 必填 | 类型 | 值可能性 | 限制 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|code|返回码，0 返回成功|是|[string]| || |
|data|用户ID|是|[array]| || |
|msg|返回提示信息，与返回码对应|是|[string]| || |


**详细说明**：
接口描述：参数groupID所属组ID，必须参数，根组ID为'root'。如果需要将用户关联到其他组织架构，可先用组织架构的查询接口(queryGroupByPath)获取ID。参数password密码，为了在数据传输过程中（数据从浏览器/客户端到服务端的过程）保障密码数据的安全，强烈建议使用RSA算法对密码字段进行加密后的密码（将pwdModel参数设置为'rsa'）。加密方式参考详见demo中public模块的encrypt函数，以及handle_rsa.js。如果您不想对密码字段进行加密（强烈不建议如此），可以在请求中不传pwdModel参数或者将pwdModel参数设置为'clear'。认证策略ID，authComposeId获取方式，用“开发者工具”过滤请求 authComposeId/queryAll，在控制台“业务管理”-&gt;“认证管理”-&gt;“认证策略”页面中打开您新增用户所属的用户目录，找到所属用户目录的认证策略查询接口，查看响应体数据获取对应的认证策略ID用户策略ID，userPolicyId获取方式，用“开发者工具”过滤请求 userPolicy/queryUserPolicy，进入控制台“业务管理”-&gt;“策略管理”-&gt;“用户策略”页面，查看响应体数据获取所需策略的ID请求示例{
    "status": 1,
    "name": "testUser",
    "description": "",
    "password": "22033431e0eb565d3fdbfa9b4f124798cbbd48bb9ab34c4bb9d97bce7d12a8c218b0ad677e3d6de5162fad14245e942755b3db3ae822a9e49fa633498382a720a41b11a7fafe13bc09225444983f3974ede2824f6b195186ef32d8184fbf2af67c3f7a3dbcabc89c3d560d6f4044a8f15d3acec043d6c7fccba3681f44da239451a2eba0701121839cf6c771b3e67b5c9a8174bc9b117aba74aea0c3b8e736c1976751153a38826f3af80169586530fa3ee2f414aed46ec0c6f8ac90deed08203fe22e09123f5fcfce9eeb58ced1f92715e7b003e19142eaa0f97cded5f2a97cb3c0aee6585a62db60977d9af60f7d7d2e0d021fca704fc0b4076c39297c3ea9",
    "email": "",
    "phone": "",
    "groupId": "root",
    "expiredTime": "0",
    "inheritGroup": 1,
    "roleIdList": [
        "23c916f0-5583-11eb-880a-913383f106f2"
    ]
}错误信息错误提示错误码用户或组织架构最多关联1000个应用10000000密码不能属于常见弱密码10000001暂时不支持批量功能10000001外部ID重复，请重新输入10000000密码不能包含用户名10000000用户名（%s）已存在77200005组织架构不存在77200004认证策略不存在77200004用户策略不存在77200004角色不存在或已被删除77200004超级管理员角色不允许被分配10000001SYSTEM管理员为系统内置管理员，请使用其他名字10000001管理员角色不存在77200005操作失败10000000

#### 应用分类授权-基于id
##### 接口信息

**API Path**
/api/v3/resourceGroup/assignById

**请求协议**
HTTP

**请求方法**
POST

**请求参数**Json
Object

| 参数名 | 说明 | 必填 | 类型 | 值可能性 |  限制 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|id|基于应用分类 id 请求时为必传字段|是|[string]| | |4cffbdb0-daf7-11ee-99c1-ad5ce62be579|
|op|取值范围：["reset", "append", "delete"]，<br />分别表示重置，追加，删除|是|[string]| | |reset|
|data|授权对象|是|[object]| | | |
|data>>user|用户|是|[array]| | |[{"directoryDomain":"local","id":"3e12e620-daf6-11ee-99c1-ad5ce62be579","effectiveTime":"1709646812000","expireTime":"1709913599999"}]|
|data>>user>>directoryDomain|用户目录唯一标识，为用户授权应用分类权限时为必传字段|是|[string]| | |local|
|data>>user>>id|用户 id ，基于 id 为用户授权应用分类权限时为必传字段|是|[string]| | |3e12e620-daf6-11ee-99c1-ad5ce62be579|
|data>>user>>name|用户 name ，基于 name 为用户授权应用分类权限时为必传字段|是|[string]| | | |
|data>>user>>externalId|用户外部 id ，基于外部 id 为用户授权应用分类权限时为必传字段|是|[string]| | | |
|data>>user>>effectiveTime|生效时间|是|[string]| | |1709646812000|
|data>>user>>expireTime|过期时间|是|[string]| | |1709913599999|
|data>>userGroup|组织架构|是|[array]| | |[{"directoryDomain":"custom83665","id":"5141600b-f276-4919-93a0-162be255f2ce","effectiveTime":"1709646812000","expireTime":"1709913599999"}]|
|data>>userGroup>>directoryDomain|用户目录唯一标识，为组织架构授权应用分类权限时为必传字段|是|[string]| | |custom83665|
|data>>userGroup>>id|组织架构 id ，基于 id 为组织架构授权应用分类权限时为必传字段|是|[string]| | |5141600b-f276-4919-93a0-162be255f2ce|
|data>>userGroup>>fullPath|组织架构全路径 ，基于 name 为组织架构授权应用分类权限时为必传字段|是|[string]| | | |
|data>>userGroup>>externalId|组织架构外部 id ，基于外部 id 为组织架构授权应用分类权限时为必传字段|是|[string]| | | |
|data>>userGroup>>effectiveTime|生效时间|是|[string]| | |1709646812000|
|data>>userGroup>>expireTime|过期时间|是|[string]| | |1709913599999|
|data>>userBand|角色|是|[array]| | |[{"directoryDomain":"custom83665","id":"5141600b-f276-4919-93a0-162be255f2ce","effectiveTime":"1709646812000","expireTime":"1709913599999"}]|
|data>>userBand>>directoryDomain|角色目录唯一标识，为角色授权应用分类权限时为必传字段|是|[string]| | |custom83665|
|data>>userBand>>id|角色 id ，基于 id 为角色授权应用分类权限时为必传字段|是|[string]| | |5141600b-f276-4919-93a0-162be255f2ce|
|data>>userBand>>name|角色 name ，基于 name 为角色授权应用分类权限时为必传字段|是|[string]| | | |
|data>>userBand>>externalId|角色外部 id ，基于外部 id 为角色授权应用分类权限时为必传字段|是|[string]| | | |
|data>>userBand>>effectiveTime|生效时间|是|[string]| | |1709646812000|
|data>>userBand>>expireTime|过期时间|是|[string]| | |1709913599999|

**响应内容**：

**返回结果**
>成功 (200)
Json
Object

| 参数名  | 说明 | 必填 | 类型 | 值可能性 | 限制 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|code|"OK" 表示成功，其他表示出错。具体含义请参考错误码定义|是|[string]| ||OK|
|data|响应数据|是|[object]| || |
|msg|描述信息|是|[string]| ||请求成功|
|traceId|链路请求的标识|是|[string]| ||00b27e69598c3483|
"""

# 后置api文档
post_api_content = """
#### ID删除外部组织架构
##### 接口信息

**API Path**
/api/v3/group/bulkDeleteByIdList

**请求协议**
HTTPS

**请求方法**
POST

**请求头部**：
| 头部标签 | 必填 | 说明 | 类型 | 值可能性 | 限制 | 头部内容 | 示例 | 
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|Content-Type|是||[string]|||application/json|application/json|

**请求参数**Json
Object

| 参数名 | 说明 | 必填 | 类型 | 值可能性 |  限制 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|idList|外部组织架构ID列表|是|[array]| | |idList、pathList、externalIdList三选一|
|directoryDomain|外部用户目录域|是|[string]| | | |
|recursive|递归删除所有下属组织架构：0不递归删除，1递归删除|否|[number]|0:| | |

**响应内容**：

**返回结果**
>成功 (200)
Json
Object

| 参数名  | 说明 | 必填 | 类型 | 值可能性 | 限制 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|code|0:成功，|是|[number]| || |
|data|删除的组织架构总数|是|[number]| || |
|msg|返回描述|是|[string]| || |

**详细说明**：
接口描述：对于删除接口，如果删除已经不存在的数据，不会报错，这会认为是成功的操作，返回状态码200且错误码为0批量删除只允许删除属于同一个用户目录下的外部用户组织架构部分参数，如关联对象ID，需要通过在控制台手动获取，以Chrome浏览器为例，获取方式为F12打开“开发者工具”，在Network中找到对应对象的查询接口手动获取该对象的ID用户目录ID，userDirectoryId获取方式，用“开发者工具”过滤请求 userDirectory/queryAll，打开控制台“业务管理”-&gt;“用户管理”页面，查看响应体数据获取对应用户目录的ID，也可以通过用户目录查询接口获取ID请求示例{
	"pathList": ["/a"],
	"userDirectoryName": "LDAP用户目录"
}错误信息错误提示错误码参数检查失败10000001操作失败10000000

#### Id批量删除本地用户
##### 接口信息

**API Path**
/api/v3/user/bulkDeleteByIdList

**请求协议**
HTTPS

**请求方法**
POST

**请求头部**：
| 头部标签 | 必填 | 说明 | 类型 | 值可能性 | 限制 | 头部内容 | 示例 | 
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|Content-Type|是||[string]|||application/json|application/json|

**请求参数**Json
Object

| 参数名 | 说明 | 必填 | 类型 | 值可能性 |  限制 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|idList| |是|[array]| | | |
|directoryDomain| |是|[string]| | | |

**响应内容**：

**返回结果**
>成功 (200)
Json
Object

| 参数名  | 说明 | 必填 | 类型 | 值可能性 | 限制 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|code|返回码，0 返回成功|是|[string]| || |
|data|报文数据主体|是|[object]| || |
|msg|返回提示信息，与返回码对应|是|[string]| || |


**详细说明**：
接口描述：对于删除接口，如果删除已经不存在的数据，不会报错，这会认为是成功的操作，返回状态码200且错误码为0请求示例{
	"idList": ["b0301390-5ac5-11eb-a393-bbd9cb0893d1"]
}错误信息错误提示错误码参数检查失败10000001超级管理员，不允许删除10000001操作失败10000000

#### Id批量删除角色
##### 接口信息

**API Path**
/api/v3/role/bulkDeleteByIdList

**请求协议**
HTTPS

**请求方法**
POST

**请求头部**：
| 头部标签 | 必填 | 说明 | 类型 | 值可能性 | 限制 | 头部内容 | 示例 | 
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|Content-Type|是||[string]|||application/json|application/json|

**请求参数**Json
Object

| 参数名 | 说明 | 必填 | 类型 | 值可能性 |  限制 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|idList| |是|[array]| | | |
|directoryDomain| |是|[string]| | | |

**响应内容**：

**返回结果**
>成功 (200)
Json
Object

| 参数名  | 说明 | 必填 | 类型 | 值可能性 | 限制 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|code|返回码，0 返回成功|是|[string]| || |
|data|报文数据主体|是|[object]| || |
|msg|返回提示信息，与返回码对应|是|[string]| || |

**详细说明**：
接口描述：对于删除接口，如果删除已经不存在的数据，不会报错，这会认为是成功的操作，返回状态码200且错误码为0请求示例{
	"idList": ["b0301390-5ac5-11eb-a393-bbd9cb0893d1"]
}错误信息错误提示错误码参数检查失败10000001超级管理员，不允许删除10000001操作失败10000000


#### 批量删除应用分类
##### 接口信息

**API Path**
/api/v1/resource/deleteResourceGroup

**请求协议**
HTTPS

**请求方法**
POST

**请求头部**：
| 头部标签 | 必填 | 说明 | 类型 | 值可能性 | 限制 | 头部内容 | 示例 | 
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|Content-Type|是||[string]|||application/json|application/json|

**请求参数**Json
Object

| 参数名 | 说明 | 必填 | 类型 | 值可能性 |  限制 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|idList|被删的id列表|是|[array]|:| | |

**响应内容**：

**返回结果**
>成功 (200)
Json
Object

| 参数名  | 说明 | 必填 | 类型 | 值可能性 | 限制 | 示例 |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|code|0:成功，|是|[number]| || |
|data| |是|[object]| || |
|data>>length|删除的应用数|是|[string]| || |
|data>>name|异常态的应用名|否|[array]| || |
|msg| |是|[string]| || |

**详细说明**：
接口描述：

对于删除接口，如果删除已经不存在的数据，不会报错，这会认为是成功的操作，返回状态码200且错误码为0注意：只允许删除没有关联任何应用的应用组。如果应用组关联了应用，必须先将关联的应用删除，才允许删除应用组。


请求示例
{
    &quot;idList&quot;: [&quot;a1240650-5ae7-11eb-a393-bbd9cb0893d1&quot;]
}

错误信息



错误提示
错误码




参数检查失败
10000001


默认应用分类，不允许删除
77200008


删除失败，请先将当前应用分类下的WEB全网应用移动至其它分类
77200008


删除失败
10000000


存在已选应用处于 采集中/试运行 状态, 请取消选择
77200008
"""
