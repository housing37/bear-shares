__fname = 'teddy_bot'
__filename = __fname + '.py'
cStrDivider = '#================================================================#'
cStrDivider_1 = '#----------------------------------------------------------------#'
print('', cStrDivider, f'GO _ {__filename} -> starting IMPORTs & declaring globals', cStrDivider, sep='\n')

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.ext import CallbackQueryHandler, CallbackContext
# from telegram import ChatAction
import time
import random
from datetime import datetime
import json, time, os, traceback, sys
import webbrowser
# os.environ["BING_COOKIES"] = cook
from BingImageCreator import ImageGen, ImageGenAsync
import tweepy, requests, os

# myst37.020
# cook = "1CIx4heldQFrBstIQ-KL7d7ix-Rif8Di0yW_vsuk-Gsfb9lGzgTWTQ20KJ5oJR_Y7bmVNNKrKS_MVEN4v-OjGPVVsQ2a-h9zZkMC90Fj74frtXRSfKPzzJ5p8hdX27bfvEgUQlVJAzC92Mo_dFLTYvr_SgpQrFp-eUbdI-cByE9F57vWbER9z287be7cdsw6TP1_BYzzC9G1jkpYMgi-vYw"
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

# Telegram Bot token obtained from BotFather
USE_PROD = False
IMG_REQUEST_CNT = 0
TOKEN_dev = '6911413573:AAGrff9aK3aSfaDhGaT5Iyf68zqRcPHrGN0' # TeddySharesBot (dev)
TOKEN_prod = '6805964502:AAHL99OquXuZUPzpgqWNDbeBY_pgGpANO0A' # BearSharesBot (prod)
TOKEN = TOKEN_prod if USE_PROD else TOKEN_dev
CONSUMER_KEY = 'nil_key'
CONSUMER_SECRET = 'nil_key'
ACCESS_TOKEN = 'nil_key'
ACCESS_TOKEN_SECRET = 'nil_key'
PROMO_TWEET_TEXT = 'nil_text'

# Dictionary to keep track of users who have been greeted
greeted_users = {}

def set_twitter_promo_text():
    global PROMO_TWEET_TEXT
    PROMO_TWEET_TEXT = 'Test auto tweet w/ image\n\nFind this souce code @ t.me/SolAudits0\nOnly on #PulseChain'
    if USE_PROD:
        PROMO_TWEET_TEXT = 'New $BearShares NFT image created!\n\nGenerate your own @ t.me/BearShares\nOnly on #PulseChain'

def set_twitter_auth_keys():
    global CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
    # @SolAudits
    CONSUMER_KEY = 'ufotTV5H0BMXgCS9p1Hf9LOM6'
    CONSUMER_SECRET = 'Cped9xDs4T0gpC0guq9CVETAMryB6jqTMhyHmb0f3wfLorBKKX'
    ACCESS_TOKEN = '1754679966657056768-9PKkUuNWKvpTBuPjTh8q9r9LBmX14w'
    ACCESS_TOKEN_SECRET = 'CLw7QEu83Y7NI0lXTOMXGBRMErDgb9nxO9rSPJUY8A8bo'
    if USE_PROD:
        # @BearSharesNFT
        CONSUMER_KEY = 'HdZLxkPGZNAzWOzFlVNEqxIeP'
        CONSUMER_SECRET = 'f2yUKDkLniQKEwouoheUbcJxFNPR2brieGQPq6t0gFGFGdV2dJ'
        ACCESS_TOKEN = '1756813801020596224-UBAFOB3xtW6xrVykGBPKAovZ6kDiMd'
        ACCESS_TOKEN_SECRET = 'qKNnDiSZrRFGbR4WCey2MXpG3XNLpmfTDa2jzeSMZxq1P'


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

# async def button_click(update: Update, context: CallbackContext) -> None:
#     query = update.callback_query
#     query.answer()
#     user_id = query.from_user.id
#     message = "You have started a conversation with the bot. Now you can interact with it."

#     # Send a message acknowledging the button click
#     await query.message.reply_text(message)

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

def validate_admin_user(str_uname):
    lst_admins = ['@housing37', '@WhiteRabbit0x0', '@mrGabriel7']
    return '@'+str_uname in lst_admins

def get_img_from_url(img_url):
    funcname = 'get_img_from_url'
    print(cStrDivider_1, f'ENTER - {funcname}', sep='\n')
    img_file = 'image.jpg'
    success = False
    response = requests.get(img_url)
    if response.status_code == 200:
        with open(img_file, 'wb') as image_file:
            image_file.write(response.content)
        success = True
    else:
        print("Failed to download image.")
    print('', f'EXIT - {funcname} _ status: {success}', cStrDivider_1, sep='\n')
    return img_file, success # success / fail

def delete_img_file(img_file):
    funcname = 'delete_img_file'
    print(cStrDivider_1, f'ENTER - {funcname}', sep='\n')
    os.remove(img_file)
    print("Image file deleted.")
    print('', f'EXIT - {funcname}', cStrDivider_1, sep='\n')
    
