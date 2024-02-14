__fname = 'teddy_bot'
__filename = __fname + '.py'
cStrDivider = '#================================================================#'
cStrDivider_1 = '#----------------------------------------------------------------#'
print('', cStrDivider, f'GO _ {__filename} -> starting IMPORTs & declaring globals', cStrDivider, sep='\n')


from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.ext import CallbackQueryHandler, CallbackContext
# from telegram import ChatAction
import time
import random
from datetime import datetime
import json, time, os, traceback, sys
import webbrowser

# myst37.020
# cook = "1CIx4heldQFrBstIQ-KL7d7ix-Rif8Di0yW_vsuk-Gsfb9lGzgTWTQ20KJ5oJR_Y7bmVNNKrKS_MVEN4v-OjGPVVsQ2a-h9zZkMC90Fj74frtXRSfKPzzJ5p8hdX27bfvEgUQlVJAzC92Mo_dFLTYvr_SgpQrFp-eUbdI-cByE9F57vWbER9z287be7cdsw6TP1_BYzzC9G1jkpYMgi-vYw"
# lst_cookies =[
#     # myst37.014
#     "1-AhuVhuYkNn4kh6m8T72bEg4xn9S6wqt0TWqDWcbS1NUnO4SLoWWMr4VhaXuV1j1W56-2H8ihDg5SYH8cZQPox6mOyxpCYojTcAFvpNvMSKLa9WlILBMTG65xcyvB2Z4IpSNnmqCkHTFtUJSSiV7avAYVvz72M1RhIPCGeqszXfGcLpOk9z6We4jCaNNzf2SGQzKPlYt6k-aC6le2hrCVg",
#     # myst37.015
#     "1HVwcZVHsgR9AH6Lmu_VeRCtSsrI6b9SBu9U0Grj8KGqOVxJRrCZUfjSs1NNS448h2ttG0Egsoc3dsrFku7D5R7z9WyHDcKYqxdfrQCMsZThEjIedubs8BFS4zOwryk-vsv2zuvTbA3BOlrFjcl4tQInXEq3Xdv04EWHADeWfTfBgWWo-Oxoiylj9KvKUx7_sV5vxq72lR0HxiDQDPvCngQ",
#     # myst37.016
#     "1RTGjcQkCYaUfk-jI4OCe1K1lFb0N60SUcgwT46onrYd2_UITKYzLttpSETocCEcsdKSLdzdRlP9NBl1xwpWfx1egozVMigurWjjdA0CiTUCQlP4MCG7p_UcB-VEsGEq09Y0c-IPpi5Bf5lelCzg0peWwy5cGOd2J23GLViWpBD-k1UNkfhfdiT7T1GxDePCmxt744-a1dHjLVrLEA9dkDQ",
#     # myst37.021
#     "1BmCGFpK08XlfcXBQf_W6iF_BPh6i9cg-6JAuA17tC_tlg7nGW-VG2c4VSqoa_okPgQTs5qjNRmSgifp30jJ20YAOdFACU6JmOHc8EDfSnszQrmQqwSOOHAmub8bGfPIM7rRn86TjoPXqFtn0a96w-R6F53-ne5EZo55sb6Dxt2vOZxsug5pDrtNW5K-hqGBeZj_yhxf_uffBWt_LIF3BEg",
#     # myst37.022
#     "15b2vveo09pnXUXXW6wOlLXbpP88N2tKXr_r3ePQdv0lyvo49iqDXjjnaw5kim6tCOKeHKDeGTN4JzlDkoeW-WkpzXX_jWiHqxTFcQh_jzsEmtPL-ou1Q9vWShc_JT1NI4b9gTvjGdUrsez3bIEsu6GXIRvCipa4OASe_GnAc7WW2Ajv1IEVA0JRQ2w3_ByNT76zdTHDOJrgsTZzoN8s4Ag"
# ]
dict_cookies ={
    "myst37.014":
    "1-AhuVhuYkNn4kh6m8T72bEg4xn9S6wqt0TWqDWcbS1NUnO4SLoWWMr4VhaXuV1j1W56-2H8ihDg5SYH8cZQPox6mOyxpCYojTcAFvpNvMSKLa9WlILBMTG65xcyvB2Z4IpSNnmqCkHTFtUJSSiV7avAYVvz72M1RhIPCGeqszXfGcLpOk9z6We4jCaNNzf2SGQzKPlYt6k-aC6le2hrCVg",
    "myst37.015":
    "1HVwcZVHsgR9AH6Lmu_VeRCtSsrI6b9SBu9U0Grj8KGqOVxJRrCZUfjSs1NNS448h2ttG0Egsoc3dsrFku7D5R7z9WyHDcKYqxdfrQCMsZThEjIedubs8BFS4zOwryk-vsv2zuvTbA3BOlrFjcl4tQInXEq3Xdv04EWHADeWfTfBgWWo-Oxoiylj9KvKUx7_sV5vxq72lR0HxiDQDPvCngQ",
    "myst37.016":
    "1RTGjcQkCYaUfk-jI4OCe1K1lFb0N60SUcgwT46onrYd2_UITKYzLttpSETocCEcsdKSLdzdRlP9NBl1xwpWfx1egozVMigurWjjdA0CiTUCQlP4MCG7p_UcB-VEsGEq09Y0c-IPpi5Bf5lelCzg0peWwy5cGOd2J23GLViWpBD-k1UNkfhfdiT7T1GxDePCmxt744-a1dHjLVrLEA9dkDQ",
    "myst37.021":
    "1BmCGFpK08XlfcXBQf_W6iF_BPh6i9cg-6JAuA17tC_tlg7nGW-VG2c4VSqoa_okPgQTs5qjNRmSgifp30jJ20YAOdFACU6JmOHc8EDfSnszQrmQqwSOOHAmub8bGfPIM7rRn86TjoPXqFtn0a96w-R6F53-ne5EZo55sb6Dxt2vOZxsug5pDrtNW5K-hqGBeZj_yhxf_uffBWt_LIF3BEg",
    "myst37.022":
    "15b2vveo09pnXUXXW6wOlLXbpP88N2tKXr_r3ePQdv0lyvo49iqDXjjnaw5kim6tCOKeHKDeGTN4JzlDkoeW-WkpzXX_jWiHqxTFcQh_jzsEmtPL-ou1Q9vWShc_JT1NI4b9gTvjGdUrsez3bIEsu6GXIRvCipa4OASe_GnAc7WW2Ajv1IEVA0JRQ2w3_ByNT76zdTHDOJrgsTZzoN8s4Ag"
}
# os.environ["BING_COOKIES"] = cook
from BingImageCreator import ImageGen, ImageGenAsync

