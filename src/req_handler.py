__fname = 'req_handler'
__filename = __fname + '.py'
cStrDivider = '#================================================================#'
cStrDivider_1 = '#----------------------------------------------------------------#'
print('', cStrDivider, f'GO _ {__filename} -> starting IMPORTs & declaring globals', cStrDivider, sep='\n')

#=====================================================#
#         imports                                     #
#=====================================================#
from _env import env
import _web3 # from web3 import Account, Web3, HTTPProvider
import _abi
import _bst_keeper
from db_controller import *
from req_helpers import *
from datetime import datetime
import json, time
from ethereum.abi import encode_abi, decode_abi # pip install ethereum

# twitter support
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
    # ref: https://stackoverflow.com/a/53073789
    # ref: https://googlechromelabs.github.io/chrome-for-testing/#stable
    # $ wget https://storage.googleapis.com/chrome-for-testing-public/122.0.6261.128/linux64/chromedriver-linux64.zip
    # $ unzip chromedriver_linux64.zip
    # $ cd chromedriver_linux64
    # $ sudo rm /usr/bin/chromedriver
    # $ sudo mv chromedriver /usr/bin
    # $ chromedriver --version

#=====================================================#
#         global static keys                          #
#=====================================================#
kPin = 'admin_pin'
kUserId = "user_id"
kKeyVals = "key_vals"

VERBOSE_LOG = False
WEB_DRIVER_WAIT_SEC = 30 # num sec to wait for html render
WEB_DRIVER_WAIT_CNT = 6 # num of tries to wait and find 'X:' in each html rendered
WEB_DRIVE_WAIT_SLEEP_SEC = 0.1 # sleep sec before next web driver wait attempt
LST_IGNORE_TWITTER_AT = ['BearSharesX']

# twitter access globals
CONSUMER_KEY = 'nil_tw_key'
CONSUMER_SECRET = 'nil_tw_key'
ACCESS_TOKEN = 'nil_tw_key'
ACCESS_TOKEN_SECRET = 'nil_tw_key'

#=====================================================#
#         TG cmd / request handler static keys        #
#=====================================================#
#-----------------------------------------------------#
# TRINITY _  'Edit Commands' (TG: @BotFather)
#-----------------------------------------------------#
# trinity - show help info
# trinity_help - show help info
# trinity_register_as_shiller - <wallet_address> <tweet_url>
# trinity_confirm_twitter - <tweet_url>
# trinity_submit_shill - <tweet_url>
# trinity_request_cashout - no_params
# trinity_show_my_rates - no_params
# trinity_show_my_earnings - no_params
# trinity_set_wallet - <wallet_address>
# admin_show_user_rates - <tg_user_at>
# admin_show_user_earnings - <tg_user_at>
# admin_show_user_shills - <tg_user_at>
# admin_list_all_pend_shills - no_params
# admin_approve_pend_shill - <tg_user_at> <shill_id>
# admin_view_shill_status - <tg_user_at> <shill_id> <shill_url>
# admin_pay_shill_rewards - <tg_user_at>
# admin_log_removed_shill - <tg_user_at> <shill_id>
# admin_scan_web_for_dead_shills - pending
# admin_set_shiller_rates - pending

# LEFT OFF HERE .... 031424
# TODO: i don’t think admins can view shills the are NOT pending and NOT removed (in order to review and update is_approved=TRUE to is_removed=TRUE)
	# - however, this may be what ‘/admin_scan_web_for_dead_shills’ is for

#-----------------------------------------------------#
#   TRINITY
#-----------------------------------------------------#
# '/trinity_register_as_shiller'
kSHILLER_REG = "trinity_register_as_shiller"
LST_CMD_REG_USER = ['<wallet_address>', '<tweet_url>']
STR_ERR_REG_USER = f'Please tweet "@BearSharesX #Trinity register" 👍️️️️️️\n Then use that link to register with cmd:\n /{kSHILLER_REG} {" ".join(LST_CMD_REG_USER)}'
LST_KEYS_REG_USER_RESP = env.LST_KEYS_PLACEHOLDER
DB_PROC_ADD_NEW_USER = 'ADD_NEW_TG_USER'
LST_KEYS_REG_USER = ['user_id','user_at','user_handle','wallet_address','trinity_tw_url']
# LST_KEYS_REG_USER = ['user_id','user_at','user_handle','wallet_address','trinity_tw_url','trinity_tw_id','tw_user_at']
    # PRE-DB: validate 'trinity_tw_url' contains texts '@BearSharesX' & 'trinity'

# '/trinity_confirm_twitter'
kTWITTER_CONF = "trinity_confirm_twitter"
LST_CMD_TW_CONF = ['<tweet_url>']
STR_ERR_TW_CONF = f'To keep your registration up-to-date, please tweet "@BearSharesX #Trinity register" once a week 👍️️️️️️\n Then use that link to confirm your twitter with cmd:\n /{kTWITTER_CONF} {" ".join(LST_CMD_TW_CONF)}'
LST_KEYS_TW_CONF_RESP = env.LST_KEYS_PLACEHOLDER
DB_PROC_RENEW_TW_CONFRIM = 'UPDATE_TWITTER_CONF'
LST_KEYS_TW_CONF = ['user_id','user_at','trinity_tw_url']
# LST_KEYS_TW_CONF = ['user_id','user_at','trinity_tw_url','trinity_tw_id','tw_user_at']
    # PRE-DB: validate 'trinity_tw_url' contains texts '@BearSharesX' & 'trinity'

# '/trinity_submit_shill'
kSUBMIT_SHILL = "trinity_submit_shill"
LST_CMD_SUBMIT_SHILL = ['<tweet_url>']
STR_ERR_SUBMIT_SHILL = f'Please submit your shill using the cmd:\n /{kSUBMIT_SHILL} {" ".join(LST_CMD_SUBMIT_SHILL)}\n tweets must at least contain "@BearSharesX" to be credited'
LST_KEYS_SUBMIT_SHILL_RESP = env.LST_KEYS_PLACEHOLDER
DB_PROC_ADD_SHILL = 'ADD_USER_SHILL_TW'
LST_KEYS_SUBMIT_SHILL = ['user_id','user_at','post_url']
# LST_KEYS_SUBMIT_SHILL = ['user_id','user_at','post_url','post_id']

# '/trinity_request_cashout'
kREQUEST_CASHOUT = "trinity_request_cashout"
LST_CMD_REQUEST_CASHOUT = [] # ['<tg_user_at>']
STR_ERR_REQUEST_CASHOUT = f'nil_err_response_tg'
LST_KEYS_REQUEST_CASHOUT_RESP = env.LST_KEYS_PLACEHOLDER
DB_PROC_REQUEST_CASHOUT = 'SET_USER_WITHDRAW_REQUESTED'
LST_KEYS_REQUEST_CASHOUT = ['user_id','user_at']
    # POST-DB: python TG notify admin_pay to process
	# POST-DB: python TG notify p_tg_user_id that request has been submit (w/ user_earns.usd_owed)

