#!/bin/bash

source ./.env
#
# 包管理系统的目录结构：
#
#-/-+-<package>/-+-<os>/-+-<arch>/-+-<ver>/-+-package.json: 对包数据文件进行签名保护
#   |            |       |         |        +-<package-data-file>
#   |            |       |         +-platform.json: 某个平台支持哪些版本
#   |            |       +-amd64-...
#   |            +-windows-...
#   |            +-platforms.json: 某个包支持哪些平台(OS&芯片架构)
#   +-packages.json: 系统有哪些包可以下载
#

usage() {
    echo "Usage: build-packages.sh [-p PACKAGE] [-k KEY_FILE] [--clean] [--build] [--pack] [--index] [--upload] [--all]"
    echo "Options:"
    echo "  -p, --package        Package name (optional, if not specified, will process all packages)"
    echo "  -k, --key            Private key file (default: costrict-private.pem)"
    echo "  --clean              Need clean first"
    echo "  --build              Need build packages"
    echo "  --pack               Need pack packages"
    echo "  --index              Need index packages"
    echo "  --all                Execute all steps except for 'upload' (clean, build, pack, index)"
    echo "  --upload             Need upload packages"
    echo "  --upload-to <env>    Upload package to <env>, env: def, all, prod, test, qianliu"
    echo "  -h, --help           Help information"
    exit 1
}

enable_upload() {
    case "$1" in
        def) need_upload=true; upload_prod=true; upload_test=true; upload_qianliu=false;;
        all) need_upload=true; upload_prod=true; upload_test=true; upload_qianliu=true;;
        prod) need_upload=true; upload_prod=true;;
        test) need_upload=true; upload_test=true;;
        qianliu) need_upload=true; upload_qianliu=true;;
        *) usage;;
    esac
}
# 默认私钥文件
key_file="costrict-private.pem"

# 默认参数值
need_clean=false
need_build=false
need_pack=false
need_index=false
need_upload=false
upload_prod=false
upload_test=false
upload_qianliu=false

# Parse command line options
args=$(getopt -o hp:k: --long help,package:,key:,clean,build,pack,index,all,upload,upload-to: -n 'build-packages.sh' -- "$@")
[ $? -ne 0 ] && usage

eval set -- "$args"

while true; do
    case "$1" in
        -p|--package) package="$2"; shift 2;;
        -k|--key) key_file="$2"; shift 2;;
        --clean) need_clean=true; shift;;
        --build) need_build=true; shift;;
        --pack) need_pack=true; shift;;
        --index) need_index=true; shift;;
        --all) need_clean=true; need_build=true; need_pack=true; need_index=true; shift;;
        --upload) enable_upload "def"; shift;;
        --upload-to) enable_upload "$2"; shift 2;;
        -h|--help) usage; exit 0;;
        --) shift; break;;
        *) usage;;
    esac
done

# Function to build a package for multiple platforms
build_app() {
    local package_name="$1"
    local version="$2"
    local path="$3"
    
    echo "Starting multi-platform build for package: $package_name, version: $version"
    echo ""
    
    # 获取当前路径的绝对路径
    local current_dir=$(pwd)
    echo "Current directory: $current_dir"
    
    # 使用传入的path参数作为目标路径
    local target_dir="$current_dir/$path"
    echo "Target directory: $target_dir"
    
    # 检查目标路径是否存在
    if [ ! -d "$target_dir" ]; then
        echo "Error: Target directory $target_dir does not exist!"
        exit 1
    fi
    
    # Supported platforms and architectures
    PLATFORMS=("linux" "windows" "darwin")
    ARCHITECTURES=("amd64" "arm64")
    
    # Build all combinations
    for os in "${PLATFORMS[@]}"; do
        for arch in "${ARCHITECTURES[@]}"; do
            echo "==== Building $package_name for $os/$arch ===="
            
            # 创建输出目录
            local output_dir="$current_dir/$package_name/$os/$arch/$version"
            mkdir -p "$output_dir"
            
            # 设置输出文件名
            local output_file="$package_name"
            if [ "$os" = "windows" ]; then
                output_file="$output_file.exe"
            fi
            
            # 完整输出路径
            local output_target="$output_dir/$output_file"
            
            echo "Output target: $output_target"
            
            # 到目标路径执行build.py
            (cd "$target_dir" && python ./build.py --software "$version" --os "$os" --arch "$arch" --output "$output_target")
            if [ $? -ne 0 ]; then
                echo "Build failed for $package_name on $os/$arch"
                exit 1
            fi
            echo ""
        done
    done
    
    echo "All builds completed successfully for package: $package_name"
}

