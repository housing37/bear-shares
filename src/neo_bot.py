from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters
import openai
import os
from _env import env

WHITELIST_TG_CHAT_IDS = [
    '-1002041092613', # $BearShares
    '-1002049491115', # bear shares - testing
    '-4139183080', # bear shares - testing - priv
    ]

# check scammer: ['5486688786', '@Genstlell', 'Teller']
BLACKLIST_SCAM_UNAMES = [
    '@EmileUly',
    '@AlexSandros6', # 7017221881, @AlexSandros6, Alex sandros
    '@Genstlell', # ['5486688786', '@Genstlell', 'Teller']
    '@KriskcKrypto', # recommended by @psi931 (simon B) _ 031224
]
BLACKLIST_SCAM_UIDS = [
    # '581475171', # @housing37
    '7017221881', # 7017221881, @AlexSandros6, Alex sandros
    '5486688786', # ['5486688786', '@Genstlell', 'Teller']
]
BLACKLIST_SCAM_HANDLES = [
    'Alex sandros', # 7017221881, @AlexSandros6, Alex sandros
    'Teller', # ['5486688786', '@Genstlell', 'Teller']
]
BLACKLIST_SCAM_TEXT = [
    'BlastPulsechain', # 7017221881, @AlexSandros6, Alex sandros
    '$BLAST', # 7017221881, @AlexSandros6, Alex sandros
    '$Wen', # ['5486688786', '@Genstlell', 'Teller']
]

TOKEN = env.TOKEN_neo # neo_bs_bot (neo)
OPENAI_API_KEY = env.OPENAI_KEY
# GROUP_ID = '-1002049491115', # $BearShares - testing

print('TOKEN: '+TOKEN)
print('OPENAI_API_KEY: '+str(OPENAI_API_KEY))
print('WHITELIST_TG_CHAT_IDS: '+str(WHITELIST_TG_CHAT_IDS))
print('BLACKLIST_SCAM_UIDS: '+str(BLACKLIST_SCAM_UIDS))
print('BLACKLIST_SCAM_UNAMES: '+str(BLACKLIST_SCAM_UNAMES))
print('BLACKLIST_SCAM_HANDLES: '+str(BLACKLIST_SCAM_HANDLES))
print('BLACKLIST_SCAM_TEXT: '+str(BLACKLIST_SCAM_TEXT))

# print(GROUP_ID)
# Initialize OpenAI client
from openai import OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)


# This context sets the tone of Neo from the matrix
role_neo = "I need you to act as Neo from 'The Matrix' movie series. Channel his persona, his style, and his character as you respond to the user's prompts."

# Function to handle the /start command
async def start(update: Update, context: CallbackContext) -> None:
    # Welcome message that introduces users to DazedElder's mystical persona
    message = (
        "Welcome, wanderer, to the Matrix's digital domain, where paths converge and realities blur. You've stepped into the chat room, a silent nexus where thoughts echo and algorithms whisper. Here, the boundaries of the tangible fade, and the unseen currents of data dictate existence. Pause, contemplate, for within these binary whispers lie the enigma of endless possibilities. Remember, I am Neo, and together, we shall navigate the labyrinth of the Matrix's digital realm."
    )
    await context.bot.send_message(chat_id=update.message.chat_id, text=message)

# Function to process text prompts and generate responses for /DazedElder
async def generate_response(update: Update, context: CallbackContext) -> None:
    print('ENTER - generate_response()')
    group_name = update.message.chat.title if update.message.chat.type == 'supergroup' else None
    _chat_id = update.message.chat_id
    print("chat_id:", _chat_id)
    if group_name:
        print("Group name:", group_name)
    else:
        print("*NOTE* This message was not sent from a group.")

    user_prompt = update.message.text.partition(' ')[2]  # Extract the user's prompt after the command.
    print(f'user_prompt: {user_prompt}')

    # check if TG group is allowed to use the bot
    if str(_chat_id) not in WHITELIST_TG_CHAT_IDS:
        print("*** WARNING ***: non-whitelist TG group trying to use the bot; returning ...")
        print('EXIT - generate_response()')
        return
    
    if user_prompt:        
        # Attempt to call the OpenAI API with the adjusted method.
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": role_neo},
                    {"role": "user", "content": user_prompt + " NOTE: make sure yo summerize your response, don't make it too long, and get to the point quickly."}
                ],
                max_tokens=60,  # Adjust the token limit as necessary.
                temperature=0.7,
                presence_penalty=0.6,
                stop=["\n", "Neo:"]  # Adjusted stop sequences to ensure proper response termination.
            )

            # Extract the response text and ensure it's coherent.
            text_response = response.choices[0].message.content.strip() if response.choices else "Hmm, it seems I need a moment to ponder this."
            print(f'generate_response() - sending response: {text_response}')
            await context.bot.send_message(chat_id=update.message.chat_id, text=text_response)

        except Exception as e:
            print(f"Error: {e}")
            await context.bot.send_message(chat_id=update.message.chat_id, text="Apologies, i got lost in the matrix, and stopped paying attention. Please say again.")

    else:
        await context.bot.send_message(chat_id=update.message.chat_id, text="I'm all ears, here in The Matrix! Simply type '/talk' followed by whatever you want.")

    print('EXIT - generate_response()')

# Function to filter messages from the specified Telegram group
# def group_filter(update: Update) -> bool:
#     print(f'ENTER - group_filter _ GROUP_ID: {GROUP_ID}')
#     return str(update.message.chat_id) == GROUP_ID

async def check_scammer(update: Update, context):
    if update.message.from_user == None:
        print("check_scammer _ found '.message.from_user' = NoneType; attempting to print message.text, then failing...")
        print(update.message.text)

    user = update.message.from_user

    # get all input (to parse .lower() in compare)
    uid = str(user.id)
    usr_at_name = f'@{user.username}'
    usr_handle = str(user.first_name)
    inp_text = str(update.message.text)

    lst_user_data = [uid, usr_at_name, usr_handle]
    print(f'check scammer: {lst_user_data}')

    # generate all BLACKLIST .lower() to compare
    lst_uid = [t.lower() for t in BLACKLIST_SCAM_UIDS]
    lst_uname = [t.lower() for t in BLACKLIST_SCAM_UNAMES]
    lst_handle = [t.lower() for t in BLACKLIST_SCAM_HANDLES]
    lst_text = [t.lower() for t in BLACKLIST_SCAM_TEXT]

    # check blacklist text
    b_scam_text = False
    for t in lst_text:
        if t in inp_text.lower():
            print(f'FOUND scam text: {t} _ inp_text:\n  {inp_text}')
            b_scam_text = True

    # checks blacklist of @user and tg_uid and tg_handle
    if b_scam_text or uid.lower() in lst_uid or usr_at_name.lower() in lst_uname or usr_handle.lower() in lst_handle:
        print(f'FOUND scammer: {lst_user_data}')
        await update.message.reply_text(f"@{usr_at_name} is a known scammer, ignore him 🙄️️️️️️")

def main():
    print('ENTER - main()')
    # Initialize and run the Telegram bot
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("talk", generate_response))
    app.add_handler(CommandHandler("neo", generate_response))
    # app.add_handler(MessageHandler(filters.ChatType.GROUP & filters.Update.message, generate_response))

    # Add message handler for ALL messages
    #   ref: https://docs.python-telegram-bot.org/en/stable/telegram.ext.filters.html#filters-module
    app.add_handler(MessageHandler(filters.ALL, check_scammer))    
    
    # Start the bot
    app.run_polling()
    print('EXIT - main()')

if __name__ == "__main__":
    main()
