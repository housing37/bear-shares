__fname = 'teddy_bot'
__filename = __fname + '.py'
cStrDivider = '#================================================================#'
cStrDivider_1 = '#----------------------------------------------------------------#'
print('', cStrDivider, f'GO _ {__filename} -> starting IMPORTs & declaring globals', cStrDivider, sep='\n')
'''
    REQUIREMENTS... (python3.11)
        $ sudo add-apt-repository ppa:deadsnakes/ppa -y
        $ sudo apt update
        $ sudo apt install python3.11
        $ python3.11 --version
        $ python3.11 -m pip install python-telegram-bot BingImageCreator
        $ python3.11 -m pip install cffi
        $ python3.11 -m pip install --ignore-installed openai
        $ python3.11 -m pip install tweepy selenium lxml read_env
    REQUIREMENTS... (python3.12 -> required '--break-system-packages')
        $ python3 -m pip install python-telegram-bot BingImageCreator --break-system-packages
        $ python3 -m pip install tweepy selenium lxml read_env --break-system-packages
'''

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.ext import CallbackQueryHandler, CallbackContext
# from telegram import ChatAction
import time, threading
import random
from datetime import datetime
import json, time, os, traceback, sys
import webbrowser
# os.environ["BING_COOKIES"] = cook
from BingImageCreator import ImageGen, ImageGenAsync
from openai import OpenAI # pip install openai
import tweepy, requests, os, url_short
# from testing import gen_img.BingImgGenerator
# from testing import BingImgGenerator
from _test.gen_img import BingImgGenerator
from _env import env
# Now you can use BingImgGenerator in teddy_bot.py

DEBUG_PRINT_LEVEL = 1

