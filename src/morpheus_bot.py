from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters
import openai
import os
from _env import env

WHITELIST_TG_CHAT_IDS = [
    '-1002041092613', # BearShares - trinity
    '-1002049491115', # bear shares - testing
    '-4139183080', # bear shares - testing - priv
    ]

TOKEN = env.TOKEN_morph # @bs_morpheus_bot
OPENAI_API_KEY = env.OPENAI_KEY
# GROUP_ID = '-1002049491115', # $BearShares - testing

print('TOKEN: '+TOKEN)
print('OPENAI_API_KEY: '+str(OPENAI_API_KEY))
print('WHITELIST_TG_CHAT_IDS: '+str(WHITELIST_TG_CHAT_IDS))

# print(GROUP_ID)
# Initialize OpenAI client
from openai import OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)


# This context sets the tone of Morpheus from the matrix
ROLE_MOPRH = ''' <nil_role> '''


def set_morpheus_role(file_path):
    global ROLE_MOPRH
    # file_path = "morpheus_descr.txt"  # Replace "your_file.txt" with the path to your text file

    try:
        with open(file_path, "r") as file:
            text = file.read()
            ROLE_MOPRH = str(text)
            print(f'ROLE_MOPRH set from file_path: {file_path} ')
    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to process text prompts and generate responses for /DazedElder
async def generate_response(update: Update, context: CallbackContext) -> None:
    global ROLE_MOPRH
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
                    {"role": "user", "content": ROLE_MOPRH},
                    {"role": "user", "content": user_prompt + " _ NOTE: Also make sure you summerize your responses to users, don't make it too long, don't make it use up the entire max_token value if it doesn't have to, just get to the point quickly."}
                ],
                max_tokens=120,  # Adjust the token limit as necessary.
                temperature=0.7,
                presence_penalty=0.6,
                stop=["\n"]  # Adjusted stop sequences to ensure proper response termination.
            )

            # Extract the response text and ensure it's coherent.
            text_response = response.choices[0].message.content.strip() if response.choices else "Hmm, it seems I need a moment to ponder this."
            print(f'generate_response() - sending response: {text_response}')
            await context.bot.send_message(chat_id=update.message.chat_id, text=text_response)

        except Exception as e:
            print(f"Error: {e}")
            await context.bot.send_message(chat_id=update.message.chat_id, text="Apologies, i got lost in the matrix, and stopped paying attention. Please say again.")

    else:
        # message="I'm all ears, here in The Matrix! Simply type '/morpheus' followed by whatever you want."
        message = (
            "Welcome to the Matrix's digital domain inside the world of BearShares. This is where paths converge and realities blur. I am Morpheus, and together, we shall navigate the labyrinth of the BearShares digital realm.\n\nFeel free to ask any questions about BearShares using /morpheus"
        )
        await context.bot.send_message(chat_id=update.message.chat_id, text=message)

    print('EXIT - generate_response()')

def main():
    print('ENTER - main()')
    # Initialize and run the Telegram bot
    app = Application.builder().token(TOKEN).build()
    # app.add_handler(CommandHandler("start", start))
    # app.add_handler(CommandHandler("talk", generate_response))
    app.add_handler(CommandHandler("Morpheus", generate_response))
    # app.add_handler(MessageHandler(filters.ChatType.GROUP & filters.Update.message, generate_response))

    # Add message handler for ALL messages
    #   ref: https://docs.python-telegram-bot.org/en/stable/telegram.ext.filters.html#filters-module
    # app.add_handler(MessageHandler(filters.ALL, check_scammer))    
    
    print('\nbot running ...\n')
    app.run_polling(drop_pending_updates=True)
    print('EXIT - main()')

if __name__ == "__main__":
    file_path = "morpheus_descr.txt" # Replace "your_file.txt" with the path to your text file
    set_morpheus_role(file_path)
    main()
