#!/bin/bash
# set -euo pipefail
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

sudo() {
    command $@
}

wait_for_apisix_ready() {
    local max_attempts=30
    local wait_seconds=2
    local attempt=1
    
    source ./configure.sh
    
    log "INFO" "等待APISIX服务启动..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s -f http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X GET > /dev/null 2>&1; then
            log "INFO" "APISIX服务已准备就绪，可以添加upstream配置"
            return 0
        fi
        
        log "INFO" "APISIX服务尚未就绪，等待${wait_seconds}秒后重试... (尝试 $attempt/$max_attempts)"
        sleep $wait_seconds
        attempt=$((attempt + 1))
    done
    
    log "ERROR" "APISIX服务在${max_attempts}次尝试后仍未准备就绪"
    return 1
}

validate_environment() {
    local required_files=(
        "configure.sh"
        "tpl-resolve.sh"
        "docker-download-images.sh"
        "db-initdb.sh"
        "docker-compose.yml.tpl"
        "apisix-ai-gateway.sh"
        "apisix-casdoor.sh"
        "apisix-chatrag.sh"
        "apisix-codereview.sh"
        "apisix-completion-v2.sh"
        "apisix-costrict-apps.sh"
        "apisix-cotun.sh"
        "apisix-credit-manager.sh"
        "apisix-embedder.sh"
        "apisix-grafana.sh"
        "apisix-issue.sh"
        "apisix-oidc-auth.sh"
        #"apisix-quota-manager.sh"
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
    local auto_ip=false
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --auto-ip)
                auto_ip=true
                shift
                ;;
            *)
                # Unknown option
                shift
                ;;
        esac
    done
    
    log "INFO" "Script started, log file: $LOG_FILE"

    # Environment validation
    validate_environment
    cd "$BASE_DIR" || exit 1

    # Parameter replacement
    if [[ "$auto_ip" = true ]]; then
        log "INFO" "Auto IP mode enabled, setting COSTRICT_BACKEND to SERVER_IP: $SERVER_IP"
        safe_sed "s/COSTRICT_BACKEND=\".*\"/COSTRICT_BACKEND=\"$SERVER_IP\"/g" configure.sh
    else
        log "INFO" "Auto IP mode disabled, skipping COSTRICT_BACKEND configuration"
    fi

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
    
    # Wait for APISIX to be ready
    if ! wait_for_apisix_ready; then
        log "ERROR" "APISIX服务启动失败，无法继续配置"
        exit 1
    fi

    # Configure APISIX
    local apisix_scripts=(
        "apisix-ai-gateway.sh"
        "apisix-casdoor.sh"
        "apisix-chatrag.sh"
        "apisix-codereview.sh"
        "apisix-completion-v2.sh"
        "apisix-costrict-apps.sh"
        "apisix-cotun.sh"
        "apisix-credit-manager.sh"
        "apisix-embedder.sh"
        "apisix-grafana.sh"
        "apisix-issue.sh"
        "apisix-oidc-auth.sh"
        #"apisix-quota-manager.sh"
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
    log "INFO" "Please login to the AI-GATEWAY backend [http://${COSTRICT_BACKEND}:${PORT_HIGRESS_CONTROL}] (default account: admin, password: test123), and add your LLM api-key in the Channels section! (If the page is blank, please wait as containers may take some time to start)"
}

main "$@"