# '/trinity_show_my_rates'
kSHOW_USR_RATES = "trinity_show_my_rates" # '/show_my_rates'
LST_CMD_SHOW_RATES = [] # ['<tg_user_at>','<twitter|tiktok|reddit>']
STR_ERR_SHOW_RATES = f'''please use cmd format:\n /{kSHOW_USR_RATES} {" ".join(LST_CMD_SHOW_RATES)}'''
LST_KEYS_SHOW_RATES_RESP = env.LST_KEYS_PLACEHOLDER
DB_PROC_GET_USR_RATES = 'GET_USER_PAY_RATES'
LST_KEYS_SHOW_RATES = ['user_id','user_at','platform'] # const: unknown, twitter, tiktok, reddit

# '/trinity_show_my_earnings'
kSHOW_USR_EARNS = "trinity_show_my_earnings" # '/show_my_earnings'
LST_CMD_SHOW_EARNS = [] # ['<tg_user_at>']
STR_ERR_SHOW_EARNS = f'''please use cmd format :\n /{kSHOW_USR_EARNS} {" ".join(LST_CMD_SHOW_EARNS)}'''
LST_KEYS_SHOW_EARNS_RESP = env.LST_KEYS_PLACEHOLDER
DB_PROC_GET_USR_EARNS = 'GET_USER_EARNINGS'
LST_KEYS_SHOW_EARNS = ['user_id','user_at']

# '/trinity_set_wallet'
kSET_WALLET = "trinity_set_wallet"
LST_CMD_SET_WALLET = ['<wallet_address>']
STR_ERR_SET_WALLET = f'''please use cmd format :\n /{kSET_WALLET} {" ".join(LST_CMD_SET_WALLET)}'''
LST_KEYS_SET_WALLET_RESP = env.LST_KEYS_PLACEHOLDER
DB_PROC_SET_WALLET = 'SET_WALLET_ADDR'
LST_KEYS_SET_WALLET = ['user_id','user_at','wallet_address']

# '/admin_show_user_rates'
kADMIN_SHOW_USR_RATES = "admin_show_user_rates" 
LST_CMD_SHOW_RATES_ADMIN = ['<tg_user_at>'] # ['<tg_user_at>','<twitter|tiktok|reddit>']
STR_ERR_SHOW_RATES_ADMIN = f'''please use cmd format:\n /{kADMIN_SHOW_USR_RATES} {" ".join(LST_CMD_SHOW_RATES_ADMIN)}'''
LST_KEYS_SHOW_RATES_RESP_ADMIN = env.LST_KEYS_PLACEHOLDER
DB_PROC_GET_USR_RATES_ADMIN = 'GET_USER_PAY_RATES_ADMIN'
LST_KEYS_SHOW_RATES_ADMIN = ['admin_id','user_at','platform'] # const: unknown, twitter, tiktok, reddit

# '/admin_show_user_earnings'
kADMIN_SHOW_USR_EARNS = "admin_show_user_earnings" 
LST_CMD_SHOW_EARNS_ADMIN = ['<tg_user_at>']
STR_ERR_SHOW_EARNS_ADMIN = f'''please use cmd format :\n /{kADMIN_SHOW_USR_EARNS} {" ".join(LST_CMD_SHOW_EARNS_ADMIN)}'''
LST_KEYS_SHOW_EARNS_RESP_ADMIN = env.LST_KEYS_PLACEHOLDER
DB_PROC_GET_USR_EARNS_ADMIN = 'GET_USER_EARNINGS_ADMIN'
LST_KEYS_SHOW_EARNS_ADMIN = ['admin_id','user_at']

# '/admin_show_user_shills'
kADMIN_SHOW_USR_SHILLS = "admin_show_user_shills"
LST_CMD_USR_SHILLS_ADMIN = ['<tg_user_at>'] # optional: ['<tg_user_at>','<approved|yes>','<removed|yes>']
STR_ERR_USR_SHILLS_ADMIN = f'''please use cmd format :\n /{kADMIN_SHOW_USR_SHILLS} {" ".join(LST_CMD_USR_SHILLS_ADMIN)}'''
LST_KEYS_USR_SHILLS_RESP = env.LST_KEYS_PLACEHOLDER
DB_PROC_GET_USR_SHILLS_ALL = 'GET_USER_SHILLS_ALL'
LST_KEYS_USR_SHILLS = ['admin_id','user_at','approved','removed']

# '/admin_list_all_pend_shills'
kADMIN_LIST_ALL_PEND_SHILLS = "admin_list_all_pend_shills"
LST_CMD_PEND_SHILLS_ADMIN = [] # optional: ['<removed|yes>']
STR_ERR_PEND_SHILLS_ADMIN = f'''please use cmd format :\n /{kADMIN_LIST_ALL_PEND_SHILLS} {" ".join(LST_CMD_PEND_SHILLS_ADMIN)}'''
LST_KEYS_ALL_PEND_SHILLS_RESP = env.LST_KEYS_PLACEHOLDER
DB_PROC_GET_PEND_SHILLS = 'GET_PEND_SHILLS_ALL' # get where 'is_approved' = False
LST_KEYS_ALL_PEND_SHILLS = ['admin_id','removed']

# '/admin_approve_pend_shill'
kADMIN_APPROVE_SHILL = "admin_approve_pend_shill"
LST_CMD_APPROVE_SHILLS_ADMIN = ['<tg_user_at>','<shill_id>'] # default: ['<twitter|tiktok|reddit>'] # select: ['<htag|short_txt|long_txt|img_meme|short_vid|long_vid>']
STR_ERR_APPROVE_SHILLS_ADMIN = f'''please use cmd format :\n /{kADMIN_APPROVE_SHILL} {" ".join(LST_CMD_APPROVE_SHILLS_ADMIN)}'''
LST_KEYS_APPROVE_SHILL_RESP = env.LST_KEYS_PLACEHOLDER
DB_PROC_APPROVE_SHILL_STATUS = "UPDATE_USER_SHILL_APPR_EARNS" 
LST_KEYS_APPROVE_SHILL = ['admin_id','user_at', 'shill_id','shill_plat','shill_type']
    # PRE-DB: admin views / inspects shill_url on the web (determines: plat, type, pay, approve)
    # POST-DB: python TG message to shiller confirming approval & earnings updated (w/ shill url, shill type, pay_usd)

