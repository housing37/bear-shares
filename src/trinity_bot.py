__fname = 'trinity_bot'
__filename = __fname + '.py'
cStrDivider = '#================================================================#'
cStrDivider_1 = '#----------------------------------------------------------------#'
print('', cStrDivider, f'GO _ {__filename} -> starting IMPORTs & declaring globals', cStrDivider, sep='\n')

#------------------------------------------------------------#
#   IMPORTS                                                  #
#------------------------------------------------------------#
from _env import env
import time
from datetime import datetime
import time, os, traceback, sys
# import random, json
import req_handler
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters

#------------------------------------------------------------#
#   GLOBALS                                                  #
#------------------------------------------------------------#
# constants
LST_TG_CMDS = req_handler.DICT_CMD_EXE.keys()
WHITELIST_CHAT_IDS = [
    '-1002041092613', # $BearShares
    '-1002049491115', # $BearShares - testing
    '-4139183080', # TeddyShares - testing
    ]
BLACKLIST_TEXT = [
    'smart vault', 'smart-vault', 'smart_vault', # @JstKidn
    ]

# input select
USE_PROD_TG = False

#------------------------------------------------------------#
#   FUNCTIONS                                                #
#------------------------------------------------------------#
def set_tg_token():
    global TOKEN
    TOKEN = env.TOKEN_prod if USE_PROD_TG else env.TOKEN_dev

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
    funcname = 'cmd_handler'
    print(cStrDivider_1, f'ENTER - {funcname} _ {get_time_now()}', sep='\n')
    group_name = update.message.chat.title if update.message.chat.type == 'supergroup' else None
    _chat_id = update.message.chat_id

    user = update.message.from_user
    uid = user.id
    str_handle = user.first_name + ' ' + user.last_name
    str_uname = user.username
    inp_split = update.message.text.split()

    # check if TG group is whitelisted to use (prints group info and deny)
    valid_cmd = inp_split[0] in LST_TG_CMDS
    valid_chat, str_deny = is_valid_chat_id(str(_chat_id), group_name, str_uname, str_handle)
    if not valid_chat or not valid_cmd:
        await context.bot.send_message(chat_id=update.message.chat_id, text=str_deny+' '+inp_split[0])    
        print('', f'EXIT - {funcname} _ {get_time_now()}', cStrDivider_1, sep='\n')
        return

    # LEFT OFF HERE ... need to invoke req_handler
    #   w/ str_cmd & str_
    # d = {}
    # d = [d[i] = i for i in inp_split]
    print('req_handler.exe_tg_cmd ...')
    jsonResp = req_handler.exe_tg_cmd(inp_split)
    print('printing jsonResp ...')
    print(jsonResp)
    print('exiting ...')
    exit(0)
    return jsonResp # JSONResponse(...) -> Response(json.dumps(dict), mimetype="application/json" )

    # inp 
    # str_cmd = inp[:inp.find(' '):] # slicing out /<command>
    # str_prompt = inp[inp.find(' ')+1::] # slicing out /<command>

    

    # filter / update prompt to deal with spammers (using 'BLACKLIST_TEXT')
    str_prompt = filter_prompt(str_prompt)

    str_conf = f'@{str_uname} (aka. {str_handle}) -> please wait, generating image ...\n    "{str_prompt}"'
    print(str_conf)

    await context.bot.send_message(chat_id=update.message.chat_id, text=str_conf)

    lst_imgs, err = gen_ai_image(str_prompt)

    if err > 0:
        str_err = f"@{str_uname} (aka. {str_handle}) -> BING said NO!\n   change it up & try again : /"
        if err == 1:
            str_err = f"@{str_uname} (aka. {str_handle}) -> description TOO SHORT, need at least 50 chars (~10 words or so)"
        str_err = str_err + f'\n    "{str_prompt}"'
        await context.bot.send_message(chat_id=update.message.chat_id, text=str_err)
        print(str_err)
        print('', f'EXIT - {funcname} _ {get_time_now()}', cStrDivider_1, sep='\n')
        return

    print('SENDING IMAGE to TG ...')
    # pick one random image from lst_imgs
    r_idx = -1
    url = 'nil_url'
    while True:
        r_idx = random.randint(0, len(lst_imgs)-1)
        is_img = 'r.bing.com' not in lst_imgs[r_idx]
        no_end_dot = lst_imgs[r_idx][-1] != '.'
        # if 'r.bing.com' not in lst_imgs[r_idx]:
        if is_img and no_end_dot:
            url = lst_imgs[r_idx]
            break

    # Create an inline keyboard markup with a button
    inline_keyboard = [
        [InlineKeyboardButton("Request Tweet", callback_data=f'@{str_uname} (aka. {str_handle})')]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    try:
        await context.bot.send_message(
            chat_id=update.message.chat_id, 
            text=f'@{str_uname} (aka. {str_handle}) -> here is your image\n  "{str_prompt}" ...\n {url}',
            # reply_markup = ReplyKeyboardMarkup([['Your Button Text']])
            reply_markup = reply_markup
            )
    except Exception as e:
        # note_021724: exception added for TG: @enriquebambo (aka. 🍊 👾 𝐄η𝐑𝕚ⓀẸⓑᗩｍ𝕓ㄖ 👾🍊 {I DM First, I'm Impostor})
        #   sending response with TG button was causing a crash (but images were indeed successfully received from BING)
        print_except(e, debugLvl=1)
        print('Sending to TG w/o tweet button... ')
        await context.bot.send_message(
            chat_id=update.message.chat_id, 
            text=f'@{str_uname} (aka. {str_handle}) -> here is your image\n  "{str_prompt}" ...\n {url}')
    print('', f'EXIT - {funcname} _ {get_time_now()}', cStrDivider_1, sep='\n')

async def test(update, context):
    funcname = 'test'
    print(f'\nENTER - {funcname}\n')
    await context.bot.send_message(chat_id=update.message.chat_id, text="test successful")

def main():
    # global TOKEN
    dp = Application.builder().token(TOKEN).build()
    # Create the Update and pass in the bot's token
    # update = Update(token=TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    # dp = update.dispatcher

    # Register command handlers
    # dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("test", test))
    

    # register all commands -> from req_handler.DICT_CMD_EXE.keys()
    for str_cmd in LST_TG_CMDS:
        dp.add_handler(CommandHandler(str_cmd, cmd_handler))


    # dp.add_handler(CommandHandler("register_as_shiller", cmd_handler)) # user_id, wallet addr, twitter prof link
    # dp.add_handler(CommandHandler("submit_shill_link", cmd_handler)) # user_id, tweet link
    # dp.add_handler(CommandHandler("show_my_rates", cmd_handler)) # user_id
    # dp.add_handler(CommandHandler("show_my_earnings", cmd_handler)) # user_id

    # # user cash-out, checks for admin approval first
    # dp.add_handler(CommandHandler("withdraw_my_earnings", cmd_handler)) # user_id

    # # admin: list shills waiting for approval (user_id | all)
    # #   include remove history / cnt
    # dp.add_handler(CommandHandler("admin_list_pend_shills", cmd_handler) # user_id
    # dp.add_handler(CommandHandler("admin_list_pend_shills_all", cmd_handler))
    # dp.add_handler(CommandHandler("admin_approve_shill", cmd_handler) # shill_id | url
    # dp.add_handler(CommandHandler("admin_view_user_shills", cmd_handler) # user_id
    # dp.add_handler(CommandHandler("admin_view_shill_status", cmd_handler_shill_status) # user_id, shill_id
    # dp.add_handler(CommandHandler("admin_pay_shill", cmd_handler) # shill_id | url
    # dp.add_handler(CommandHandler("admin_log_removed_shill", cmd_handler) # shill_id | url
    # dp.add_handler(CommandHandler("admin_scan_for_removed_shills", cmd_handler)
    # dp.add_handler(CommandHandler("admin_set_shiller_rates", cmd_handler) # user_id, [rates]


    # Add the button click handler
    # dp.add_handler(CallbackQueryHandler(button_click))
    # Register message handler for new chat members
    # dp.add_handler(MessageHandler(filters.StatusUpdate._NewChatMembers, new_chat_members))

    # Register message handler for all other messages
    # dp.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo)) # ~ = negate (ie. AND NOT)
    # dp.add_handler(MessageHandler(filters.Command, bad_command))
    # Start the Bot
    dp.run_polling()
    # Update.start_polling()

    # Run the bot until you press Ctrl-C
    # Update.idle()

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
    
    ## exe ##
    try:
        # select to use prod bot or dev bot
        inp = input('Select token type to use:\n  0 = prod (@BearSharesBot)\n  1 = dev (@TeddySharesBot)\n  > ')
        USE_PROD_TG = True if inp == '0' else False
        print(f'  input = {inp} _ USE_PROD_TG = {USE_PROD_TG}')

        set_tg_token()        
        main()
    except Exception as e:
        print_except(e, debugLvl=0)
    
    ## end ##
    print(f'\n\nRUN_TIME_START: {RUN_TIME_START}\nRUN_TIME_END:   {get_time_now()}\n')

print('', cStrDivider, f'# END _ {__filename}', cStrDivider, sep='\n')