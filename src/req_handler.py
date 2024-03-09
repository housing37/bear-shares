__fname = 'req_handler'
__filename = __fname + '.py'
cStrDivider = '#================================================================#'
cStrDivider_1 = '#----------------------------------------------------------------#'
print('', cStrDivider, f'GO _ {__filename} -> starting IMPORTs & declaring globals', cStrDivider, sep='\n')

#=====================================================#
#         imports                                     #
#=====================================================#
from _env import env
from db_controller import *
from req_helpers import *
from datetime import datetime
import json

# twitter support
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

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
#-----------------------------------------------------#
#   TRINITY
#-----------------------------------------------------#
# '/register_as_shiller'
kSHILLER_REG = "register_as_shiller"
LST_REG_USER_PARAMS = ['<wallet_address>', '<tweet_url>']
STR_REG_USER_ERR = f'Please tweet "@BearSharesNFT trinity" 👍️️️️️️\n Then use that link to register with cmd:\n /{kSHILLER_REG} {" ".join(LST_REG_USER_PARAMS)}'
LST_KEYS_REG_USER = ['user_id','user_at','user_handle','wallet_address','trinity_tw_url']
LST_KEYS_REG_USER_RESP = env.LST_KEYS_PLACEHOLDER
DB_PROC_ADD_NEW_USER = 'ADD_NEW_TG_USER'
    # PRE-DB: validate 'trinity_tw_url' contains texts '@BearSharesNFT' & 'trinity'

# '/confirm_twitter'
kTWITTER_CONF = "validate_twitter"
LST_KEYS_TW_CONF = ['user_id', 'trinity_tw_url']
LST_KEYS_TW_CONF_RESP = env.LST_KEYS_PLACEHOLDER
DB_PROC_RENEW_TW_CONFRIM = 'UPDATE_TWITTER_CONF'
    # PRE-DB: validate 'trinity_tw_url' contains texts '@BearSharesNFT' & 'trinity'

# '/submit_shill_link'
kSUBMIT_SHILL = "add_new_shill"
LST_KEYS_SUBMIT_SHILL = ['user_id', 'post_url']
LST_KEYS_SUBMIT_SHILL_RESP = env.LST_KEYS_PLACEHOLDER
DB_PROC_ADD_SHILL = 'ADD_USER_SHILL_TW'

# '/show_my_rates'
kSHOW_RATES = "get_user_rates"
LST_KEYS_SHOW_RATES = ['user_id', 'platform'] # const: unknown, twitter, tiktok, reddit
LST_KEYS_SHOW_RATES_RESP = env.LST_KEYS_PLACEHOLDER
DB_PROC_GET_USR_RATES = 'GET_USER_PAY_RATES'

# '/show_my_earnings'
kSHOW_EARNINGS = "get_user_earns"
LST_KEYS_SHOW_EARNINGS = ['user_id']
LST_KEYS_SHOW_EARNINGS_RESP = env.LST_KEYS_PLACEHOLDER
DB_PROC_GET_USR_EARNS = 'GET_USER_EARNINGS'

# '/request_cashout'
kREQUEST_CASHOUT = "request_user_earns_cashout"
LST_KEYS_REQUEST_CASHOUT = ['user_id']
LST_KEYS_REQUEST_CASHOUT_RESP = env.LST_KEYS_PLACEHOLDER
DB_PROC_REQUEST_CASHOUT = 'SET_USER_WITHDRAW_REQUESTED'
    # POST-DB: python TG notify admin_pay to process
	# POST-DB: python TG notify p_tg_user_id that request has been submit (w/ user_earns.usd_owed)

# '/admin_show_user_shills'
kADMIN_SHOW_USR_SHILLS = "get_usr_shills"
LST_KEYS_USR_SHILLS = ['admin_id','user_id','approved','removed']
LST_KEYS_USR_SHILLS_RESP = env.LST_KEYS_PLACEHOLDER
DB_PROC_GET_USR_SHILLS_ALL = 'GET_USER_SHILLS_ALL'

# '/admin_list_all_pend_shills'
kADMIN_LIST_ALL_PEND_SHILLS = "get_all_pend_shills"
LST_KEYS_ALL_PEND_SHILLS = ['admin_id','removed']
LST_KEYS_ALL_PEND_SHILLS_RESP = env.LST_KEYS_PLACEHOLDER
DB_PROC_GET_PEND_SHILLS = 'GET_PEND_SHILLS_ALL' # get where 'is_approved' = False