# '/admin_view_shill_status'
kADMIN_VIEW_SHILL = "admin_view_shill_status"
LST_CMD_VIEW_SHILL_ADMIN = ['<tg_user_at>','<shill_id>','<shill_url>']
STR_ERR_VIEW_SHILL_ADMIN = f'''please use cmd format :\n /{kADMIN_VIEW_SHILL} {" ".join(LST_CMD_VIEW_SHILL_ADMIN)}'''
LST_KEYS_VIEW_SHILL_RESP = env.LST_KEYS_PLACEHOLDER
DB_PROC_GET_USR_SHILL = 'GET_USER_SHILL'
LST_KEYS_VIEW_SHILL = ['admin_id','user_at','shill_id','shill_url']

# '/admin_pay_shill_rewards' _ NOTE: requires solidty 'payOutBST' call _ ** HOUSE ONLY **
# NOTE: 'kADMIN_PAY_SHILL_EARNS' pays out at current rate in db
#   if admin wants to change payout, they must do so using 'kADMIN_SET_USR_SHILL_PAY_RATE', 
#    before using 'kADMIN_APPROVE_SHILL', and then call 'kADMIN_PAY_SHILL_EARNS'
kADMIN_PAY_SHILL_EARNS = "admin_pay_shill_rewards"
LST_CMD_PAY_SHILL_ADMIN = ['<tg_user_at>']
STR_ERR_PAY_SHILL_ADMIN = f'''please use cmd format :\n /{kADMIN_PAY_SHILL_EARNS} {" ".join(LST_CMD_PAY_SHILL_ADMIN)}'''
LST_KEYS_PAY_SHILL_EARNS_RESP = env.LST_KEYS_PLACEHOLDER
DB_PROC_SET_USR_PAY_SUBMIT = 'SET_USER_PAY_TX_SUBMIT' # -> get_usr_pay_usd_appr_sum, set_usr_pay_usd_tx_submit
LST_KEYS_PAY_SHILL_EARNS = ['admin_id','user_at']
    # POST-DB: perform python/solidity 'payOutBST(user_earns.usd_owed, wallet_address, aux_token)' to get tx data for DB_PROC_SET_USR_PAY_CONF
    #	        get 'wallet_address' from 'GET_USER_EARNINGS(tg_user_id)'
kADMIN_PAY_SHILL_EARNS_conf = "admin_pay_shill_rewards_conf"
LST_KEYS_PAY_SHILL_EARNS_CONF_RESP = env.LST_KEYS_PLACEHOLDER
DB_PROC_SET_USR_PAY_CONF = 'SET_USER_PAY_TX_STATUS' # -> set_usr_pay_usd_tx_status
LST_KEYS_PAY_SHILL_EARNS_CONF = ['admin_id','user_at','chain_usd_paid','tx_hash','tx_status','payout_wallet_addr','pay_tok_addr','pay_tok_symb','aux_tok_burn']
    # PRE-DB: perform python/solidity 'payOutBST' to get tx data for DB_PROC_SET_USR_PAY_CONF

# '/admin_log_removed_shill'
kADMIN_SET_SHILL_REM = "admin_log_removed_shill"
LST_CMD_SET_SHILL_REM_ADMIN = ['<tg_user_at>','<shill_id>'] # default: ['<removed>']
STR_ERR_SET_SHILL_REM_ADMIN = f'''please use cmd format :\n /{kADMIN_SET_SHILL_REM} {" ".join(LST_CMD_SET_SHILL_REM_ADMIN)}'''
LST_KEYS_SET_SHILL_REM_RESP = env.LST_KEYS_PLACEHOLDER
DB_PROC_SET_SHILL_REM = 'SET_USER_SHILL_REMOVED'
LST_KEYS_SET_SHILL_REM = ['admin_id','tg_user_at','shill_id','removed']

# '/admin_scan_web_for_dead_shills' _ NOTE: requires twitter post web scrape
kADMIN_CHECK_USR_REM_SHILLS = "admin_scan_web_for_dead_shills"
LST_CMD_CHECK_USR_REM_ADMIN = ['<tg_user_at>','<approved|yes>','removed|no']
STR_ERR_CHECK_USR_REM_ADMIN = f'''please use cmd format :\n /{kADMIN_CHECK_USR_REM_SHILLS} {" ".join(LST_CMD_CHECK_USR_REM_ADMIN)}'''
LST_KEYS_CHECK_USR_REM_SHILLS_RESP = env.LST_KEYS_PLACEHOLDER
DB_PROC_CHECK_USR_REM_SHILL = DB_PROC_GET_USR_SHILLS_ALL 
LST_KEYS_CHECK_USR_REM_SHILLS = ['admin_id','user_at','approved','removed']
    # POST-DB: web scrape those post_urls to see if they are still working / viewable

# '/admin_set_shiller_rate'
kADMIN_SET_USR_SHILL_PAY_RATE = "admin_set_shiller_rate"
LST_CMD_SET_USR_RATE_ADMIN = ['<tg_user_at>','<pay_usd>','<twitter|tiktok|reddit>','<htag|short_txt|long_txt|img_meme|short_vid|long_vid>']
STR_ERR_SET_USR_RATE_ADMIN = f'''please use cmd format :\n /{kADMIN_SET_USR_SHILL_PAY_RATE} {" ".join(LST_CMD_SET_USR_RATE_ADMIN)}'''
LST_KEYS_SET_USR_SHILL_PAY_RATE_RESP = env.LST_KEYS_PLACEHOLDER
DB_PROC_SET_USR_RATES = 'SET_USER_PAY_RATE'
LST_KEYS_SET_USR_SHILL_PAY_RATE = ['admin_id','user_at','shill_plat','shill_type','pay_usd']

#-----------------------------------------------------#
#   NEO
#-----------------------------------------------------#
# '/blacklist_user'
kADD_BLACKLIST_SCAMMER = "blacklist_user"
LST_CMD_BLIST_REQUEST_ADMIN = ['<tg_user_at>','<bl_user_at>']
STR_ERR_BLIST_REQUEST_ADMIN = f'''please use cmd format :\n /{kADD_BLACKLIST_SCAMMER} {" ".join(LST_CMD_BLIST_REQUEST_ADMIN)}'''
LST_KEYS_ADD_BLACKLIST_SCAMMER_RESP = env.LST_KEYS_PLACEHOLDER
DB_PROC_ADD_BLACKLIST_SCAMMER = 'ADD_REQUEST_USER_BLACKLIST'
LST_KEYS_ADD_BLACKLIST_SCAMMER = ['admin_or_user_id','bl_user_id','bl_user_at','bl_user_handle','tg_chan_id']

# LEFT OFF HERE ... need endpoint for neo to check if a user is blacklisted (instead of using array in neo_bot.py)

