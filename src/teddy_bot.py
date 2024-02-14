# import logging

# from telegram import Update, ForceReply, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

# logger = logging.getLogger(__name__)

# # Store bot screaming status
# screaming = False

# # Pre-assign menu text
# FIRST_MENU = "<b>Menu 1</b>\n\nA beautiful menu with a shiny inline button."
# SECOND_MENU = "<b>Menu 2</b>\n\nA better menu with even more shiny inline buttons."

# # Pre-assign button text
# NEXT_BUTTON = "Next"
# BACK_BUTTON = "Back"
# TUTORIAL_BUTTON = "Tutorial"

# # Build keyboards
# FIRST_MENU_MARKUP = InlineKeyboardMarkup([[
#     InlineKeyboardButton(NEXT_BUTTON, callback_data=NEXT_BUTTON)
# ]])
# SECOND_MENU_MARKUP = InlineKeyboardMarkup([
#     [InlineKeyboardButton(BACK_BUTTON, callback_data=BACK_BUTTON)],
#     [InlineKeyboardButton(TUTORIAL_BUTTON, url="https://core.telegram.org/bots/api")]
# ])


# def echo(update: Update, context: CallbackContext) -> None:
#     """
#     This function would be added to the dispatcher as a handler for messages coming from the Bot API
#     """

#     # Print to console
#     print(f'{update.message.from_user.first_name} wrote {update.message.text}')

#     if screaming and update.message.text:
#         context.bot.send_message(
#             update.message.chat_id,
#             update.message.text.upper(),
#             # To preserve the markdown, we attach entities (bold, italic...)
#             entities=update.message.entities
#         )
#     else:
#         # This is equivalent to forwarding, without the sender's name
#         update.message.copy(update.message.chat_id)


# def scream(update: Update, context: CallbackContext) -> None:
#     """
#     This function handles the /scream command
#     """

#     global screaming
#     screaming = True


# def whisper(update: Update, context: CallbackContext) -> None:
#     """
#     This function handles /whisper command
#     """

#     global screaming
#     screaming = False


# def menu(update: Update, context: CallbackContext) -> None:
#     """
#     This handler sends a menu with the inline buttons we pre-assigned above
#     """

#     context.bot.send_message(
#         update.message.from_user.id,
#         FIRST_MENU,
#         parse_mode=ParseMode.HTML,
#         reply_markup=FIRST_MENU_MARKUP
#     )


# def button_tap(update: Update, context: CallbackContext) -> None:
#     """
#     This handler processes the inline buttons on the menu
#     """

#     data = update.callback_query.data
#     text = ''
#     markup = None

#     if data == NEXT_BUTTON:
#         text = SECOND_MENU
#         markup = SECOND_MENU_MARKUP
#     elif data == BACK_BUTTON:
#         text = FIRST_MENU
#         markup = FIRST_MENU_MARKUP

#     # Close the query to end the client-side loading animation
#     update.callback_query.answer()

#     # Update message content with corresponding menu section
#     update.callback_query.message.edit_text(
#         text,
#         ParseMode.HTML,
#         reply_markup=markup
#     )


# def main() -> None:
#     updater = Updater("6911413573:AAGrff9aK3aSfaDhGaT5Iyf68zqRcPHrGN0")

#     # Get the dispatcher to register handlers
#     # Then, we register each handler and the conditions the update must meet to trigger it
#     dispatcher = updater.dispatcher

#     # Register commands
#     dispatcher.add_handler(CommandHandler("scream", scream))
#     dispatcher.add_handler(CommandHandler("whisper", whisper))
#     dispatcher.add_handler(CommandHandler("menu", menu))

#     # Register handler for inline buttons
#     dispatcher.add_handler(CallbackQueryHandler(button_tap))

#     # Echo any message that is not a command
#     dispatcher.add_handler(MessageHandler(~Filters.command, echo))

#     # Start the Bot
#     updater.start_polling()

#     # Run the bot until you press Ctrl-C
#     updater.idle()


# if __name__ == '__main__':
#     main()


from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.ext import CallbackQueryHandler, CallbackContext
# from telegram import ChatAction
import time
import random