# NOTE: browser inspector says cookies expire in ~14 days (2 weeks)
#   cookies below created: 02.17.24 or earlier
dict_cookies ={
    "bear37.012":
    "1NwrFzGaK8Kq3Ad61Tr6oJLvCZbdB6awMEGEYolfrfrdqEycaWu-EVpBDcoCsY-MtakFNdetR1SGfWZF3DasY4ej48dsYiC6vwAJoqpPOjJSv9mggCn_L3nTQUuvuqON0hu7qUhN-jxV9SBBz1MYgXDAhrqwmbZ4HJ66CuEQOJYBsqn3Fawg5OTv8JDLHaouQA5aR9GqvVZCAmJqGi4l1kQ7ao9Gc44RD50MLPOB9CIY",
    "bear37.008":
    "10RN0qwZcnwu_OAn3vRbgXQApaFyUMnWVHEFphMY4LiX3t_oDjxJjiGrs1FoUAfa2WCrC0IOvcuyTIQGgeZExfei62LJC1UZX3ArFnHNXBP_PfQ6bL6DwuLVCe94CDoC1sTenbVsK5MdRlIiTlMcKmB0fbu8ILiAOH9qQ56g_qquSKHtfyXP7kXeW8rKN5thZNj7yebd_GDUwRByzoG3MtQ",
    "bear37.007":
    "119HjqE1nJNvTrQeGcH6rzCHT5PkoFBtI58q77wQx9bQItFgvMbHpUmG0FARi7JGE64zHakJsksLz9KZ4PzUszNFj5XmTi3b2br6es6WZ0fniLATDQBnWzXWciFwU03nsqAmGJOO6xBsyh6TBk4J0_i8i2FExlX2MOIuOCcLcP7rNkHee2R7mRUSW5z8rtZEg2bs3-XJwLlsFfrNB3AgM8Q",
    "bear37.006":
    "1vzxHTu2YFDzWZUXCFZebL6_jLJPAaAJpv05laagtwoZw5rQw_FS0ViK8rFL4WO4rKUhGSJJvSOA6O_o6gkrBTLqkLeaRt3sXgYKUsY_RYujUY_S0PvNintKXglKjhcQ54DjW141ZTS4M9eOfX8fydOU_PTlKyao0OMamxHpykPvaUYBk_AyaoadWgG1Go74LVBRMUS5b-bEvt-T_WsAq2Q",
    "bear37.005":
    "1blMo3vKvsBUhncM8TCtBgCQtnQKOckqrxOQNFyKvPcMxK1qA941UdydLNIWEgr4TNHBvfMFTMaAY_WYh-2ANgQGs8sZDJhEuah7N6ihmMgheb3KcrZH9xO3tWVXgXEwlXgPUcm8krXXsL1TPpZ6ciVYA0lzpqUZOHI2Bi_tYC11fS_L0EBf47HWcN4wK0p7aNlavT6Q72ZmXNeCQktAXFQ",
    "bear37.004":
    "1tuUM7FlAGQk3suWakRbic5lger_ogljcVicprlGJIgOrzx2DFOzYZu7WLwExqSuiyBTuzQmwVu9zo45IWkL6XR0L-yWkjXmxU08c36VCnVJAuSFnLtZyEU6HKZRHZoRbsln0Zld5Q2yyboKULI6Z3eBa6093qCFP0NP_6ezBc3NO2GQ7AHLkP7JCCR3UQnfyGQEkGhHW0FVNAkf4MAnIRw",
    "bear37.003":
    "1eGR1oDkHYMYnMhqJviowUjZ42EtIaPam7UeawgUSWTSjgqscIl_dyiymbAYNYbOiO5YAjNN03k0IvvgpGpqUpkqsGkUy9gqiHoppksvD0ZphRE4vOugomSgT353q1eUy76dPFmZybCETVMPgsBzcJAgyU_Z4f9tsTUfgpGpoM18McVCvT2WN0ggF_7z8Uim5_LJ4qHatQbYXQVWxu_0AnA",
    "bear37.002":
    "11y9lpdJUGEmUp28oQ4rxScJAAyy5xXmNBNW1tOCtyLNldaYSv50CnyB_DT6CxGBuGVWiqEOjHgLQIiRH67NVxMlC5vY0XPFsr-gZ2L0qPwwfvHdeNZpcz3XvOFkC69Vo_ir1dNiYry-3pyzDdjgd5pJt_l_ONx916wwGnL-0mCzJaDx3c5QmnBaI_OLjPwHFxtY4nqZvFsOrb8IzXBn9pDEBpACYr2ADHxYQcFhzy54",
    "bear37.001":
    "1WeMHVixB_2yoKeH8fUIdDbH1Wqx7qRmb9VBK0hIff06hvkxbTq-pOSjolhISDSEkSB8TUEEBXlqXCyEsxVdneKY-bi2tqesP6pezTzrGyzffXO-M0sisDxDlqIuAhwsQ7WpJFKZoIGNHuX_Rl2CeCrNY6nKxTrHQLrzLSVHnnbtLJodNyznbSupBWVxCcvRp0QQV28B66q1Hj-K9R0oKkA",

    "myst37.014":
    "1O6qciHnTFDgJ03jeUGnyBaAqJJYSBPgHXH40-YsLu98wLrXvhaddk1Q58S2HdItxybkBnF2CRXn19cN6mfGPEv4885wJMwqjRCJ0EfJLZMNpvILQ8o22im_5q1DTRnqNv_G6mnNTV8OvXXVLaSzxfaDWly8UnLebIvpiQpe0ih9679E3pbYmojYlLROlAgh_Ov9qvJghHNuR6tZlKxCVMg",
    "myst37.015":
    "1vfrfP_8hf-1Bh_fwm9gSTw6nupNV5ZeKR_7UhcYrWOyz07C_axau9EY9hmMPeVAbE0YRlKwz4X5ugRLGvv4ORjLYscCqBPtf9s3_cALCGuAjBj5-ewRtk7Hm7VFvIC4UqgHlxfys1bfI4leH8dryZJnxVlfL1xkNlcNqKCBmeU2shcb3kAN7zgNl9PlLcwy4NZfHykPLSw807WaKn61vxw",
    "myst37.016":
    "11JioWskagKPJr8R8yZ-t5pNQl0OeEra2OXSosp8LgNL9OZeVcnx4kBd6oWfBLk1hRfh0SrVlivJYPSFvZmt-sn2V1dlNVmzJ1omwNsnODuZNrzwvWGAcTcIOyyRn8yxP9v1zmm4Sf6g8LPAOfmklf8V1mDj2nz8wRsw1hD8FQvUm9HXszlY924DfcJeYOVgyBjkRq78av1xiH3WnSM-aBQ",
    "myst37.017":
    "18m5eiyraHoefftPy3APxWjljtk1ZPnL7G23R2lypkZhOag-KOStZPxIjVon279wv5pyRnQUfGwWZzilzjSsfXg_7oqefQUohz98oJe7FrWTuHvimBnSxffW0FClHF4dna8UUOe1W6SkTRUoXJKJ7eYF5MdWx43uM8PfZqGmOWEb-K6q0Gjde2pjV8iSWVQOIJg_RW_gOhu1FFB1iS3Rr2w",
    "myst37.018":
    "1yJTyZdFLqHqNkO46kJSCEdPI1xBisx_sWovMAsfTu6bjNBRo6mNLORzVwFeq4OJWA04iR9-JBctTT3CI2dOT9N67e9smYkIUCTjGTKO4xYhx64M2JqMgd-J9MzRLSzfJTKpxK9yyxiT7Vqrdc_nOKX3ZmSXT2CXjG02GFrdpKvfJlTsXELzUMCkb7rbc8XmYCaHODrM_trpX60aPgrO42g",
    "myst37.019":
    "1kN1Y9EW_S-C5Jz6idhVSrJ051fXNYHdi_dfeC0rEw305lPxxCPYeQh6lI3hVUqs2rL-ZBP11vn4xGiGJcCl2A4N8fuEqW1ZiEkIKDdqALLVb32QiAJGTny76uCGLkTFyO90uDBVEvN0JgHbkcYxEPJ5TCYHgegSmZf2coO3YejEcF69frCw2EhRG-GY6WDj0ibqO5uV9y0dbgQdgZCI-vA",
    "myst37.020":
    "15Qcr0DG07nUL-JRNH4NjiLrmO4YY57zKG8cbPThzMc23aObETd32Ey1m8U2CfN6Y8hVO_iobUCu5rezyNUP4vsfAh3AKggJVQCr-mBiQ03dnbOpvjpNTMmY2c1_3zXiO_UlZDbjyRheQt490rboOdAAAVWTUDPA9773t2X3qz7isjHfKk8n2m05CPOnHu0om-5cha9jpHn6hqbxk_hce5w",
    "myst37.021":
    "1jbyrRLRU4xfAUtRZngWIbO7KFy2kNi9bMCt81wmuITnMbZMe-2i42sFz530SNU_JUS7vQEDMB1CzGYplRmHowCD1XZn5edSLxRe7dozczMItteERwrYVTaZcYiI2OQkLXRrGS9b80yOjW_gOWIO_klZwlSO-JVZyKMBqNRWJcGR0u192ZA-jlW21MuLUXNWNvJFZ6Cuepz8LLqyCEtIApw",
    "myst37.022":
    "1SSgxK-AK9szOZgW5VucHQs3cZvNzJJ8EE3cHHP5c7r6IdrQ_qAvGTOYPWakQ6kjfumFosvTYGtsPm_TO119AKhxORgINBmbrd9hT1cF6v1qgBP_PjINJI3fyBF0aVk0WK-sE2NtF8AVJG-h7knYgu6Pv4sJ6MKiKUKVW91TIOBgxVSHuthw3n_VjplTS87tDWHdwqZxPUySODoqhwNCW0g",
}
DICT_LOGINS ={
    "bear37.001@hotmail.com":
    "bear102938",
    "bear37.002@hotmail.com":
    "bear102938",
    "bear37.003@hotmail.com":
    "bear102938",
    "bear37.004@hotmail.com":
    "bear102938",
    "bear37.005@hotmail.com":
    "bear102938",
    "bear37.006@hotmail.com":
    "bear102938",
    # "bear37.007@hotmail.com":
    # "bear102938",
    # "bear37.008@hotmail.com":
    # "bear102938",
    # "bear37.009@hotmail.com":
    # "bear102938",
}

