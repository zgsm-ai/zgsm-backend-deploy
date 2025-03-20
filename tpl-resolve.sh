#!/bin/sh

function usage() {
    echo "tpl-resolve.sh [-f input-filename] [-o output-filename] [-h]"
    echo "  input-filename: Input filename, if not specified, all .yaml,.yml,.conf files in the current directory, including subdirectories, will be processed"
    echo "  output-filename: Output filename, if not specified, the input file will be modified directly"
    echo "tpl-resolve.sh reads configuration items from the configure.sh file"
    echo "  Replaces variable definitions enclosed in {{ and }} like {{varname}} with the value of the variable varname"
}

while getopts "f:o:h" opt
do
    case $opt in
        f)
        input=$OPTARG;;
        o)
        output=$OPTARG;;
        h)
        usage
        exit 0;;
        ?)
        usage
        exit 1;;
    esac
done

. ./configure.sh

#
# Processes variable markers in a .tpl file, resolving variable values to actual values
# @param input_file Input file
# @param output_file Output file
#
function resolve_file() {
    input_file=$1
    output_file=$2
    cp -f "$input_file" "$output_file"
    echo generate $input_file to $output_file ...

    # Query all {{variables}} and replace their values
    for i in `grep -o -w -E "\{\{([[:alnum:]]|\.|_)*\}\}" $output_file|sort|uniq|tr -d '\r'`; do
        # Extract key name
        key=${i:2:(${#i}-4)}
        # Get key value: Search file content
        value=$(eval echo \$$key)
        echo "$key=>$value"
        # Replace file content
        if echo "$value" | grep -vq '#'; then
            sed -i "s#$i#$value#g" "$output_file";
        elif echo "$value" | grep -vq '/'; then
            sed -i "s/$i/$value/g" "$output_file";
        elif echo "$value" | grep -vq ','; then
            sed -i "s,$i,$value,g" "$output_file";
        else
            echo "The $value contains special characters "#/," at the same time, and the replacement cannot be performed"
        fi
    done
}

#
#   Processes all .tpl files in a directory
#   @param dir Directory path
#
function resolve_dir() {
    dir="$1"
    echo generate $dir ...

    for entry in "$dir"/*; do
        if [ -d "$entry" ]; then
            # If it is a directory, call recursively
            resolve_dir "$entry"
        elif [ -f "$entry" ] && [[ "$entry" == *.tpl ]]; then
            # If it is a .tpl file, remove the suffix and output the filename
            filename="${entry%.tpl}"  # Remove the .tpl suffix
            # Output the filename without the suffix
            resolve_file "$entry" "$filename"
        fi
    done
}

if [ ""X == "$output"X ]; then
    output="$input"
fi

if [ X"" == X"$input" ]; then
    resolve_dir .
else
    resolve_file $input $output
    cat $output
fi
