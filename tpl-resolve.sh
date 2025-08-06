#!/bin/sh

function usage() {
    echo "tpl-resolve.sh [-f input-filename] [-o output-filename] [-h]"
    echo "  input-filename: Input filename, if not specified, process all .yaml, .yml, .conf files in the current directory, including subdirectories"
    echo "  output-filename: Output filename, if not specified, directly modify the input file"
    echo "tpl-resolve.sh reads configuration items from configure.sh"
    echo "  Variables defined in {{varname}} will be replaced with the value of the variable varname"
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
. ./scripts/newest-images.list
#
# Process variable markers in a .tpl file, resolve variables to actual values
# @param input_file Input file
# @param output_file Output file
#
function resolve_file() {
    input_file=$1
    output_file=$2
    cp -f "$input_file" "$output_file"
    echo generate $input_file to $output_file ...

    # Find all {{variables}} and replace with values
    for i in `grep -o -w -E "\{\{([[:alnum:]]|\.|_)*\}\}" $output_file|sort|uniq|tr -d '\r'`; do
        # Extract key name
        key=${i:2:(${#i}-4)}
        # Get key value: search file content
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
            echo "The value $value contains special characters \"#/,\" simultaneously, unable to perform replacement"
        fi
    done
}

#
#   Process all .tpl files in a directory
#   @param dir Directory path
#
function resolve_dir() {
    dir="$1"
    echo generate $dir ...

    for entry in "$dir"/*; do
        if [ -d "$entry" ]; then
            # If it's a directory, call recursively
            resolve_dir "$entry"
        elif [ -f "$entry" ] && [[ "$entry" == *.tpl ]]; then
            # If it's a .tpl file, remove the extension and output the filename
            filename="${entry%.tpl}"  # Remove .tpl extension
            # Output the filename without the extension
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
