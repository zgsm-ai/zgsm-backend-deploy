#!/bin/bash
set -euo pipefail
# -------------------------- 初始化配置 --------------------------
SCRIPT_NAME=$(basename "$0")
LOG_FILE="${SCRIPT_NAME%.*}.log"
exec > >(tee -a "$LOG_FILE") 2>&1
# -------------------------- 常量定义 --------------------------
declare -r SERVER_IP='192.168.14.133'
declare -r CHAT_MODEL_IP='http://127.74.1.32:8888'
declare -r CHAT_MODEL_TYPE='deepseek-chat'
declare -r CHAT_API_KEY='sk-edd332b8844445f6ef8c683b754141d'
declare -r COMPLETION_MODEL_IP='http://127.74.1.32:9999/v1/completions'
declare -r COMPLETION_MODEL_TYPE='DeepSeek-Coder-V2-Lite-Base'
declare -r COMPLETION_API_KEY='sk-e0d435b568876745f4438c583b4561d'
declare -r BASE_DIR="$HOME/sxf/zgsm-compose-deploy"

# -------------------------- 函数定义 --------------------------
log() {
    local level=$1
    local message=$2
    local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    echo -e "[${timestamp}] [${level}] ${message}"
}

validate_environment() {
    local required_files=(
        "configure.sh"
        "chatgpt/custom.yml.tpl"
        "tpl-resolve.sh"
        "chatgpt-initdb.sh"
        "docker-compose.yml"
        "apisix-chatgpt.sh"
        "apisix-copilot.sh"
        "apisix-issue.sh"
        "apisix-keycloak.sh"
        "keycloak-import.sh"
    )

    [[ -d "$BASE_DIR" ]] || {
        log "ERROR" "基础目录不存在: $BASE_DIR"
        exit 1
    }

    for file in "${required_files[@]}"; do
        local full_path="${BASE_DIR}/${file}"
        [[ -f "$full_path" ]] || {
            log "ERROR" "必要文件缺失: $full_path"
            exit 1
        }
    done
}

safe_sed() {
    local pattern=$1
    local file=$2
    log "INFO" "正在修改文件: $file"
    if ! sed -i.bak "$pattern" "$file"; then
        log "ERROR" "文件修改失败: $file"
        exit 1
    fi
    # 显示修改差异后删除备份
    diff -u "${file}.bak" "$file" || true
    rm -f "${file}.bak"
}

safe_chown() {
    # 需要修改权限的目录数组
    declare -a dirs=(
        "/etcd/data"
        "/postgres/data"
        "/es/data"
    )

    # 检查并创建目录（如果需要）
    for dir in "${dirs[@]}"; do
        full_path="${BASE_DIR}${dir}"

        # 自动创建目录（如果不存在）
        if [[ ! -d "$full_path" ]]; then
            echo "Creating directory: $full_path"
            if ! sudo mkdir -p "$full_path"; then
                echo "Error: Failed to create directory $full_path" >&2
                exit 1
            fi
        fi

        echo "Processing: $full_path"

        # 修改所有权
        if ! sudo chown -R 1000:1000 "$full_path"; then
            echo "Error: chown failed for $full_path" >&2
            exit 1
        fi

        # 修改权限
        if ! sudo chmod -R 0775 "$full_path"; then
            echo "Error: chmod failed for $full_path" >&2
            exit 1
        fi
    done

    echo "All permissions updated successfully"
}

# -------------------------- 主逻辑 --------------------------
main() {
    log "INFO" "脚本启动，日志文件: $LOG_FILE"

    # 环境校验
    validate_environment
    cd "$BASE_DIR" || exit 1

    # 参数替换
    safe_sed "s/ZGSM_BACKEND=\".*\"/ZGSM_BACKEND=\"$SERVER_IP\"/g" configure.sh
    safe_sed "s#OPENAI_MODEL_HOST=\".*\"#OPENAI_MODEL_HOST=\"$COMPLETION_MODEL_IP\"#g" configure.sh
    safe_sed "s/OPENAI_MODEL=\".*\"/OPENAI_MODEL=\"$COMPLETION_MODEL_TYPE\"/g" configure.sh
    safe_sed "s/OPENAI_MODEL_API_KEY=\".*\"/OPENAI_MODEL_API_KEY=\"$COMPLETION_API_KEY\"/g" configure.sh
    safe_sed "s#server_url: \".*\"#server_url: \"$CHAT_MODEL_IP\"#g" chatgpt/custom.yml.tpl
    safe_sed "s/api_key: \".*\"/api_key: \"$CHAT_API_KEY\"/g" chatgpt/custom.yml.tpl
    safe_sed "s/CHAT_MODEL=\".*\"/CHAT_MODEL=\"$CHAT_MODEL_TYPE\"/g" configure.sh

    # 执行子脚本
    local sub_scripts=(
        "tpl-resolve.sh"
        "chatgpt-initdb.sh"
    )
    for script in "${sub_scripts[@]}"; do
        log "INFO" "执行子脚本: $script"
        if ! bash "$script"; then
            log "ERROR" "子脚本执行失败: $script"
            exit 1
        fi
    done

    # 修改目录权限
    safe_chown

    # 启动Docker服务
    log "INFO" "启动Docker容器"
    if ! docker-compose -f docker-compose.yml up -d; then
        log "ERROR" "Docker启动失败"
        exit 1
    fi

    sleep 20

    # 配置APISIX
    local apisix_scripts=(
        "apisix-chatgpt.sh"
        "apisix-copilot.sh"
        "apisix-issue.sh"
        "apisix-keycloak.sh"
        "keycloak-import.sh"
    )
    for script in "${apisix_scripts[@]}"; do
        log "INFO" "执行APISIX配置: $script"
        if ! bash "$script"; then
            log "ERROR" "APISIX配置失败: $script"
            exit 1
        fi
    done

    sleep 10

    log "INFO" "所有操作执行完成"
}

main "$@"