# Function to build configuration package directories
build_conf() {
    local package_name="$1"
    local version="$2"
    local path="$3"
    local target="$4"
    
    echo "Starting configuration build for package: $package_name, version: $version"
    echo ""
    
    # 获取当前路径的绝对路径
    local current_dir=$(pwd)
    echo "Current directory: $current_dir"
    
    # 使用传入的path参数作为源路径
    local source_dir="$current_dir/$path"
    echo "Source directory: $source_dir"
    
    # 检查源路径是否存在
    if [ ! -d "$source_dir" ]; then
        echo "Error: Source directory $source_dir does not exist!"
        exit 1
    fi
    
    # Supported platforms and architectures
    PLATFORMS=("linux" "windows" "darwin")
    ARCHITECTURES=("amd64" "arm64")
    
    # 复制所有平台的配置文件
    for os in "${PLATFORMS[@]}"; do
        for arch in "${ARCHITECTURES[@]}"; do
            echo "==== Building $package_name for $os/$arch ===="
            
            # 创建输出目录
            local output_dir="$current_dir/$package_name/$os/$arch/$version"
            mkdir -p "$output_dir"
            
            # 源文件路径
            local source_file="$source_dir/$os/$arch/$target"
            
            # 目标文件路径
            local target_file="$output_dir/$target"
            
            echo "Source file: $source_file"
            echo "Target file: $target_file"
            
            # 检查源文件是否存在
            if [ ! -f "$source_file" ]; then
                echo "Warning: Source file $source_file does not exist, skipping..."
                continue
            fi
            
            # 复制文件
            cp "$source_file" "$target_file"
            if [ $? -ne 0 ]; then
                echo "Error: Failed to copy $source_file to $target_file"
                exit 1
            fi
            
            echo "Successfully copied $source_file to $target_file"
            echo ""
        done
    done
    
    echo "All configuration builds completed successfully for package: $package_name"
}

build_package() {
    local package="$1"
    
    # 从package-versions.json中获取指定包的版本号和路径
    local package_version=$(jq -r ".packages[] | select(.name == \"${package}\") | .version" package-defs.json)
    local package_path=$(jq -r ".packages[] | select(.name == \"${package}\") | .path" package-defs.json)
    local package_type=$(jq -r ".packages[] | select(.name == \"${package}\") | .type" package-defs.json)

    if [ -z "$package_path" ] || [ "$package_path" = "null" ]; then
        echo "Skipping build step for ${package}..."
        return
    fi

    if [ -z "$package_version" ] || [ "$package_version" = "null" ]; then
        echo "Error: Version not found for package '${package}' in package-defs.json!"
        exit 1
    fi

    if [ -z "$package_type" ] || [ "$package_type" = "null" ]; then
        echo "Error: 'type' not found for package '${package}' in package-defs.json!"
        exit 1
    fi
    
    echo "=============================================="
    echo "Building package: $package, version: $package_version, path: $package_path"
    echo "=============================================="
    if [ "exec" == "$package_type" ]; then
        build_app "${package}" "${package_version}" "${package_path}"
    else
        local package_target=$(jq -r ".packages[] | select(.name == \"${package}\") | .target" package-defs.json)

        if [ -z "$package_target" ] || [ "$package_target" = "null" ]; then
            echo "Error: 'target' not found for package '${package}' in package-defs.json!"
            exit 1
        fi
        build_conf "${package}" "${package_version}" "${package_path}" "${package_target}"
    fi
}

