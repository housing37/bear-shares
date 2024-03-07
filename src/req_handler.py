__fname = 'req_handler'
__filename = __fname + '.py'
cStrDivider = '#================================================================#'
cStrDivider_1 = '#----------------------------------------------------------------#'
print('', cStrDivider, f'GO _ {__filename} -> starting IMPORTs & declaring globals', cStrDivider, sep='\n')

#=====================================================#
#         imports                                     #
#=====================================================#
from _env import env
from flask import request
from db_controller import *
from req_helpers import *
import json
import tweepy

#=====================================================#
#         global static keys                          #
#=====================================================#
kPin = 'admin_pin'
kUserId = "user_id"
kKeyVals = "key_vals"

# twitter access globals
CONSUMER_KEY = 'nil_tw_key'
CONSUMER_SECRET = 'nil_tw_key'
ACCESS_TOKEN = 'nil_tw_key'
ACCESS_TOKEN_SECRET = 'nil_tw_key'

#=====================================================#
#         TG cmd / request handler static keys        #
#=====================================================#
# '/register_as_shiller'
kSHILLER_REG = "add_new_user"
LST_KEYS_REG_SHILLER = ['user_id', 'wallet_address', 'trinity_tw_url']
LST_KEYS_REG_SHILLER_RESP = env.LST_KEYS_REG_SHILLER_RESP
DB_PROC_ADD_NEW_USER = 'ADD_NEW_TG_USER'
    # validate 'trinity_tw_url' contains texts '@BearSharesNFT' & 'trinity'
    # insert into 'users' (...) values (...)

# '/confirm_twitter'
kTWITTER_CONF = "validate_twitter"
LST_KEYS_TW_CONF = ['user_id', 'trinity_tw_url']
LST_KEYS_TW_CONF_RESP = env.LST_KEYS_REG_SHILLER_RESP
DB_PROC_RENEW_TW_CONFRIM = 'UPDATE_TWITTER_CONF'

# '/submit_shill_link'
kSUBMIT_SHILL = "add_new_shill"
LST_KEYS_SUBMIT_SHILL = ['user_id', 'post_url']
LST_KEYS_SUBMIT_SHILL_RESP = env.LST_KEYS_REG_SHILLER_RESP
DB_PROC_ADD_SHILL = 'ADD_USER_SHILL_TW'
    # validate 'post_url' is not in 'shills' table yet
    # insert into 'shills' (...) values (...) for user_id
    # check number of pending shills (is_apporved=False), return rate-limit info
    #	perhaps set a max USD per day that people can earn?

# '/show_my_rates'
kSHOW_RATES = "get_user_rates"
LST_KEYS_SHOW_RATES = ['user_id', 'platform'] # const: unknown, twitter, tiktok, reddit
LST_KEYS_SHOW_RATES_RESP = env.LST_KEYS_REG_SHILLER_RESP
DB_PROC_GET_USR_RATES = 'GET_USER_PAY_RATES'
    # select * from 'user_shill_rates' for user_id (order by id desc limit 1)

# '/show_my_earnings'
kSHOW_EARNINGS = "get_user_earns"
LST_KEYS_SHOW_EARNINGS = ['user_id']
LST_KEYS_SHOW_EARNINGS_RESP = env.LST_KEYS_REG_SHILLER_RESP
DB_PROC_GET_USR_EARNS = 'GET_USER_EARNINGS'
    # select * from 'user_earns' where 'user_earns.fk_user_id=user_id'

# '/request_cashout'
kREQUEST_CASHOUT = "request_user_earns_cashout"
LST_KEYS_REQUEST_CASHOUT = ['user_id']
LST_KEYS_REQUEST_CASHOUT_RESP = env.LST_KEYS_REG_SHILLER_RESP
DB_PROC_REQUEST_CASHOUT = 'SET_USER_WITHDRAW_REQUESTED'
    # select 'user_earns.usd_owed' for user_id (req: usd_owed >= <some-min-amnt>)
    # select 'users.wallet_address' for user_id
    # use solidity 'transfer' to send 'usd_owed' amount to 'wallet_address'
    # update 'user_earns.withdraw_request' where 'user_earns.usd_owed > 0' for user_id

# '/admin_show_user_shills'
kADMIN_SHOW_USR_SHILLS = "get_usr_shills"
LST_KEYS_USR_SHILLS = ['admin_id','user_id','approved','removed']
LST_KEYS_USR_SHILLS_RESP = env.LST_KEYS_REG_SHILLER_RESP
DB_PROC_GET_USR_SHILLS_ALL = 'GET_USER_SHILLS_ALL'
    # select * from 'shills' where 'shills.is_approved=True|False' and 'shills.is_removed=True|False' for user_id

