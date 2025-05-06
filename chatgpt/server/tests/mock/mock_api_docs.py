# Test points
test_points = [
    "Query Application Category Authorization-Normal Scenario-Verify that the interface successfully returns application category authorization information when providing correct name, fieldMode, sortBy, entityType, pageIndex, and pageSize."
]

# Tested API documentation
tested_api = """
#### Query Application Category Authorization-Based on Name
##### Interface Information

**API Path**
/api/v3/resourceGroupAssign/queryByName

**Request Protocol**
HTTP

**Request Method**
POST

**Request Parameters**Json
Object

| Parameter Name | Description | Required | Type | Possible Values | Constraints | Example |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|name|Application category name, required field when requesting based on name|Yes|[string]| | |SSL Internal Application|
|fieldMode|Return field mode, possible values: ["all", "lite"], <br />representing "return all fields", "return simplified fields"|Yes|[string]| | |all|
|sortBy|Sort method, default is: "default"|Yes|[string]| | |default|
|entityType|Entity type, possible values: ["group", "band", "user"], <br />representing organization structure, role, user. Empty array or not passing means query all entity types|Yes|[object]| | |["user", "group", "band"]|
|pageIndex|Page number|Yes|[number]| | | |
|pageSize|Maximum number of items per page|Yes|[number]| | | |

**Response Content**:

**Return Result**
>Success (200)
Json
Object

| Parameter Name | Description | Required | Type | Possible Values | Constraints | Example |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|code|Error code|Yes|[string]| ||OK|
|data|Response data|Yes|[object]| || |
|data>>count|Total number of query results|Yes|[number]| ||4|
|data>>pageCount|Total number of pages|Yes|[number]| ||1|
|data>>pageSize|Page size|Yes|[number]| ||20|
|data>>pageIndex|Current page number|Yes|[number]| ||1|
|data>>data|Application authorization details|Yes|[array]| ||[{"id":"5141600b-f276-4919-93a0-162be255f2ce","name":"/","displayName":"","entityType":"group","userDirectoryId":"6c97c0d0-db08-11ee-9cc7-6f7f82e11f93","path":"","bandType":0,"isDeleted":0,"serverName":"custom_dir","dataType":"externalUserGroup","effectiveTime":"0","expireTime":"0","description":"","authorisedStatus":1},{"id":"0fccfc00-dc5f-11ee-931f-a9e941254445","name":"Local Role","displayName":"","entityType":"band","userDirectoryId":"1","path":"","bandType":0,"isDeleted":0,"serverName":"Local User Directory","dataType":"localUserBand","effectiveTime":"0","expireTime":"0","description":"","authorisedStatus":1},{"id":"3e12e620-daf6-11ee-99c1-ad5ce62be579","name":"hzm","displayName":"hzm","entityType":"user","userDirectoryId":"1","path":"/","bandType":0,"isDeleted":0,"serverName":"Local User Directory","dataType":"localUser","effectiveTime":"1709222400000","expireTime":"1709395199999","description":"","authorisedStatus":3},{"id":"12b3eb60-dbc7-11ee-8fa8-035bfe34954c","name":"Zhang San","displayName":"Zhang San","entityType":"user","userDirectoryId":"1","path":"/","bandType":0,"isDeleted":0,"serverName":"Local User Directory","dataType":"localUser","effectiveTime":"1709740800000","expireTime":"1709805540999","description":"","authorisedStatus":2}]|
|data>>data>>id|Authorization object ID|Yes|[string]| ||5141600b-f276-4919-93a0-162be255f2ce|
|data>>data>>name|Authorization object name|Yes|[string]| ||/|
|data>>data>>displayName|Authorization object display name|Yes|[string]| || |
|data>>data>>entityType|group: Organization structure<br />band: Role<br />user: User|Yes|[string]| ||group|
|data>>data>>userDirectoryId|User directory ID|Yes|[string]| ||6c97c0d0-db08-11ee-9cc7-6f7f82e11f93|
|data>>data>>isDeleted|External deleted status, 0 Not deleted, 1 Deleted|Yes|[number]| ||0|
|data>>data>>serverName|User directory name|Yes|[string]| ||custom_dir|
|data>>data>>dataType|Data type, for example:<br />externalUserGroup: External organization structure<br />localUserBand: Local role<br />localUser: Local user|Yes|[string]| ||externalUserGroup|
|data>>data>>effectiveTime|Effective timestamp, example 1709222400000|Yes|[string]| ||0|
|data>>data>>expireTime|Expiry timestamp, example 1709222400000|Yes|[string]| ||0|
|data>>data>>description|Description information|Yes|[string]| || |
|data>>data>>authorisedStatus|Authorization status<br />1: Never expires<br />2: About to expire<br />3: Expired|Yes|[number]| ||1|
|msg|Description information|Yes|[string]| ||Request successful|
|traceId|Request trace identifier|Yes|[string]| ||00bf58d2f1b31b0c|

"""