def tweet_promo(str_tweet, img_url):
    funcname = 'tweet_promo'
    print(cStrDivider_1, f'ENTER - {funcname}', sep='\n')

    # Authenticate to Twitter
    client = tweepy.Client(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )
    auth = tweepy.OAuth1UserHandler(
        CONSUMER_KEY,
        CONSUMER_SECRET,
        ACCESS_TOKEN,
        ACCESS_TOKEN_SECRET,
    )

    # Create API object
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # download image
    img_file, success = get_img_from_url(img_url)
    if not success:
        print("FAILED - Tweeted promo with image!")
        print('', f'EXIT - {funcname}', cStrDivider_1, sep='\n')
        return None, False

    # Upload image and tweet
    media = api.media_upload(img_file)
    response = client.create_tweet(text=str_tweet, media_ids=[media.media_id])
    print("Tweeted promo with image!")

    # clean up
    delete_img_file(img_file)

    print('', f'EXIT - {funcname}', cStrDivider_1, sep='\n')
    return response, True

async def button_click(update: Update, context: CallbackContext) -> None:
    funcname = 'button_click'
    print(cStrDivider_1, f'ENTER - {funcname}', sep='\n')
    str_uname = update.callback_query.from_user.username
    str_handle = update.callback_query.from_user.first_name
    print(f'from user: @{str_uname} (aka. {str_handle})')
    if not validate_admin_user(str_uname):
        str_resp = f'NOPE! user not allowed'
        await context.bot.send_message(chat_id=update.callback_query.message.chat_id, text=str_resp)
        print(str_resp)
        print('', f'EXIT - {funcname}', cStrDivider_1, sep='\n')
        return
    
    # original message data & specified 'InlineKeyboardButton' callback_data
    og_msg_data = update.callback_query.message.text
    callback_data = update.callback_query.data
    img_url = og_msg_data[og_msg_data.find('http')::]

    # Perform your desired actions here
    print(f'og_msg_data: {og_msg_data}')
    print(f'callback_data: {callback_data}') # callback_data = '@username (aka. handle)'
    print(f'img_url: {img_url}')
    
    # tweet promo
    str_tweet = PROMO_TWEET_TEXT + f'\n\nauthor: TG -> {callback_data}' # should we use 't.me/username' ?
    response, success = tweet_promo(str_tweet, img_url) # callback_data = TG author
    tweet_data = response.data
    tweet_text = tweet_data['text']
    idx_start = tweet_text.rfind('http')
    url = tweet_text[idx_start::]
    # print(f'response: {response}')
    # print(f'tweet_data: {tweet_data}')
    print(f'tweet_text:\n{tweet_text}')
    # print(f'idx_start: {idx_start}')
    print(f'\nurl: {url}')

    str_resp = f'@{str_uname} (aka. {str_handle}) -> Promo Tweet Sent Successfully!\n  tweet: {url}\n  author: {callback_data}'
    if not success:
        str_resp = f'@{str_uname} (aka. {str_handle}) -> Promo Tweet FAILED to send : /'
    print(f'\nstr_resp: {str_resp}')
    await context.bot.send_message(chat_id=update.callback_query.message.chat_id, text=str_resp)

    print('', f'EXIT - {funcname}', cStrDivider_1, sep='\n')
    
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
        str_err = f"@{str_uname} (aka. {str_handle}) -> err: BING said NO!\n   change it up & try again : /"
        if err == 1:
            str_err = f"@{str_uname} (aka. {str_handle}) -> err: description TOO SHORT, need at least 50 chars (~10 words or so)"
        str_err = str_err + f'\n    "{str_prompt}"'
        await context.bot.send_message(chat_id=update.message.chat_id, text=str_err)
        print(str_err)
        print('', f'EXIT - {funcname}', cStrDivider_1, sep='\n')
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

    # Create an inline keyboard markup with a button
    inline_keyboard = [
        [InlineKeyboardButton("Tweet This Promo", callback_data=f'@{str_uname} (aka. {str_handle})')]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    await context.bot.send_message(
        chat_id=update.message.chat_id, 
        text=f'@{str_uname} (aka. {str_handle}) -> here is your image\n  "{str_prompt}" ...\n {url}',
        # reply_markup = ReplyKeyboardMarkup([['Your Button Text']])
        reply_markup = reply_markup
        )
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

    # loop until no exception
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
            # print("Exception caught:", e)
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
    dp.add_handler(CommandHandler("tweet_promo", tweet_promo))
    # Add the button click handler
    dp.add_handler(CallbackQueryHandler(button_click))
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
        inp = input('Select token type to use:\n  0 = prod (@BearSharesBot)\n  1 = dev (@TeddySharesBot)\n  > ')
        USE_PROD = True if inp == '0' else False
        print(f'  input = {inp} _ USE_PROD = {USE_PROD}')

        TOKEN = TOKEN_prod if USE_PROD else TOKEN_dev
        set_twitter_auth_keys()
        set_twitter_promo_text()
        print(f'\nCONSUMER_KEY: {CONSUMER_KEY}')
        print(f'PROMO_TWEET_TEXT:\n{PROMO_TWEET_TEXT}\n') 
        main()
    except Exception as e:
        print_except(e, debugLvl=0)
    
    ## end ##
    print(f'\n\nRUN_TIME_START: {RUN_TIME_START}\nRUN_TIME_END:   {get_time_now()}\n')

print('', cStrDivider, f'# END _ {__filename}', cStrDivider, sep='\n')