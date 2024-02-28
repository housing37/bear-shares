from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters
import openai
import os
from _env import env

TOKEN = env.TOKEN_neo # neo_bs_bot (neo)
OPENAI_API_KEY = env.OPENAI_KEY
GROUP_ID = '-1002049491115', # $BearShares - testing

print(TOKEN)
print(OPENAI_API_KEY)
print(GROUP_ID)
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
    user_prompt = update.message.text.partition(' ')[2]  # Extract the user's prompt after the command.

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
def group_filter(update: Update) -> bool:
    print(f'ENTER - group_filter _ GROUP_ID: {GROUP_ID}')
    return True
    # return str(update.message.chat_id) == GROUP_ID

def main():
    print('ENTER - main()')
    # Initialize and run the Telegram bot
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("talk", generate_response))
    # app.add_handler(MessageHandler(filters.ChatType.GROUP & filters.Update.message, generate_response))

    # Start the bot
    app.run_polling()
    print('EXIT - main()')

if __name__ == "__main__":
    main()