# Function to build multiple packages
build_packages() {
    local version="$1"

    # 从package-versions.json读取包信息
    echo "Reading package information from package-defs.json..."
    
    # 使用jq解析JSON
    local packages_json=$(cat package-defs.json)
    local package_count=$(echo "$packages_json" | jq '.packages | length')
    
    echo "Found $package_count packages to build"
    echo ""

    # 遍历每个包
    for ((i=0; i<package_count; i++)); do
        local package_name=$(echo "$packages_json" | jq -r ".packages[$i].name")

        build_package "${package_name}"
        echo ""
    done
    
    echo "All packages built successfully!"
}

# Function to get package type from package-defs.json
get_package_type() {
    local package_name=$1

    local package_type=$(jq -r ".packages[] | select(.name == \"${package_name}\") | .type // empty" package-defs.json)
    if [ -z "$package_type" ] || [ "$package_type" = "null" ]; then
        echo "exec"
    else
        echo "$package_type"
    fi
}

# Function to get package description from package-defs.json
get_package_description() {
    local package_name=$1

    local package_description=$(jq -r ".packages[] | select(.name == \"${package_name}\") | .description // empty" package-defs.json)
    if [ -z "$package_description" ] || [ "$package_description" = "null" ]; then
        echo "No description information"
    else
        echo "$package_description"
    fi
}

get_package_filename() {
    local package_name=$1

    local package_filename=$(jq -r ".packages[] | select(.name == \"${package_name}\") | .filename // empty" package-defs.json)
    if [ -z "$package_filename" ] || [ "$package_filename" = "null" ]; then
        echo ""
    else
        echo "$package_filename"
    fi
}

pack_package() {
    local package=$1
    local os=$2
    local arch=$3
    local ver=$4
    local file=$5
    local type=$6
    local description="$7"
    local filename="$8"
    
    echo "smc package build ${package} -f ${file} -k ${key_file} --os ${os} --arch ${arch} --version ${ver} --type ${type} --filename ${filename} --description ${description}"
    smc package build ${package} -f ${file} -k ${key_file} --os ${os} --arch ${arch} --version ${ver} --type ${type} --filename "${filename}" --description "${description}"
}

