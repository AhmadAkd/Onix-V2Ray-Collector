#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Telegram Bot Starter
راه‌انداز ساده ربات تلگرام
"""

import asyncio
import logging
import os
import sys
from telegram_bot_enhanced import EnhancedTelegramBot


def setup_logging():
    """تنظیم لاگ‌گیری"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('telegram_bot.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def get_bot_token():
    """دریافت Bot Token"""
    # اول از متغیر محیطی
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if token:
        return token

    # سپس از فایل .env
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('TELEGRAM_BOT_TOKEN='):
                    return line.split('=', 1)[1].strip()
    except FileNotFoundError:
        pass

    # در نهایت hardcoded
    return "8474552244:AAERRNE4n7_aFIeqxRlwEmutYn9jUvd9yUQ"


async def main():
    """تابع اصلی"""
    print("🤖 Starting V2Ray Collector Telegram Bot...")

    # تنظیم لاگ‌گیری
    setup_logging()
    logger = logging.getLogger(__name__)

    # دریافت Bot Token
    bot_token = get_bot_token()
    if not bot_token:
        logger.error("❌ Bot token not found!")
        print("❌ Bot token not found!")
        print("💡 Please set TELEGRAM_BOT_TOKEN environment variable or create .env file")
        return

    logger.info(f"✅ Bot token loaded: {bot_token[:10]}...")
    print(f"✅ Bot token loaded: {bot_token[:10]}...")

    # ایجاد ربات
    bot = EnhancedTelegramBot(bot_token)

    # دریافت اطلاعات ربات
    print("📡 Getting bot info...")
    bot_info = await bot.get_bot_info()

    if bot_info:
        print(f"✅ Bot info retrieved:")
        print(f"  Name: {bot_info.get('first_name')}")
        print(f"  Username: @{bot_info.get('username')}")
        print(f"  ID: {bot_info.get('id')}")

        logger.info(f"Bot initialized: @{bot_info.get('username')}")
    else:
        print("❌ Failed to get bot info")
        logger.error("Failed to get bot info")
        return

    # حذف webhook موجود (اگر وجود دارد)
    print("🔗 Cleaning up webhook...")
    await bot.delete_webhook()

    # شروع polling
    print("🚀 Starting bot polling...")
    print("📱 Bot is now running! Send /start to your bot in Telegram.")
    print("⏹️  Press Ctrl+C to stop the bot.")

    try:
        await bot.start_polling()
    except KeyboardInterrupt:
        print("\n⏹️  Bot stopped by user")
        logger.info("Bot stopped by user")
    except Exception as e:
        print(f"❌ Bot error: {e}")
        logger.error(f"Bot error: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)