# '/admin_approve_pend_shill'
kADMIN_APPROVE_SHILL = "approve_pend_shill"
LST_KEYS_APPROVE_SHILL = ['admin_id','user_id', 'shill_id','shill_plat','shill_type','pay_usd','approved']
LST_KEYS_APPROVE_SHILL_RESP = env.LST_KEYS_PLACEHOLDER
DB_PROC_APPROVE_SHILL_STATUS = "UPDATE_USER_SHILL_APPR_EARNS" 
    # PRE-DB: admin views / inspects shill_url on the web (determines: plat, type, pay, approve)
    # POST-DB: python TG message to shiller confirming approval & earnings updated (w/ shill url, shill type, pay_usd)

# '/admin_view_shill_status'
kADMIN_VIEW_SHILL = "get_usr_shill"
LST_KEYS_VIEW_SHILL = ['admin_id','user_id','shill_id','shill_url']
LST_KEYS_VIEW_SHILL_RESP = env.LST_KEYS_PLACEHOLDER
DB_PROC_GET_USR_SHILL = 'GET_USER_SHILL'

# '/admin_pay_shill_rewards' _ NOTE: requires solidty 'transfer' call _ ** HOUSE ONLY **
kADMIN_PAY_SHILL_EARNS = "pay_usr_owed_shill_earns"
LST_KEYS_PAY_SHILL_EARNS = ['admin_id','user_id']
LST_KEYS_PAY_SHILL_EARNS_RESP = env.LST_KEYS_PLACEHOLDER
DB_PROC_SET_USR_PAY_SUBMIT = 'SET_USER_PAY_TX_SUBMIT' # -> get_usr_pay_usd_appr_sum, set_usr_pay_usd_tx_submit
    # POST-DB: perform python/solidity 'transfer(user_earns.usd_owed, wallet_address)' to get tx data for DB_PROC_SET_USR_PAY_CONF
    #	        get 'wallet_address' from 'GET_USER_EARNINGS(tg_user_id)'
LST_KEYS_PAY_SHILL_EARNS_CONF = ['admin_id','user_id','chain_usd_paid','tx_hash','tx_status','tok_addr','tok_symb','tok_amnt']
DB_PROC_SET_USR_PAY_CONF = 'SET_USER_PAY_TX_STATUS' # -> set_usr_pay_usd_tx_status
    # PRE-DB: perform python/solidity 'transfer' to get tx data for DB_PROC_SET_USR_PAY_CONF

# '/admin_log_removed_shill'
kADMIN_SET_SHILL_REM = "set_shill_removed"
LST_KEYS_SET_SHILL_REM = ['admin_id','tg_user_id','shill_id','removed']
LST_KEYS_SET_SHILL_REM_RESP = env.LST_KEYS_PLACEHOLDER
DB_PROC_SET_SHILL_REM = 'SET_USER_SHILL_REMOVED'

# '/admin_scan_web_for_dead_shills' _ NOTE: requires twitter post web scrape
kADMIN_CHECK_USR_REM_SHILLS = "check_usr_removed_shills"
LST_KEYS_CHECK_USR_REM_SHILLS = ['admin_id','user_id','approved','removed']
LST_KEYS_CHECK_USR_REM_SHILLS_RESP = env.LST_KEYS_PLACEHOLDER
DB_PROC_CHECK_USR_REM_SHILL = DB_PROC_GET_USR_SHILLS_ALL 
    # POST-DB: web scrape those post_urls to see if they are still working / viewable

# '/admin_set_shiller_rate'
kADMIN_SET_USR_SHILL_PAY_RATE = "set_user_shill_pay_rate"
LST_KEYS_SET_USR_SHILL_PAY_RATE = ['admin_id','user_id','shill_plat','shill_type','pay_usd']
LST_KEYS_SET_USR_SHILL_PAY_RATE_RESP = env.LST_KEYS_PLACEHOLDER
DB_PROC_SET_USR_RATES = 'SET_USER_PAY_RATE'

#-----------------------------------------------------#
#   NEO
#-----------------------------------------------------#
# '/blacklist_user'
kADD_BLACKLIST_SCAMMER = "add_user_to_blacklist_scammers"
LST_KEYS_ADD_BLACKLIST_SCAMMER = ['admin_or_user_id','bl_user_id','bl_user_at','bl_user_handle','tg_chan_id']
LST_KEYS_ADD_BLACKLIST_SCAMMER_RESP = env.LST_KEYS_PLACEHOLDER
DB_PROC_ADD_BLACKLIST_SCAMMER = 'ADD_REQUEST_USER_BLACKLIST'