# '/admin_list_all_pend_shills'
kADMIN_LIST_ALL_PEND_SHILLS = "get_all_pend_shills"
LST_KEYS_ALL_PEND_SHILLS = ['admin_id','removed']
LST_KEYS_ALL_PEND_SHILLS_RESP = env.LST_KEYS_REG_SHILLER_RESP
DB_PROC_GET_PEND_SHILLS = 'GET_PEND_SHILLS_ALL' # get where 'is_approved' = False
    # select * from 'shills' where 'shills.is_approved=False' for all users

# '/admin_approve_pend_shill'
kADMIN_APPROVE_SHILL = "approve_pend_shill"
LST_KEYS_APPROVE_SHILL = ['admin_id','user_id', 'shill_id','shill_plat','shill_type','pay_usd','approved']
LST_KEYS_APPROVE_SHILL_RESP = env.LST_KEYS_REG_SHILLER_RESP
DB_PROC_APPROVE_SHILL_STATUS = "UPDATE_USER_SHILL_APPR_EARNS" 
    # admin views shill_url on the web
    # set 'shills.is_approved=True|False' where 'shills.is_removed=False' for 'user_id + shill_id|url' combo
    # set 'shills.pay_usd
    # update 'user_earns.usd_total|owed' accordingly (+-) for user_id

# '/admin_view_shill_status'
kADMIN_VIEW_SHILL = "get_usr_shill"
LST_KEYS_VIEW_SHILL = ['admin_id','user_id','shill_id','shill_url']
LST_KEYS_VIEW_SHILL_RESP = env.LST_KEYS_REG_SHILLER_RESP
DB_PROC_GET_USR_SHILL = 'GET_USER_SHILL'
    # select * from 'shills' where 'shills.id|shill_url=shill_id|url' for user_id

# '/admin_pay_shill_rewards' _ NOTE: requires solidty 'transfer' call _ ** HOUSE ONLY **
kADMIN_PAY_SHILL_EARNS = "pay_usr_owed_shill_earns"
LST_KEYS_PAY_SHILL_EARNS = ['admin_id','user_id']
LST_KEYS_PAY_SHILL_EARNS_RESP = env.LST_KEYS_REG_SHILLER_RESP
DB_PROC_UPDATE_USR_PAID_EARNS = 'UPDATE_USER_SHILL_PAID_EARNS'
    # check 'user_earns.withdraw_request=True' for 'user_id'
    # validate 'user_earns.usd_owed' == 
    #   total of (select 'shills.pay_usd' where 'shills.is_paid=False' & 'shills.is_approved=True & 'shills.is_removed=False') for user_id
    # update 'user_earns.usd_owed|paid' where 'user_earns.fk_user_id=user_id'
    # update 'shills.is_paid=True' for user_id
    # then perform solidity 'transfer' call on 'users.wallet_address' for user_id

# '/admin_log_removed_shill'
kADMIN_SET_SHILL_REM = "set_shill_removed"
LST_KEYS_SET_SHILL_REM = ['admin_id','tg_user_id','shill_id','removed']
LST_KEYS_SET_SHILL_REM_RESP = env.LST_KEYS_REG_SHILLER_RESP
DB_PROC_SET_SHILL_REM = 'SET_USER_SHILL_REMOVED'
    # updated 'shills.is_removed' for 'shills.user_id + shills.shill_id|url' combo

# '/admin_scan_web_for_removed_shills' _ NOTE: requires twitter post web scrape
kADMIN_CHECK_USR_REM_SHILLS = "check_usr_removed_shills"
LST_KEYS_CHECK_USR_REM_SHILLS = ['admin_id','user_id','approved','removed']
LST_KEYS_CHECK_USR_REM_SHILLS_RESP = env.LST_KEYS_REG_SHILLER_RESP
DB_PROC_CHECK_USR_REM_SHILL = DB_PROC_GET_USR_SHILLS_ALL 
    # select post_url from 'shills' where 'shills.is_removed=False' for user_id
    # then web scrape those post_urls to see if they are still working / viewable

# '/admin_set_shiller_rate'
kADMIN_SET_USR_SHILL_PAY_RATE = "set_user_shill_pay_rate"
LST_KEYS_SET_USR_SHILL_PAY_RATE = ['admin_id','user_id','shill_play','shill_type','pay_usd']
LST_KEYS_SET_USR_SHILL_PAY_RATE_RESP = env.LST_KEYS_REG_SHILLER_RESP
DB_PROC_SET_USR_RATES = 'SET_USER_PAY_RATE'
    # update 'user_shill_rates' for user_id

