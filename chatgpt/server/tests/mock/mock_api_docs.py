# Test points
test_points = [
    "Query Application Category Authorization - Normal Scenario - Verify that the interface can successfully return application category authorization information when correct name, fieldMode, sortBy, entityType, pageIndex and pageSize are provided."
]

# API documentation being tested
tested_api = """
#### Query Application Category Authorization - Based on Name
##### Interface Information

**API Path**
/api/v3/resourceGroupAssign/queryByName

**Request Protocol**
HTTP

**Request Method**
POST

**Request Parameters** Json
Object

| Parameter Name | Description | Required | Type | Possible Values | Constraints | Example |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|name|Application category name, required field when requesting based on name|Yes|[string]| | |SSL Internal Application|
|fieldMode|Return field mode, value range: ["all", "lite"], <br />representing "return all fields", "return simplified fields"|Yes|[string]| | |all|
|sortBy|Sort method, default: "default"|Yes|[string]| | |default|
|entityType|Entity type, value range: ["group", "band", "user"], <br />representing organization structure, role, user, empty array or no value means query all entity types|Yes|[object]| | |["user", "group", "band"]|
|pageIndex|Page number|Yes|[number]| | | |
|pageSize|Maximum number of items displayed per page|Yes|[number]| | | |

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
|data>>data>>isDeleted|Externally deleted, 0 Not deleted, 1 Deleted|Yes|[number]| ||0|
|data>>data>>serverName|User directory name|Yes|[string]| ||custom_dir|
|data>>data>>dataType|Data type, for example:<br />externalUserGroup: External organization structure<br />localUserBand: Local role<br />localUser: Local user|Yes|[string]| ||externalUserGroup|
|data>>data>>effectiveTime|Effective timestamp, e.g., 1709222400000|Yes|[string]| ||0|
|data>>data>>expireTime|Expiry timestamp, e.g., 1709222400000|Yes|[string]| ||0|
|data>>data>>description|Description information|Yes|[string]| || |
|data>>data>>authorisedStatus|Authorization status<br />1: Never expires;<br />2: About to expire;<br />3: Expired|Yes|[number]| ||1|
|msg|Description message|Yes|[string]| ||Request successful|
|traceId|Request trace identifier|Yes|[string]| ||00bf58d2f1b31b0c|

"""

# Prerequisite API documentation
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

**Request Parameters** Json
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
|code|Error code, non-zero indicates error, refer to error code definition for specific meaning|Yes|[number]| || |
|data|Return content|Yes|[object]| || |
|data>>id|Application category ID|Yes|[string]| || |
|msg|Description message|Yes|[string]| || |


**Detailed Description**:
Interface description:
Request example
{
    &quot;name&quot;: &quot;First Category&quot;,
    &quot;description&quot;: &quot;This is an application category&quot;
}

Error information



Error prompt
Error code




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

**Request Parameters** Json
Object

| Parameter Name | Description | Required | Type | Possible Values | Constraints | Example |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|directoryDomain| |Yes|[string]| | | |
|name|Username|Yes|[string]| | | |
|group|Belonging group|Yes|[object]| | | |
|group>>op| |Yes|[string]| | |set|
|group>>key| |Yes|[string]| | |id、externalId、path|
|group>>data| |Yes|[string]| | | |
|password|Password|No|[string]| | | |
|externalId|User external ID|No|[string]| | | |
|displayName|Display name|No|[string]| | | |
|inheritGroup|Inherit application authorization from belonging group: 0 do not inherit, 1 inherit|No|[number]|1:,0:| | |
|status|Enable status: 0 disabled, 1 enabled|No|[number]|0:,1:| | |
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
|msg|Return message, corresponding to the return code|Yes|[string]| || |

