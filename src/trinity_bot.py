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
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, CallbackContext

import req_handler

# Define the timestamp representing the bot's last online time
last_online_time = time.time()  # Initialize with current time

#------------------------------------------------------------#
#   GLOBALS                                                  #
#------------------------------------------------------------#
# constants
DEBUG_LVL = 3
LST_TG_CMDS = list(req_handler.DICT_CMD_EXE.keys())
CHAT_ID_0 = '-1002041092613', # BearShares - trinity
WHITELIST_CHAT_IDS = [
    # '-1002041092613', # $BearShares
    CHAT_ID_0,
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
USE_PAYOUT_ONLY = False # True = remove 'kADMIN_PAY_SHILL_EARNS' from LST_TG_CMDS

# disable parsing '.from_user.first_name' (note_031824: db encoding errors)
DISABLE_TG_HANDLES = True 

TRINITY_INFO = '''
Greetings! I'm Trinity! I reward you for your tweets!
(DM me @bs_trinity_bot for added privacy 👍️️️️️️)

Welcome to $BST (BearSharesTrinity Token)!
$BST is a PRC20 token designed to pay you to tweet... it's that simple 🤷️️️️
$BST can be redeemed 1:1 for USD stablecoin on our web dapp
Web-Dapp: bearshares.vercel.app/trinity.html

* START EARNING NOW *
Follow these two simple steps to begin earning...
    1) Sign up by tweeting "@BearSharesX #Trinity register"
        then just share the link to that tweet in this Telegram chat
    2) Earn $BST by tweeting anything you like with "@BearSharesX" included
        then simply share the link to that tweet in this Telegram chat

    To check your earnings and request a $BST cashout...
        CMD: /trinity_show_my_earnings
        CMD: /trinity_request_cashout
        CMD: /trinity_set_wallet

NOTE: Better-Pays-More (earn more for memes, videos, etc.)
    - your pay rates increase as your tweets improve
        CMD: /trinity_show_my_rates

Questions: @housing37

*IMORTANT* 
    you need a TG @username setup to register

GLHF!
'''

#------------------------------------------------------------#
#   FUNCTIONS                                                #
#------------------------------------------------------------#
def set_tg_token():
    global TOKEN
    TOKEN = env.TOKEN_trin if USE_PROD_TG else env.TOKEN_trin_pay
    # TOKEN = env.TOKEN_trin if USE_PROD_TG else env.TOKEN_dev
    # TOKEN = env.TOKEN_prod if USE_PROD_TG else env.TOKEN_trin

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

def past_queue_limit(_msg_time, _q_sec=5*60):
    sec_diff = time.time() - _msg_time
    if sec_diff > _q_sec: print(f"Ignoring message sent more than {_q_sec} sec ago.")
    return sec_diff > _q_sec

async def cmd_handler(update: Update, context):
    # Calculate the timestamp of 5 minutes ago
    if past_queue_limit(update.message.date.timestamp()): return

    global USE_ALT_ACCT
    funcname = 'cmd_handler'
    print(cStrDivider_1, f'ENTER - {funcname} _ {get_time_now()}', sep='\n')
    
    chat_type = update.message.chat.type
    is_dm = chat_type == 'private'
    group_name = update.message.chat.title if update.message.chat.type == 'supergroup' else None
    _chat_id = update.message.chat_id

    user = update.message.from_user
    uid = user.id
    uname_at = user.username
    uname_handle = user.first_name
    # uname_handle = user.first_name + ' ' + user.last_name
    inp_split = list(update.message.text.split())

    # parse about @user (if user simply hit enter from cmd description list in TG chat)
    if '@' in inp_split[0]: inp_split[0] = inp_split[0].split('@')[0]

    # check if TG group is whitelisted to use (prints group info and deny)
    #   NOTE: at this point, inp_split[0] is indeed a valid command
    print(f'handling cmd: '+inp_split[0])
    print(f"chat_type: {chat_type}")
    tg_cmd = inp_split[0][1::] # parses out the '/'

    # fail: if not in WHITELIST_CHAT_IDS and not a DM
    valid_chat, str_deny = is_valid_chat_id(str(_chat_id), group_name, uname_at, uname_handle)
    # print(valid_cmd, valid_chat, chat_type, str_deny, sep='\n')
    if not valid_chat and not is_dm:
        await context.bot.send_message(chat_id=update.message.chat_id, text=str_deny+' '+inp_split[0])    
        print('', f'EXIT - {funcname} _ {get_time_now()}', cStrDivider_1, sep='\n')
        return

    # validate that TG @username is setup (required to participate)
    if uname_at == None:
        str_r = f'invalid TG user. You must have a TG @username setup for your account. Please add an @username to your TG account and try to register again.'
        print(str_r)
        print('', f'EXIT - {funcname} _ {get_time_now()}', cStrDivider_1, sep='\n')
        await update.message.reply_text(str_r)
    
    # NOTE: all non-admin db procs require 'tg_user_id' & 'tg_user_at' (ie. uid & uname_at)
    if 'admin' not in tg_cmd:
        inp_split.insert(1, uid)
        inp_split.insert(2, uname_at)
        if USE_ALT_ACCT: 
            # inp_split[1] = '1058890141'
            # inp_split[2] = 'laycpirates'
            inp_split[1] = '6919802491'
            inp_split[2] = 'fricardooo'

        # handle cmds that need more data
        if tg_cmd == req_handler.kSHILLER_REG: # ['<wallet_address>', '<tweet_url>']
            if DISABLE_TG_HANDLES:
                inp_split.insert(3, 'nil_disabled')
            elif USE_ALT_ACCT: 
                # inp_split.insert(3, 'LAO Pirates')
                inp_split.insert(3, 'ʀɨƈօʄʀɨƈօ👑🐉🐲')
            else:
                inp_split.insert(3, uname_handle)

        if tg_cmd == req_handler.kSHOW_USR_RATES: # ['user_id','user_at','platform']
            inp_split.insert(3, 'twitter') # const: unknown, twitter, tiktok, reddit

    # NOTE: all admin db procs require 'tg_admin_id' & 'tg_user_at' (ie. uid & <tg_user_at>)    
    else: # if 'admin' in tg_cmd
        inp_split.insert(1, uid)
        if USE_ALT_ACCT: 
            inp_split[1] = '1058890141'
            # inp_split[2] = 'laycpirates'

        # compensate for users using '@' or not
        if len(inp_split) >= 3 and inp_split[2][0] == '@': # remove '@' if there
            inp_split[2] = inp_split[2][1:]

        if tg_cmd == req_handler.kADMIN_SHOW_USR_RATES: # ['admin_id','tg_user_at','platform']
            inp_split.insert(3, 'twitter') # const: unknown, twitter, tiktok, reddit
        
        if tg_cmd == req_handler.kADMIN_SHOW_USR_SHILLS:
            # if user gave 1 param, auto add 'approved' & 'removed'
            if len(inp_split) == 3:
                inp_split.append('0') # set is_approved=False
                inp_split.append('0') # set is_remved=False

            # if user gave 2 param, auto add 'removed'
            if len(inp_split) == 4:
                inp_split.append('0') # set is_remved=False

        if tg_cmd == req_handler.kADMIN_LIST_ALL_PEND_SHILLS:
            # if user gave no params, auto add 'removed'
            if len(inp_split) == 2:
                inp_split.append('0') # set is_remved=False
        
        if tg_cmd == req_handler.kADMIN_APPROVE_SHILL:
            # if user did not give 2 params ['<tg_user_at>','<shill_id>']
            if len(inp_split) != 4:
                str_r = f'invalid cmd; please use format::\n /{tg_cmd} {" ".join(req_handler.LST_CMD_APPROVE_SHILLS_ADMIN)}'
                print(str_r)
                print('', f'EXIT - {funcname} _ {get_time_now()}', cStrDivider_1, sep='\n')
                await update.message.reply_text(str_r)
            else:
                # Creating buttons for the first step
                keyboard = [
                    [
                        InlineKeyboardButton("Level 0", callback_data='level_0'),
                        InlineKeyboardButton("Level 1", callback_data='level_1'),
                        InlineKeyboardButton("Level 2", callback_data='level_2')],
                    [
                        InlineKeyboardButton("Level 3", callback_data='level_3'),
                        InlineKeyboardButton("Level 4", callback_data='level_4'),
                        InlineKeyboardButton("Level 5", callback_data='level_5')],
                ]
                context.user_data['inp_split'] = list(inp_split)
                print('', f'EXIT - {funcname} _ {get_time_now()}', cStrDivider_1, sep='\n')
                await update.message.reply_text('Select shill pay level (used to calc payment):', reply_markup=InlineKeyboardMarkup(keyboard))
            return # invokes 'cmd_exe'
        
        if tg_cmd == req_handler.kADMIN_VIEW_SHILL: # ['<tg_user_at>','<shill_id>','<shill_url>']
            # if user gave 2 params 
            if len(inp_split) == 4:
                inp_split.append('<nil_shill_url>')

        if tg_cmd == req_handler.kADMIN_SET_SHILL_REM: # ['<tg_user_at>','<shill_id>','removed']
            # if user did not give 2 params ['<tg_user_at>','<shill_id>']
            if len(inp_split) != 4:
                str_r = f'invalid cmd; please use format::\n /{tg_cmd} {" ".join(req_handler.LST_CMD_SET_SHILL_REM_ADMIN)}'
                print(str_r)
                print('', f'EXIT - {funcname} _ {get_time_now()}', cStrDivider_1, sep='\n')
                await update.message.reply_text(str_r)
            else:
                # Creating buttons for the first step
                keyboard = [
                    [
                        InlineKeyboardButton("removed", callback_data='1'),
                    ],
                    [
                        InlineKeyboardButton("not-removed", callback_data='0'),
                    ],
                ]
                context.user_data['inp_split'] = list(inp_split)
                print('', f'EXIT - {funcname} _ {get_time_now()}', cStrDivider_1, sep='\n')
                await update.message.reply_text(f'Mark this shill as removed or not-removed?', reply_markup=InlineKeyboardMarkup(keyboard))
            return # invokes 'cmd_exe'
        
        # NOTE: 'kADMIN_PAY_SHILL_EARNS' pays out at current rate in db
        #   if admin wants to change payout, they must do so using 'kADMIN_SET_USR_SHILL_PAY_RATE', 
        #    before using 'kADMIN_APPROVE_SHILL', and then call 'kADMIN_PAY_SHILL_EARNS'
        if tg_cmd == req_handler.kADMIN_PAY_SHILL_EARNS:
            # if user did not give 3 param ['<tg_user_at>','<aux_tok_addr>',<'sel_aux_send'>]
            if len(inp_split) != 5:
                str_r = f'invalid cmd; please use format:\n /{tg_cmd} {" ".join(req_handler.LST_CMD_PAY_SHILL_ADMIN)}'
                print(str_r)
                print('', f'EXIT - {funcname} _ {get_time_now()}', cStrDivider_1, sep='\n')
                await update.message.reply_text(str_r)
                return

    context.user_data['inp_split'] = list(inp_split)
    await cmd_exe(update, context)
    print('', f'EXIT - {funcname} _ {get_time_now()}', cStrDivider_1, sep='\n')

async def btn_option_selects(update: Update, context):
    print('btn_option_selects - ENTER')
    query = update.callback_query

    inp_split = context.user_data['inp_split']
    tg_cmd = inp_split[0][1::] # parses out the '/'
    if tg_cmd == req_handler.kADMIN_APPROVE_SHILL:
        shill_type = str(query.data)
        inp_split.append('twitter') # set shill_plat='twitter'
        inp_split.append(shill_type) # set shill_type='unknown'
    if tg_cmd == req_handler.kADMIN_SET_SHILL_REM:
        is_removed = str(query.data)
        inp_split.append(is_removed) # set removed=is_removed

    context.user_data['inp_split'] = list(inp_split)
    await cmd_exe(update, context)

async def cmd_exe(update: Update, context: CallbackContext, aux_cmd=False):
    global CHAT_ID_0
    funcname = 'cmd_exe'
    print(cStrDivider_1, f'ENTER - {funcname} _ {get_time_now()}', sep='\n')
    
    inp_split = list(context.user_data['inp_split'])
    print(f'cmd_exe: '+inp_split[0])
    tg_cmd = inp_split[0][1::] # parses out the '/'
    
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

        if not update.message:
            # await update.callback_query.message.reply_text(f"err_{err_num}: {err_msg}")
            if not aux_cmd: await update.callback_query.message.reply_text(f"err_{err_num}: {err_msg}")
        else:
            str_resp = f"err_{err_num}: {err_msg}"
            if tg_cmd == req_handler.kREQUEST_CASHOUT:
                lst_resp_arr = response_dict['PAYLOAD']['dbProcResult'] if response_dict['PAYLOAD']['dbProcResult'] else [{}]
                usd_owed = lst_resp_arr[0]['usd_owed'] if 'usd_owed' in lst_resp_arr[0] else 'err'
                cashout_min = lst_resp_arr[0]['usd_withdraw_min'] if 'usd_withdraw_min' in lst_resp_arr[0] else 'err'
                str_resp = str_resp + f'\n usd_owed: {usd_owed}\n usd_cashout_min: {cashout_min}'
                # await update.message.reply_text(str_resp)
                if not aux_cmd: await update.message.reply_text(str_resp)
            else:
                # await update.message.reply_text(str_resp)
                if not aux_cmd: await update.message.reply_text(str_resp)
    else:
        d_resp = response_dict['PAYLOAD']['result_arr'][0]
        # [print(k, d_resp[k]) for k in d_resp.keys()]
        d_txt_rates = { 
                'level_0':'🙏️️️️️️ a simple hashtag',
                'level_1':'👍️️ a few words',
                'level_2':'😉️️️️️️ a nice shill',
                'level_3':'😮️️️️️️ include a meme',
                'level_4':'😘️️️️️️ include a video',
                'level_5':'🤝️️️️️️ something really nice',
                }
        d_txt_rates_alt = { 
                'pay_usd_hashtag':d_txt_rates['level_0'],
                'pay_usd_short_text':d_txt_rates['level_1'],
                'pay_usd_long_text':d_txt_rates['level_2'],
                'pay_usd_img_meme':d_txt_rates['level_3'],
                'pay_usd_short_vid':d_txt_rates['level_4'],
                'pay_usd_long_vid':d_txt_rates['level_5'],
                }
        # if tg_cmd == 'register_as_shiller':
        if tg_cmd == req_handler.kSHILLER_REG:
            # str_wallet = d_resp['wallet_address_inp'] if d_resp['wallet_address_inp'] != '0x0' else "add with -> '/trinity_set_wallet'"

            # obfuscate wallet_address
            str_wallet = d_resp['wallet_address_inp']
            if len(str_wallet) > 15:
                str_wallet = str_wallet[:6] + 'xxxxxx' + str_wallet[-4:]
            elif str_wallet == '0x0':
                str_wallet = "add with -> '/trinity_set_wallet'"
            str_r = f"user: @{d_resp['tg_user_at']}\n wallet: {str_wallet}\n twitter: @{d_resp['tw_user_at']}\n starting rates ..."
            lst_d_resp = response_dict['PAYLOAD']['result_arr']
            for d in lst_d_resp:
                str_r = str_r + f"\n   {d_txt_rates[d['type_descr']]}: ${d['pay_usd']}"
            await update.message.reply_text(f"Shiller Registration Successfull!\n {str_r}\n\nto set wallet DM @bs_trinity_bot and use '/trinity_set_wallet'")

        # elif tg_cmd == 'confirm_twitter':
        elif tg_cmd == req_handler.kTWITTER_CONF:
            await update.message.reply_text(f"Twitter confirmation updated successfully!")

        # elif tg_cmd == 'submit_shill_link':
        elif tg_cmd == req_handler.kSUBMIT_SHILL:
            await update.message.reply_text(f"Shilled tweet submitted for approval! Thanks!")

        # elif tg_cmd == 'request_cashout':
        elif tg_cmd == req_handler.kREQUEST_CASHOUT:
            lst_resp_arr = response_dict['PAYLOAD']['result_arr']
            lst_admin_tg_at = [f"@{r['tg_user_at']}" for r in lst_resp_arr if r['is_admin'] or r['is_admin_pay']]

            # obfuscate wallet_address
            for r in lst_resp_arr:
                str_wallet = r['wallet_address']
                if len(str_wallet) > 15:
                    str_wallet = str_wallet[:6] + 'xxxxxx' + str_wallet[-4:]
                r['wallet_address'] = str_wallet

            if len(lst_resp_arr) == 1: # admin invoked '/request_cashout'
                lst_user_tg_at = [f"User(TG): @{r['tg_user_at']}\n Twitter: @{r['tw_user_at']}\n usd_amnt: {r['usd_owed']}\n wallet: {r['wallet_address']}" for r in lst_resp_arr]
            else: # non-admin invoked '/request_cashout'
                lst_user_tg_at = [f"User(TG): @{r['tg_user_at']}\n Twitter: @{r['tw_user_at']}\n usd_amnt: {r['usd_owed']}\n wallet: {r['wallet_address']}" for r in lst_resp_arr if not r['is_admin'] and not r['is_admin_pay']]
            str_r = "".join(lst_user_tg_at)
            str_r = str_r + f'\n\n Notifying Admins(TG): {" ".join(lst_admin_tg_at)}'
            await update.message.reply_text(f"Cashout request submitted! ...\n {str_r}")

        # elif tg_cmd == 'show_my_rates' or tg_cmd == 'admin_show_user_rates':   
        elif tg_cmd == req_handler.kSHOW_USR_RATES or tg_cmd == req_handler.kADMIN_SHOW_USR_RATES:
            ommit_ = ['status','info','user_id','tg_user_id_inp','platform_inp']
            str_r = '\n   '.join([str(d_txt_rates_alt[k])+':      $'+str(round(float(d_resp[k]), 3)) for k in d_resp.keys() if str(k) not in ommit_])
            await update.message.reply_text(f"Your current rates (per tweet) ...\n   {str_r}")

        # elif tg_cmd == 'show_my_earnings' or tg_cmd == 'admin_show_user_earnings':
        elif tg_cmd == req_handler.kSHOW_USR_EARNS or tg_cmd == req_handler.kADMIN_SHOW_USR_EARNS:
            inc_ = ['usd_total','usd_paid','usd_owed','withdraw_requested']
            str_r = '\n '.join([str(k)+': '+str(d_resp[k]) for k in d_resp.keys() if str(k) in inc_])
            await update.message.reply_text(f"Your current earnings ...\n {str_r}")

        elif tg_cmd == req_handler.kADMIN_SHOW_USR_SHILLS:
            # get common params for str_r
            lst_resp_0 = response_dict['PAYLOAD']['result_arr'][0]
            tg_user_at = lst_resp_0['tg_user_at_inp']
            appr = 'yes' if lst_resp_0['is_approved'] else 'no'
            rem = 'yes' if lst_resp_0['is_removed'] else 'no'
            str_r = f'@{tg_user_at} | approved: {appr} | removed: {rem}'
            
            # loop through & append unique params for str_r
            lst_resp = response_dict['PAYLOAD']['result_arr']
            inc_ = ['shill_id','pay_usd','is_paid','is_approved','post_url']
            for d in lst_resp:
                str_r = str_r + '\n'
                for k in inc_:
                    v = d[k]
                    if k == 'is_paid' or k == 'is_approved' : v = bool(v)
                    str_r = str_r + f'\n {k}: {v}'
            await update.message.reply_text(f"Shill list for {str_r}")

        elif tg_cmd == req_handler.kADMIN_LIST_ALL_PEND_SHILLS:
            # loop through & append unique params for str_r
            lst_resp = response_dict['PAYLOAD']['result_arr']
            # inc_ = ['shill_id','pay_usd','is_paid','is_approved','is_removed','post_url','tg_user_at']
            inc_ = ['shill_id','post_url','tg_user_at']
            str_r = ''
            for d in lst_resp:
                str_r = str_r + '\n'
                for k in inc_:
                    v = d[k]
                    k_ = str(k)
                    # if k_ == 'is_paid' or k_ == 'is_approved' or k_ == 'is_removed' : v = bool(v)
                    if k == 'shill_id': k_ = 'Shill ID'
                    if k == 'post_url': k_ = 'Tweet'
                    if k == 'tg_user_at': 
                        k_ = 'User(TG)'
                        v = '@'+v
                    str_r = str_r + f'\n {k_}: {v}'
            
            msg_txt = f"Pending Shills (not yet approved for pay) _ cnt: {len(lst_resp)} {str_r}"            
            await update.message.reply_text(msg_txt)

        elif tg_cmd == req_handler.kADMIN_APPROVE_SHILL:
            d_resp = response_dict['PAYLOAD']['result_arr'][0]
            # inc_ = ['tg_user_at_inp','shill_id_inp','pay_usd','usd_owed','usd_paid','usd_total','shill_url','shill_type_inp']
            # d_resp['tg_user_at_inp'] = '@'+str(d_resp['tg_user_at_inp'])
            # str_r = '\n '.join([str(k)+': '+str(d_resp[k]) for k in d_resp.keys() if str(k) in inc_])
            d_resp_sel = {}
            d_resp_sel['User(TG)'] = '@' + d_resp['tg_user_at_inp']
            d_resp_sel['Shill ID'] = d_resp['shill_id_inp']
            d_resp_sel['Shill'] = d_resp['shill_url']
            d_resp_sel['Approval'] = d_resp['shill_type_inp']
            d_resp_sel['Approved Pay'] = '$' + f"{d_resp['usd_owed']:.2f}"
            d_resp_sel['total owed'] = '$' + f"{d_resp['usd_owed']:.2f}"
            d_resp_sel['total paid'] = '$' + f"{d_resp['usd_paid']:.2f}"
            d_resp_sel['total earned'] = '$' + f"{d_resp['usd_owed']:.2f}"
            str_r = '\n '.join([str(k)+': '+str(d_resp_sel[k]) for k in d_resp_sel.keys()])
            msg_txt = f"Shill has been approved for payment ...\n {str_r}"            
            await update.callback_query.message.reply_text(msg_txt) # reply to message sender

            # TODO: return tg_user_id from database (not working with @name)
            # > import telegram
            # > help(telegram.Bot.get_chat)
            # user = await context.bot.get_chat('@'+d_resp['tg_user_at_inp']) 
            # await context.bot.send_message(chat_id=user.id, text=msg_txt) # send DM to approved user
            if update.message is None or update.message.chat_id is None or str(update.message.chat_id) != str(CHAT_ID_0): # if reply_text is not to the main chat
                await context.bot.send_message(chat_id=int(CHAT_ID_0[0]), text=msg_txt) # send to CHAT_ID_0 = "BearShares - trinity"

            # LEFT OFF HERE ... need to store and return chat IDs for TG groups using the bot (and tg_user_id)

        elif tg_cmd == req_handler.kADMIN_VIEW_SHILL:
            d_resp = response_dict['PAYLOAD']['result_arr'][0]
            shill_id = d_resp['shill_id']
            inc_ = ['post_url','shill_id','pay_usd','is_approved','tg_user_at_inp','is_paid','shill_plat','shill_type']
            d_resp['tg_user_at_inp'] = '@'+str(d_resp['tg_user_at_inp'])
            str_r = '\n '.join([str(k)+': '+str(d_resp[k]) for k in d_resp.keys() if str(k) in inc_])
            await update.message.reply_text(f"Info for shill id: {shill_id} ...\n {str_r}")

        elif tg_cmd == req_handler.kADMIN_SET_SHILL_REM:
            d_resp = response_dict['PAYLOAD']['result_arr'][0]
            shill_id = d_resp['shill_id_inp']
            inc_ = ['post_url','pay_usd','is_approved','tg_user_at_inp','is_removed','post_url']
            d_resp['tg_user_at_inp'] = '@'+str(d_resp['tg_user_at_inp'])
            str_r = '\n '.join([str(k)+': '+str(d_resp[k]) for k in d_resp.keys() if str(k) in inc_])
            await update.callback_query.message.reply_text(f"Remove set for shill id: {shill_id} ...\n {str_r}")

        elif tg_cmd == req_handler.kSET_WALLET:
            # inc_ = ['wallet_address','info']
            # str_r = '\n '.join([str(k)+': '+str(d_resp[k]) for k in d_resp.keys() if str(k) in inc_])

            # obfuscate wallet_address
            str_wallet = d_resp['wallet_address']
            if str_wallet != '0x0' and len(str_wallet) > 15:
                str_wallet = str_wallet[:6] + 'xxxxxx' + str_wallet[-4:]
            await update.message.reply_text(f"Set cashout wallet ...\n {str_wallet}")

        elif tg_cmd == req_handler.kADMIN_PAY_SHILL_EARNS:
            inc_ = ['pay_tok_addr_inp','pay_tx_hash_inp','old_usd_owed','chain_usd_paid_inp','usd_owed_paid_diff','usd_total','usd_owed','tx_status_set','pay_tx_status_inp','tg_user_at_inp']
            d_resp['tg_user_at_inp'] = '@'+str(d_resp['tg_user_at_inp'])
            d_resp['$BST'] = d_resp['pay_tok_addr_inp']
            d_resp['tx hash'] = d_resp['pay_tx_hash_inp']
            inc_ = ['$BST','tx hash','old_usd_owed','chain_usd_paid_inp','usd_owed_paid_diff','usd_total','usd_owed','tx_status_set','pay_tx_status_inp','tg_user_at_inp']
            str_r = '\n '.join([str(k)+': '+str(d_resp[k]) for k in d_resp.keys() if str(k) in inc_])
            # str_r = '\n '.join([str(k)+': '+str(d_resp[k]) for k in d_resp.keys()])
            await update.message.reply_text(f"Payout Tx Processed ...\n {str_r}")
        else:
            await update.message.reply_text(f"'/{tg_cmd}' Executed Successfully! _ ")
        
    print('', f'EXIT - {funcname} _ {get_time_now()}', cStrDivider_1, sep='\n')

def valid_tweet_url(_tw_url):
    # check for validate tweet url
    keyVals = {'_tw_url':_tw_url}
    keyVals, success = req_handler.parse_twitter_url(keyVals, '_tw_url')
    return keyVals, success

def used_bs_tweet_url(_keyVals):
    success, jsonResp, dbProcResult = req_handler.execute_db_proc(_keyVals, 'TW_URL_IS_USED')
    if success: return bool(dbProcResult[0]['is_used'])
    else: True # db proc failes, return True (act like shill already used)

async def attempt_aux_cmd_exe(update: Update, context):
    funcname = 'attempt_aux_cmd_exe'
    user = update.message.from_user
    uid = user.id
    uname_at = user.username
    uname_handle = 'nil_disabled'

    # validate user has @username setup
    if uname_at == None:
        print(f'{get_time_now()} __ action : found uname_at == None; skip attempt_aux_cmd_exe')
        return
    
    if USE_ALT_ACCT: 
        # uid = '1058890141'
        # uname_at = 'laycpirates'
        uid = '6919802491'
        uname_at = 'fricardooo'

    # check if message text 'could' contain a tweet url
    inp = update.message.text
    if 'x.com' not in inp and 'twitter.com' not in inp: return

    print(f'{get_time_now()} __ action : found potential tweet url')
    print(cStrDivider_1, f'ENTER - {funcname} _ {get_time_now()}', sep='\n')

    # traverse through string, check for valid tweet url, 
    #   if valid tweet, check db to see if its been used yet
    #   if not used yet, generate aux_inp_split & attempt /register & /submit
    inp_split = list(update.message.text.split())
    for str_ in inp_split:
        keyVals, valid_tweet = valid_tweet_url(str_)
        if valid_tweet:
            tweet_is_used = used_bs_tweet_url(keyVals) # db check for used reg or shill
            print(f'tweet_is_used: {tweet_is_used}')
            if not tweet_is_used:
                valid_shill, msg = req_handler.valid_trinity_tweet(str_, ['@BearSharesX']) # net request
                valid_reg, msg = req_handler.valid_trinity_tweet(str_, ['@BearSharesX', 'Trinity', 'register']) # net request
                print(f'valid_shill: {valid_shill}')
                if valid_shill:
                    aux_inp_split = ['/'+req_handler.kSUBMIT_SHILL, uid, uname_at, str_]
                    context.user_data['inp_split'] = list(aux_inp_split)
                    await cmd_exe(update, context, aux_cmd=True)
                
                print(f'valid_reg: {valid_reg}')
                if valid_reg:
                    aux_inp_split = ['/'+req_handler.kSHILLER_REG, uid, uname_at, uname_handle, '0x0', str_]
                    context.user_data['inp_split'] = list(aux_inp_split)
                    await cmd_exe(update, context, aux_cmd=True)
                print(f'valid_shill: {valid_shill}')
                print(f'valid_reg: {valid_reg}')

    print('', f'EXIT - {funcname} _ {get_time_now()}', cStrDivider_1, sep='\n')

async def log_activity(update: Update, context):
    if update.message == None:
        print(f'{get_time_now()} _ action : found .message == None; returning')
        return

    chat_type = str(update.message.chat.type)
    chat_id = update.message.chat_id
    user = update.message.from_user
    uid = str(user.id)
    usr_at_name = f'@{user.username}'
    usr_handle = user.first_name
    inp = update.message.text
    lst_user_data = [uid, usr_at_name, usr_handle]
    lst_chat_data = [chat_id, chat_type]
    print(f'{get_time_now()} _ action: {lst_user_data}, {lst_chat_data}')
    
    if not USE_PAYOUT_ONLY and update.message.text: await attempt_aux_cmd_exe(update, context)

async def test(update: Update, context):
    funcname = 'test'
    print(f'\nENTER - {funcname}\n')
    await context.bot.send_message(chat_id=update.message.chat_id, text="test successful trinity")

async def trinity_help(update, context):
    funcname = 'trinity_help'
    print(f'\nENTER - {funcname}\n')
    await update.message.reply_text(TRINITY_INFO)

def main():
    # global TOKEN
    # create dispatcher with TG bot token
    dp = Application.builder().token(TOKEN).build()

    # Register command handlers
    # dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("test", test))
    dp.add_handler(CallbackQueryHandler(btn_option_selects))
    dp.add_handler(CommandHandler("trinity", trinity_help))
    dp.add_handler(CommandHandler("trinity_help", trinity_help))

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
    dp.run_polling(drop_pending_updates=True)


    # allowed_updates = [
    #     'message',                  # Allows your bot to receive new messages sent by users.
    #     'edited_message',           # Allows your bot to receive edited messages.
    #     'channel_post',             # Allows your bot to receive new messages sent in channels.
    #     'edited_channel_post',      # Allows your bot to receive edited messages sent in channels.
    #     'callback_query',           # Allows your bot to receive callback queries from inline keyboards or inline buttons.
    #     'inline_query',             # Allows your bot to receive inline queries from users.
    #     'chosen_inline_result',     # Allows your bot to receive chosen inline results from users.
    #     'poll',                     # Allows your bot to receive updates related to polls.
    #     'poll_answer'               # Allows your bot to receive poll answers from users.
    # ]    

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
        # inp = input('\nSelect token type to use:\n  0 = prod \n  1 = dev \n  > ')
        inp = input('\nSelect token type to use:\n  0 = trinity \n  1 = trinity_pay \n  > ')
        USE_PROD_TG = True if inp == '0' else False
        print(f'  input = {inp} _ USE_PROD_TG = {USE_PROD_TG}')

        inp = input('\nUse alt tg_user_id for testing (USE_ALT_ACCT)? [y/n]:\n  > ')
        USE_ALT_ACCT = True if inp.lower() == 'y' or inp.lower() == '1' else False
        print(f'  input = {inp} _ USE_ALT_ACCT = {USE_ALT_ACCT}')

        inp = input('\nONLY Run payout shills cmd (USE_PAYOUT_ONLY)? [y/n]:\n  > ')
        USE_PAYOUT_ONLY = True if inp.lower() == 'y' or inp.lower() == '1' else False
        print(f'  input = {inp} _ USE_PAYOUT_ONLY = {USE_PAYOUT_ONLY}')
        if USE_PAYOUT_ONLY: # clear cmd list and only add payout cmds
            LST_TG_CMDS = []
            LST_TG_CMDS.append(req_handler.kADMIN_PAY_SHILL_EARNS)
            LST_TG_CMDS.append(req_handler.kADMIN_PAY_SHILL_EARNS_conf)
        else: # remove payout cmds from default list already set in global
            LST_TG_CMDS.remove(req_handler.kADMIN_PAY_SHILL_EARNS)
            LST_TG_CMDS.remove(req_handler.kADMIN_PAY_SHILL_EARNS_conf)

        set_tg_token()  
        print(f'\nUSE_PROD_TG: {USE_PROD_TG}')
        print(f'USE_ALT_ACCT: {USE_ALT_ACCT}')
        print(f'USE_PAYOUT_ONLY: {USE_PAYOUT_ONLY}')
        print(f'Telegram TOKEN: {TOKEN}')
        print(f'Contract Address (symb): {env.bst_contr_addr} ({env.bst_contr_symb})\n')
        # print(f'OpenAI OPENAI_KEY: {OPENAI_KEY}')
        # print(f'CONSUMER_KEY: {CONSUMER_KEY}')
        # print(f'PROMO_TWEET_TEXT:\n{PROMO_TWEET_TEXT}\n')   
        main()
    except Exception as e:
        print_except(e, debugLvl=DEBUG_LVL)
    
    ## end ##
    print(f'\n\nRUN_TIME_START: {RUN_TIME_START}\nRUN_TIME_END:   {get_time_now()}\n')

print('', cStrDivider, f'# END _ {__filename}', cStrDivider, sep='\n')



# @BearSharesNFT ...
# https://twitter.com/BearSharesX/status/1769436246084919550?s=19 # only '@BearSharesNFT'

# @SolAudits ... @bearsharesx
# https://x.com/SolAudits/status/1777412699086897210 # register
# https://x.com/SolAudits/status/1777413084904055091
# https://x.com/SolAudits/status/1777415144860946445

# @SolAudits ...
# ex tweet_conf (fails): https://x.com/SolAudits/status/1765925371851972744?s=20 # only '@BearSharesNFT'
# ex tweet_conf (valid): https://x.com/SolAudits/status/1765925225844089300?s=20
# ex tweet_conf (valid): https://x.com/SolAudits/status/1766554515094778118?s=20
# ex tweet_conf (valid): https://x.com/SolAudits/status/1766580860604571739?s=20
# ex tweet_conf (valid): https://x.com/SolAudits/status/1766584748527247440?s=20
# ex tweet_conf (valid): https://x.com/SolAudits/status/1766586177438564670?s=20

# ex tweet_shill (fails): https://x.com/TopGunHexadian/status/1766339571342553408?s=20
# ex tweet_shill (valid): https://x.com/SolAudits/status/1766663759961940205?s=20

# @TeddyShares ...
# ex tweet_conf (valid): https://x.com/TeddyShares/status/1767453126896881733?s=20
# ex tweet_shill (valid): https://x.com/teddyshares/status/1768088560433787068?s=46&t=nEQblYL5Q2q_AqjDvXnRZg