#-----------------------------------------------------#
DICT_CMD_EXE = {
    # USER CMDS
    kSHILLER_REG:[kSHILLER_REG,LST_KEYS_REG_USER,LST_KEYS_REG_USER_RESP,DB_PROC_ADD_NEW_USER,LST_CMD_REG_USER,STR_ERR_REG_USER],
    kTWITTER_CONF:[kTWITTER_CONF,LST_KEYS_TW_CONF,LST_KEYS_TW_CONF_RESP,DB_PROC_RENEW_TW_CONFRIM,LST_CMD_TW_CONF,STR_ERR_TW_CONF],
    kSUBMIT_SHILL:[kSUBMIT_SHILL,LST_KEYS_SUBMIT_SHILL,LST_KEYS_SUBMIT_SHILL_RESP,DB_PROC_ADD_SHILL,LST_CMD_SUBMIT_SHILL,STR_ERR_SUBMIT_SHILL],
    kREQUEST_CASHOUT:[kREQUEST_CASHOUT,LST_KEYS_REQUEST_CASHOUT,LST_KEYS_REQUEST_CASHOUT_RESP,DB_PROC_REQUEST_CASHOUT,LST_CMD_REQUEST_CASHOUT,STR_ERR_REQUEST_CASHOUT],
    kSHOW_USR_RATES:[kSHOW_USR_RATES,LST_KEYS_SHOW_RATES,LST_KEYS_SHOW_RATES_RESP,DB_PROC_GET_USR_RATES,LST_CMD_SHOW_RATES,STR_ERR_SHOW_RATES],
    kSHOW_USR_EARNS:[kSHOW_USR_EARNS,LST_KEYS_SHOW_EARNS,LST_KEYS_SHOW_EARNS_RESP,DB_PROC_GET_USR_EARNS,LST_CMD_SHOW_EARNS,STR_ERR_SHOW_EARNS],
    kSET_WALLET:[kSET_WALLET,LST_KEYS_SET_WALLET,LST_KEYS_SET_WALLET_RESP,DB_PROC_SET_WALLET,LST_CMD_SET_WALLET,STR_ERR_SET_WALLET],
    # ADMIN CMDS
    kADMIN_SHOW_USR_RATES:[kADMIN_SHOW_USR_RATES,LST_KEYS_SHOW_RATES_ADMIN,LST_KEYS_SHOW_RATES_RESP_ADMIN,DB_PROC_GET_USR_RATES_ADMIN,LST_CMD_SHOW_RATES_ADMIN,STR_ERR_SHOW_RATES_ADMIN],
    kADMIN_SHOW_USR_EARNS:[kADMIN_SHOW_USR_EARNS,LST_KEYS_SHOW_EARNS_ADMIN,LST_KEYS_SHOW_EARNS_RESP_ADMIN,DB_PROC_GET_USR_EARNS_ADMIN,LST_CMD_SHOW_EARNS_ADMIN,STR_ERR_SHOW_EARNS_ADMIN],
    kADMIN_SHOW_USR_SHILLS:[kADMIN_SHOW_USR_SHILLS,LST_KEYS_USR_SHILLS,LST_KEYS_USR_SHILLS_RESP,DB_PROC_GET_USR_SHILLS_ALL,LST_CMD_USR_SHILLS_ADMIN,STR_ERR_USR_SHILLS_ADMIN],
    kADMIN_LIST_ALL_PEND_SHILLS:[kADMIN_LIST_ALL_PEND_SHILLS,LST_KEYS_ALL_PEND_SHILLS,LST_KEYS_ALL_PEND_SHILLS_RESP,DB_PROC_GET_PEND_SHILLS,LST_CMD_PEND_SHILLS_ADMIN,STR_ERR_PEND_SHILLS_ADMIN],
    kADMIN_APPROVE_SHILL:[kADMIN_APPROVE_SHILL,LST_KEYS_APPROVE_SHILL,LST_KEYS_APPROVE_SHILL_RESP,DB_PROC_APPROVE_SHILL_STATUS,LST_CMD_APPROVE_SHILLS_ADMIN,STR_ERR_APPROVE_SHILLS_ADMIN],
    kADMIN_VIEW_SHILL:[kADMIN_VIEW_SHILL,LST_KEYS_VIEW_SHILL,LST_KEYS_VIEW_SHILL_RESP,DB_PROC_GET_USR_SHILL,LST_CMD_VIEW_SHILL_ADMIN,STR_ERR_VIEW_SHILL_ADMIN],
    kADMIN_PAY_SHILL_EARNS:[kADMIN_PAY_SHILL_EARNS,LST_KEYS_PAY_SHILL_EARNS,LST_KEYS_PAY_SHILL_EARNS_RESP,DB_PROC_SET_USR_PAY_SUBMIT,LST_CMD_PAY_SHILL_ADMIN,STR_ERR_PAY_SHILL_ADMIN],
    kADMIN_SET_SHILL_REM:[kADMIN_SET_SHILL_REM,LST_KEYS_SET_SHILL_REM,LST_KEYS_SET_SHILL_REM_RESP,DB_PROC_SET_SHILL_REM,LST_CMD_SET_SHILL_REM_ADMIN,STR_ERR_SET_SHILL_REM_ADMIN],
    kADMIN_CHECK_USR_REM_SHILLS:[kADMIN_CHECK_USR_REM_SHILLS,LST_KEYS_CHECK_USR_REM_SHILLS,LST_KEYS_CHECK_USR_REM_SHILLS_RESP,DB_PROC_CHECK_USR_REM_SHILL,LST_CMD_CHECK_USR_REM_ADMIN,STR_ERR_CHECK_USR_REM_ADMIN],
    kADMIN_SET_USR_SHILL_PAY_RATE:[kADMIN_SET_USR_SHILL_PAY_RATE,LST_KEYS_SET_USR_SHILL_PAY_RATE,LST_KEYS_SET_USR_SHILL_PAY_RATE_RESP,DB_PROC_SET_USR_RATES,LST_CMD_SET_USR_RATE_ADMIN,STR_ERR_SET_USR_RATE_ADMIN],

    kADMIN_PAY_SHILL_EARNS_conf:[kADMIN_PAY_SHILL_EARNS_conf,LST_KEYS_PAY_SHILL_EARNS_CONF,LST_KEYS_PAY_SHILL_EARNS_CONF_RESP,DB_PROC_SET_USR_PAY_CONF,['<nil_lst>'],'<nil_str>'],
}