# Telegram Bot token obtained from BotFather
USE_RAND_COOKIE = False
USE_GEN_IMG = False
USE_PROD = False
IMG_REQUEST_CNT = 0
IMG_REQUEST_SUCCESS_CNT = 0
TOKEN = 'nil_token'
CONSUMER_KEY = 'nil_key'
CONSUMER_SECRET = 'nil_key'
ACCESS_TOKEN = 'nil_key'
ACCESS_TOKEN_SECRET = 'nil_key'
PROMO_TWEET_TEXT = 'nil_text'
# LST_ADMINS = ['@housing37', '@WhiteRabbit0x0', '@mrGabriel7']
LST_ADMINS = ['@housing37', '@WhiteRabbit0x0']
# LST_ADMINS = ['@housing37']
IDX_LAST_COOKIE = -1

# Dictionary to keep track of users who have been greeted
greeted_users = {}

USE_OPEN_AI = False
OPENAI_KEY = 'nil_key'
USE_HD_GEN = False
RESP_RECEIVED = False
USE_SHORT_URL = True

WHITELIST_TG_CHAT_IDS = [
    '-1002041092613', # $BearShares
    '-1002049491115', # $BearShares - testing
    '-4139183080', # TeddyShares - testing
    '581475171', # @
    '-1002030864744', # Pulse Rekt Room (formally plusd scam room)
    ]