# LEFT OFF HERE ... need endpoint for neo to check if a user is blacklisted (instead of using array in neo_bot.py)

#-----------------------------------------------------#
DICT_CMD_EXE = {
    "register_as_shiller":[kSHILLER_REG,LST_KEYS_REG_USER,LST_KEYS_REG_USER_RESP,DB_PROC_ADD_NEW_USER,LST_REG_USER_PARAMS,STR_REG_USER_ERR],
    "confirm_twitter":[kTWITTER_CONF,LST_KEYS_TW_CONF,LST_KEYS_TW_CONF_RESP,DB_PROC_RENEW_TW_CONFRIM],
    "submit_shill_link":[kSUBMIT_SHILL,LST_KEYS_SUBMIT_SHILL,LST_KEYS_SUBMIT_SHILL_RESP,DB_PROC_ADD_SHILL],
    "show_my_rates":[kSHOW_RATES,LST_KEYS_SHOW_RATES,LST_KEYS_SHOW_RATES_RESP,DB_PROC_GET_USR_RATES],
    "show_my_earnings":[kSHOW_EARNINGS,LST_KEYS_SHOW_EARNINGS,LST_KEYS_SHOW_EARNINGS_RESP,DB_PROC_GET_USR_EARNS],
    "request_cashout":[kREQUEST_CASHOUT,LST_KEYS_REQUEST_CASHOUT,LST_KEYS_REQUEST_CASHOUT_RESP,DB_PROC_REQUEST_CASHOUT],
    "admin_show_user_shills":[kADMIN_SHOW_USR_SHILLS,LST_KEYS_USR_SHILLS,LST_KEYS_USR_SHILLS_RESP,DB_PROC_GET_USR_SHILLS_ALL],
    "admin_list_all_pend_shills":[kADMIN_LIST_ALL_PEND_SHILLS,LST_KEYS_ALL_PEND_SHILLS,LST_KEYS_ALL_PEND_SHILLS_RESP,DB_PROC_GET_PEND_SHILLS],
    "admin_approve_pend_shill":[kADMIN_APPROVE_SHILL,LST_KEYS_APPROVE_SHILL,LST_KEYS_APPROVE_SHILL_RESP,DB_PROC_APPROVE_SHILL_STATUS],
    "admin_view_shill_status":[kADMIN_VIEW_SHILL,LST_KEYS_VIEW_SHILL,LST_KEYS_VIEW_SHILL_RESP,DB_PROC_GET_USR_SHILL],
    "admin_pay_shill_rewards":[kADMIN_PAY_SHILL_EARNS,LST_KEYS_PAY_SHILL_EARNS,LST_KEYS_PAY_SHILL_EARNS_RESP,DB_PROC_SET_USR_PAY_SUBMIT],
    "admin_log_removed_shill":[kADMIN_SET_SHILL_REM,LST_KEYS_SET_SHILL_REM,LST_KEYS_SET_SHILL_REM_RESP,DB_PROC_SET_SHILL_REM],
    "admin_scan_web_for_dead_shills":[kADMIN_CHECK_USR_REM_SHILLS,LST_KEYS_CHECK_USR_REM_SHILLS,LST_KEYS_CHECK_USR_REM_SHILLS_RESP,DB_PROC_CHECK_USR_REM_SHILL],
    'admin_set_shiller_rates':[kADMIN_SET_USR_SHILL_PAY_RATE,LST_KEYS_SET_USR_SHILL_PAY_RATE,LST_KEYS_SET_USR_SHILL_PAY_RATE_RESP,DB_PROC_SET_USR_RATES],
}