# Telegram Bot token obtained from BotFather
# TOKEN = '6911413573:AAGrff9aK3aSfaDhGaT5Iyf68zqRcPHrGN0' # TeddySharesBot (dev)
TOKEN = '6805964502:AAHL99OquXuZUPzpgqWNDbeBY_pgGpANO0A' # BearSharesBot (prod)
# BEAR_BOT = Bot(token=TOKEN)
IMG_REQUEST_CNT = 0

# Dictionary to keep track of users who have been greeted
greeted_users = {}

async def test(update, context):
    funcname = 'test'
    print(f'\nENTER - {funcname}\n')
    await context.bot.send_message(chat_id=update.message.chat_id, text="test successful")

# Function to handle the /start command
async def start(update, context):
    funcname = 'start'
    print(f'\nENTER - {funcname}\n')
    # await context.bot.send_message(chat_id=update.message.chat_id, text="Hello! I'm your friendly Telegram bot.")
    user_id = update.message.from_user.id
    message = "Welcome to the Bot! Click the button below to start."

    # Create an inline keyboard with a "Start" button
    keyboard = [[InlineKeyboardButton("Start", callback_data='start')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the message with the inline keyboard to the user
    await update.message.reply_text(message, reply_markup=reply_markup)

async def button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    user_id = query.from_user.id
    message = "You have started a conversation with the bot. Now you can interact with it."

    # Send a message acknowledging the button click
    await query.message.reply_text(message)

# Function to handle new users joining the group
async def new_chat_members(update: Update, context):
    for member in update.message.new_chat_members:
        if member.id not in greeted_users:
            greeted_users[member.id] = True
            await context.bot.send_message(chat_id=update.message.chat_id,
                                     text=f"Hello {member.first_name} (@{member.username})! Welcome to the group.")

# Function to handle all other messages
async def echo(update: Update, context):
    # context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    # await context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
    # time.sleep(2)  # Simulate typing by delaying for 2 seconds
    funcname = 'echo'
    print(f'\nENTER - {funcname}\n')
    print(f'\nEXIT - {funcname}\n')

async def bad_command(update: Update, context):
    funcname = 'gen_ai_img_1'
    print(f'\nENTER - {funcname}\n')

    user = update.message.from_user
    uid = user.id
    str_handle = user.first_name
    str_uname = user.username
    inp = update.message.text
    str_conf = f'@{str_uname} (aka. {str_handle}) -> invalid command: /{inp}'
    await context.bot.send_message(chat_id=update.message.chat_id, text=str_conf)
    print(f'\nEXIT - {funcname}\n')

def validate_input(str_input):
    return len(str_input) >= 50

async def gen_ai_img_1(update: Update, context):
    funcname = 'gen_ai_img_1'
    print(cStrDivider_1, f'ENTER - {funcname}', sep='\n')

    user = update.message.from_user
    uid = user.id
    str_handle = user.first_name
    str_uname = user.username
    inp = update.message.text
    str_prompt = inp[inp.find(' ')+1::] # slicing out /<command>
    str_conf = f'@{str_uname} (aka. {str_handle}) -> please wait, generating image ...\n    "{str_prompt}"'
    print(str_conf)

    await context.bot.send_message(chat_id=update.message.chat_id, text=str_conf)

    lst_imgs, err = gen_ai_image(str_prompt)

    if err > 0:
        str_err = f"@{str_uname} (aka. {str_handle}) -> ERR: BING said NO!\n   change it up & try again : /"
        if err == 1:
            str_err = f"@{str_uname} (aka. {str_handle}) -> ERR: description TOO SHORT, need at least 50 chars (~10 words or so)"
        str_err = str_err + f'\n    "{str_prompt}"'
        await context.bot.send_message(chat_id=update.message.chat_id, text=str_err)
        print(str_err)
        return

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
    await context.bot.send_message(chat_id=update.message.chat_id, text=f'@{str_uname} (aka. {str_handle}) -> here is your image\n  "{str_prompt}" ...\n {url}')
    print('', f'EXIT - {funcname}', cStrDivider_1, sep='\n')

async def gen_ai_img_x(update: Update, context):
    funcname = 'gen_ai_img_x'
    print(cStrDivider_1, f'ENTER - {funcname}', sep='\n')

    user = update.message.from_user
    uid = user.id
    str_handle = user.first_name
    str_uname = user.username
    str_text = f'@{str_uname} (aka. {str_handle}) -> please wait, we are generating your images...'
    await context.bot.send_message(chat_id=update.message.chat_id, text=str_text)
    inp = update.message.text
    str_prompt = inp[inp.find(' ')::] # slicing out /<command>
    lst_imgs, err = gen_ai_image(str_prompt)

    public_img_url = lst_imgs[0]
    await context.bot.send_message(chat_id=update.message.chat_id, text=f'@{str_uname} here is one image (for your prompt "{str_prompt}")...\n {public_img_url}\n the rest have been DMed to you!')
    # await context.bot.send_message(chat_id=update.message.chat_id, text=f'@{str_uname} here is one image (for prompt {str_prompt}): {public_img_url}')
    await context.bot.send_message(chat_id=uid, text=f'Hey! Here are all the images generated for your prompt: {str_prompt}')
    for url in lst_imgs:
        await context.bot.send_message(chat_id=uid, text=url)
        # safari = webbrowser.get('safari')  # specify the browser
        # safari.open_new_tab(url)

    print('', f'EXIT - {funcname}', cStrDivider_1, sep='\n')

# def get_rand_cookie(_lst_cookies):
#     idx = random.randint(0, len(_lst_cookies)-1)
#     return idx, _lst_cookies[idx]

def get_rand_cookie(_dict_cookies):
    lst_keys = list(_dict_cookies.keys())
    idx_key = random.randint(0, len(lst_keys)-1)
    str_key = lst_keys[idx_key]
    return idx_key, str_key, _dict_cookies[str_key]
    
def gen_ai_image(str_prompt):
    global IMG_REQUEST_CNT
    funcname = 'gen_ai_image'
    IMG_REQUEST_CNT += 1
    print(f'\nENTER - {funcname} _ IMG_REQUEST_CNT: {IMG_REQUEST_CNT}')
    print(f'str_prompt: {str_prompt}')

    lst_imgs = []
    err = 0

    if not validate_input(str_prompt):
        err = 1
        return lst_imgs, err
    # gen = ImageGen(auth_cookie=cook, auth_cookie_SRCHHPGUSR=cook, quiet=False)
    # lst_imgs = gen.get_images(str_prompt)

    # print('DONE GETTING IMAGES...')
    # print(*lst_imgs, sep='\n')
    # print('SENDING IMAGES...')
    # return lst_imgs, err

    # loop until no exception
    # _idx, _cookie = get_rand_cookie(lst_cookies)
    _idx, _key, _cookie = get_rand_cookie(dict_cookies)
    print(f'cookie idx: {_idx}')
    print(f'cookie key: {_key}')
    while True:
        try:
            gen = ImageGen(auth_cookie=_cookie, auth_cookie_SRCHHPGUSR=_cookie, quiet=False)
            # gen = ImageGenAsync(auth_cookie=cook, quiet=False)
            
            lst_imgs = gen.get_images(str_prompt)
            break  # Exit the loop if no exception is caught
        except Exception as e:
            print_except(e, debugLvl=1)
            print("Exception caught:", e)
            err = 2
            time.sleep(2)  # Wait for 5 seconds before the next attempt
            return lst_imgs, err


    print('DONE GETTING IMAGES...')
    print(*lst_imgs, sep='\n')
    print('SENDING IMAGES...')
    
    print('', f'EXIT - {funcname}', sep='\n')
    return lst_imgs, err

def main():
    # global TOKEN
    dp = Application.builder().token(TOKEN).build()
    # Create the Update and pass in the bot's token
    # update = Update(token=TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    # dp = update.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler("test", test))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("gen_image", gen_ai_img_1))
    dp.add_handler(CommandHandler("gen_image_x", gen_ai_img_x))

    # Register message handler for new chat members
    # dp.add_handler(MessageHandler(filters.StatusUpdate._NewChatMembers, new_chat_members))

    # Register message handler for all other messages
    # dp.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo)) # ~ = negate (ie. AND NOT)
    dp.add_handler(MessageHandler(filters.Command, bad_command))
    # Start the Bot
    dp.run_polling()
    # Update.start_polling()

    # Run the bot until you press Ctrl-C
    # Update.idle()

# if __name__ == '__main__':
#     main()


#------------------------------------------------------------#
#   DEFAULT SUPPORT                                          #
#------------------------------------------------------------#
READ_ME = f'''
    *DESCRIPTION*
        choose blockchain
        get latest tx pool
            OR
        search for 'from' address 
         and loop get tx pool

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
        main()
    except Exception as e:
        print_except(e, debugLvl=0)
    
    ## end ##
    print(f'\n\nRUN_TIME_START: {RUN_TIME_START}\nRUN_TIME_END:   {get_time_now()}\n')

print('', cStrDivider, f'# END _ {__filename}', cStrDivider, sep='\n')