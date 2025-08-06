#!/bin/bash
set -euo pipefail
# -------------------------- Initialize Configuration --------------------------
SCRIPT_NAME=$(basename "$0")
LOG_FILE="${SCRIPT_NAME%.*}.log"
exec > >(tee -a "$LOG_FILE") 2>&1
# -------------------------- Constants Definition --------------------------
# Get the machine's IP
SERVER_IP=$(hostname -I | awk '{ print $1 }')
declare -r SERVER_IP
declare -r BASE_DIR=$(pwd)

# -------------------------- Function Definitions --------------------------
docker-compose() {
    # Check if docker has compose subcommand
    if docker compose version >/dev/null 2>&1; then
        command docker compose "$@"
    else
        command docker-compose "$@"
    fi
}

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
        "docker-download-images.sh"
        "db-initdb.sh"
        "docker-compose.yml.tpl"
        "apisix-chatgpt.sh"
        "apisix-issue.sh"
        "apisix-ai-gateway.sh"
        "apisix-casdoor.sh"
        "apisix-chatrag.sh"
        "apisix-cli-tools.sh"
        "apisix-codereview.sh"
        "apisix-completion-v2.sh"
        "apisix-credit-manager.sh"
        "apisix-grafana.sh"
        "apisix-oidc-auth.sh"
        "apisix-quota-manager.sh"
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
    safe_sed "s/COSTRICT_BACKEND=\".*\"/COSTRICT_BACKEND=\"$SERVER_IP\"/g" configure.sh

    # Modify directory permissions
    safe_chown

    # Execute subscripts
    local sub_scripts=(
        "docker-download-images.sh"
        "tpl-resolve.sh"
        "db-initdb.sh"
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

    sleep 5

    # Configure APISIX
    local apisix_scripts=(
        "apisix-ai-gateway.sh"
        "apisix-casdoor.sh"
        "apisix-chatgpt.sh"
        "apisix-chatrag.sh"
        "apisix-cli-tools.sh"
        "apisix-codebase-indexer.sh"
        "apisix-codereview.sh"
        "apisix-completion-v2.sh"
        "apisix-credit-manager.sh"
        "apisix-grafana.sh"
        "apisix-issue.sh"
        "apisix-oidc-auth.sh"
        "apisix-quota-manager.sh"
    )
    for script in "${apisix_scripts[@]}"; do
        log "INFO" "Executing APISIX configuration: $script"
        if ! bash "$script"; then
            log "ERROR" "APISIX configuration failed: $script"
            exit 1
        fi
    done

    sleep 10

    source ./configure.sh

    log "INFO" "All operations completed"
    log "INFO" "Please login to the AI-GATEWAY backend [http://${COSTRICT_BACKEND}:${PORT_HIGRESS_CONTROL}] (default account: root, password: 123456), and add your LLM api-key in the Channels section! (If the page is blank, please wait as containers may take some time to start)"
}

main "$@"
