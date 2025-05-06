#!/bin/bash
set -euo pipefail
# -------------------------- Initialize Configuration --------------------------
SCRIPT_NAME=$(basename "$0")
LOG_FILE="${SCRIPT_NAME%.*}.log"
exec > >(tee -a "$LOG_FILE") 2>&1
# -------------------------- Constants Definition --------------------------
# one-api root key, custom, can be generated using 'uuidgen | tr -d '-'' command, will be configured in apisix gateway proxy-rewrite plugin. The real LLM api-keys should be configured in the one-api backend page.
declare -r ONE_API_INITIAL_ROOT_KEY="966c3157fe65461dbc731cd540b6cd5d"
declare -r ONE_API_PORT=30000
declare -r CHAT_MODEL_IP="http://one-api:${ONE_API_PORT}"  # Unified access through one-api, model configuration is done in one-api
declare -r CHAT_MODEL_TYPE='deepseek-chat'    # Chat model
declare -r CHAT_API_KEY=${ONE_API_INITIAL_ROOT_KEY}
declare -r COMPLETION_MODEL_IP="http://one-api:${ONE_API_PORT}/v1/completions" # Unified access through one-api, model configuration is done in one-api
declare -r COMPLETION_MODEL_TYPE='deepseek-chat'  # Completion model
declare -r COMPLETION_API_KEY=${ONE_API_INITIAL_ROOT_KEY}

# Get the machine's IP
SERVER_IP=$(hostname -I | awk '{ print $1 }')
declare -r SERVER_IP
declare -r BASE_DIR=$(pwd)

# -------------------------- Function Definitions --------------------------
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
        #"dex/config.yaml.tpl"
        "tpl-resolve.sh"
        "chatgpt-initdb.sh"
        "docker-compose.yml.tpl"
        "apisix-chatgpt.sh"
        "apisix-copilot.sh"
        "apisix-issue.sh"
        "apisix-keycloak.sh"
        "apisix-oidc.sh"
        "keycloak-import.sh"
    )

    [[ -d "$BASE_DIR" ]] || {
        log "ERROR" "Base directory does not exist: $BASE_DIR"
        exit 1
    }

    for file in "${required_files[@]}"; do
        local full_path="${BASE_DIR}/${file}"
        [[ -f "$full_path" ]] || {
            log "ERROR" "Required file missing: $full_path"
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
    # Show differences and delete backup
    diff -u "${file}.bak" "$file" || true
    rm -f "${file}.bak"
}

safe_chown() {
    # Directories that need permission changes
    declare -a dirs=(
        "/etcd/data"
        "/es/data"
    )

    # Check and create directories (if needed)
    for dir in "${dirs[@]}"; do
        full_path="${BASE_DIR}${dir}"

        # Automatically create directory (if it doesn't exist)
        if [[ ! -d "$full_path" ]]; then
            echo "Creating directory: $full_path"
            if ! sudo mkdir -p "$full_path"; then
                echo "Error: Failed to create directory $full_path" >&2
                exit 1
            fi
        fi

        echo "Processing: $full_path"

        # Change ownership
        if ! sudo chown -R 1000:1000 "$full_path"; then
            echo "Error: chown failed for $full_path" >&2
            exit 1
        fi

        # Change permissions
        if ! sudo chmod -R 0775 "$full_path"; then
            echo "Error: chmod failed for $full_path" >&2
            exit 1
        fi
    done

    echo "All permissions updated successfully"
}

# -------------------------- Main Logic --------------------------
main() {
    log "INFO" "Script started, log file: $LOG_FILE"

    # Environment validation
    validate_environment
    cd "$BASE_DIR" || exit 1

    # Parameter replacement
    safe_sed "s#OPENAI_MODEL_HOST=\".*\"#OPENAI_MODEL_HOST=\"$COMPLETION_MODEL_IP\"#g" configure.sh
    safe_sed "s/OPENAI_MODEL=\".*\"/OPENAI_MODEL=\"$COMPLETION_MODEL_TYPE\"/g" configure.sh
    safe_sed "s/OPENAI_MODEL_API_KEY=\".*\"/OPENAI_MODEL_API_KEY=\"$COMPLETION_API_KEY\"/g" configure.sh
    safe_sed "s#server_url: \".*\"#server_url: \"$CHAT_MODEL_IP\"#g" chatgpt/custom.yml.tpl
    safe_sed "s/api_key: \".*\"/api_key: \"$CHAT_API_KEY\"/g" chatgpt/custom.yml.tpl
    safe_sed "s/CHAT_MODEL=\".*\"/CHAT_MODEL=\"$CHAT_MODEL_TYPE\"/g" configure.sh
    safe_sed "s/ONE_API_INITIAL_ROOT_KEY=\".*\"/ONE_API_INITIAL_ROOT_KEY=\"$ONE_API_INITIAL_ROOT_KEY\"/g" configure.sh
    safe_sed "s/ONE_API_PORT=\".*\"/ONE_API_PORT=$ONE_API_PORT/g" configure.sh

    # Modify directory permissions
    safe_chown

    # Execute subscripts
    local sub_scripts=(
        "tpl-resolve.sh"
        "chatgpt-initdb.sh"
    )
    for script in "${sub_scripts[@]}"; do
        log "INFO" "Executing subscript: $script"
        if ! bash "$script"; then
            log "ERROR" "Subscript execution failed: $script"
            exit 1
        fi
    done

    # Start Docker services
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
        "apisix-oneapi.sh"
        "apisix-oidc.sh"
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
    log "INFO" "Please login to the one-api backend [http://${SERVER_IP}:${ONE_API_PORT}] (default account: root, password: 123456), and add your LLM api-key in the Channels section! (If the page is blank, please wait as containers may take some time to start)"
}

main "$@"