#-----------------------------------------------------#
DICT_CMD_EXE = {
    "register_as_shiller":[kSHILLER_REG,LST_KEYS_REG_SHILLER,LST_KEYS_REG_SHILLER_RESP,DB_PROC_ADD_NEW_USER],
    "confirm_twitter":[kTWITTER_CONF,LST_KEYS_TW_CONF,LST_KEYS_TW_CONF_RESP,DB_PROC_RENEW_TW_CONFRIM],
    "submit_shill_link":[kSUBMIT_SHILL,LST_KEYS_SUBMIT_SHILL,LST_KEYS_SUBMIT_SHILL_RESP,DB_PROC_ADD_SHILL],
    "show_my_rates":[kSHOW_RATES,LST_KEYS_SHOW_RATES,LST_KEYS_SHOW_RATES_RESP,DB_PROC_GET_USR_RATES],
    "show_my_earnings":[kSHOW_EARNINGS,LST_KEYS_SHOW_EARNINGS,LST_KEYS_SHOW_EARNINGS_RESP,DB_PROC_GET_USR_EARNS],
    "request_cashout":[kREQUEST_CASHOUT,LST_KEYS_REQUEST_CASHOUT,LST_KEYS_REQUEST_CASHOUT_RESP,DB_PROC_REQUEST_CASHOUT],
    "admin_show_user_shills":[kADMIN_SHOW_USR_SHILLS,LST_KEYS_USR_SHILLS,LST_KEYS_USR_SHILLS_RESP,DB_PROC_GET_USR_SHILLS_ALL],
    "admin_list_all_pend_shills":[kADMIN_LIST_ALL_PEND_SHILLS,LST_KEYS_ALL_PEND_SHILLS,LST_KEYS_ALL_PEND_SHILLS_RESP,DB_PROC_GET_PEND_SHILLS],
    "admin_approve_pend_shill":[kADMIN_APPROVE_SHILL,LST_KEYS_APPROVE_SHILL,LST_KEYS_APPROVE_SHILL_RESP,DB_PROC_APPROVE_SHILL_STATUS],
    "admin_view_shill_status":[kADMIN_VIEW_SHILL,LST_KEYS_VIEW_SHILL,LST_KEYS_VIEW_SHILL_RESP,DB_PROC_GET_USR_SHILL],
    "admin_pay_shill_rewards":[kADMIN_PAY_SHILL_EARNS,LST_KEYS_PAY_SHILL_EARNS,LST_KEYS_PAY_SHILL_EARNS_RESP,DB_PROC_UPDATE_USR_PAID_EARNS],
    "admin_log_removed_shill":[kADMIN_SET_SHILL_REM,LST_KEYS_SET_SHILL_REM,LST_KEYS_SET_SHILL_REM_RESP,DB_PROC_SET_SHILL_REM],
    "admin_scan_web_for_removed_shills":[kADMIN_CHECK_USR_REM_SHILLS,LST_KEYS_CHECK_USR_REM_SHILLS,LST_KEYS_CHECK_USR_REM_SHILLS_RESP,DB_PROC_CHECK_USR_REM_SHILL],
    'admin_set_shiller_rates':[kADMIN_SET_USR_SHILL_PAY_RATE,LST_KEYS_SET_USR_SHILL_PAY_RATE,LST_KEYS_SET_USR_SHILL_PAY_RATE_RESP,DB_PROC_SET_USR_RATES],
}

#=====================================================#
#         request handler accessors/mutators          #
#=====================================================#
def exe_tg_cmd(_lst_inp, _use_prod_accts):
    funcname = f'{__filename} exe_tg_cmd(_use_prod_accts={_use_prod_accts})'
    print(funcname+' - ENTER')

    # set twitter support keys for this request
    set_twitter_auth_keys(_use_prod_accts)

    # generate keyVals to pass as 'request' w/ 'tg_cmd!=None', to 'handle_request'
    tg_cmd = _lst_inp[0]
    keyVals = {}
    for i,v in enumerate(_lst_inp): 
        print(f' _lst_inp[{i}]={v}')
        if i == 0: continue # skip _lst_inp[0] == tg_cmd
        keyVals[DICT_CMD_EXE[tg_cmd][1][i]] = v # [tg_cmd][1] = LST_KEYS_...

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
    jsonResp = prepJsonResponseDbProc(arrStrReturnKeys, dbProcResult, strRespSuccessMSG, tprint=False)
    
    # (5) return client response
    return jsonResp # JSONResponse(...) -> Response(json.dumps(dict), mimetype="application/json" )
    