# Pre-API documentation
pre_api_content = """
#### Add Application Category
##### Interface Information

**API Path**
/api/v1/resource/createResourceGroup

**Request Protocol**
HTTPS

**Request Method**
POST

**Request Headers**:
| Header Label | Required | Description | Type | Possible Values | Constraints | Header Content | Example |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|Content-Type|Yes||[string]|||application/json|application/json|

**Request Parameters**Json
Object

| Parameter Name | Description | Required | Type | Possible Values | Constraints | Example |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|name|Application category name|Yes|[string]|:| | |
|description|Application category description|No|[string]|:| | |

**Response Content**:

**Return Result**
>Success (200)
Json
Object

| Parameter Name | Description | Required | Type | Possible Values | Constraints | Example |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|code|Error code, non-zero indicates error. Refer to error code definitions for details|Yes|[number]| || |
|data|Return content|Yes|[object]| || |
|data>>id|Application category ID|Yes|[string]| || |
|msg|Description information|Yes|[string]| || |


**Detailed Description**:
Interface description:
Request example
{
    &quot;name&quot;: &quot;First Category&quot;,
    &quot;description&quot;: &quot;This is an application category&quot;
}

Error Information



Error Message
Error Code




Parameter check failed
10000001


Method input parameters cannot be empty
10000001


Application category name (%s) already exists
77200005


Creation failed
10000000


#### Add User
##### Interface Information

**API Path**
/api/v3/user/create

**Request Protocol**
HTTPS

**Request Method**
POST

**Request Headers**:
| Header Label | Required | Description | Type | Possible Values | Constraints | Header Content | Example |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|Content-Type|Yes||[string]|||application/json|application/json|

**Request Parameters**Json
Object

| Parameter Name | Description | Required | Type | Possible Values | Constraints | Example |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|directoryDomain| |Yes|[string]| | | |
|name|Username|Yes|[string]| | | |
|group|Group belonging|Yes|[object]| | | |
|group>>op| |Yes|[string]| | |set|
|group>>key| |Yes|[string]| | |id、externalId、path|
|group>>data| |Yes|[string]| | | |
|password|Password|No|[string]| | | |
|externalId|User external ID|No|[string]| | | |
|displayName|Display name|No|[string]| | | |
|inheritGroup|Inherit application authorization from group: 0 not inherit, 1 inherit|No|[number]|1:,0:| | |
|status|Enabled status: 0 disabled, 1 enabled|No|[number]|0:,1:| | |
|description|Description|No|[string]| | | |
|phone|Phone number|No|[string]| | | |
|email|Email|No|[string]| | | |
|expiredTime|Expiry time, 13-digit Unix timestamp, '0' means never expires|No|[string]|0:| | |
|pwdModel|Password encryption algorithm type: 'clear' plaintext, 'rsa' asymmetric encryption|No|[string]|clear:,rsa:| | |
|DataSource| |No|[object]| | | |
|DataSource>>status| |No|[string]| | |local|
|DataSource>>displayName| |No|[string]| | |local|
|DataSource>>email| |No|[string]| | |local|
|DataSource>>description| |No|[string]| | |local|
|DataSource>>phone| |No|[string]| | |local|
|DataSource>>expiredTime| |No|[string]| | |local|

**Response Content**:

**Return Result**
>Success (200)
Json
Object

| Parameter Name | Description | Required | Type | Possible Values | Constraints | Example |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|code|Return code, 0 indicates success|Yes|[string]|OK;|| |
|data|User ID|Yes|[array]| || |
|msg|Return message corresponding to the return code|Yes|[string]| || |


**Detailed Description**:
Interface description: Parameter groupID is the group ID, a required parameter. Root group ID is 'root'. If you need to associate the user with other organizational structures, you can first use the organizational structure query interface (queryGroupByPath) to get the ID. Parameter password: To ensure the security of password data during transmission (from browser/client to server), it is strongly recommended to encrypt the password field using RSA algorithm (set pwdModel parameter to 'rsa'). For encryption methods, refer to the encrypt function in the public module of the demo, and handle_rsa.js. If you do not want to encrypt the password field (strongly not recommended), you can either not pass the pwdModel parameter in the request or set the pwdModel parameter to 'clear'. Authentication strategy ID, authComposeId retrieval method: Use "Developer Tools" to filter requests for authComposeId/queryAll, open the user directory to which your new user belongs in the console "Business Management"->"Authentication Management"->"Authentication Strategy" page, find the authentication strategy query interface for the user directory, and check the response body data to get the corresponding authentication strategy ID. User policy ID, userPolicyId retrieval method: Use "Developer Tools" to filter requests for userPolicy/queryUserPolicy, go to the console "Business Management"->"Policy Management"->"User Policy" page, and check the response body data to get the required policy ID. Request example{
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
}Error InformationError MessageError CodeUser or organization structure can be associated with at most 1000 applications10000000Password cannot be a common weak password10000001Batch function not supported temporarily10000001External ID duplicated, please re-enter10000000Password cannot contain username10000000Username (%s) already exists77200005Organization structure does not exist77200004Authentication strategy does not exist77200004User policy does not exist77200004Role does not exist or has been deleted77200004Super administrator role is not allowed to be assigned10000001SYSTEM administrator is a built-in system administrator, please use another name10000001Administrator role does not exist77200005Operation failed10000000


#### Add Organization Structure
##### Interface Information

**API Path**
/api/v3/group/create

**Request Protocol**
HTTPS

**Request Method**
POST

**Request Headers**:
| Header Label | Required | Description | Type | Possible Values | Constraints | Header Content | Example |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|Content-Type|Yes||[string]|||application/json|application/json|

**Request Parameters**Json
Object

| Parameter Name | Description | Required | Type | Possible Values | Constraints | Example |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|directoryDomain|User directory domain|Yes|[string]| | | |
|name|Organization structure name|Yes|[string]| | | |
|group| |Yes|[object]| | | |
|group>>op| |Yes|[string]| | | |
|group>>key| |Yes|[string]| | | |
|group>>data| |Yes|[string]| | | |
|description|Description|No|[string]| | | |
|externalId|External ID|No|[string]| | | |

**Response Content**:

**Return Result**
>Success (200)
Json
Object

| Parameter Name | Description | Required | Type | Possible Values | Constraints | Example |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|code|Error code, non-zero indicates error. Refer to error code definitions for details|Yes|[number]| || |
|data|Local organization structure ID|Yes|[object]| || |
|data>>id| |Yes|[array]| || |
|msg|Description information|Yes|[string]| || |

**Detailed Description**:
Interface description: Some parameters, such as associated object ID, need to be manually obtained through the console. Taking Chrome browser as an example, the retrieval method is to open "Developer Tools" with F12, find the query interface for the corresponding object in Network, and manually obtain the ID of the object. User directory ID, userDirectoryId retrieval method: Use "Developer Tools" to filter requests for userDirectory/queryAll, open the console "Business Management"->"User Management" page, check the response body data to get the ID of the corresponding user directory, or get the ID through the user directory query interface. Authentication strategy ID, authComposeId retrieval method: Use "Developer Tools" to filter requests for authComposeId/queryAll, open the user directory to which your new user belongs in the console "Business Management"->"Authentication Management"->"Authentication Strategy" page, find the authentication strategy query interface for the user directory, and check the response body data to get the corresponding authentication strategy ID. User policy ID, userPolicyId retrieval method: Use "Developer Tools" to filter requests for userPolicy/queryUserPolicy, go to the console "Business Management"->"Policy Management"->"User Policy" page, and check the response body data to get the required policy ID. Request example{
	"userDirectoryId": "d36ccb20-596a-11eb-a393-bbd9cb089321",
	"name": "External Group 1",
	"description": "1111",
	"path": "/",
	"authComposeId": "d36ccb20-596a-11eb-a393-bbd9cb0893d1",
	"roleIdEditWay": "append",
	"roleIdList": [ "7759f620-5583-11eb-880a-913383f106f2", "6559f620-5583-11eb-880a-913383f106f2"],
	"userPolicyId": "default"
}Error InformationError MessageError CodeParameter check failed10000001Organization structure name error, cannot contain /77200005Organization structure path level cannot exceed 32 levels10000001User directory does not exist77200004User organization structure name (%s) already exists77200005User can be associated with at most 1000 applications77200007Save failed, associated application does not exist or has been deleted77200004Save failed, associated application category does not exist or has been deleted77200004Operation failed10000000


#### Add Role
##### Interface Information

**API Path**
/api/v3/role/create

**Request Protocol**
HTTPS

**Request Method**
POST

**Request Headers**:
| Header Label | Required | Description | Type | Possible Values | Constraints | Header Content | Example |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|Content-Type|Yes||[string]|||application/json|application/json|

**Request Parameters**Json
Object

| Parameter Name | Description | Required | Type | Possible Values | Constraints | Example |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|directoryDomain| |Yes|[string]| | | |
|name|Username|Yes|[string]| | | |
|externalId|User external ID|No|[string]| | | |
|description|Description|No|[string]| | | |

**Response Content**:

**Return Result**
>Success (200)
Json
Object

| Parameter Name | Description | Required | Type | Possible Values | Constraints | Example |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|code|Return code, 0 indicates success|Yes|[string]| || |
|data|User ID|Yes|[array]| || |
|msg|Return message corresponding to the return code|Yes|[string]| || |


**Detailed Description**:
Interface description: Parameter groupID is the group ID, a required parameter. Root group ID is 'root'. If you need to associate the user with other organizational structures, you can first use the organizational structure query interface (queryGroupByPath) to get the ID. Parameter password: To ensure the security of password data during transmission (from browser/client to server), it is strongly recommended to encrypt the password field using RSA algorithm (set pwdModel parameter to 'rsa'). For encryption methods, refer to the encrypt function in the public module of the demo, and handle_rsa.js. If you do not want to encrypt the password field (strongly not recommended), you can either not pass the pwdModel parameter in the request or set the pwdModel parameter to 'clear'. Authentication strategy ID, authComposeId retrieval method: Use "Developer Tools" to filter requests for authComposeId/queryAll, open the user directory to which your new user belongs in the console "Business Management"->"Authentication Management"->"Authentication Strategy" page, find the authentication strategy query interface for the user directory, and check the response body data to get the corresponding authentication strategy ID. User policy ID, userPolicyId retrieval method: Use "Developer Tools" to filter requests for userPolicy/queryUserPolicy, go to the console "Business Management"->"Policy Management"->"User Policy" page, and check the response body data to get the required policy ID. Request example{
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
}Error InformationError MessageError CodeUser or organization structure can be associated with at most 1000 applications10000000Password cannot be a common weak password10000001Batch function not supported temporarily10000001External ID duplicated, please re-enter10000000Password cannot contain username10000000Username (%s) already exists77200005Organization structure does not exist77200004Authentication strategy does not exist77200004User policy does not exist77200004Role does not exist or has been deleted77200004Super administrator role is not allowed to be assigned10000001SYSTEM administrator is a built-in system administrator, please use another name10000001Administrator role does not exist77200005Operation failed10000000

#### Application Category Authorization-Based on ID
##### Interface Information

**API Path**
/api/v3/resourceGroup/assignById

**Request Protocol**
HTTP

**Request Method**
POST

**Request Parameters**Json
Object

| Parameter Name | Description | Required | Type | Possible Values | Constraints | Example |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|id|Required field when requesting based on application category id|Yes|[string]| | |4cffbdb0-daf7-11ee-99c1-ad5ce62be579|
|op|Possible values: ["reset", "append", "delete"], <br />representing reset, append, delete|Yes|[string]| | |reset|
|data|Authorization object|Yes|[object]| | | |
|data>>user|User|Yes|[array]| | |[{"directoryDomain":"local","id":"3e12e620-daf6-11ee-99c1-ad5ce62be579","effectiveTime":"1709646812000","expireTime":"1709913599999"}]|
|data>>user>>directoryDomain|User directory unique identifier, required field when authorizing application category permissions to users|Yes|[string]| | |local|
|data>>user>>id|User id, required field when authorizing application category permissions to users based on id|Yes|[string]| | |3e12e620-daf6-11ee-99c1-ad5ce62be579|
|data>>user>>name|User name, required field when authorizing application category permissions to users based on name|Yes|[string]| | | |
|data>>user>>externalId|User external id, required field when authorizing application category permissions to users based on external id|Yes|[string]| | | |
|data>>user>>effectiveTime|Effective time|Yes|[string]| | |1709646812000|
|data>>user>>expireTime|Expiry time|Yes|[string]| | |1709913599999|
|data>>userGroup|Organization structure|Yes|[array]| | |[{"directoryDomain":"custom83665","id":"5141600b-f276-4919-93a0-162be255f2ce","effectiveTime":"1709646812000","expireTime":"1709913599999"}]|
|data>>userGroup>>directoryDomain|User directory unique identifier, required field when authorizing application category permissions to organization structures|Yes|[string]| | |custom83665|
|data>>userGroup>>id|Organization structure id, required field when authorizing application category permissions to organization structures based on id|Yes|[string]| | |5141600b-f276-4919-93a0-162be255f2ce|
|data>>userGroup>>fullPath|Organization structure full path, required field when authorizing application category permissions to organization structures based on name|Yes|[string]| | | |
|data>>userGroup>>externalId|Organization structure external id, required field when authorizing application category permissions to organization structures based on external id|Yes|[string]| | | |
|data>>userGroup>>effectiveTime|Effective time|Yes|[string]| | |1709646812000|
|data>>userGroup>>expireTime|Expiry time|Yes|[string]| | |1709913599999|
|data>>userBand|Role|Yes|[array]| | |[{"directoryDomain":"custom83665","id":"5141600b-f276-4919-93a0-162be255f2ce","effectiveTime":"1709646812000","expireTime":"1709913599999"}]|
|data>>userBand>>directoryDomain|Role directory unique identifier, required field when authorizing application category permissions to roles|Yes|[string]| | |custom83665|
|data>>userBand>>id|Role id, required field when authorizing application category permissions to roles based on id|Yes|[string]| | |5141600b-f276-4919-93a0-162be255f2ce|
|data>>userBand>>name|Role name, required field when authorizing application category permissions to roles based on name|Yes|[string]| | | |
|data>>userBand>>externalId|Role external id, required field when authorizing application category permissions to roles based on external id|Yes|[string]| | | |
|data>>userBand>>effectiveTime|Effective time|Yes|[string]| | |1709646812000|
|data>>userBand>>expireTime|Expiry time|Yes|[string]| | |1709913599999|

**Response Content**:

**Return Result**
>Success (200)
Json
Object

| Parameter Name | Description | Required | Type | Possible Values | Constraints | Example |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|code|"OK" indicates success, others indicate error. Refer to error code definitions for details|Yes|[string]| ||OK|
|data|Response data|Yes|[object]| || |
|msg|Description information|Yes|[string]| ||Request successful|
|traceId|Request trace identifier|Yes|[string]| ||00b27e69598c3483|
"""

