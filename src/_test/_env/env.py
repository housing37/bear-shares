__fname = 'env'
__filename = __fname + '.py'
cStrDivider = '#================================================================#'
cStrDivider_1 = '#----------------------------------------------------------------#'
print('', cStrDivider, f'GO _ {__filename} -> starting IMPORTs & declaring globals', cStrDivider, sep='\n')
#============================================================================#
## log paths (should use same 'log' folder as access & error logs from nginx config)
#GLOBAL_PATH_DEV_LOGS = "/var/log/gasptires/dev.log"
#GLOBAL_PATH_ISE_LOGS = "/var/log/gasptires/ise.log"

GLOBAL_PATH_DEV_LOGS = "../logs/dev.log"
GLOBAL_PATH_ISE_LOGS = "../logs/ise.log"

#============================================================================#
## Misc smtp email requirements (eg_121019: inactive)
SES_SERVER = 'nil'
SES_PORT = 'nil'
SES_FROMADDR = 'nil'
SES_LOGIN = 'nil'
SES_PASSWORD = 'nil'

corp_admin_email = 'nil'
corp_recept_email = 'nil'
admin_email = 'nil'
post_receiver = 'nil'
post_receiver_2 = 'nil'

#============================================================================#
#============================================================================#
## .env support
import os
from read_env import read_env

try:
    #ref: https://github.com/sloria/read_env
    #ref: https://github.com/sloria/read_env/blob/master/read_env.py
    read_env() # recursively traverses up dir tree looking for '.env' file
except:
    print("#==========================#")
    print(" ERROR: no .env files found ")
    print("#==========================#")

# db support
dbHost = os.environ['DB_HOST']
dbName = os.environ['DB_DATABASE']
dbUser = os.environ['DB_USERNAME']
dbPw = os.environ['DB_PASSWORD']

# s3 support (use for remote server)
ACCESS_KEY = os.environ['ACCESS_KEY']
SECRET_KEY = os.environ['SECRET_KEY']

# twitter support @SolAudits
CONSUMER_KEY_0 = os.environ['CONSUMER_KEY_0']
CONSUMER_SECRET_0 = os.environ['CONSUMER_SECRET_0']
ACCESS_TOKEN_0 = os.environ['ACCESS_TOKEN_0']
ACCESS_TOKEN_SECRET_0 = os.environ['ACCESS_TOKEN_SECRET_0']

# twitter support @BearSharesNFT
CONSUMER_KEY_1 = os.environ['CONSUMER_KEY_1']
CONSUMER_SECRET_1 = os.environ['CONSUMER_SECRET_1']
ACCESS_TOKEN_1 = os.environ['ACCESS_TOKEN_1']
ACCESS_TOKEN_SECRET_1 = os.environ['ACCESS_TOKEN_SECRET_1']

# openAI
OPENAI_KEY = os.environ['OPENAI_KEY']

# telegram
TOKEN_dev = os.environ['TG_TOKEN_DEV'] # PTPTestBot @ptp_test_bot (dev)
TOKEN_prod = os.environ['TG_TOKEN_PROD'] # (prod)


#============================================================================#

