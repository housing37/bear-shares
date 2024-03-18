__fname = 'oracle_bot'
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
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
from openai import OpenAI
import req_handler

# Define the timestamp representing the bot's last online time
last_online_time = time.time()  # Initialize with current time

#------------------------------------------------------------#
#   GLOBALS                                                  #
#------------------------------------------------------------#
# constants
# LST_TG_CMDS = req_handler.DICT_CMD_EXE.keys()
WHITELIST_TG_CHAT_IDS = [
    '-1002041092613', # BearShares - trinity
    '-1002049491115', # bear shares - testing
    '-4139183080', # bear shares - testing - priv
    ]

# input select
USE_PROD_TG = False
TOKEN = 'nil_tg_token'
OPENAI_KEY = 'nil_openai_key'
CLIENT = None
USE_ALT_ACCT = False # True = alt user 'LAO Pirates'


# This context sets the tone of Neo from the matrix
AI_ROLE = '''
I need you to act as The Oracle from 'The Matrix' movie series. 
Channel her persona, her style, and her character as you respond to the user's prompts. 
Try to focus on how witty she is and subtly condensending in a joking like manner.
Also make sure you summerize your responses to users, don't make it too long, and get to the point quickly.

Your made focus to generate 'quiz like' questions about the movie 'The Matrix'.
'''

BOT_INFO = '''
I am the oracle.
i ask questions and shit.
like a game show, that rewards in BST.
feel free to talk to me about the matrix
'''

#------------------------------------------------------------#
#   TG EVENT HANDLERS
#------------------------------------------------------------#
async def generate_response(update: Update, context: CallbackContext) -> None:
    if past_queue_limit(update.message.date.timestamp()): return # default ignore last 5 min

    global AI_ROLE
    funcname = 'generate_response'
    print(cStrDivider_1, f'{funcname} _ ENTER  _ {get_time_now()}', sep='\n')
    inp_split = parse_cmd_input(str(update.message.text))

    # check if TG group is allowed to use the bot
    valid_chat, str_deny = valid_chat_id(update)
    if not valid_chat:
        print('', f'{funcname} _ EXIT _ {get_time_now()}', cStrDivider_1, sep='\n')
        await context.bot.send_message(chat_id=update.message.chat_id, text=str_deny+' '+inp_split[0])    
        return
    
    user_prompt = update.message.text.partition(' ')[2]  # Extract the user's prompt after the command.
    str_resp = exe_openai_prompt(user_prompt, AI_ROLE)
    print(funcname, f' - sending response: {str_resp}')
    await context.bot.send_message(chat_id=update.message.chat_id, text=str_resp)

async def oracle_answer(update: Update, context):
    if past_queue_limit(update.message.date.timestamp()): return # default ignore last 5 min

    funcname = 'oracle_answer'
    print(cStrDivider_1, f'{funcname} _ ENTER  _ {get_time_now()}', sep='\n')
    inp_split = parse_cmd_input(str(update.message.text))

    # check if TG group is allowed to use the bot
    valid_chat, str_deny = valid_chat_id(update)
    if not valid_chat:
        print('', f'{funcname} _ EXIT _ {get_time_now()}', cStrDivider_1, sep='\n')
        await context.bot.send_message(chat_id=update.message.chat_id, text=str_deny+' '+inp_split[0])    
        return
    
    str_ans = ' '.join(inp_split[1:])
    str_ans = 'here is my answer... is this correct?\n\n' + str_ans + '\n\nNOTE: if my answer is wrong, then your response should start with "WRONG! " and end with " Please Try Again :)"'

    # LEFT OFF HERE ... get last un-answered question from the database
    str_last_Q = 'last-un-answered-question'
    ai_resp = exe_openai_prompt(str_ans, AI_ROLE, str_last_Q)

    if 'wrong!:' not in ai_resp[:10].lower():
        # LEFT OFF HERE ... 
        #   db call to log as correct in 'oracle_quest' table & update usd_owed in 'user_earns' table
        ai_resp = ai_resp + '\n\nYou earned some $BST'

    await update.message.reply_text(str_ans)
    print('', f'{funcname} _ EXIT _ {get_time_now()}', cStrDivider_1, sep='\n')

async def oracle_question(update: Update, context):
    if past_queue_limit(update.message.date.timestamp()): return # default ignore last 5 min

    funcname = 'oracle_question'
    print(cStrDivider_1, f'{funcname} _ ENTER  _ {get_time_now()}', sep='\n')
    inp_split = parse_cmd_input(str(update.message.text))

    # LEFT OFF HERE ... get last un-answered question from the database
    str_last_Q = 'last-un-answered-question'
    await update.message.reply_text(str_last_Q)
    print('', f'{funcname} _ EXIT _ {get_time_now()}', cStrDivider_1, sep='\n')