# Post-API documentation
post_api_content = """
#### ID Delete External Organization Structure
##### Interface Information

**API Path**
/api/v3/group/bulkDeleteByIdList

**Request Protocol**
HTTPS

**Request Method**
POST

**Request Headers**:
| Header Label | Required | Description | Type | Possible Values | Constraints | Header Content | Example |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|Content-Type|Yes||[string]|||application/json|application/json|

**Request Parameters**Json
Object

| Parameter Name | Description | Required | Type | Possible Values | Constraints | Example |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|idList|External organization structure ID list|Yes|[array]| | |Choose one from idList, pathList, externalIdList|
|directoryDomain|External user directory domain|Yes|[string]| | | |
|recursive|Recursively delete all subordinate organization structures: 0 non-recursive delete, 1 recursive delete|No|[number]|0:| | |

**Response Content**:

**Return Result**
>Success (200)
Json
Object

| Parameter Name | Description | Required | Type | Possible Values | Constraints | Example |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|code|0: success|Yes|[number]| || |
|data|Total number of deleted organization structures|Yes|[number]| || |
|msg|Return description|Yes|[string]| || |

**Detailed Description**:
Interface description: For deletion interfaces, if deleting data that already does not exist, it will not report an error. This is considered a successful operation, returning status code 200 and error code 0. Batch deletion only allows deletion of external user organization structures under the same user directory. Some parameters, such as associated object ID, need to be manually obtained through the console. Taking Chrome browser as an example, the retrieval method is to open "Developer Tools" with F12, find the query interface for the corresponding object in Network, and manually obtain the ID of the object. User directory ID, userDirectoryId retrieval method: Use "Developer Tools" to filter requests for userDirectory/queryAll, open the console "Business Management"->"User Management" page, check the response body data to get the ID of the corresponding user directory, or get the ID through the user directory query interface. Request example{
	"pathList": ["/a"],
	"userDirectoryName": "LDAP User Directory"
}Error InformationError MessageError CodeParameter check failed10000001Operation failed10000000

#### ID Batch Delete Local Users
##### Interface Information

**API Path**
/api/v3/user/bulkDeleteByIdList

**Request Protocol**
HTTPS

**Request Method**
POST

**Request Headers**:
| Header Label | Required | Description | Type | Possible Values | Constraints | Header Content | Example |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|Content-Type|Yes||[string]|||application/json|application/json|

**Request Parameters**Json
Object

| Parameter Name | Description | Required | Type | Possible Values | Constraints | Example |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|idList| |Yes|[array]| | | |
|directoryDomain| |Yes|[string]| | | |

**Response Content**:

**Return Result**
>Success (200)
Json
Object

| Parameter Name | Description | Required | Type | Possible Values | Constraints | Example |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|code|Return code, 0 indicates success|Yes|[string]| || |
|data|Message data body|Yes|[object]| || |
|msg|Return message corresponding to the return code|Yes|[string]| || |


**Detailed Description**:
Interface description: For deletion interfaces, if deleting data that already does not exist, it will not report an error. This is considered a successful operation, returning status code 200 and error code 0. Request example{
	"idList": ["b0301390-5ac5-11eb-a393-bbd9cb0893d1"]
}Error InformationError MessageError CodeParameter check failed10000001Super administrator, not allowed to delete10000001Operation failed10000000

#### ID Batch Delete Roles
##### Interface Information

**API Path**
/api/v3/role/bulkDeleteByIdList

**Request Protocol**
HTTPS

**Request Method**
POST

**Request Headers**:
| Header Label | Required | Description | Type | Possible Values | Constraints | Header Content | Example |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|Content-Type|Yes||[string]|||application/json|application/json|

**Request Parameters**Json
Object

| Parameter Name | Description | Required | Type | Possible Values | Constraints | Example |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|idList| |Yes|[array]| | | |
|directoryDomain| |Yes|[string]| | | |

**Response Content**:

**Return Result**
>Success (200)
Json
Object

| Parameter Name | Description | Required | Type | Possible Values | Constraints | Example |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|code|Return code, 0 indicates success|Yes|[string]| || |
|data|Message data body|Yes|[object]| || |
|msg|Return message corresponding to the return code|Yes|[string]| || |

**Detailed Description**:
Interface description: For deletion interfaces, if deleting data that already does not exist, it will not report an error. This is considered a successful operation, returning status code 200 and error code 0. Request example{
	"idList": ["b0301390-5ac5-11eb-a393-bbd9cb0893d1"]
}Error InformationError MessageError CodeParameter check failed10000001Super administrator, not allowed to delete10000001Operation failed10000000


#### Batch Delete Application Categories
##### Interface Information

**API Path**
/api/v1/resource/deleteResourceGroup

**Request Protocol**
HTTPS

**Request Method**
POST

**Request Headers**:
| Header Label | Required | Description | Type | Possible Values | Constraints | Header Content | Example |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|Content-Type|Yes||[string]|||application/json|application/json|

**Request Parameters**Json
Object

| Parameter Name | Description | Required | Type | Possible Values | Constraints | Example |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|idList|ID list to be deleted|Yes|[array]|:| | |

**Response Content**:

**Return Result**
>Success (200)
Json
Object

| Parameter Name | Description | Required | Type | Possible Values | Constraints | Example |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|code|0: success|Yes|[number]| || |
|data| |Yes|[object]| || |
|data>>length|Number of deleted applications|Yes|[string]| || |
|data>>name|Application names in abnormal state|No|[array]| || |
|msg| |Yes|[string]| || |

**Detailed Description**:
Interface description:

For deletion interfaces, if deleting data that already does not exist, it will not report an error. This is considered a successful operation, returning status code 200 and error code 0. Note: Only application groups that are not associated with any applications can be deleted. If the application group is associated with applications, the associated applications must be deleted first before the application group can be deleted.


Request example
{
    &quot;idList&quot;: [&quot;a1240650-5ae7-11eb-a393-bbd9cb0893d1&quot;]
}

Error Information



Error Message
Error Code




Parameter check failed
10000001


Default application category, not allowed to delete
77200008


Delete failed, please move the WEB network-wide applications in the current application category to other categories first
77200008


Delete failed
10000000


Some selected applications are in collection/trial run status, please deselect them
77200008
"""