pack_dir_packages() {
    local package_dir=$1
    
    # 提取路径信息，先去掉末尾多余的/，再去掉开头多余的./
    local clean_packages=${package_dir%/}
    local clean_packages=${clean_packages#./}
    local path_parts=(${clean_packages//\// })
    
    # 检查路径是否包含足够的部分
    if [ ${#path_parts[@]} -ne 4 ]; then
        echo "Internal Error: invalid directory: ${package_dir}"
        return 0
    fi
    
    # 从路径第一节获取包名
    local pkg_name=${path_parts[0]}
    local os=${path_parts[1]}
    local arch=${path_parts[2]}
    local ver=${path_parts[3]}
    
    echo "Processing: ${pkg_name}/${os}/${arch}/${ver} ..."
    
    local pkg_type=$(get_package_type "${pkg_name}")
    local pkg_description=$(get_package_description "${pkg_name}")
    local pkg_filename=$(get_package_filename "${pkg_name}")
    
    # 查找目录中非package.json的文件
    for file in "${package_dir}"*; do
        [ -f "${file}" ] || continue
        [ "$(basename "${file}")" = "package.json" ] && continue
        pack_package "${pkg_name}" "${os}" "${arch}" "${ver}" "${file}" "${pkg_type}" "${pkg_description}" "${pkg_filename}"
    done
}

index_packages() {
    local dir=$1
    
    echo "smc package index -b ${dir}"
    smc package index -b "${dir}"
}

# Function to clean up old version directories for a package
cleanup_old_versions() {
    local package_name="$1"
        
    # 从package-versions.json中获取指定包的版本号
    local target_version=$(jq -r ".packages[] | select(.name == \"${package_name}\") | .version" package-defs.json)
    local target_path=$(jq -r ".packages[] | select(.name == \"${package_name}\") | .path" package-defs.json)
    
    if [ -z "$target_version" ] || [ "$target_version" = "null" ]; then
        echo "Skipping clean step for package '${package_name}'..."
       return 0
    fi
    if [ -z "$target_path" ] || [ "$target_path" = "null" ]; then
        echo "Skipping clean step for package '${package_name}'..."
       return 0
    fi
    
    echo "Cleaning up old versions for package: $package_name, keeping version: $target_version"
    
    # 检查包目录是否存在
    if [ ! -d "${package_name}" ]; then
        echo "Warning: Package directory '${package_name}' not found, skipping clean."
        return 0
    fi
    
    # 遍历所有平台和架构目录
    for os_dir in "${package_name}"/*/; do
        [ -d "${os_dir}" ] || continue
        
        local os=$(basename "${os_dir}")
        
        for arch_dir in "${os_dir}"*/; do
            [ -d "${arch_dir}" ] || continue
            
            local arch=$(basename "${arch_dir}")
            
            # 遍历所有版本目录
            for version_dir in "${arch_dir}"*/; do
                [ -d "${version_dir}" ] || continue
                
                local version=$(basename "${version_dir}")
                
                # 如果不是目标版本，则删除
                if [ "$version" != "$target_version" ]; then
                    echo "Removing old version: ${package_name}/${os}/${arch}/${version}"
                    rm -rf "${version_dir}"
                    if [ $? -eq 0 ]; then
                        echo "Successfully removed: ${version_dir}"
                    else
                        echo "Error: Failed to remove ${version_dir}"
                    fi
                else
                    echo "Keeping target version: ${package_name}/${os}/${arch}/${version}"
                fi
            done
        done
    done
    
    echo "Cleanup completed for package: $package_name"
}

# Function to clean up old versions for all packages
cleanup_all_old_versions() {
    # 从package-versions.json读取包信息
    echo "Reading package information from package-defs.json for clean..."
    
    # 使用jq解析JSON
    local packages_json=$(cat package-defs.json)
    local package_count=$(echo "$packages_json" | jq '.packages | length')
    
    echo "Found $package_count packages to clean"
    echo ""
    
    # 遍历每个包
    for ((i=0; i<package_count; i++)); do
        local package_name=$(echo "$packages_json" | jq -r ".packages[$i].name")
        
        echo "=============================================="
        echo "Cleaning up package: $package_name"
        echo "=============================================="
        cleanup_old_versions "$package_name"
        if [ $? -ne 0 ]; then
            echo "Cleanup failed for package: $package_name"
            exit 1
        fi
        echo ""
    done
    
    echo "All packages clean completed!"
}

upload_package() {
    local package=$1
    local ip=$2
    local port=$3
    local rootDir=$4

    local formalDir="${rootDir}/costrict"
    local uploadDir="${rootDir}/costrict-upload"

    echo rsync -avzP -e "ssh -p ${port}" ${package} "root@${ip}:${uploadDir}/"
    rsync -avzP -e "ssh -p ${port}" ${package} "root@${ip}:${uploadDir}/"

    ssh -p "${port}" "root@${ip}" <<EOF
        set -e
        echo "Transfer ${package} to formal directory..."
        if [ -d "${formalDir}/${package}" ]; then
            mv "${formalDir}/${package}" "${uploadDir}/${package}-tmp"
        fi
        mv "${uploadDir}/${package}" "${formalDir}/${package}"
        if [ -d "${uploadDir}/${package}-tmp" ]; then
            mv "${uploadDir}/${package}-tmp" "${uploadDir}/${package}"
        fi
EOF
}

upload_package_clouds() {
    local package=$1

    if [ "$upload_test" = true ]; then
        echo "=============================================="
        echo "Upload package $package to ${test_host}..."
        echo "=============================================="
        upload_package "${package}" "${test_host}" "${test_port}" "${test_path}"
    fi

    if [ "$upload_prod" = true ]; then
        echo "=============================================="
        echo "Upload package $package to ${prod_host}..."
        echo "=============================================="
        upload_package "${package}" "${prod_host}" "${prod_port}" "${prod_path}"
    fi

    if [ "$upload_qianliu" = true ]; then
        echo "=============================================="
        echo "Upload package $package to ${qianliu_host}..."
        echo "=============================================="
        upload_package "${package}" "${qianliu_host}" "${qianliu_port}" "${qianliu_path}"
    fi
}

if [ "$need_clean" = true ] || [ "$need_build" = true ] || [ "$need_pack" = true ]; then
    # 检查jq工具是否可用
    if ! command -v jq >/dev/null 2>&1; then
        echo "Error: jq command not found! Please install jq to parse JSON files."
        echo "Installation instructions:"
        echo "  Ubuntu/Debian: sudo apt-get install jq"
        echo "  CentOS/RHEL: sudo yum install jq"
        echo "  macOS: brew install jq"
        echo "  Windows: Download from https://stedolan.github.io/jq/download/"
        exit 1
    fi
    # 检查是否有模块定义文件package-defs.json
    if [ ! -f "package-defs.json" ]; then
        echo "Error: package-defs.json file not found!"
        exit 1
    fi
fi

if [ -z "$package" ]; then
    # 处理所有包
    if [ "$need_clean" = true ]; then
        echo "Cleaning up old versions for all packages..."
        cleanup_all_old_versions
    else
        echo "Skipping clean step for all packages..."
    fi

    if [ "$need_build" = true ]; then
        echo "building application for all packages..."
        build_packages
    else
        echo "Skipping build step for all packages..."
    fi

    if [ "$need_pack" = true ]; then
        echo "Building package.json for all packages..."
        # 检查私钥文件是否存在
        if [ ! -f "${key_file}" ]; then
            echo "Error: Private key file '${key_file}' not found!"
            exit 1
        fi
        for package_dir in */*/*/*/; do
            [ -d "${package_dir}" ] || continue
            pack_dir_packages "${package_dir}"
        done
    else
        echo "Skipping package step for all packages..."
    fi
    
    if [ "$need_index" = true ]; then
        echo "Building index for all packages..."
        index_packages .
    else
        echo "Skipping index step for all packages..."
    fi

    if [ "$need_upload" = true ]; then
        echo "Uploading all packages..."
        for package_dir in */; do
            package=${package_dir%/}
            [ -d "${package_dir}" ] || continue
            [ ! -f "${package_dir}platforms.json" ] && continue
            upload_package_clouds "${package}"
        done
    else
        echo "Skipping upload step for all packages..."
    fi
else
    # 处理指定包
    mkdir -p "${package}"
    # [ -d "${package}" ] || { echo "Error: Package directory '${package}' not found!"; exit 1; }

    if [ "$need_clean" = true ]; then
        echo "Cleaning up old versions for package: $package"
        cleanup_old_versions "$package"
    else
        echo "Skipping clean step for ${package}..."
    fi

    if [ "$need_build" = true ]; then
        echo "Building target for ${package}..."
        build_package "${package}"
    else
        echo "Skipping build step for ${package}..."
    fi

    if [ "$need_pack" = true ]; then
        echo "Building package.json for ${package}..."
        # 检查私钥文件是否存在
        if [ ! -f "${key_file}" ]; then
            echo "Error: Private key file '${key_file}' not found!"
            exit 1
        fi
        for package_dir in "${package}"/*/*/*/; do
            [ -d "${package_dir}" ] || continue
            pack_dir_packages "${package_dir}"
        done
    else
        echo "Skipping package step for ${package}..."
    fi

    if [ "$need_index" = true ]; then
        echo "Building index for ${package}..."
        index_packages "${package}"
    else
        echo "Skipping index step for ${package}..."
    fi

    if [ "$need_upload" = true ]; then
        echo "Uploading package: $package"
        upload_package_clouds "${package}"
    else
        echo "Skipping upload step for ${package}..."
    fi
fi


echo "Build completed."
