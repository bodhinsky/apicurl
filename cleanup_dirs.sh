#!/bin/bash

# Check if a directory path is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <directory_path>"
    exit 1
fi

# Get today's date in the format YYYY-MM-DD
today=$(date +%Y-%m-%d)

# Change to the specified directory
cd "$1" || exit 1

# Check if a folder with today's date already exists
folder_counter=0
folder_name="$today"

while [ -d "$folder_name" ]; do
    folder_counter=$((folder_counter+1))
    folder_name="$today-$folder_counter"
done

# Create the folder
mkdir "$folder_name"

# Move files that don't start with "20*" into the folder
for file in *; do
    if ! [[ "$file" == 20* ]]; then
        mv "$file" "$folder_name/"
    fi
done
