# coding: utf-8
import requests
import json
import argparse

# Keycloak 服务器配置
KEYCLOAK_URL = "http://localhost:8080/auth"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = ""
IMPORT_FNAME = "./keycloak/realm-export.json"
CLIENT_NAME = "zgsm"
CLIENT_PASSWORD = "123"

def get_args():
    global KEYCLOAK_URL, ADMIN_USERNAME, ADMIN_PASSWORD, IMPORT_FNAME
    parser = argparse.ArgumentParser(description="令keycloak导入json数据，创建realm")
    parser.add_argument('--url', type=str, help='keycloak服务器地址(如http://localhost:8080/auth)', required=True)
    parser.add_argument('--username', type=str, help='keycloak管理员的用户名', required=False)
    parser.add_argument('--password', type=str, help='keycloak管理员的密码', required=True)
    parser.add_argument('--fname', type=str, help='待导入文件的名字', required=False)
    parser.add_argument('--client-name', type=str, help='诸葛神码用户名', required=False)
    parser.add_argument('--client-password', type=str, help='诸葛神码密码', required=False)

    args = parser.parse_args()

    if args.url:
        KEYCLOAK_URL = args.url
    if args.username:
        ADMIN_USERNAME = args.username
    if args.password:
        ADMIN_PASSWORD = args.password
    if args.fname:
        IMPORT_FNAME = args.fname
    if args.fname:
        CLIENT_NAME = args.client_name
    if args.fname:
        CLIENT_PASSWORD = args.client_password

    print(f"KEYCLOAK_URL: {KEYCLOAK_URL}")
    print(f"ADMIN_USERNAME: {ADMIN_USERNAME}")
    print(f"ADMIN_PASSWORD: {ADMIN_PASSWORD}")
    print(f"IMPORT_FNAME: {IMPORT_FNAME}")
    print(f"CLIENT_NAME: {CLIENT_NAME}")
    print(f"CLIENT_PASSWORD: {CLIENT_PASSWORD}")

def get_access_token():
    """获取访问令牌"""
    token_url = f"{KEYCLOAK_URL}/realms/master/protocol/openid-connect/token"
    payload = {
        'client_id': 'admin-cli',
        'username': ADMIN_USERNAME,
        'password': ADMIN_PASSWORD,
        'grant_type': 'password'
    }
    response = requests.post(token_url, data=payload)

    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise Exception(f"Failed to get access token: {response.text}")

def create_realm(access_token, realm_data, realm_name):
    """创建新的 realm"""
    create_realm_url = f"{KEYCLOAK_URL}/admin/realms"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    response = requests.post(create_realm_url, headers=headers, json=realm_data)

    if response.status_code >= 200 and response.status_code < 210:
        print(f"status {response.status_code}: Realm '{realm_name}' created successfully.")
    else:
        raise Exception(f"status {response.status_code}: Failed to create realm: {response.text}")

def create_user(access_token, realm_name, username, password, temporary_password=False):
    create_user_url = f"{KEYCLOAK_URL}/admin/realms/{realm_name}/users"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    user_data = {
        "username": username,
        "enabled": True,
        "credentials": [
            {
                "type": "password",
                "value": password,
                "temporary": temporary_password  # 是否需在首次登录时修改密码
            }
        ]
    }
    response = requests.post(create_user_url, headers=headers, json=user_data)
    if 200 <= response.status_code < 210:
        print(f"Status {response.status_code}: User '{username}' created successfully in realm '{realm_name}'")
        return response.headers.get('Location')  # 返回新用户的URL
    else:
        raise Exception(f"Status {response.status_code}: Failed to create user: {response.text}")

def main():
    try:
        # 获取命令行参数
        get_args()

        # 获取访问令牌
        access_token = get_access_token()

        realm_data = {}
        with open(IMPORT_FNAME, 'r') as file:
            realm_data = json.load(file)
        realm_name = realm_data.get('realm')

        # 创建新的 realm
        create_realm(access_token, realm_data, realm_name)

        # 创建 user
        create_user(access_token, realm_name, CLIENT_NAME, CLIENT_PASSWORD)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