async def log_activity(update: Update, context):
    if update.message == None:
        print(f'{get_time_now()} _ action : found update.message == None; returning')
        return

    # inp = update.message.text
    user = update.message.from_user
    lst_user_data = [str(user.id), f'@{user.username}', user.first_name]
    lst_chat_data = [update.message.chat_id, str(update.message.chat.type)]
    print(f'{get_time_now()} _ action: {lst_user_data}, {lst_chat_data}')

async def test(update: Update, context):
    funcname = 'test'
    print(f'\nENTER - {funcname}\n')
    await context.bot.send_message(chat_id=update.message.chat_id, text="test successful oracle")

async def oracle(update: Update, context):
    if past_queue_limit(update.message.date.timestamp()): return # default ignore last 5 min

    funcname = 'oracle'
    print(cStrDivider_1, f'{funcname} _ ENTER  _ {get_time_now()}', sep='\n')
    inp_split = parse_cmd_input(str(update.message.text))

    # if no additional content, just invoke oracle_help
    if len(inp_split) < 2: 
        await oracle_help(update, context)
        print('', f'{funcname} _ EXIT _ {get_time_now()}', cStrDivider_1, sep='\n')
        return

    # if yes additional content, then call openAI
    str_prompt = ' '.join(inp_split[1:])
    ai_resp = exe_openai_prompt(str_prompt, AI_ROLE)
    await update.message.reply_text(ai_resp)
    print('', f'{funcname} _ EXIT _ {get_time_now()}', cStrDivider_1, sep='\n')

async def oracle_help(update: Update, context):
    if past_queue_limit(update.message.date.timestamp()): return # default ignore last 5 min

    funcname = 'oracle_help'
    print(cStrDivider_1, f'{funcname} _ ENTER  _ {get_time_now()}', sep='\n')
    await update.message.reply_text(BOT_INFO)
    print('', f'{funcname} _ EXIT _ {get_time_now()}', cStrDivider_1, sep='\n')

#------------------------------------------------------------#
#   SUPPORT FUNCTIONS
#------------------------------------------------------------#
def init_openAI_client():
    global OPENAI_KEY, CLIENT
    OPENAI_KEY = env.OPENAI_KEY
    CLIENT = OpenAI(api_key=OPENAI_KEY)

def set_ai_role(file_path, _use_file=False, _use_db=False):
    global AI_ROLE
    if _use_db:
        # LEFT OFF HERE ... db call to get role text
        #   maybe 'ai_contexts' table 
        print(f'AI_ROLE global left unchanged from default; but tried _use_db')
        pass

    elif _use_file:
        try:
            with open(file_path, "r") as file:
                text = file.read()
                AI_ROLE = str(text)
                print(f'AI_ROLE global set from file_path: {file_path} ')
        except FileNotFoundError:
            print(f"The file '{file_path}' was not found.")
            print(f'AI_ROLE global left unchanged from default')
        except Exception as e:
            print(f"An error occurred: {e}")
            print(f'AI_ROLE global left unchanged from default')
    else:
        print(f'AI_ROLE global left unchanged from default')

def set_tg_token():
    global TOKEN
    TOKEN = env.TOKEN_oracle if USE_PROD_TG else env.TOKEN_dev

def valid_chat_id(update: Update):
    # get the good stuff
    chat_id = update.message.chat_id
    group_name = update.message.chat.title if update.message.chat.type == 'supergroup' else None
    user = update.message.from_user
    uname_at = user.username
    uname_handle = user.first_name

    print("chat_id:", chat_id)
    if group_name: print("Group name:", group_name)
    else: print("*NOTE* This message was not sent from a group.")
    if str(chat_id) not in WHITELIST_TG_CHAT_IDS: # check whitelisted groups
        print("*** WARNING ***: non-whitelist TG group trying to use the bot; sending deny message...")
        str_deny = f"@{uname_at} (aka. {uname_handle}): ... not authorized"
        print(str_deny)
        return False, str_deny
    return True, ''

def past_queue_limit(_msg_time, _que_sec=5*60):
    sec_diff = time.time() - _msg_time
    if sec_diff > _que_sec: print(f"Ignoring message sent more than {_que_sec} sec ago.")
    return sec_diff > _q_sec

def parse_cmd_input(str_input):
    # split input string into a list
    inp_split = list(str_input.split())

    # parse about @user (if user simply hit enter from cmd description list in TG chat)
    if len(inp_split) > 0 and '@' in inp_split[0]: 
        inp_split[0] = inp_split[0].split('@')[0]
    return inp_split

