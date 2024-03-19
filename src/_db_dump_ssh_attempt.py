# house_031824: attempting db backups through my sql withh ssh tunneling
#   could not get this working still
#   this work follows in the following source file attempts ...
#       _db_dump_ssh_attempt.py
#       _db_controller_ssh_attempt.py

__fname = '_db_dump_ssh_attempt'
__filename = __fname + '.py'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'GO _ {__filename} -> starting IMPORTs & declaring globals', cStrDivider, sep='\n')

from _env import env
from datetime import datetime
from db_controller import *


# SSH connection details
# ssh_host = '18.226.17.71' # db server to ssh into
ssh_host = env.dbHost_prod
ssh_user = 'ubuntu' # server user name to login with
# ssh_pem_path = '/Users/greenhouse/.ssh/t2-micro-fivem-rebirth-test1.pem'  # path to .pem key file
# ssh_pem_path = '~/.ssh/t2-micro-bear001.pem'  # path to .pem key file
ssh_pem_path = '/Users/greenhouse/.ssh/t2-micro-bear001.pem'  # path to .pem key file

_ssh = {'host':ssh_host, 'user':ssh_user, 'path':ssh_pem_path}

# db dump details
dt = datetime.now().strftime('%m%d%H_%H%M') # format ex: 010624_1930
# tables = 'avm_logs avm_reasons'
tables = 'users'
fpath = f'./_backups/db_backups/the_matrix_db_{dt}ET.sql'
# exeMySqlDump(tables, fpath, use_remote=True) # db_controller.py

cli_command = 'pwd'
cli_command = 'whoami'
cli_command = 'mysql -u house'
# cli_command = 'mysqldump -u house -h 127.0.0.1 --databases the_matrix --tables users'
# cli_command = '/usr/bin/mariadb-dump -u house -h 127.0.0.1 --databases the_matrix --tables users -p'
# cli_command = 'mariadb-dump -u house -h 127.0.0.1 --databases the_matrix --tables users -p'
from sshtunnel import SSHTunnelForwarder
import os
mypkey = paramiko.RSAKey.from_private_key_file(_ssh['path'])
with SSHTunnelForwarder(
        ('18.226.17.71', 22),
        ssh_username=ssh_user,
        ssh_pkey=mypkey,
        remote_bind_address=(env.dbHost, 3306)) as tunnel:
            print("Command Input:", cli_command)
            os.system(cli_command)
            # result = subprocess.run('sudo su', shell=True, capture_output=True, text=True)
            # result = subprocess.run(cli_command, shell=True, capture_output=True, text=True, executable="/bin/bash")
            # result = subprocess.run(cli_command, shell=True, capture_output=True, executable="/bin/bash")
            # print("Command Output:", result.stdout)
            # print("Command Error:", result.stderr)
            # exeMySqlDump(tables, fpath, use_remote=True, use_ssh=True, ssh_dict=_ssh, tunnel_port=tunnel.local_bind_port) # db_controller.py
            # exeMySqlDump(tables, fpath, use_remote=True, use_ssh=True, ssh_dict=_ssh, tunnel_port=3306) # db_controller.py
            # exeMySqlDump(tables, fpath, use_remote=False) # db_controller.py

# note_010524: not working yet
# exeMySqlDump(table, fpath, use_remote=True, over_ssh=True, ssh_dict=_ssh) # db_controller.py

print('', cStrDivider, f'# END _ {__filename}', cStrDivider, sep='\n')