#=====================================================#
#         request handler accessors/mutators          #
#=====================================================#
# '/bst/submit_shill_web' _ key_vals={tg_cmd_sim, tg_user_at, tweet_url}
# '/bst/request_pay_web' _ key_vals={tg_cmd_sim, tg_user_at}
# '/bst/shiller_info_web' _ key_vals={tg_cmd_sim, tg_user_at}
def bst_web_request(request):
    funcname = f'{__filename} bst_web_request'
    print(funcname + ' - ENTER')

    # parse request to get keVals to simulate call to 'exe_tg_cmd'
    bErr, jsonResp, keyVals = parse_request(request, 'TRINITY_WEB_DAPP')
    if bErr: return jsonResp # JSONResponse(...)

    # exe db call to get tg_user_id to simulate call to 'exe_tg_cmd'
    bErr, jsonResp, dbProcResult = execute_db_proc({'tg_user_at':keyVals['tg_user_at']}, 'GET_TG_USER_ID_WEB')
    if bErr: return jsonResp # JSONResponse(...)
    
    # generate lst_inp to simulate call to 'exe_tg_cmd'
    tg_cmd = str(keyVals['tg_cmd_sim'])
    tg_user_id = dbProcResult[0]['tg_user_id']
    lst_inp = [tg_cmd, tg_user_id]
    lst_inp.extend([keyVals[k] for k in keyVals])    

    # append edge case params for web request 'view my stuff'
    #   NOTE: don't need to append anything for 'kSHOW_USR_EARNS'
    if tg_cmd == kSHOW_USR_RATES: lst_inp.append('twitter') # platform=twitter
    if tg_cmd == kADMIN_SHOW_USR_SHILLS: lst_inp.extend(['0','0']) # is_approved=False, is_removed=False

    # NOTE: returns from 'handle_request'
    return exe_tg_cmd(lst_inp, False, True) # True = coming from web-dapp

def exe_tg_cmd(_lst_inp, _is_tg_prod_acct, _is_web_dapp=False):
    funcname = f'{__filename} exe_tg_cmd(_is_tg_prod_acct={_is_tg_prod_acct}, _is_web_dapp={_is_web_dapp})'
    print(funcname+' - ENTER')

    # generate keyVals to pass as 'request' w/ 'tg_cmd!=None', to 'handle_request'
    tg_cmd = _lst_inp[0][1::] # parse out the '/'
    lst_params = _lst_inp[1::]
    keyVals = {}
    print(' tg_cmd: '+tg_cmd)
    print(' lst_params: ', *lst_params, sep='\n  ')
    print(' DICT_CMD_EXE[tg_cmd][1]: ', *DICT_CMD_EXE[tg_cmd][1], sep='\n  ')

    # validate input cmd params count
    if len(lst_params) != len(DICT_CMD_EXE[tg_cmd][1]):
        print(' ** WARNING **: input cmd param count != db required param count; forcing return fail')
        str_req_params = ''.join(DICT_CMD_EXE[tg_cmd][-1])
        bErr, jsonResp = prepJsonResponseValidParams(keyVals, False, tprint=True, errMsg=f'invalid number of params; {str_req_params}') # False = force fail
        return jsonResp

    # generate keyVals from input cmd params
    for i,v in enumerate(lst_params): 
        print(f' lst_params[{i}]={v}')
        keyVals[DICT_CMD_EXE[tg_cmd][1][i]] = str(v) # [tg_cmd][1] = LST_KEYS_...
    
    print(' generated keyVals ...')
    [print(f'  keyVals[{k}]={keyVals[k]}') for k in keyVals.keys()]
    # simuate: 'handle_request(request, kREQUEST_KEY)' w/ added 'tg_cmd'
    return handle_request(keyVals, DICT_CMD_EXE[tg_cmd][0], tg_cmd)

#=====================================================#
#         STATIC request handler support              #
#=====================================================#
def handle_request(request, req_handler_key, tg_cmd=None):
    funcname = f'{__filename} handle_request'
    print(funcname + ' - ENTER')
    
    # (1) vaidate & parse request param key/vals
    bErr, jsonResp, keyVals = parse_request(request, req_handler_key, tg_cmd)
    if bErr:
        return jsonResp # JSONResponse(...)
        
    # (2) perfom database executions
    bErr, jsonResp, dbProcResult = execute_db_calls(keyVals, req_handler_key, tg_cmd)
    if bErr:
        return jsonResp # JSONResponse(...)

    # (3) generate success response params
    arrStrReturnKeys, strRespSuccessMSG = generate_resp_params(req_handler_key, keyVals, tg_cmd)
    
    # (4) prepare return json model
    # jsonResp = prepJsonResponseDbProc(arrStrReturnKeys, dbProcResult, strRespSuccessMSG, tprint=False)
    if tg_cmd: jsonResp = prepJsonResponseDbProc_ALL(arrStrReturnKeys, dbProcResult, strRespSuccessMSG, tprint=VERBOSE_LOG)
    else: jsonResp = prepJsonResponseDbProc(arrStrReturnKeys, dbProcResult, strRespSuccessMSG, tprint=VERBOSE_LOG)
    
    # (5) return client response
    return jsonResp # JSONResponse(...) -> Response(json.dumps(dict), mimetype="application/json" )