def parse_request(request, req_handler_key, tg_cmd=None): # (1)
    funcname = f'{__filename} parse_request'
    print(funcname + ' - ENTER')
    
    if tg_cmd:
        keyVals = dict(request)
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
    validParams0 = validate_params(keyVals, req_handler_key)
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
# append req_handler_key, parse keyVals params, invoke database function
def execute_db_calls(keyVals, req_handler_key, tg_cmd=None): # (2)
    funcname = f'{__filename} execute_db_calls'
    print(funcname + ' - ENTER')

    # perfom database executions
    bErr=False
    jsonResp={}
    dbProcResult = None

    if tg_cmd != None:
        if tg_cmd in DICT_CMD_EXE.keys():
            if tg_cmd == 'register_as_shiller' or tg_cmd == 'confirm_twitter' and not valid_trinity_tweet(keyVals['trinity_tw_url']):
                dbProcResult=-1
                bErr, jsonResp = prepJsonResponseDbProcErr(dbProcResult, tprint=True)
                return bErr, jsonResp, dbProcResult
                            
            # if 'user_id' in keyVals: del keyVals['user_id']
            stored_proc = DICT_CMD_EXE[tg_cmd][3] # [tg_cmd][3] = 'stored-proc-name'
            dbProcResult = exe_stored_proc(-1, stored_proc, keyVals)
            bErr, jsonResp = prepJsonResponseDbProcErr(dbProcResult, tprint=True)
        else:
            dbProcResult=-1
            bErr, jsonResp = prepJsonResponseDbProcErr(dbProcResult, tprint=True)
    else:
        pass # http request integration
    
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
        pass # http request integration
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
def valid_trinity_tweet(_tw_url):
    full_text = get_tweet_text(_tw_url)
    full_text = '' if not full_text else full_text                
    lst_text = full_text.lower().split()
    if '@bearsharesnft' not in lst_text or 'trinity' not in lst_text:
        dbProcResult=-1
        bErr, jsonResp = prepJsonResponseDbProcErr(dbProcResult, tprint=True)
        return bErr, jsonResp, dbProcResult

def get_tweet_text(_tw_url):
    global CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
    funcname = f'get_tweet_text({_tw_url})'
    print(cStrDivider_1, f'ENTER - {funcname}', sep='\n')

    # Authenticate to Twitter
    # client = tweepy.Client(
    #     consumer_key=CONSUMER_KEY,
    #     consumer_secret=CONSUMER_SECRET,
    #     access_token=ACCESS_TOKEN,
    #     access_token_secret=ACCESS_TOKEN_SECRET
    # )
    auth = tweepy.OAuth1UserHandler(
        CONSUMER_KEY,
        CONSUMER_SECRET,
        ACCESS_TOKEN,
        ACCESS_TOKEN_SECRET,
    )

    # Create API object
    api = tweepy.API(auth, wait_on_rate_limit=True)
    # Extract tweet ID from the URL
    tweet_id = tweet_url.split('/')[-1]
    
    try:
        # Fetch the tweet
        tweet = api.get_status(tweet_id, tweet_mode='extended')
        
        # Extract and return the tweet text
        return tweet.full_text
    except tweepy.TweepError as e:
        print(f"tweepy.TweepError: {e}")
        return None

def set_twitter_auth_keys(_use_prod_accts):
    global CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
    if _use_prod_accts:
        # @BearSharesNFT
        CONSUMER_KEY = env.CONSUMER_KEY_1
        CONSUMER_SECRET = env.CONSUMER_SECRET_1
        ACCESS_TOKEN = env.ACCESS_TOKEN_1
        ACCESS_TOKEN_SECRET = env.ACCESS_TOKEN_SECRET_1
    else:
        # @SolAudits
        CONSUMER_KEY = env.CONSUMER_KEY_0
        CONSUMER_SECRET = env.CONSUMER_SECRET_0
        ACCESS_TOKEN = env.ACCESS_TOKEN_0
        ACCESS_TOKEN_SECRET = env.ACCESS_TOKEN_SECRET_0

#====================================================#
#====================================================#

print(__filename, f"\n CLASSES & FUNCTIONS initialized:- STARTING -> additional '{__filename}' run scripts (if applicable) . . .")
print(__filename, f"\n  DONE Executing additional '{__filename}' run scripts ...")
print('#======================================================================#')
