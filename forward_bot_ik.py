from telethon import TelegramClient, events
from telethon.network import ConnectionTcpFull
import logging

# Enable detailed logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Telegram API credentials (hardcoded)
api_id = 29052843
api_hash = "cc4e2a7bff47daf36d18bcf81c63e166"
phone = "+2347064976568"
DESTINATION_CHAT_ID = 799248202
SOURCE_CHAT_ID = -1001098711099
KEYWORDS = ["ago palace", "ago", "festac", "isolo", "surulere", "amuwo", "mushin"]

# Initialize client with explicit data center
client = TelegramClient('session_name', api_id, api_hash,
                       connection=ConnectionTcpFull,
                       use_ipv6=False,
                       timeout=30)

@client.on(events.NewMessage(chats=[SOURCE_CHAT_ID]))
async def handler(event):
    message_text = event.message.text.lower() if event.message.text else ""
    found_keywords = [kw for kw in KEYWORDS if kw.lower() in message_text]
    if found_keywords:
        try:
            chat = await event.get_chat()
            sender = await event.get_sender()
            notification = (
                f"Keyword(s) {', '.join(found_keywords)} found in {chat.title or 'Unknown Chat'} (Chat ID: {event.chat_id})\n"
                f"Message: {event.message.text}\n"
                f"From: {sender.first_name or 'Unknown'} (@{sender.username or 'No Username'})"
            )
            await client.forward_messages(DESTINATION_CHAT_ID, event.message)
            await client.send_message(DESTINATION_CHAT_ID, notification)
            logger.info(f"Forwarded message with keywords: {found_keywords}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")

async def main():
    try:
        logger.debug("Attempting to connect to Telegram...")
        await client.start(phone=phone)
        logger.info("Client started successfully")
        await client.run_until_disconnected()
    except Exception as e:
        logger.error(f"Failed to start client: {e}")
        raise

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())