def parse_request(request, req_handler_key, tg_cmd=None): # (1)
    funcname = f'{__filename} parse_request'
    print(funcname + ' - ENTER')
    
    if tg_cmd:
        keyVals = dict(request)
        print('HIT - tg_cmd: '+tg_cmd)
        if tg_cmd in DICT_CMD_EXE.keys():
            if tg_cmd == kTWITTER_CONF or tg_cmd == kSHILLER_REG:
                # add 'tweet_id' & 'twitter_at' to keyVals
                keyVals, success = parse_twitter_url(keyVals, 'trinity_tw_url') 
                if not success:
                    bErr, jsonResp = prepJsonResponseValidParams(keyVals, False, tprint=VERBOSE_LOG, errMsg='invalid tweet url, please try again') # False = force fail
                    return bErr, jsonResp, None # JSONResponse(...)

                # check if tweet url contains text list
                success, msg = valid_trinity_tweet(keyVals['trinity_tw_url'], ['@BearSharesX', 'Trinity','register'])
                if not success:
                    bErr, jsonResp = prepJsonResponseValidParams(keyVals, False, tprint=VERBOSE_LOG, errMsg='invalid tweet confirmation / '+msg) # False = force fail
                    return bErr, jsonResp, None # dbProcResult
                
            if tg_cmd == kSUBMIT_SHILL:
                # add 'tweet_id' & 'twitter_at' to keyVals
                keyVals, success = parse_twitter_url(keyVals, 'post_url')
                if not success:
                    bErr, jsonResp = prepJsonResponseValidParams(keyVals, False, tprint=VERBOSE_LOG, errMsg='invalid tweet shill url, please try again') # False = force fail
                    return bErr, jsonResp, None # JSONResponse(...)

                # check if tweet url contains text list
                success, msg = valid_trinity_tweet(keyVals['post_url'], ['@BearSharesX'])
                if not success:
                    bErr, jsonResp = prepJsonResponseValidParams(keyVals, False, tprint=VERBOSE_LOG, errMsg='invalid shill, '+msg) # False = force fail
                    return bErr, jsonResp, None # dbProcResult
                
            if tg_cmd == kADMIN_SHOW_USR_SHILLS:
                # LST_KEYS_USR_SHILLS = ['admin_id','user_at','approved','removed']
                if keyVals['approved']=='yes' or keyVals['approved']=='approved' or keyVals['approved']=='1' or keyVals['approved'].lower()=='true':
                    keyVals['approved'] = '1'
                else:
                    keyVals['approved'] = '0'

                if keyVals['removed']=='yes' or keyVals['removed']=='removed' or keyVals['removed']=='1' or keyVals['removed'].lower()=='true':
                    keyVals['removed'] = '1'
                else:
                    keyVals['removed'] = '0'

            if tg_cmd == kADMIN_LIST_ALL_PEND_SHILLS:
                if keyVals['removed']=='yes' or keyVals['removed']=='removed' or keyVals['removed']=='1' or keyVals['removed'].lower()=='true':
                    keyVals['removed'] = '1'
                else:
                    keyVals['removed'] = '0'

            if tg_cmd == kADMIN_SET_SHILL_REM:
                if keyVals['removed']=='yes' or keyVals['removed']=='removed' or keyVals['removed']=='1' or keyVals['removed'].lower()=='true':
                    keyVals['removed'] = '1'
                else:
                    keyVals['removed'] = '0'
        else:
            bErr, jsonResp = prepJsonResponseValidParams(keyVals, False, tprint=VERBOSE_LOG, errMsg='command not found') # False = force fail
            return bErr, jsonResp, -1 # dbProcResult
        
    else:
        # note: utilizing additional dict here (instead of just request.form/args/get_json())
        #   because we want to be secure the params passed to the database are only the keys we want
        reqParamsImmutDict = request.form
        #print(funcname, 'reqParamsImmutDict - DONE', f'{reqParamsImmutDict}', tprint=True)

        # validate required params & set local vars
        keyVals = reqParamsImmutDict.copy()["key_vals"] if reqParamsImmutDict is not None else None

        keyVals = json.loads(keyVals)
        #print(funcname, 'keyVals - DONE', tprint=True)

    # validate request params (PIN, keys, etc.)
    validParams0 = validate_params(keyVals, req_handler_key, tg_cmd)
    #print(funcname, 'validParams0 - DONE', tprint=True)

    #bErr, jsonResp = prepJsonResponseValidParams(keyVals, validParams0, valid_PIN, tprint=True)
    bErr, jsonResp = prepJsonResponseValidParams(keyVals, validParams0, tprint=True)
    #print(funcname, 'prepJsonResponseValidParams - DONE', tprint=True)
    if bErr:
        return bErr, jsonResp, None # JSONResponse(...)
        
    return bErr, jsonResp, keyVals

#=====================================================#
#         DYNAMIC request handler support             #
#=====================================================#
def execute_db_proc(keyVals, stored_proc):
    funcname = f'{__filename} execute_db_call_simple'
    print(funcname + ' - ENTER')
    dbProcResult = exe_stored_proc(-1, stored_proc, keyVals)
    bErr, jsonResp = prepJsonResponseDbProcErr(dbProcResult, tprint=VERBOSE_LOG)
    if bErr: return False, 'db error occurred', dbProcResult
    return True, jsonResp, dbProcResult

    # LEFT OFF HERE ...

# append req_handler_key, parse keyVals params, invoke database function
def execute_db_calls(keyVals, req_handler_key, tg_cmd=None): # (2)
    funcname = f'{__filename} execute_db_calls'
    print(funcname + ' - ENTER')

    # perfom database executions
    bErr=False
    jsonResp={}
    dbProcResult = None

    if tg_cmd != None:
        print('HIT - tg_cmd: '+tg_cmd)
        if tg_cmd in DICT_CMD_EXE.keys():                            
            # if 'user_id' in keyVals: del keyVals['user_id']
            stored_proc = DICT_CMD_EXE[tg_cmd][3] # [tg_cmd][3] = 'stored-proc-name'
            dbProcResult = exe_stored_proc(-1, stored_proc, keyVals)
            if dbProcResult[0]['status'] == 'failed': errMsg = dbProcResult[0]['info']
            else: errMsg = None
            bErr, jsonResp = prepJsonResponseDbProcErr(dbProcResult, tprint=VERBOSE_LOG, errMsg=errMsg) # errMsg != None: force fail from db
            # bErr, jsonResp = prepJsonResponseDbProcErr(dbProcResult, tprint=True)
            
            if tg_cmd == kADMIN_PAY_SHILL_EARNS and not bErr:

                # parse db return into solidity input
                usd_val_pay = int(float(dbProcResult[0]['tot_owed']) * 10**6) # convert to BST decimal precision
                wallet_addr = dbProcResult[0]['wallet_address']
                aux_token = 0
                
                # generate solidity function input params
                lst_func_params = [usd_val_pay, wallet_addr, aux_token]
                lst_params = list(_abi.BST_FUNC_MAP_WRITE[_abi.BST_PAYOUT_FUNC_SIGN])
                lst_params.insert(2, lst_func_params)
                
                # init myWEB3 driver and set the gas needed for 'payOutBST' (highend average)
                #   NOTE: 'sender' should be account that will be doing the payout
                W3_ = _web3.myWEB3().init_nat(1, env.sender_addr_trinity, env.sender_secr_trinity) # 1 = pulsechain
                W3_.set_gas_params(W3_.W3, _gas_limit=800_000, _fee_perc_markup=0.5)

                # finalize input params for writing to blockchain
                BST_ADDRESS = W3_.W3.to_checksum_address(env.bst_contr_addr)
                tup_params = (BST_ADDRESS,lst_params[0],lst_params[1],lst_params[2],lst_params[3],W3_,360) # 360 = _tx_wait_sec

                # set default failure vals blockchain write response
                tx_receipt, tx_hash, d_ret_log, chain_usd_paid, tx_status = (-37, '0x37', {}, -37.0, -2)
                try:
                    # write to blockchain with input params (invoking _bst_keeper.py)
                    tx_receipt, tx_hash, d_ret_log = _bst_keeper.write_with_hash(*tup_params)                    
                    if tx_receipt != -1: # ie. 'exception' did NOT occur within 'W3.eth.wait_for_transaction_receipt'
                        print(' ... generating a success tx lst_params_ for db update (tx_receipt != -1)\n')
                        if '_usdAmntPaid' in d_ret_log.keys(): chain_usd_paid = float(d_ret_log['_usdAmntPaid']) / 10**6
                        tx_status = int(tx_receipt['status']) # 'tx_status'
                    else:
                        print(' ... generating failed tx lst_params_ for db update (e: tx_receipt == -1)\n')
                        tx_status = -1 # -1 = exception occurred within 'W3.eth.wait_for_transaction_receipt'

                    # simulates a tg input cmd 'lst_params_' for LST_KEYS_PAY_SHILL_EARNS_CONF
                    lst_params_ = [
                        keyVals['admin_id'], # 'admin_id'
                        keyVals['user_at'], # 'user_at'
                        chain_usd_paid, # 'chain_usd_paid'
                        tx_hash, # 'tx_hash'
                        tx_status, # 'tx_status'
                        wallet_addr, # 'payout_wallet_addr'
                        env.bst_contr_addr, # 'pay_tok_addr'
                        env.bst_contr_symb, # 'pay_tok_symb'
                        aux_token, # 'aux_tok_burn'
                    ]

                except Exception as e:
                    print_except(e, debugLvl=0)
                    print(' ... generating failed tx lst_params_ for db update (e: write_with_hash)\n')
                    # generate a failed 'lst_params_' for LST_KEYS_PAY_SHILL_EARNS_CONF
                    lst_params_ = [
                        keyVals['admin_id'], # 'admin_id'
                        keyVals['user_at'], # 'user_at'
                        chain_usd_paid, # 'chain_usd_paid' # default -1.0
                        tx_hash, # 'tx_hash' # default '0x37'
                        tx_status, # 'tx_status' # -2 = exception occurred within '_bst_keeper.write_with_hash'
                        wallet_addr, # 'payout_wallet_addr'
                        env.bst_contr_addr, # 'pay_tok_addr'
                        env.bst_contr_symb, # 'pay_tok_symb'
                        aux_token, # 'aux_tok_burn'
                    ]
                
                # generate keyVals from simulated input cmd params (lst_params_)
                tg_cmd = kADMIN_PAY_SHILL_EARNS_conf
                keyVals_ = {}
                print(' tg_cmd: '+tg_cmd)
                print(' lst_params_: ', *lst_params_, sep='\n  ')
                print(' DICT_CMD_EXE[tg_cmd][1]: ', *DICT_CMD_EXE[tg_cmd][1], sep='\n  ')
                for i,v in enumerate(lst_params_): 
                    print(f' lst_params_[{i}]={v}')
                    keyVals_[DICT_CMD_EXE[tg_cmd][1][i]] = str(v) # [tg_cmd][1] = LST_KEYS_...
                stored_proc = DICT_CMD_EXE[tg_cmd][3] # [tg_cmd][3] = 'stored-proc-name'

                # exe db call to update status on payout tx attempt
                dbProcResult = exe_stored_proc(-1, stored_proc, keyVals_)
                if dbProcResult[0]['status'] == 'failed': errMsg = dbProcResult[0]['info']
                else: errMsg = None
                bErr, jsonResp = prepJsonResponseDbProcErr(dbProcResult, tprint=VERBOSE_LOG, errMsg=errMsg) # errMsg != None: force fail from db

        else:
            dbProcResult=-1
            bErr, jsonResp = prepJsonResponseDbProcErr(dbProcResult, tprint=True)
    else:
        # NOTE: current http request integration is delgated through 'exe_tg_cmd'
        print('HIT - http request integration')
        pass 
    
    return bErr, jsonResp, dbProcResult