BLACKLIST_TEXT = [
    'smart vault', 'smart-vault', 'smart_vault', # @JstKidn
    ]
SELENIUM_HEADLESS = True
MIN_DESCR_CHAR_CNT = 25
MIN_DESCR_WORD_CNT = int(MIN_DESCR_CHAR_CNT / 5)
#------------------------------------------------------------#
#   FUNCTIONS                                                #
#------------------------------------------------------------#
def set_tg_token():
    global TOKEN
    TOKEN = env.TOKEN_prod if USE_PROD else env.TOKEN_dev

def init_openAI_client():
    global OPENAI_KEY
    OPENAI_KEY = env.OPENAI_KEY

def set_twitter_auth_keys():
    global CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
    # @SolAudits
    CONSUMER_KEY = env.CONSUMER_KEY_0
    CONSUMER_SECRET = env.CONSUMER_SECRET_0
    ACCESS_TOKEN = env.ACCESS_TOKEN_0
    ACCESS_TOKEN_SECRET = env.ACCESS_TOKEN_SECRET_0
    if USE_PROD:
        # @BearSharesX
        CONSUMER_KEY = env.CONSUMER_KEY_1
        CONSUMER_SECRET = env.CONSUMER_SECRET_1
        ACCESS_TOKEN = env.ACCESS_TOKEN_1
        ACCESS_TOKEN_SECRET = env.ACCESS_TOKEN_SECRET_1

def set_twitter_promo_text():
    global PROMO_TWEET_TEXT
    PROMO_TWEET_TEXT = 'Test auto tweet w/ image\n\nFind this souce code @ t.me/SolAudits0\nOnly on #PulseChain'
    if USE_PROD:
        PROMO_TWEET_TEXT = 'New #BearShares NFT image created!\n\nGenerate your own @ t.me/BearShares\nOnly on #PulseChain'

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
    funcname = 'bad_command'
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
    return len(str_input) >= MIN_DESCR_CHAR_CNT