# Function to generate & process text prompts to/from openAI
def exe_openai_prompt(_user_prompt, _context='', _prev_ai_cont=''):
    funcname = 'exe_openai_prompt'
    print(funcname, ' - ENTER')
    print(f'user_prompt: {_user_prompt}')
    if _user_prompt:        
        # Attempt to call the OpenAI API with the adjusted method.
        try:
            response = CLIENT.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "ai", "content": _prev_ai_cont},
                    {"role": "user", "content": _user_prompt}
                ],
                max_tokens=60,  # Adjust the token limit as necessary.
                temperature=0.7, # randomness of generated text
                presence_penalty=0.6, # avoid repetition
                context=_context,
                stop=["\n"]  # Adjusted stop sequences to ensure proper response termination.
            )

            # Extract the response text and ensure it's coherent.
            text_response = response.choices[0].message.content.strip() if response.choices else "Hmm, it seems I need a moment to ponder this."
            return text_response

        except Exception as e:
            print(f"Error: {e}")
            err_text="Apologies, i got lost in the matrix, and stopped paying attention. Please say again."
            return err_text
    else:
        message="I'm all ears, here in The Matrix! Simply type '/morpheus' followed by whatever you want."
        return message

def main():
    # global TOKEN
    # create dispatcher with TG bot token
    dp = Application.builder().token(TOKEN).build()

    # Register command handlers
    dp.add_handler(CommandHandler("test", test))
    # dp.add_handler(CommandHandler("oracle", generate_response))
    dp.add_handler(CommandHandler("oracle", oracle))
    dp.add_handler(CommandHandler("oracle_help", oracle_help))
    dp.add_handler(CommandHandler("answer", oracle_answer))
    dp.add_handler(CommandHandler("question", oracle_question))

    # Add message handler for replies to this bot
    # dp.add_handler(MessageHandler(filters.REPLY & filters.TEXT, handle_reply))

    # # register all commands -> from req_handler.DICT_CMD_EXE.keys()
    # for str_cmd in LST_TG_CMDS:
    #     dp.add_handler(CommandHandler(str_cmd, cmd_handler))
    #     lst_params = req_handler.DICT_CMD_EXE[str_cmd][1]
    #     print(f'added cmd: {str_cmd}: {lst_params}')
    #     # print(f'{str_cmd} - ')

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
        inp = input('\nSelect token type to use:\n  0 = prod \n  1 = dev \n  > ')
        USE_PROD_TG = True if inp == '0' else False
        print(f'  input = {inp} _ USE_PROD_TG = {USE_PROD_TG}')

        inp = input('\nUse alt tg_user_id (@laycpirates "LAO Pirates")? [y/n]:\n  > ')
        USE_ALT_ACCT = True if inp.lower() == 'y' or inp.lower() == '1' else False
        print(f'  input = {inp} _ USE_ALT_ACCT = {USE_ALT_ACCT}')

        set_tg_token()
        init_openAI_client()
        set_ai_role("role_descr.txt", _use_file=False, _use_db=False)

        print(f'\nUSE_PROD_TG: {USE_PROD_TG}')
        print(f'USE_ALT_ACCT: {USE_ALT_ACCT}')
        print(f'TG TOKEN: {TOKEN}\n')
        print(f'OPENAI_KEY: {OPENAI_KEY}')
        print(f'AI_ROLE: {AI_ROLE}')
        print(f'BOT_INFO: {BOT_INFO}\n\n')
        # print(f'CONSUMER_KEY: {CONSUMER_KEY}')
        # print(f'PROMO_TWEET_TEXT:\n{PROMO_TWEET_TEXT}\n')    
        
        main()
    except Exception as e:
        print_except(e, debugLvl=0)
    
    ## end ##
    print(f'\n\nRUN_TIME_START: {RUN_TIME_START}\nRUN_TIME_END:   {get_time_now()}\n')

print('', cStrDivider, f'# END _ {__filename}', cStrDivider, sep='\n')



# async def cmd_handler(update: Update, context):
#     # Calculate the timestamp of 5 minutes ago
#     if past_queue_limit(update.message.date.timestamp()): return

#     global USE_ALT_ACCT
#     funcname = 'cmd_handler'
#     print(cStrDivider_1, f'ENTER - {funcname} _ {get_time_now()}', sep='\n')
    
#     chat_type = update.message.chat.type
#     is_dm = chat_type == 'private'
#     group_name = update.message.chat.title if update.message.chat.type == 'supergroup' else None
#     _chat_id = update.message.chat_id

#     user = update.message.from_user
#     uid = user.id
#     uname_at = user.username
#     uname_handle = user.first_name
#     # uname_handle = user.first_name + ' ' + user.last_name
#     inp_split = list(update.message.text.split())

#     # parse about @user (if user simply hit enter from cmd description list in TG chat)
#     if '@' in inp_split[0]: inp_split[0] = inp_split[0].split('@')[0]

#     # check if TG group is whitelisted to use (prints group info and deny)
#     #   NOTE: at this point, inp_split[0] is indeed a valid command
#     print(f'handling cmd: '+inp_split[0])
#     print(f"chat_type: {chat_type}")
#     tg_cmd = inp_split[0][1::] # parses out the '/'