import os
import webbrowser
# myst37.020
# cook = "1CIx4heldQFrBstIQ-KL7d7ix-Rif8Di0yW_vsuk-Gsfb9lGzgTWTQ20KJ5oJR_Y7bmVNNKrKS_MVEN4v-OjGPVVsQ2a-h9zZkMC90Fj74frtXRSfKPzzJ5p8hdX27bfvEgUQlVJAzC92Mo_dFLTYvr_SgpQrFp-eUbdI-cByE9F57vWbER9z287be7cdsw6TP1_BYzzC9G1jkpYMgi-vYw"
lst_cookies =[
    # myst37.014
    "1-AhuVhuYkNn4kh6m8T72bEg4xn9S6wqt0TWqDWcbS1NUnO4SLoWWMr4VhaXuV1j1W56-2H8ihDg5SYH8cZQPox6mOyxpCYojTcAFvpNvMSKLa9WlILBMTG65xcyvB2Z4IpSNnmqCkHTFtUJSSiV7avAYVvz72M1RhIPCGeqszXfGcLpOk9z6We4jCaNNzf2SGQzKPlYt6k-aC6le2hrCVg",
    # myst37.015
    "1HVwcZVHsgR9AH6Lmu_VeRCtSsrI6b9SBu9U0Grj8KGqOVxJRrCZUfjSs1NNS448h2ttG0Egsoc3dsrFku7D5R7z9WyHDcKYqxdfrQCMsZThEjIedubs8BFS4zOwryk-vsv2zuvTbA3BOlrFjcl4tQInXEq3Xdv04EWHADeWfTfBgWWo-Oxoiylj9KvKUx7_sV5vxq72lR0HxiDQDPvCngQ",
    # myst37.016
    "1RTGjcQkCYaUfk-jI4OCe1K1lFb0N60SUcgwT46onrYd2_UITKYzLttpSETocCEcsdKSLdzdRlP9NBl1xwpWfx1egozVMigurWjjdA0CiTUCQlP4MCG7p_UcB-VEsGEq09Y0c-IPpi5Bf5lelCzg0peWwy5cGOd2J23GLViWpBD-k1UNkfhfdiT7T1GxDePCmxt744-a1dHjLVrLEA9dkDQ",
    # myst37.021
    "1BmCGFpK08XlfcXBQf_W6iF_BPh6i9cg-6JAuA17tC_tlg7nGW-VG2c4VSqoa_okPgQTs5qjNRmSgifp30jJ20YAOdFACU6JmOHc8EDfSnszQrmQqwSOOHAmub8bGfPIM7rRn86TjoPXqFtn0a96w-R6F53-ne5EZo55sb6Dxt2vOZxsug5pDrtNW5K-hqGBeZj_yhxf_uffBWt_LIF3BEg",
    # myst37.022
    "15b2vveo09pnXUXXW6wOlLXbpP88N2tKXr_r3ePQdv0lyvo49iqDXjjnaw5kim6tCOKeHKDeGTN4JzlDkoeW-WkpzXX_jWiHqxTFcQh_jzsEmtPL-ou1Q9vWShc_JT1NI4b9gTvjGdUrsez3bIEsu6GXIRvCipa4OASe_GnAc7WW2Ajv1IEVA0JRQ2w3_ByNT76zdTHDOJrgsTZzoN8s4Ag"
]
# os.environ["BING_COOKIES"] = cook
from BingImageCreator import ImageGen, ImageGenAsync

# Telegram Bot token obtained from BotFather
TOKEN = '6911413573:AAGrff9aK3aSfaDhGaT5Iyf68zqRcPHrGN0'
# BEAR_BOT = Bot(token=TOKEN)

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
    print(f'\nENTER - {funcname}\n')

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
        str_err = f"@{str_uname} (aka. {str_handle}) -> ERR: an unknown error has occurred\n  BING said NO!\n   maybe you used a bad word or something, please try again : /"
        if err == 1:
            str_err = f"@{str_uname} (aka. {str_handle}) -> ERR: input description is TOO SHORT, must be at least 50 chars (~10 words or so)"
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
    print(f'\nEXIT - {funcname}\n')

async def gen_ai_img_x(update: Update, context):
    funcname = 'gen_ai_img_x'
    print(f'\nENTER - {funcname}\n')

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
    print(f'\nEXIT - {funcname}\n')

def get_rand_cookie(_lst_cookies):
    idx = random.randint(0, len(_lst_cookies)-1)
    return idx, _lst_cookies[idx]
    
def gen_ai_image(str_prompt):
    funcname = 'gen_ai_image'
    print(f'\nENTER - {funcname}\n')
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
    _idx, _cookie = get_rand_cookie(lst_cookies)
    print(f'using cookie idx: {_idx}')
    while True:
        try:
            gen = ImageGen(auth_cookie=_cookie, auth_cookie_SRCHHPGUSR=_cookie, quiet=False)
            # gen = ImageGenAsync(auth_cookie=cook, quiet=False)
            
            lst_imgs = gen.get_images(str_prompt)
            break  # Exit the loop if no exception is caught
        except Exception as e:
            print("Exception caught:", e)
            err = 2
            time.sleep(2)  # Wait for 5 seconds before the next attempt
            return lst_imgs, err


    print('DONE GETTING IMAGES...')
    print(*lst_imgs, sep='\n')
    print('SENDING IMAGES...')
    print(f'\nEXIT - {funcname}\n')
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

if __name__ == '__main__':
    main()
