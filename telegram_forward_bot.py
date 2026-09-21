import asyncio import logging import os from telegram import Update from telegram.ext import Application, ContextTypes, MessageHandler, filters from telegram.error import TelegramError
logging.basicConfig( format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO ) logger = logging.getLogger(name)
BOT_TOKEN = os.getenv("BOT_TOKEN") SOURCE_CHANNEL_ID = int(os.getenv("SOURCE_CHANNEL_ID", "-100123456789")) DESTINATION_CHANNEL_ID = int(os.getenv("DESTINATION_CHANNEL_ID", "-100987654321"))
FORWARD_FILTERS = { "photos": True, "videos": True, "documents": True, "text": True, "links": True, }
async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: try: message = update.message
    if not should_forward_message(message):
        return
    
    await message.forward(chat_id=DESTINATION_CHANNEL_ID)
    logger.info(f"✅ Forwarded message ID {message.message_id}")
    
except TelegramError as e:
    logger.error(f"❌ Telegram error: {e}")
except Exception as e:
    logger.error(f"❌ Error: {e}")
def should_forward_message(message) -> bool: if message.text and FORWARD_FILTERS["text"]: return True if message.photo and FORWARD_FILTERS["photos"]: return True if message.video and FORWARD_FILTERS["videos"]: return True if message.document and FORWARD_FILTERS["documents"]: return True if message.entities and FORWARD_FILTERS["links"]: return True
return False
async def start_logging(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: await update.message.reply_text( "🤖 Auto-Forward Bot Started!\n\n" f"📤 Source: {SOURCE_CHANNEL_ID}\n" f"📥 Destination: {DESTINATION_CHANNEL_ID}" )
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: logger.error(f"Error: {context.error}")
def main(): if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE": logger.error("❌ Set BOT_TOKEN!") return
application = Application.builder().token(BOT_TOKEN).build()

application.add_handler(
    MessageHandler(filters.COMMAND, start_logging)
)

application.add_handler(
    MessageHandler(
        filters.Chat(SOURCE_CHANNEL_ID) & ~filters.COMMAND,
        forward_message
    )
)

application.add_error_handler(error_handler)

logger.info("🚀 Bot starting...")
application.run_polling(allowed_updates=Update.ALL_TYPES)
if name == 'main': main()