"""

# Post API documentation
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

**Request Parameters** Json
Object

| Parameter Name | Description | Required | Type | Possible Values | Constraints | Example |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|idList|External organization structure ID list|Yes|[array]| | |idList、pathList、externalIdList three-choose-one|
|directoryDomain|External user directory domain|Yes|[string]| | | |
|recursive|Recursively delete all subordinate organization structures: 0 do not recursively delete, 1 recursively delete|No|[number]|0:| | |

**Response Content**:

**Return Result**
>Success (200)
Json
Object

| Parameter Name | Description | Required | Type | Possible Values | Constraints | Example |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|code|0: Success,|Yes|[number]| || |
|data|Deleted organization structure count|Yes|[number]| || |
|msg|Return description|Yes|[string]| || |

**Detailed Description**:
Interface description: For delete interfaces, if the data to be deleted does not exist, it will not be reported as an error, and this will be considered a successful operation, returning status code 200 and error code 0. Batch deletion is only allowed to delete external user organization structures belonging to the same user directory. Some parameters, such as associated object ID, need to be manually obtained through F12 in Chrome browser to get the ID of the corresponding object. User directory ID, userDirectoryId acquisition method, use "Developer Tools" filter request userDirectory/queryAll, open the "Business Management" page in the console, view the response body data to get the ID of the corresponding user directory, or obtain the ID through the user directory query interface. Request example {
	"pathList": ["/a"],
	"userDirectoryName": "LDAP User Directory"
} Error information Error prompt Error code Parameter check failed 10000001 Operation failed 10000000

#### Id Batch Delete Local User
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

**Request Parameters** Json
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
|msg|Return message, corresponding to the return code|Yes|[string]| || |


**Detailed Description**:
Interface description: For delete interfaces, if the data to be deleted does not exist, it will not be reported as an error, and this will be considered a successful operation, returning status code 200 and error code 0 Request example {
	"idList": ["b0301390-5ac5-11eb-a393-bbd9cb0893d1"]
} Error information Error prompt Error code Parameter check failed 10000001 Super administrator, not allowed to delete 10000001 Operation failed 10000000

#### Id Batch Delete Role
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

**Request Parameters** Json
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
|msg|Return message, corresponding to the return code|Yes|[string]| || |

**Detailed Description**:
Interface description: For delete interfaces, if the data to be deleted does not exist, it will not be reported as an error, and this will be considered a successful operation, returning status code 200 and error code 0 Request example {
	"idList": ["b0301390-5ac5-11eb-a393-bbd9cb0893d1"]
} Error information Error prompt Error code Parameter check failed 10000001 Super administrator, not allowed to delete 10000001 Operation failed 10000000


#### Batch Delete Application Category
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

**Request Parameters** Json
Object

| Parameter Name | Description | Required | Type | Possible Values | Constraints | Example |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|idList|Deleted id list|Yes|[array]|:| | |

**Response Content**:

**Return Result**
>Success (200)
Json
Object

| Parameter Name | Description | Required | Type | Possible Values | Constraints | Example |
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ |
|code|0: Success,|Yes|[number]| || |
|data| |Yes|[object]| || |
|data>>length|Deleted application count|Yes|[string]| || |
|data>>name|Exceptional application name|No|[array]| || |
|msg| |Yes|[string]| || |

**Detailed Description**:
Interface description:

For delete interfaces, if the data to be deleted does not exist, it will not be reported as an error, and this will be considered a successful operation, returning status code 200 and error code 0 Note: Only allow delete applications that are not associated with any applications. If the application group is associated with applications, you must first delete the associated applications before allowing the deletion of the application group.


Request example
{
    &quot;idList&quot;: [&quot;a1240650-5ae7-11eb-a393-bbd9cb0893d1&quot;]
}

Error information



Error prompt
Error code




Parameter check failed
10000001


Default application category, not allowed to delete
77200008


Delete failed, please move the current application category's WEB full-network application to other categories first
77200008


Delete failed
10000000


There are already selected applications in the "Collecting/Trial Run" state, please cancel the selection
77200008
"""
