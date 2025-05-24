__fname = 'teddy_app'
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
        $ python3.11 -m pip install telethon
    REQUIREMENTS... (python3.12 -> required '--break-system-packages')
        $ python3 -m pip install telethon --break-system-packages
'''
# ref: my.telegram.org
# Use the api_id and api_hash from my.telegram.org (set in env.py -> .env)
from telethon import TelegramClient, events
from datetime import datetime
from _env import env
client = TelegramClient('session_name', env.API_ID, env.API_HASH)
ROSE_ID = '609517172'
CHAT_ID = -1002030864744 # Pulse Rekt Room (formally plusd scam room)
TOOL_ID = '1343247050', # @Cryptoking2022 - 'DAVE | OMNIPRESENT' - pDAI scammer
TEST_ID = '1427560544' # JSSgram
AUTO_DELETE_MSG = [TOOL_ID, ]
def get_time_now(dt=True):
    if dt: return '['+datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[0:-4]+']'
    return '['+datetime.now().strftime("%H:%M:%S.%f")[0:-4]+']'

@client.on(events.NewMessage)
async def handle_message(event):
    # only hande -> Pulse Rekt Room
    if str(event.message.chat_id) != str(CHAT_ID):
        return
    
    sender = await event.get_sender()
    usr_handle = sender.first_name
    message_id = event.message.id
    if sender:
        print(f"{get_time_now()} _ uid: {sender.id}, user_at|handle: @{sender.username} | {usr_handle}, msg_id: {message_id}, chat_id: {event.message.chat_id}, txt: {event.text}")
        # if str(sender.id) == ROSE_ID and str(event.message.chat_id) == str(CHAT_ID) and 'hous' in event.text:
        #     await client.delete_messages(entity=CHAT_ID, message_ids=[message_id])
        #     print(f"  Deleted msg_id {message_id} from chat {CHAT_ID}\n   msg: {event.text}")
        if str(sender.id) in AUTO_DELETE_MSG and str(event.message.chat_id) == str(CHAT_ID):
            await client.delete_messages(entity=CHAT_ID, message_ids=[message_id])
            print(f"  Deleted msg_id {message_id} from chat {CHAT_ID}\n   msg: {event.text}")
    else:
        print(f"Message (no sender): {event.text}")

async def main():
    await client.start(phone=env.API_USR_PHONE)
    print("Listening for messages...")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())


# ALT INTEGRATIN (UN-TESTED)
# from pyrogram import Client, filters

# # Replace with your credentials
# api_id = 123456
# api_hash = 'your_api_hash_here'
# phone = '+1234567890'

# # Create the client
# app = Client("my_account", api_id=api_id, api_hash=api_hash, phone_number=phone)

# # Message handler
# @app.on_message(filters.all)
# async def log_message(client, message):
#     sender = message.from_user
#     if sender:
#         print(f"ID: {sender.id}, Username: @{sender.username}, Message: {message.text}")
#     else:
#         print(f"Message (no sender): {message.text}")

# # Run the client
# app.run()