#!/bin/sh

# retry function attempts to execute a command until one of the following conditions is met:
#   1. Command executes successfully (returns exit code 0)
#   2. Command output contains any specified keyword
#   3. Preset timeout is reached
#
# Parameters:
#   $1: cmd          Command string to execute
#   $2: timeout      Maximum timeout in seconds
#   $3: interval     Retry interval in seconds
#   $@: keywords     Optional keyword list (starting from 4th parameter)
#
# Return values:
#   0: Success or keyword condition met
#   1: Timeout failure
#
# Features:
#   - Real-time command output
#   - Automatic handling of stdout/stderr
#   - Supports keyword-based success detection for non-zero exit codes
#   - Second-level timeout precision
#
retry() {
    local cmd="$1"
    local timeout="$2"
    local interval="$3"
    shift 3
    local keywords=("$@")

    local start_time=$(date +%s)
    local end_time=$((start_time + timeout))

    while true; do
        # Check timeout
        if [ $(date +%s) -ge $end_time ]; then
            echo "error: Command $cmd execution timed out"
            return 1
        fi

        # Execute command and capture output/status
        output=$(eval "$cmd" 2>&1)
        status=$?
        echo "$output"

        # Check command success
        if [ $status -eq 0 ]; then
            return 0
        fi

        # Check keyword matches
        for keyword in "${keywords[@]}"; do
            if [[ $output == *"$keyword"* ]]; then
                echo "Command $cmd failed but contains keyword '$keyword', considered successful"
                return 0
            fi
        done

        # Retry wait
        echo "Command $cmd failed, retrying later... (Status code: $status)"
        sleep "$interval"
    done
}

# fatal prints error message and exits
fatal() {
    echo "Error: $1" >&2
    exit 1
}
