#!/bin/bash

JSON_FILE=$1

# Function to create directories based on JSON
create_directories() {
  echo "Creating directories..."
  providers=$(jq -c '.providers[]' "$JSON_FILE")
  for provider in $providers; do
    provider_name=$(echo "$provider" | jq -r '.name')
    models=$(echo "$provider" | jq -r '.models[]')

    # Create provider directory
    provider_dir="providers/$provider_name"
    if [ ! -d "$provider_dir" ]; then
      mkdir -p "$provider_dir"
      echo "Created directory: $provider_dir"
    else
      echo "Directory already exists: $provider_dir"
    fi

    # Create model directories
    for model in $models; do
      model_dir="$provider_dir/$model"
      if [ ! -d "$model_dir" ]; then
        mkdir -p "$model_dir"
        echo "Created directory: $model_dir"
      else
        echo "Directory already exists: $model_dir"
      fi
    done
  done
}

# Function to create a backup of a specified folder
create_backup() {
  local source_folder=$1
  local backup_folder=$2
  local timestamp=$(date +"%Y%m%d%H%M%S")

  # Check if source folder exists
  if [ ! -d "$source_folder" ]; then
    echo "Source folder $source_folder does not exist."
    return 1
  fi

  # Create backup folder if it does not exist
  mkdir -p "$backup_folder"

  # Create the backup
  local backup_name=$(basename "$source_folder")
  local backup_path="$backup_folder/${backup_name}_backup_$timestamp"

  cp -r "$source_folder" "$backup_path"

  if [ $? -eq 0 ]; then
    echo "Backup of $source_folder created at $backup_path"
  else
    echo "Failed to create backup."
    return 1
  fi
}

create_backup "src" "backups/src-backup"
create_backup "tests" "backups/tests-backup"
create_directories