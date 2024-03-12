__fname = 'trinity_bot'
__filename = __fname + '.py'
cStrDivider = '#================================================================#'
cStrDivider_1 = '#----------------------------------------------------------------#'
print('', cStrDivider, f'GO _ {__filename} -> starting IMPORTs & declaring globals', cStrDivider, sep='\n')

#------------------------------------------------------------#
#   IMPORTS                                                  #
#------------------------------------------------------------#
# import random, 
from _env import env
import time, os, traceback, sys, json, pprint
from datetime import datetime
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters

import req_handler

#------------------------------------------------------------#
#   GLOBALS                                                  #
#------------------------------------------------------------#
# constants
LST_TG_CMDS = req_handler.DICT_CMD_EXE.keys()
WHITELIST_CHAT_IDS = [
    '-1002041092613', # $BearShares
    '-1002049491115', # $BearShares - testing
    # '-4139183080', # ?
    '-1001941928043', # TeddyShares - testing
    ]
BLACKLIST_TEXT = [
    'smart vault', 'smart-vault', 'smart_vault', # @JstKidn
    ]

# input select
USE_PROD_TG = False
TOKEN = 'nil_tg_token'
USE_ALT_ACCT = False # True = alt user 'LAO Pirates'

#------------------------------------------------------------#
#   FUNCTIONS                                                #
#------------------------------------------------------------#
def set_tg_token():
    global TOKEN
    # TOKEN = env.TOKEN_prod if USE_PROD_TG else env.TOKEN_dev
    TOKEN = env.TOKEN_prod if USE_PROD_TG else env.TOKEN_trin

def is_valid_chat_id(_chat_id, _group_name, _uname, _handle):
    print("chat_id:", _chat_id)
    if _group_name: print("Group name:", _group_name)
    else: print("*NOTE* This message was not sent from a group.")
    if str(_chat_id) not in WHITELIST_CHAT_IDS: # check whitelisted groups
        print("*** WARNING ***: non-whitelist TG group trying to use the bot; sending deny message...")
        str_deny = f"@{_uname} (aka. {_handle}): ... not authorized"
        print(str_deny)
        return False, str_deny
    return True, ''

def filter_prompt(_prompt):
    funcname = 'filter_prompt'
    # print(f'ENTER - {funcname}')
    prompt_edit = _prompt.lower()
    found_blacklist = False
    print("Checking '_prompt' for BLACKLIST_TEXT...")
    for i in BLACKLIST_TEXT:
        print(' [X] '+i)
        if i in prompt_edit:
            print(f'  found BLACKLIST_TEXT: {i} ... (editing & continue)')
            prompt_edit = prompt_edit.replace(i, 'bear shares')
            found_blacklist = True

    if found_blacklist:
        return prompt_edit
    return _prompt
    