#=====================================================#
#         request handler accessors/mutators          #
#=====================================================#
def exe_tg_cmd(_lst_inp, _use_prod_accts):
    funcname = f'{__filename} exe_tg_cmd(_use_prod_accts={_use_prod_accts})'
    print(funcname+' - ENTER')

    # set twitter support keys for this request
    # set_twitter_auth_keys(_use_prod_accts)

    # generate keyVals to pass as 'request' w/ 'tg_cmd!=None', to 'handle_request'
    tg_cmd = _lst_inp[0][1::] # parse out the '/'
    lst_params = _lst_inp[1::]
    keyVals = {}
    print('tg_cmd: '+tg_cmd)
    print('lst_params: '+str(lst_params))
    print('DICT_CMD_EXE[tg_cmd][1]: '+str(DICT_CMD_EXE[tg_cmd][1]))

    # validate input cmd params count
    if len(lst_params) != len(DICT_CMD_EXE[tg_cmd][1]):
        print('** WARNING **: input cmd param count != db required param count; forcing return fail')
        str_req_params = ''.join(DICT_CMD_EXE[tg_cmd][-1])
        bErr, jsonResp = prepJsonResponseValidParams(keyVals, False, tprint=True, errMsg=f'invalid number of params; {str_req_params}') # False = force fail
        return jsonResp
    
    # generate keyVals from input cmd params
    for i,v in enumerate(lst_params): 
        print(f' lst_params[{i}]={v}')
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
    # jsonResp = prepJsonResponseDbProc(arrStrReturnKeys, dbProcResult, strRespSuccessMSG, tprint=False)
    if tg_cmd: jsonResp = prepJsonResponseDbProc_ALL(arrStrReturnKeys, dbProcResult, strRespSuccessMSG, tprint=False)
    else: jsonResp = prepJsonResponseDbProc(arrStrReturnKeys, dbProcResult, strRespSuccessMSG, tprint=False)
    
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
            if (tg_cmd == 'register_as_shiller' or tg_cmd == 'confirm_twitter') and not valid_trinity_tweet(keyVals['trinity_tw_url']):
                dbProcResult=-1
                # bErr, jsonResp = prepJsonResponseDbProcErr(dbProcResult, tprint=True)
                bErr, jsonResp = prepJsonResponseValidParams(keyVals, False, tprint=True, errMsg='invalid tweet confirmation url') # False = force fail
                return bErr, jsonResp, dbProcResult
                            
            # if 'user_id' in keyVals: del keyVals['user_id']
            stored_proc = DICT_CMD_EXE[tg_cmd][3] # [tg_cmd][3] = 'stored-proc-name'
            dbProcResult = exe_stored_proc(-1, stored_proc, keyVals)
            bErr, jsonResp = prepJsonResponseDbProcErr(dbProcResult, tprint=True)
        else:
            dbProcResult=-1
            bErr, jsonResp = prepJsonResponseDbProcErr(dbProcResult, tprint=True)
    else:
        print('HIT - http request integration')
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
    funcname = f'{__filename} valid_trinity_tweet'
    print(funcname + ' - ENTER')
    lst_text = ['@bearsharesnft', 'trinity']
    return search_tweet_for_text(_tw_url, lst_text, True) # True = '--headless'
    
def search_tweet_for_text(tweet_url, _lst_text=[], _headless=True):
    funcname = f'{__filename} search_tweet_for_text'
    print(funcname + ' - ENTER')
    try:
        options = Options()
        print(f' using --headless={_headless}')
        if _headless:
            options.add_argument("--headless")  # Run Chrome in headless mode

            # required, else '--headless' fails
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
            options.add_argument(f"user-agent={user_agent}")
            options.add_argument("--enable-javascript")  

        # Initialize a Selenium WebDriver & get tweet_url page
        print(f' getting page: {tweet_url} _ {get_time_now(dt=False)}')
        driver = webdriver.Chrome(options=options)
        driver.get(tweet_url)
        print(f' getting page: {tweet_url} _ {get_time_now(dt=False)} _ DONE')
        
        # NOTE: when tweet 'Views' count is shown, then tweet text is shown as well
        print(f' waiting for full html body text _ {get_time_now()}')
        WebDriverWait(driver, 30).until(EC.text_to_be_present_in_element((By.TAG_NAME, 'BODY'), 'Views')) 
        print(f' waiting for full html body text _ {get_time_now()} _ DONE')        
        
        # get / search body text for '_lst_text' items
        body_text = driver.find_element(By.TAG_NAME, 'body').text
        print(f' searching body_text for items in _lst_text: {_lst_text}')
        for t in _lst_text:
            if t.lower() in body_text.lower(): 
                print(f' FOUND text: {t}')
            else:
                print(f' FAILED to find text: {t.lower()} _ returning False')
                return False
        print(f' SUCCESS found all text in _lst_text _ returning True')
        return True
        
    except Exception as e:
        print(f" Error scraping tweet: {e}")
        return False
    finally:
        # Close the browser
        driver.quit()

def get_time_now(dt=True):
    if dt: return '['+datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[0:-4]+']'
    return '['+datetime.now().strftime("%H:%M:%S.%f")[0:-4]+']'

#====================================================#
#====================================================#

print(__filename, f"\n CLASSES & FUNCTIONS initialized:- STARTING -> additional '{__filename}' run scripts (if applicable) . . .")
print(__filename, f"\n  DONE Executing additional '{__filename}' run scripts ...")
print('#======================================================================#')