# append req_handler_key, set arrStrReturnKeys & strRespSuccessMSG
def generate_resp_params(req_handler_key, keyVals=None, tg_cmd=None): # (3)
    funcname = f'{__filename} generate_resp_params'
    print(funcname + ' - ENTER')
    
    # success response params
    arrStrReturnKeys = ["nil_keys"]
    strRespSuccessMSG = "nil_msg"

    if tg_cmd != None:
        if tg_cmd in DICT_CMD_EXE.keys():
            arrStrReturnKeys = DICT_CMD_EXE[tg_cmd][2] # [tg_cmd][2] = LST_KEYS_..._RESP
            strRespSuccessMSG = f"CMD {tg_cmd} successful!"
        else:
            arrStrReturnKeys = [f"nil_keys, err failed to find req_handler_key: {req_handler_key}"]
            strRespSuccessMSG = f"nil_msg, err failed to find req_handler_key: {req_handler_key}"
    else:
        pass # http request integration
        
    return arrStrReturnKeys, strRespSuccessMSG

# append req_handler_key, invoke keyVals validation function
def validate_params(keyVals, req_handler_key, tg_cmd=None):
    funcname = f'{__filename} validate_params'
    print(funcname + ' - ENTER')
    #valid_PIN = validatePIN(keyVals)
    
    if tg_cmd != None:
        if tg_cmd in DICT_CMD_EXE.keys():
            return valid_keys(keyVals, DICT_CMD_EXE[tg_cmd][1]) # [tg_cmd][1] = LST_KEYS_...
        else:
            return False
    else:
        # http request integration
        return req_handler_key == 'TRINITY_WEB_DAPP'
    return False

#=====================================================#
#         endpoint key validation support             #
#=====================================================#
def validatePIN(keyVals):
    funcname = f'({__filename}) validatePIN'
    if kPin not in keyVals:
        return False

    vPin = str(keyVals[kPin])
    print(funcname, f"procValidatePIN({vPin})...")
    dbResult = procValidatePIN(strPIN=vPin)
    print(funcname, f"procValidatePIN({vPin}) = {dbResult}")
    return dbResult > 0

## all endpoint key validations ##
def valid_keys(keyVals, lst_valid_keys):
    funcname = f'{__filename} valid_keys'
    print(funcname + ' - ENTER')
    if keyVals is None or len(keyVals) < 1:
        print(funcname, 'FAILED static/constant keyVals check lenth; returning False')
        return False
    for idx, key in enumerate(lst_valid_keys):
        if key not in keyVals:
            print(funcname, f'FAILED static/constant keyVals check key: {key}; returning False')
            return False
    return True

#=====================================================#
#         twitter support                             #
#=====================================================#
def valid_trinity_tweet(_tw_url, _lst_text):
    funcname = f'{__filename} valid_trinity_tweet'
    print(funcname + ' - ENTER')
    return search_tweet_for_text(_tw_url, _lst_text, True) # True = '--headless'
    # return soup_search_tweet_for_text(_tw_url, lst_text)

def parse_twitter_url(_keyVals, _key):
    funcname = f'{__filename} parse_twitter_url'
    print(funcname + ' - ENTER')

    # parse twitter @username & tweet id (note: 'https' required, else fails)
    #   ex: https://x.com/SolAudits/status/1765925225844089300?s=20
    tw_url = _keyVals[_key]
    # valid_uri = '?' in tw_url and tw_url.startswith('https://')
    valid_uri = tw_url.startswith('https://')
    if not valid_uri: return _keyVals, False # check for no slash ('/') in url

    # append '?s=20' if needed
    #   for some reason 'search_tweet_for_text' fails w/o it
    #    while users are indeed submitting tweets w/o it
    if '?' not in tw_url: tw_url += '?s=20' 

    lst_items = tw_url.split('/')
    valid_dom = 'x.com' in lst_items[2] or 'twitter.com' in lst_items[2]
    if not valid_dom: return _keyVals, False
    _keyVals['tweet_id'] = lst_items[5].split('?')[0] if '?' in lst_items[5] else lst_items[5]
    _keyVals['twitter_at'] = lst_items[3]

    # fail: if twitter_at is in ignore list
    if _keyVals['twitter_at'].lower() in [v.lower() for v in LST_IGNORE_TWITTER_AT]: 
        print(f" found attempt to use '@{_keyVals['twitter_at']}' in twitter ignore list, returning False")
        return _keyVals, False

    return _keyVals, True