def validate_admin_user(str_uname):
    global LST_ADMINS
    return False if str_uname == None else '@'+str_uname in LST_ADMINS

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
    print(cStrDivider_1, f'ENTER - {funcname} _ {get_time_now()}', sep='\n')
    str_uname = update.callback_query.from_user.username
    str_handle = update.callback_query.from_user.first_name
    print(f'from user: @{str_uname} (aka. {str_handle})')
    if not validate_admin_user(str_uname):
        str_resp = f'@housing37 or @WhiteRabbit0x0 tweet requested (from: @{str_uname}): '
        message_id = update.callback_query.message.message_id
        chat_id = update.effective_chat.id
        # post_link = f"t.me/BearShares/{chat_id}?message_id={message_id}"
        post_link = f"t.me/BearShares/{message_id}" # ex: https://t.me/BearShares/3284
        str_resp = str_resp + post_link
        
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
    
    # tweet promo (note: callback_data[1:] = remove '@' from user name )
    str_tweet = PROMO_TWEET_TEXT + f'\n\nauthor: t.me/{callback_data[1:]}' # should we use 't.me/username' ?
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

    str_resp = f'\ntweet: {url}\nauthor: {callback_data}\nplease like & rt'
    if not success:
        str_resp = f'@{str_uname} (aka. {str_handle}) -> Promo Tweet FAILED to send : /'
    print(f'\nstr_resp: {str_resp}')
    await context.bot.send_message(chat_id=update.callback_query.message.chat_id, text=str_resp)

    print('', f'EXIT - {funcname} _ {get_time_now()}', cStrDivider_1, sep='\n')

def filter_prompt(_prompt):
    funcname = 'filter_prompt'
    print(f'ENTER - {funcname}')
    prompt_edit = _prompt.lower()
    found_blacklist = False
    for i in BLACKLIST_TEXT:
        print(i)
        # if BLACKLIST_TEXT[i] in prompt_edit:
        if i in prompt_edit:
            print(f'found BLACKLIST_TEXT: {i}')
            prompt_edit = prompt_edit.replace(i, 'bear shares')
            found_blacklist = True

    if found_blacklist:
        return prompt_edit
    return _prompt

