#!/bin/bash
set -euo pipefail
# -------------------------- Initialize configuration --------------------------
SCRIPT_NAME=$(basename "$0")
LOG_FILE="${SCRIPT_NAME%.*}.log"
exec > >(tee -a "$LOG_FILE") 2>&1
# -------------------------- Constant definition --------------------------
declare -r SERVER_IP='192.168.14.133'
declare -r CHAT_MODEL_IP='http://127.74.1.32:8888'
declare -r CHAT_MODEL_TYPE='deepseek-chat'
declare -r CHAT_API_KEY='sk-edd332b8844445f6ef8c683b754141d'
declare -r COMPLETION_MODEL_IP='http://127.74.1.32:9999/v1/completions'
declare -r COMPLETION_MODEL_TYPE='DeepSeek-Coder-V2-Lite-Base'
declare -r COMPLETION_API_KEY='sk-e0d435b568876745f4438c583b4561d'
declare -r BASE_DIR=$(pwd)

# -------------------------- Function definition --------------------------
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
        "docker-compose.yml.tpl"
        "apisix-chatgpt.sh"
        "apisix-copilot.sh"
        "apisix-issue.sh"
        "apisix-keycloak.sh"
        "keycloak-import.sh"
    )

    [[ -d "$BASE_DIR" ]] || {
        log "ERROR" "Basic directory does not exist: $BASE_DIR"
        exit 1
    }

    for file in "${required_files[@]}"; do
        local full_path="${BASE_DIR}/${file}"
        [[ -f "$full_path" ]] || {
            log "ERROR" "Required file is missing: $full_path"
            exit 1
        }
    done
}

safe_sed() {
    local pattern=$1
    local file=$2
    log "INFO" "Modifying file: $file"
    if ! sed -i.bak "$pattern" "$file"; then
        log "ERROR" "File modification failed: $file"
        exit 1
    fi
    # Display modification differences and then delete the backup
    diff -u "${file}.bak" "$file" || true
    rm -f "${file}.bak"
}

safe_chown() {
    # Array of directories that need permission modification
    declare -a dirs=(
        "/etcd/data"
        "/es/data"
    )

    # Check and create directories (if needed)
    for dir in "${dirs[@]}"; do
        full_path="${BASE_DIR}${dir}"

        # Automatically create directory (if it does not exist)
        if [[ ! -d "$full_path" ]]; then
            echo "Creating directory: $full_path"
            if ! sudo mkdir -p "$full_path"; then
                echo "Error: Failed to create directory $full_path" >&2
                exit 1
            fi
        fi

        echo "Processing: $full_path"

        # Modify ownership
        if ! sudo chown -R 1000:1000 "$full_path"; then
            echo "Error: chown failed for $full_path" >&2
            exit 1
        fi

        # Modify permissions
        if ! sudo chmod -R 0775 "$full_path"; then
            echo "Error: chmod failed for $full_path" >&2
            exit 1
        fi
    done

    echo "All permissions updated successfully"
}

# -------------------------- Main logic --------------------------
main() {
    log "INFO" "Script started, log file: $LOG_FILE"

    # Environment validation
    validate_environment
    cd "$BASE_DIR" || exit 1

    # Parameter replacement
    safe_sed "s/ZGSM_BACKEND=\".*\"/ZGSM_BACKEND=\"$SERVER_IP\"/g" configure.sh
    safe_sed "s#OPENAI_MODEL_HOST=\".*\"#OPENAI_MODEL_HOST=\"$COMPLETION_MODEL_IP\"#g" configure.sh
    safe_sed "s/OPENAI_MODEL=\".*\"/OPENAI_MODEL=\"$COMPLETION_MODEL_TYPE\"/g" configure.sh
    safe_sed "s/OPENAI_MODEL_API_KEY=\".*\"/OPENAI_MODEL_API_KEY=\"$COMPLETION_API_KEY\"/g" configure.sh
    safe_sed "s#server_url: \".*\"#server_url: \"$CHAT_MODEL_IP\"#g" chatgpt/custom.yml.tpl
    safe_sed "s/api_key: \".*\"/api_key: \"$CHAT_API_KEY\"/g" chatgpt/custom.yml.tpl
    safe_sed "s/CHAT_MODEL=\".*\"/CHAT_MODEL=\"$CHAT_MODEL_TYPE\"/g" configure.sh

    # Modify directory permissions
    safe_chown

    # Execute sub-scripts
    local sub_scripts=(
        "tpl-resolve.sh"
        "chatgpt-initdb.sh"
    )
    for script in "${sub_scripts[@]}"; do
        log "INFO" "Executing sub-script: $script"
        if ! bash "$script"; then
            log "ERROR" "Sub-script execution failed: $script"
            exit 1
        fi
    done

    # Start Docker service
    log "INFO" "Starting Docker containers"
    if ! docker-compose -f docker-compose.yml up -d; then
        log "ERROR" "Docker startup failed"
        exit 1
    fi

    sleep 20

    # Configure APISIX
    local apisix_scripts=(
        "apisix-chatgpt.sh"
        "apisix-copilot.sh"
        "apisix-issue.sh"
        "apisix-keycloak.sh"
        "keycloak-import.sh"
    )
    for script in "${apisix_scripts[@]}"; do
        log "INFO" "Executing APISIX configuration: $script"
        if ! bash "$script"; then
            log "ERROR" "APISIX configuration failed: $script"
            exit 1
        fi
    done

    sleep 10

    log "INFO" "All operations completed"
}

main "$@"