def search_tweet_for_text(tweet_url, _lst_text=[], _headless=True):
    global WEB_DRIVER_WAIT_CNT, WEB_DRIVER_WAIT_SEC, WEB_DRIVE_WAIT_SLEEP_SEC
    funcname = f'{__filename} search_tweet_for_text'
    print(funcname + ' - ENTER')

    try:
        options = Options()
        print(f' using --headless={_headless}')
        if _headless:
            # user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
            # user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15"
            user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.111 Safari/537.36" # AWS ubuntu instance

            options.add_argument("--no-sandbox") # ref: https://stackoverflow.com/a/53073789 (required for 'headless' on AWS ubuntu instance)
            options.add_argument("--headless")  # Run Chrome in headless mode
            options.add_argument(f"user-agent={user_agent}") # required, else '--headless' fails
            options.add_argument("--enable-javascript")  

        # Initialize a Selenium WebDriver & get tweet_url page
        print(f' getting page: {tweet_url} _ {get_time_now(dt=False)}')
        driver = webdriver.Chrome(options=options)
        # if '?' in tweet_url: 
        #     tweet_url = tweet_url.split('?')[0]
        #     print(" found '?' in tweet_url; parsed out and going with:\n  "+tweet_url)
        driver.get(tweet_url)
        print(f' getting page: {tweet_url} _ {get_time_now(dt=False)} _ DONE')
        
        # loop setup
        title = ''
        title_check = 'X:' # end loop when found (signifies full tweet text is extractable)
        check_cnt = 1

        # loop through 'WebDriverWait' to find a meta tag w/ specific 'property' & 'content'
        #   keep trying until 'title_check' is found or WEB_DRIVER_WAIT_CNTWEB_DRIVER_WAIT_CNT reached 
        while title_check not in title and check_cnt <= WEB_DRIVER_WAIT_CNT:
            try:
                print(f' Waiting for meta tag _ *ATTEMPT* # {check_cnt} _ {get_time_now()}')    
                WebDriverWait(driver, WEB_DRIVER_WAIT_SEC).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'meta[property="og:title"]')))
                meta_tag = driver.find_element(By.CSS_SELECTOR, 'meta[property="og:title"]')
                title = str(meta_tag.get_attribute("content"))
                print(f' Found meta tag w/ Title:\n  {title} _ {get_time_now()}')
            except Exception as e:
                print(f'  Error waiting for html text _ {get_time_now()} _ {WEB_DRIVER_WAIT_SEC} sec TIMEOUT (maybe)')
                if check_cnt == WEB_DRIVER_WAIT_CNT:
                    raise # end loop, break & raise if last check is exception
                else:
                    print(f"   **Exception** e: '{e}'\n  continuing while loop ...")
            check_cnt += 1
            time.sleep(WEB_DRIVE_WAIT_SLEEP_SEC) # sleep sec before next web driver attempt

    except Exception as e:
        print(f" Error scraping tweet\n  **Exception** e: '{e}'\n  returning False")
        return False, 'network error, check your tweet url'
    finally:
        # Close the browser
        driver.quit()

    search_text = str(title)
    print(f' searching html text for items in _lst_text: {_lst_text}')
    for t in _lst_text:
        if t.lower() in search_text.lower(): 
            print(f' FOUND text: {t}')
        else:
            print(f' FAILED to find text: {t.lower()} _ returning False')
            return False, 'must contain '+t
    print(f' SUCCESS found all text in _lst_text _ returning True')
    return True, ''

def get_time_now(dt=True):
    if dt: return '['+datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[0:-4]+']'
    return '['+datetime.now().strftime("%H:%M:%S.%f")[0:-4]+']'

#====================================================#
#====================================================#

print(__filename, f"\n CLASSES & FUNCTIONS initialized:- STARTING -> additional '{__filename}' run scripts (if applicable) . . .")
print(__filename, f"\n  DONE Executing additional '{__filename}' run scripts ...")
print('#======================================================================#')


# # searching <body> tag example...
# #  NOTE: when tweet 'Views' count is shown, then tweet text is shown as well
# print(f' waiting for full html body text _ {get_time_now()}')
# WebDriverWait(driver, WEB_DRIVER_WAIT_SEC).until(EC.text_to_be_present_in_element((By.TAG_NAME, 'BODY'), 'Views')) 
# print(f' waiting for full html body text _ {get_time_now()} _ DONE')        
# 
# get / search body text for '_lst_text' items
# body_text = driver.find_element(By.TAG_NAME, 'body').text
# search_text = str(body_text)


# def soup_search_tweet_for_text(tweet_url, _lst_text=[]):
#     funcname = f'{__filename} soup_search_tweet_for_text'
#     print(funcname + f' - ENTER _ {get_time_now()}')
#     import requests
#     from bs4 import BeautifulSoup

#     user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
#     headers = {
#         'User-Agent': user_agent,
#         }
#     # response = requests.get(url, headers=headers)
#     # Send a GET request to the URL
#     print(f' getting ur: {tweet_url}')
#     response = requests.get(tweet_url, headers=headers)
#     print(f' response.content: {response.content}')
#     print()
#     print()
#     # Check if the request was successful
#     if response.status_code == 200:
#         # Parse the HTML content using BeautifulSoup
#         soup = BeautifulSoup(response.content, 'html.parser')

#         # Find the meta tag with the specified property
#         meta_tag = soup.find('meta', property='og:title')

#         # Extract the content attribute of the meta tag
#         if meta_tag:
#             title = meta_tag.get('content')
#             print(" Title:", title)
#             print(f' searching body_text for items in _lst_text: {_lst_text}')
#             for t in _lst_text:
#                 if t.lower() in title.lower(): 
#                     print(f' FOUND text: {t}')
#                 else:
#                     print(f' FAILED to find text: {t.lower()} _ returning False')
#                     return False
#             print(f' SUCCESS found all text in _lst_text _ returning True ... {get_time_now()}')
#             return True
#         else:
#             print(f" Meta tag not found, returning False ... {get_time_now()}")
#             return False
#     else:
#         print(f" Failed to fetch URL: (returning False _ {get_time_now()})\n  status_code: {response.status_code}")
#         return False
        