async def gen_ai_img_1(update: Update, context):
    global USE_OPEN_AI
    funcname = 'gen_ai_img_1'
    print(cStrDivider_1, f'ENTER - {funcname} _ {get_time_now()}', sep='\n')
    group_name = update.message.chat.title if update.message.chat.type == 'supergroup' else None
    _chat_id = update.message.chat_id
    print("chat_id:", _chat_id)
    if group_name:
        print("Group name:", group_name)
    else:
        print("*NOTE* This message was not sent from a group.")
    user = update.message.from_user
    uid = user.id
    str_handle = user.first_name
    str_uname = user.username
    inp = update.message.text
    

    # check if TG group is allowed to use the bot
    if str(_chat_id) not in WHITELIST_TG_CHAT_IDS:
        print("*** WARNING ***: non-whitelist TG group trying to use the bot; sending deny message...")
        str_conf = f"@{str_uname} (aka. {str_handle}) -> NO! Fuck Off! Don't steal like a #Democrat :/ "
        print(str_conf)
        await context.bot.send_message(chat_id=update.message.chat_id, text=str_conf)    
        print('', f'EXIT - {funcname} _ {get_time_now()}', cStrDivider_1, sep='\n')
        return

    str_prompt = inp[inp.find(' ')+1::] # slicing out /<command>

    # filter / update prompt to deal with spammers (using 'BLACKLIST_TEXT')
    str_prompt = filter_prompt(str_prompt)

    str_conf = f'@{str_uname} (aka. {str_handle}) -> please wait, generating image ...\n    "{str_prompt}"'
    print(str_conf)
    # await context.bot.send_message(chat_id=update.message.chat_id, text=str_conf)
    await update.message.reply_text(f" ... i'll give it a shot 👍️️ ")

    if USE_OPEN_AI:
        lst_imgs, err = gen_ai_image_openAI(str_prompt)
    else:
        lst_imgs, err = gen_ai_image(str_prompt)
    
    if err > 0:
        str_err = f"@{str_uname} (aka. {str_handle}) -> BING said NO!\n   change it up & try again : /"
        str_err_reply = f" ... BING said NO, try changing it up 🤷️️️️️️"
        if err == 1:
            str_err = f"@{str_uname} (aka. {str_handle}) -> description TOO SHORT, need at least {MIN_DESCR_CHAR_CNT} chars (~{MIN_DESCR_WORD_CNT} words or so)"
            str_err_reply = f" ... description TOO SHORT, need about {MIN_DESCR_WORD_CNT} words"
        str_err = str_err + f'\n    "{str_prompt}"'
        # await context.bot.send_message(chat_id=update.message.chat_id, text=str_err)
        await update.message.reply_text(str_err_reply)
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

    if USE_SHORT_URL:
        url = url_short.make_tiny(url)

    # Create an inline keyboard markup with a button
    inline_keyboard = [
        [InlineKeyboardButton("Request Tweet", callback_data=f'@{str_uname} (aka. {str_handle})')]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    try:
        # await context.bot.send_message(
        #     chat_id=update.message.chat_id, 
        #     text=f'@{str_uname} (aka. {str_handle}) -> here is your image\n  "{str_prompt}" ...\n {url}',
        #     # reply_markup = ReplyKeyboardMarkup([['Your Button Text']])
        #     reply_markup = reply_markup
        #     )
        await update.message.reply_text(f" ... your image ...\n {url}", reply_markup = reply_markup)
    except Exception as e:
        # note_021724: exception added for TG: @enriquebambo (aka. 🍊 👾 𝐄η𝐑𝕚ⓀẸⓑᗩｍ𝕓ㄖ 👾🍊 {I DM First, I'm Impostor})
        #   sending response with TG button was causing a crash (but images were indeed successfully received from BING)
        print_except(e, debugLvl=DEBUG_PRINT_LEVEL)
        print('Sending to TG w/o tweet button... ')
        # await context.bot.send_message(
        #     chat_id=update.message.chat_id, 
        #     text=f'@{str_uname} (aka. {str_handle}) -> here is your image\n  "{str_prompt}" ...\n {url}')
        await update.message.reply_text(f" ... your image ...\n {url}")
    print('', f'EXIT - {funcname} _ {get_time_now()}', cStrDivider_1, sep='\n')

def gen_ai_image_openAI(str_prompt):
    global IMG_REQUEST_CNT, IMG_REQUEST_SUCCESS_CNT, USE_HD_GEN
    funcname = 'gen_ai_image_openAI'
    IMG_REQUEST_CNT += 1
    print(f'\nENTER - {funcname} _ IMG_REQUEST_CNT: {IMG_REQUEST_CNT}')
    print(f'str_prompt: {str_prompt}')

    lst_imgs = []
    err = 0

    if not validate_input(str_prompt):
        err = 1
        return lst_imgs, err

    try:
        lst_imgs = exe_request_openAI(str_prompt, USE_HD_GEN) # True = HD (False = standard)
        IMG_REQUEST_SUCCESS_CNT += 1

    except Exception as e:
        print_except(e, debugLvl=1)
        print(f'img request cnt: {IMG_REQUEST_CNT}')
        print(f'img request success ratio: {IMG_REQUEST_SUCCESS_CNT}/{IMG_REQUEST_CNT}')
        # print("Exception caught:", e)
        err = 2
        time.sleep(2) # force user to wait for next attempt
        return lst_imgs, err
        
    print(f'img request cnt: {IMG_REQUEST_CNT}')
    print(f'img request success ratio: {IMG_REQUEST_SUCCESS_CNT}/{IMG_REQUEST_CNT}')
    print('', f'EXIT - {funcname} _ IMG_REQUEST_CNT: {IMG_REQUEST_CNT}', sep='\n')
    return lst_imgs, err

def exe_request_openAI(descr, use_hd=False):
    global OPENAI_KEY, RESP_RECEIVED
    print(f'ENTER - exe_request_openAI')
    
    quality = 'hd' if use_hd else 'standard'
    print(f'Sending request... openAI (quality: {quality}) _ {get_time_now()}')
    print('waiting for results... openAI')

    try:
        # start 'print_wait_dots' waiting thread
        RESP_RECEIVED = False
        dot_thread = threading.Thread(target=print_wait_dots)
        dot_thread.start()

        # execute request to openAI
        client = OpenAI(api_key=OPENAI_KEY)
        response = client.images.generate(
            model="dall-e-3",
            prompt=descr,
            size="1024x1024",
            quality=quality,
            n=1,
        )

    except Exception as e:
        print_except(e, debugLvl=1)
        raise
    finally:
        # end/join print 'dot' thread for waiting
        RESP_RECEIVED = True
        dot_thread.join()
    
    print(f'\nresponse recieved _ {get_time_now()}')
    # print(response.data)
    revised_prompt = response.data[0].revised_prompt
    image_url = response.data[0].url
    print(f'revised_prompt...\n {revised_prompt}')
    print(f'image_url...\n {image_url}')

    print(f'\nEXIT - exe_request_openAI _ {get_time_now()}')
    return [image_url]

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

def get_next_login(_dict_logins):
    global IDX_LAST_COOKIE
    lst_emails = list(_dict_logins.keys())
    login_cnt = len(lst_emails)
    idx_email = 0 if IDX_LAST_COOKIE == login_cnt-1 else IDX_LAST_COOKIE + 1
    str_pw = lst_emails[idx_email]
    IDX_LAST_COOKIE = idx_email
    return idx_email, str_pw, _dict_logins[str_pw]

def get_rand_login(_dict_logins):
    lst_emails = list(_dict_logins.keys())
    idx_email = random.randint(0, len(lst_emails)-1)
    str_pw = lst_emails[idx_email]
    return idx_email, str_pw, _dict_logins[str_pw]

def get_next_cookie(_dict_cookies):
    global IDX_LAST_COOKIE
    lst_keys = list(_dict_cookies.keys())
    cookie_cnt = len(lst_keys)
    idx_key = 0 if IDX_LAST_COOKIE == cookie_cnt-1 else IDX_LAST_COOKIE + 1
    str_key = lst_keys[idx_key]
    IDX_LAST_COOKIE = idx_key
    return idx_key, str_key, _dict_cookies[str_key]

def get_rand_cookie(_dict_cookies):
    lst_keys = list(_dict_cookies.keys())
    idx_key = random.randint(0, len(lst_keys)-1)
    str_key = lst_keys[idx_key]
    return idx_key, str_key, _dict_cookies[str_key]
    
def gen_ai_image(str_prompt):
    global IMG_REQUEST_CNT, IMG_REQUEST_SUCCESS_CNT, USE_GEN_IMG, USE_RAND_COOKIE, SELENIUM_HEADLESS
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
    
    if USE_GEN_IMG:
        # _idx, _key, _cookie = get_next_login(DICT_LOGINS)
        _idx, _key, _cookie = get_rand_login(DICT_LOGINS)
    else:
        if USE_RAND_COOKIE:
            _idx, _key, _cookie = get_rand_cookie(dict_cookies)
        else:
            _idx, _key, _cookie = get_next_cookie(dict_cookies)
    
    print(f'cookie idx: {_idx}\ncookie key: {_key}')

    try:
        if USE_GEN_IMG:
            big = BingImgGenerator(_key, _cookie) # selenium integration
            lst_imgs = big.execute_gen_image(str_prompt, use_cli=False, headless=SELENIUM_HEADLESS) 
            if len(lst_imgs) == 0: err = 2
        else:
            gen = ImageGen(auth_cookie=_cookie, auth_cookie_SRCHHPGUSR=_cookie, quiet=False)
            # gen = ImageGenAsync(auth_cookie=cook, quiet=False)
            lst_imgs = gen.get_images(str_prompt)

        IMG_REQUEST_SUCCESS_CNT += 1

    except Exception as e:
        print_except(e, debugLvl=DEBUG_PRINT_LEVEL)
        print(f'cookie idx: {_idx}\ncookie key: {_key}')
        print(f'img request cnt: {IMG_REQUEST_CNT}')
        print(f'img request success ratio: {IMG_REQUEST_SUCCESS_CNT}/{IMG_REQUEST_CNT}')
        # print("Exception caught:", e)
        err = 3
        time.sleep(2)  # Wait for 5 seconds before the next attempt
        return lst_imgs, err

    print('DONE GETTING IMAGES from BING...')
    # print(*lst_imgs, sep='\n')
    print(f'cookie idx: {_idx}\ncookie key: {_key}')
    print(f'img request cnt: {IMG_REQUEST_CNT}')
    print(f'img request success ratio: {IMG_REQUEST_SUCCESS_CNT}/{IMG_REQUEST_CNT}')
    print('', f'EXIT - {funcname} _ IMG_REQUEST_CNT: {IMG_REQUEST_CNT}', sep='\n')
    return lst_imgs, err

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
    # dp.add_handler(MessageHandler(filters.Command, bad_command))

    # Add message handler for ALL messages
    #   ref: https://docs.python-telegram-bot.org/en/stable/telegram.ext.filters.html#filters-module
    dp.add_handler(MessageHandler(filters.ALL, log_activity))
    print('added handler ALL: log_activity')

    # Start the Bot
    print('\nbot running ...\n')
    dp.run_polling(drop_pending_updates=True)

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

def print_wait_dots():
    global RESP_RECEIVED
    while not RESP_RECEIVED:
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(1)  # Adjust sleep duration as needed
        
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
        USE_PROD = True if inp == '0' else False
        print(f'  input = {inp} _ USE_PROD = {USE_PROD}')

        ans = input('\nUse openAI? [y/n]:\n  > ')
        USE_OPEN_AI = True if ans == 'y' or ans == '1' else False
        print(f'  input = {ans} _ USE_OPEN_AI = {USE_OPEN_AI}')
        if USE_OPEN_AI:
            ans = input('\nUse HD image generating? [y/n]:\n  > ')
            USE_HD_GEN = True if ans == 'y' or ans == '1' else False
            print(f'  input = {ans} _ USE_HD_GEN = {USE_HD_GEN}')
        else:
            # select to use gen_img.py or no (not = using BingImageCreator.py)
            inp = input("\nUse selenium gen_img.py? [y/n]\n  > ")
            USE_GEN_IMG = True if inp == 'y' or inp == '1' else False
            print(f'  input = {inp} _ USE_GEN_IMG (selenium) = {USE_GEN_IMG}')

            # if not using selenium (ie. indeed using cookies & not emails)
            if not USE_GEN_IMG:
                # select to use random cookie
                inp = input("\nCycle through cookies randomly? [y/n]\n  > ")
                USE_RAND_COOKIE = True if inp == 'y' or inp == '1' else False
                print(f'  input = {inp} _ USE_RAND_COOKIE = {USE_RAND_COOKIE}')
        
        # TOKEN = TOKEN_prod if USE_PROD else TOKEN_dev
        set_tg_token()
        init_openAI_client()
        set_twitter_auth_keys()
        set_twitter_promo_text()
        print(f'\nSELENIUM_HEADLESS: {SELENIUM_HEADLESS}')
        print(f'Telegram TOKEN: {TOKEN}')
        print(f'OpenAI OPENAI_KEY: {OPENAI_KEY}')
        print(f'CONSUMER_KEY: {CONSUMER_KEY}')
        print(f'PROMO_TWEET_TEXT:\n{PROMO_TWEET_TEXT}\n') 
        main()
    except Exception as e:
        print_except(e, debugLvl=DEBUG_PRINT_LEVEL)
    
    ## end ##
    print(f'\n\nRUN_TIME_START: {RUN_TIME_START}\nRUN_TIME_END:   {get_time_now()}\n')

print('', cStrDivider, f'# END _ {__filename}', cStrDivider, sep='\n')