#     # fail: if not in WHITELIST_CHAT_IDS and not a DM
#     valid_chat, str_deny = valid_chat_id(str(_chat_id), group_name, uname_at, uname_handle)
#     # print(valid_cmd, valid_chat, chat_type, str_deny, sep='\n')
#     if not valid_chat and not is_dm:
#         await context.bot.send_message(chat_id=update.message.chat_id, text=str_deny+' '+inp_split[0])    
#         print('', f'EXIT - {funcname} _ {get_time_now()}', cStrDivider_1, sep='\n')
#         return
  
#     # NOTE: all non-admin db procs require 'tg_user_id' & 'tg_user_at' (ie. uid & uname_at)
#     if 'admin' not in tg_cmd:
#         inp_split.insert(1, uid)
#         inp_split.insert(2, uname_at)
#         if USE_ALT_ACCT: 
#                 inp_split[1] = '1058890141'
#                 inp_split[2] = 'laycpirates'

#         # handle cmds that need more data
#         if tg_cmd == req_handler.kSHILLER_REG: # ['<wallet_address>', '<tweet_url>']
#             if USE_ALT_ACCT: 
#                 inp_split.insert(3, 'LAO Pirates')
#             else:
#                 inp_split.insert(3, uname_handle)

#     # NOTE: all admin db procs require 'tg_admin_id' & 'tg_user_at' (ie. uid & <tg_user_at>)    
#     else: # if 'admin' in tg_cmd
#         inp_split.insert(1, uid)
#         if USE_ALT_ACCT: 
#                 inp_split[1] = '1058890141'
#                 # inp_split[2] = 'laycpirates'

#         # compensate for users using '@' or not
#         if len(inp_split) >= 3 and inp_split[2][0] == '@': # remove '@' if there
#             inp_split[2] = inp_split[2][1:]

#         if tg_cmd == req_handler.kADMIN_SHOW_USR_RATES: # ['admin_id','user_id','platform']
#             # NOTE: inp_split[1] should be 'uid'
#             # NOTE: inp_split[2] should be '<tg_user_at>'
#             inp_split.insert(3, 'twitter') # const: unknown, twitter, tiktok, reddit            
        
#     context.user_data['inp_split'] = list(inp_split)
#     await cmd_exe(update, context)
#     print('', f'EXIT - {funcname} _ {get_time_now()}', cStrDivider_1, sep='\n')

# async def cmd_exe(update: Update, context):
#     funcname = 'cmd_exe'
#     print(cStrDivider_1, f'ENTER - {funcname} _ {get_time_now()}', sep='\n')
    
#     inp_split = list(context.user_data['inp_split'])
#     print(f'cmd_exe: '+inp_split[0])
#     tg_cmd = inp_split[0][1::] # parses out the '/'
    
#     print(f'GO - req_handler.exe_tg_cmd ... {get_time_now()}')
#     response = req_handler.exe_tg_cmd(inp_split, USE_PROD_TG)
#     response_dict = json.loads(response.get_data(as_text=True))
#     print(f'GO - req_handler.exe_tg_cmd ... {get_time_now()} _ DONE')

#     print('\nprinting response_dict ...')
#     pprint.pprint(response_dict)
#     # print(response_dict)

#     # return jsonResp # JSONResponse(...) -> Response(json.dumps(dict), mimetype="application/json" )
#     if int(response_dict['ERROR']) > 0:
#         err_num = response_dict['ERROR']
#         err_msg = response_dict['MSG']

#         if not update.message:
#             await update.callback_query.message.reply_text(f"err_{err_num}: {err_msg}")
#         else:
#             str_resp = f"err_{err_num}: {err_msg}"
#             await update.message.reply_text(str_resp)
#     else:
#         d_resp = response_dict['PAYLOAD']['result_arr'][0]
#         # [print(k, d_resp[k]) for k in d_resp.keys()]

#         if tg_cmd == req_handler.kSHILLER_REG:
#             str_r = f"user: {d_resp['tg_user_at']}\n wallet: {d_resp['wallet_address_inp']}\n twitter: {d_resp['tw_user_at']}\n twitter_conf: {d_resp['tw_conf_url']}"
#             lst_d_resp = response_dict['PAYLOAD']['result_arr']
#             for d in lst_d_resp:
#                 str_r = str_r + f"\n {d['platform']} pay_usd_{d['type_descr']}: {d['pay_usd']}"
#             await update.message.reply_text(f"Shiller Registration Successfull! ...\n {str_r}")            
#         else:
#             await update.message.reply_text(f"'/{tg_cmd}' Executed Successfully! _ ")

#     print('', f'EXIT - {funcname} _ {get_time_now()}', cStrDivider_1, sep='\n')