async def cmd_handler(update: Update, context):
    global USE_ALT_ACCT
    funcname = 'cmd_handler'
    print(cStrDivider_1, f'ENTER - {funcname} _ {get_time_now()}', sep='\n')
    group_name = update.message.chat.title if update.message.chat.type == 'supergroup' else None
    _chat_id = update.message.chat_id

    user = update.message.from_user
    uid = user.id
    uname_at = user.username
    uname_handle = user.first_name
    # uname_handle = user.first_name + ' ' + user.last_name
    inp_split = update.message.text.split()

    # check if TG group is whitelisted to use (prints group info and deny)
    #   NOTE: at this point, inp_split[0] is indeed a valid command
    print(f'handling cmd: '+inp_split[0])
    tg_cmd = inp_split[0][1::] # parses out the '/'
    valid_chat, str_deny = is_valid_chat_id(str(_chat_id), group_name, uname_at, uname_handle)
    # print(valid_cmd, valid_chat, str_deny, sep='\n')
    if not valid_chat:
        await context.bot.send_message(chat_id=update.message.chat_id, text=str_deny+' '+inp_split[0])    
        print('', f'EXIT - {funcname} _ {get_time_now()}', cStrDivider_1, sep='\n')
        return

    # ex tweet_conf (fails): https://x.com/SolAudits/status/1765925371851972744?s=20 # only '@BearSharesNFT'
    # ex tweet_conf (valid): https://x.com/SolAudits/status/1765925225844089300?s=20
    # ex tweet_conf (valid): https://x.com/SolAudits/status/1766554515094778118?s=20
    # ex tweet_conf (valid): https://x.com/SolAudits/status/1766580860604571739?s=20
    # ex tweet_conf (valid): https://x.com/SolAudits/status/1766584748527247440?s=20
    # ex tweet_conf (valid): https://x.com/SolAudits/status/1766586177438564670?s=20

    # ex tweet_shill (fails): https://x.com/TopGunHexadian/status/1766339571342553408?s=20
    # ex tweet_shill (valid): https://x.com/SolAudits/status/1766663759961940205?s=20
    
    # NOTE: all non-admin db procs require 'tg_user_id' & 'tg_user_at' (ie. uid & uname_at)
    if 'admin' not in tg_cmd:
        inp_split.insert(1, uid)
        inp_split.insert(2, uname_at)
        if USE_ALT_ACCT: 
                inp_split[1] = '1058890141'
                inp_split[2] = 'laycpirates'

        # handle cmds that need more data
        if tg_cmd == 'register_as_shiller':
            if USE_ALT_ACCT: 
                inp_split.insert(3, 'LAO Pirates')
            else:
                inp_split.insert(3, uname_handle)
        
        if tg_cmd == 'request_cashout': # ['user_id','user_at']
            # NOTE: inp_split[1] should be 'uid'
            # NOTE: inp_split[2] should be 'uname_at'
            # NOTE: TODO
            pass

        if tg_cmd == 'show_my_rates': # ['user_id','user_at','platform']
            # NOTE: inp_split[1] should be 'uid'
            # NOTE: inp_split[2] should be 'uname_at'
            inp_split.insert(3, 'twitter') # const: unknown, twitter, tiktok, reddit

        # if tg_cmd == 'show_my_earnings': # ['user_id','user_at']
        #     # NOTE: inp_split[1] should be 'uid'
        #     # NOTE: inp_split[2] should be 'uname_at'
        #     pass

    # NOTE: all admin db procs require 'tg_admin_id' & 'tg_user_at' (ie. uid & <tg_user_at>)    
    else: # if 'admin' in tg_cmd
        inp_split.insert(1, uid)

        if tg_cmd == 'admin_show_user_rates': # ['admin_id','user_id','platform']
            # NOTE: inp_split[1] should be 'uid'
            # NOTE: inp_split[2] should be '<tg_user_at>'
            inp_split.insert(3, 'twitter') # const: unknown, twitter, tiktok, reddit

        # if tg_cmd == 'admin_show_user_earnings': # ['admin_id','user_id']
        #     # NOTE: inp_split[1] should be 'uid'
        #     # NOTE: inp_split[2] should be '<tg_user_at>'
        #     pass


    print(f'GO - req_handler.exe_tg_cmd ... {get_time_now()}')
    response = req_handler.exe_tg_cmd(inp_split, USE_PROD_TG)
    response_dict = json.loads(response.get_data(as_text=True))
    print(f'GO - req_handler.exe_tg_cmd ... {get_time_now()} _ DONE')

    print('\nprinting response_dict ...')
    pprint.pprint(response_dict)
    # print(response_dict)

    # return jsonResp # JSONResponse(...) -> Response(json.dumps(dict), mimetype="application/json" )
    if int(response_dict['ERROR']) > 0:
        err_num = response_dict['ERROR']
        err_msg = response_dict['MSG']
        await update.message.reply_text(f"err_{err_num}: {err_msg}")
    else:
        d_resp = response_dict['PAYLOAD']['result_arr'][0]
        # [print(k, d_resp[k]) for k in d_resp.keys()]

        if tg_cmd == 'register_as_shiller':
            str_r = f"user: {d_resp['tg_user_at']}\n wallet: {d_resp['wallet_address_inp']}\n twitter: {d_resp['tw_user_at']}\n twitter_conf: {d_resp['tw_conf_url']}"
            lst_d_resp = response_dict['PAYLOAD']['result_arr']
            for d in lst_d_resp:
                str_r = str_r + f"\n {d['platform']} pay_usd_{d['type_descr']}: {d['pay_usd']}"
            await update.message.reply_text(f"Shiller Registration Successfull! ...\n {str_r}")
        elif tg_cmd == 'confirm_twitter':
            await update.message.reply_text(f"Twitter confirmation updated successfully!")
        elif tg_cmd == 'submit_shill_link':
            await update.message.reply_text(f"Shilled tweet submitted for approval! Thanks!")
        elif tg_cmd == 'show_my_rates' or tg_cmd == 'admin_show_user_rates':   
            ommit_ = ['status','info','user_id','tg_user_id_inp','platform_inp']
            str_r = '\n '.join([str(k)+': '+str(round(float(d_resp[k]), 3)) for k in d_resp.keys() if str(k) not in ommit_])
            await update.message.reply_text(f"Your current rates (per tweet) ...\n {str_r}")
        elif tg_cmd == 'show_my_earnings' or tg_cmd == 'admin_show_user_earnings':
            inc_ = ['usd_total','usd_paid','usd_owed','wallet_address','withdraw_requested']
            str_r = '\n '.join([str(k)+': '+str(d_resp[k]) for k in d_resp.keys() if str(k) in inc_])
            await update.message.reply_text(f"Your current earnings ...\n {str_r}")
        else:
            await update.message.reply_text(f"'/{tg_cmd}' Executed Successfully! _ ")
        
    print('', f'EXIT - {funcname} _ {get_time_now()}', cStrDivider_1, sep='\n')

async def log_activity(update: Update, context):
    user = update.message.from_user
    uid = str(user.id)
    usr_at_name = f'@{user.username}'
    usr_handle = user.first_name
    inp = update.message.text
    lst_user_data = [uid, usr_at_name, usr_handle]
    print(f'{get_time_now()} _ activity : {lst_user_data}')

async def test(update, context):
    funcname = 'test'
    print(f'\nENTER - {funcname}\n')
    await context.bot.send_message(chat_id=update.message.chat_id, text="test successful")

