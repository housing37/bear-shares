#!/bin/bash

# ssh_alias="ssh_bear001"
# Define the SSH connection parameters
ssh_user="ubuntu"
ssh_host="18.226.17.71"
ssh_pem_key="~/.ssh/t2-micro-bear001.pem"

# Define the local file path for the dump
backup_dir="../database/_backups"
dt=$(date +'%m%d%H_%H%M')
backup_file="$backup_dir/the_matrix_db_${dt}ET.sql"

# SSH into the server and run the mysqldump command
ssh -i "$ssh_pem_key" "$ssh_user@$ssh_host" \
    "mysqldump -u house -p -h 127.0.0.1 --databases the_matrix" > "$backup_file"

# Check if the mysqldump command was successful
if [ $? -eq 0 ]; then
    echo "MySQL dump completed successfully. Output saved to: $backup_file"
else
    echo "Error: MySQL dump failed."
fi