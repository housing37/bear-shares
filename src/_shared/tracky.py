import os
import logging
# from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import json

# Load environment variables
# load_dotenv()
# TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TOKEN = '6911413573:AAGrff9aK3aSfaDhGaT5Iyf68zqRcPHrGN0'

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory storage for demonstration
invite_counts = {}
# Tracks which users have already credited an inviter
user_has_credited = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message."""
    await update.message.reply_text('Welcome! Please mention your inviter by typing @username.')

async def track_invites(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Track the invites based on mentions, ensuring each invited user credits an inviter only once, with detailed logging."""
    user_id = update.message.from_user.id
    username = update.message.from_user.username if update.message.from_user.username else "a user without a username"

    if update.message.entities:
        for entity in update.message.entities:
            if entity.type == 'mention':
                inviter_username = update.message.text[entity.offset:entity.offset+entity.length]
                logger.info(f"Mention detected from {username} ({user_id}) to {inviter_username}")

                if user_id in user_has_credited:
                    logger.warning(f"{username} ({user_id}) attempted to credit {inviter_username} again.")
                    await update.message.reply_text("You have already credited your inviter.")
                else:
                    invite_counts[inviter_username] = invite_counts.get(inviter_username, 0) + 1
                    user_has_credited[user_id] = inviter_username
                    confirmation_message = f"{inviter_username} has been credited by you. Total invites: {invite_counts[inviter_username]}."
                    await update.message.reply_text(confirmation_message)
                    logger.info(f"{username} ({user_id}) successfully credited {inviter_username}. Total now: {invite_counts[inviter_username]}")
                return  # Exit after processing a mention to avoid sending additional messages

async def display_invites(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display the number of invites per user for admins with styled Markdown formatting."""
    chat_member = await context.bot.get_chat_member(update.message.chat_id, update.message.from_user.id)
    if chat_member.status in ['administrator', 'creator']:
        # Start building the message with Markdown formatting
        message = "*Invites per user:*\n"
        for user, count in invite_counts.items():
            # Escape special characters in the username
            escaped_username = user.replace('_', r'\_').replace('*', r'\*').replace('[', r'\[').replace(']', r'\]').replace('(', r'\(').replace(')', r'\)').replace('~', r'\~').replace('`', r'\`').replace('>', r'\>').replace('#', r'\#').replace('+', r'\+').replace('-', r'\-').replace('=', r'\=').replace('|', r'\|').replace('{', r'\{').replace('}', r'\}').replace('.', r'\.').replace('!', r'\!')
            # Append each user and their invite count, formatting usernames as bold
            message += f"**{escaped_username}**: {count} invite(s)\n"
        
        # Escape special characters in the message text
        escaped_message = message.replace('_', r'\_').replace('*', r'\*').replace('[', r'\[').replace(']', r'\]').replace('(', r'\(').replace(')', r'\)').replace('~', r'\~').replace('`', r'\`').replace('>', r'\>').replace('#', r'\#').replace('+', r'\+').replace('-', r'\-').replace('=', r'\=').replace('|', r'\|').replace('{', r'\{').replace('}', r'\}').replace('.', r'\.').replace('!', r'\!')

        # Send the message with MarkdownV2 parse mode
        await context.bot.send_message(chat_id=update.effective_chat.id, text=escaped_message, parse_mode="MarkdownV2")
    else:
        await update.message.reply_text("You do not have permission to use this command.")

def export_invite_counts() -> None:
    """Export invite counts to a JSON file."""
    with open('invite_counts.json', 'w') as file:
        json.dump(invite_counts, file)

def import_invite_counts() -> None:
    """Import invite counts from a JSON file."""
    global invite_counts
    try:
        with open('invite_counts.json', 'r') as file:
            invite_counts = json.load(file)
    except FileNotFoundError:
        logger.warning("Invite counts file not found. Starting with empty counts.")

async def check_pinned_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Check pinned messages for mentions."""
    # Implementation goes here
    pass

def main() -> None:
    """Start the bot."""
    import_invite_counts()  # Import invite counts from file

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, track_invites))
    application.add_handler(CommandHandler("invites", display_invites))
    application.add_handler(CommandHandler("checkpinned", check_pinned_messages))  # Add command to check pinned messages

    application.run_polling()

    export_invite_counts()  # Export invite counts to file

if __name__ == '__main__':
    main()
