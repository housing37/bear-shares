#!/bin/bash

# ssh_alias="ssh_bear001"
# Define the SSH connection parameters
ssh_user="ubuntu"
# ssh_host="3.16.26.237"
# ssh_pem_key="~/.ssh/t2-micro-fivem-rebirth-test1.pem"
# ssh_host="18.226.17.71"
ssh_host="3.15.7.87"
ssh_pem_key="~/.ssh/t2-micro-bear001.pem"


# Define the local file path for the dump
# backup_dir="./src/_backups/db_backups"
backup_dir="./_backups"
dt=$(date +'%m%d%y_%H%M%S')
# backup_file="$backup_dir/avm_gms_serv_db_${dt}ET.sql"
backup_file="$backup_dir/the_matrix_db_${dt}ET.sql"

# SSH into the server and run the mysqldump command
ssh -i "$ssh_pem_key" "$ssh_user@$ssh_host" \
    "mysqldump -u house -p -h 127.0.0.1 --databases the_matrix --tables log_tg_user_at_changes log_tw_conf_urls shills user_blacklist_scammers user_earns user_shill_rates users" > "$backup_file"
    # "mysqldump -u house -p -h 127.0.0.1 --databases gms_serv --tables avm_logs avm_reasons" > "$backup_file"
    

# Check if the mysqldump command was successful
if [ $? -eq 0 ]; then
    echo "MySQL dump completed successfully. Output saved to: $backup_file"
else
    echo "Error: MySQL dump failed."
fi