def main():
    # global TOKEN
    # create dispatcher with TG bot token
    dp = Application.builder().token(TOKEN).build()

    # Register command handlers
    # dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("test", test))

    # register all commands -> from req_handler.DICT_CMD_EXE.keys()
    for str_cmd in LST_TG_CMDS:
        dp.add_handler(CommandHandler(str_cmd, cmd_handler))
        lst_params = req_handler.DICT_CMD_EXE[str_cmd][1]
        print(f'added cmd: {str_cmd}: {lst_params}')
        # print(f'{str_cmd} - ')

    # Add message handler for ALL messages
    #   ref: https://docs.python-telegram-bot.org/en/stable/telegram.ext.filters.html#filters-module
    dp.add_handler(MessageHandler(filters.ALL, log_activity))
    print('added handler ALL: log_activity')

    # Start the Bot
    print('\nbot running ...\n')
    dp.run_polling()

    

#------------------------------------------------------------#
#   DEFAULT SUPPORT                                          #
#------------------------------------------------------------#
READ_ME = f'''
    *DESCRIPTION*
        nil

    *NOTE* INPUT PARAMS...
        nil
        
    *EXAMPLE EXECUTION*
        $ python3 {__filename} -<nil> <nil>
        $ python3 {__filename}
'''

#ref: https://stackoverflow.com/a/1278740/2298002
def print_except(e, debugLvl=0):
    #print(type(e), e.args, e)
    if debugLvl >= 0:
        print('', cStrDivider, f' Exception Caught _ e: {e}', cStrDivider, sep='\n')
    if debugLvl >= 1:
        print('', cStrDivider, f' Exception Caught _ type(e): {type(e)}', cStrDivider, sep='\n')
    if debugLvl >= 2:
        print('', cStrDivider, f' Exception Caught _ e.args: {e.args}', cStrDivider, sep='\n')
    if debugLvl >= 3:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        strTrace = traceback.format_exc()
        print('', cStrDivider, f' type: {exc_type}', f' file: {fname}', f' line_no: {exc_tb.tb_lineno}', f' traceback: {strTrace}', cStrDivider, sep='\n')

def wait_sleep(wait_sec : int, b_print=True, bp_one_line=True): # sleep 'wait_sec'
    print(f'waiting... {wait_sec} sec')
    for s in range(wait_sec, 0, -1):
        if b_print and bp_one_line: print(wait_sec-s+1, end=' ', flush=True)
        if b_print and not bp_one_line: print('wait ', s, sep='', end='\n')
        time.sleep(1)
    if bp_one_line and b_print: print() # line break if needed
    print(f'waiting... {wait_sec} sec _ DONE')

def get_time_now(dt=True):
    if dt: return '['+datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[0:-4]+']'
    return '['+datetime.now().strftime("%H:%M:%S.%f")[0:-4]+']'

def read_cli_args():
    print(f'\nread_cli_args...\n # of args: {len(sys.argv)}\n argv lst: {str(sys.argv)}')
    for idx, val in enumerate(sys.argv): print(f' argv[{idx}]: {val}')
    print('read_cli_args _ DONE\n')
    return sys.argv, len(sys.argv)

if __name__ == "__main__":
    ## start ##
    RUN_TIME_START = get_time_now()
    print(f'\n\nRUN_TIME_START: {RUN_TIME_START}\n'+READ_ME)
    lst_argv_OG, argv_cnt = read_cli_args()
    # USE_ALT_ACCT = len(lst_argv_OG) > 1 # True = alt user 'LAO Pirates'
    
    ## exe ##
    try:
        # select to use prod bot or dev bot
        inp = input('\nSelect token type to use:\n  0 = prod (@BearSharesBot)\n  1 = dev \n  > ')
        USE_PROD_TG = True if inp == '0' else False
        print(f'  input = {inp} _ USE_PROD_TG = {USE_PROD_TG}')

        inp = input('\nUse alt tg_user_id ("LAO Pirates")? [y/n]:\n  > ')
        USE_ALT_ACCT = True if inp.lower() == 'y' or inp.lower() == '1' else False
        print(f'  input = {inp} _ USE_ALT_ACCT = {USE_ALT_ACCT}')

        set_tg_token()  
        print(f'\nUSE_PROD_TG: {USE_PROD_TG}')
        print(f'USE_ALT_ACCT: {USE_ALT_ACCT}')
        print(f'Telegram TOKEN: {TOKEN}\n')
        # print(f'OpenAI OPENAI_KEY: {OPENAI_KEY}')
        # print(f'CONSUMER_KEY: {CONSUMER_KEY}')
        # print(f'PROMO_TWEET_TEXT:\n{PROMO_TWEET_TEXT}\n')    
        main()
    except Exception as e:
        print_except(e, debugLvl=0)
    
    ## end ##
    print(f'\n\nRUN_TIME_START: {RUN_TIME_START}\nRUN_TIME_END:   {get_time_now()}\n')

print('', cStrDivider, f'# END _ {__filename}', cStrDivider, sep='\n')