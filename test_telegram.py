#!/usr/bin/env python3
"""
تست سریع Telegram Collector
"""

import asyncio
import os
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی
load_dotenv('config.env')

async def test_telegram_bot():
    """تست ساده Telegram Bot"""
    
    # دریافت Token از محیط
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN', '')
    
    if not bot_token or bot_token == 'your_bot_token_here':
        print("❌ لطفاً ابتدا Bot Token را در فایل config.env تنظیم کنید")
        print("\\n📝 مراحل:")
        print("1. به @BotFather در تلگرام پیام دهید")
        print("2. دستور /newbot را ارسال کنید")
        print("3. نام و username ربات را انتخاب کنید")
        print("4. Token دریافتی را در config.env قرار دهید")
        print("5. دوباره این اسکریپت را اجرا کنید")
        return
    
    print(f"✅ Bot Token یافت شد: {bot_token[:10]}...")
    
    try:
        from telegram import Bot
        
        # ایجاد Bot
        bot = Bot(token=bot_token)
        
        # تست اتصال
        print("🔄 در حال تست اتصال...")
        me = await bot.get_me()
        
        print(f"✅ اتصال موفق!")
        print(f"🤖 نام ربات: {me.first_name}")
        print(f"👤 Username: @{me.username}")
        print(f"🆔 Bot ID: {me.id}")
        
        print("\\n✅ Telegram Bot آماده استفاده است!")
        print("\\n📝 مراحل بعدی:")
        print("1. ربات را به کانال‌های مورد نظر اضافه کنید")
        print("2. کانال‌ها را در config.env تنظیم کنید")
        print("3. telegram_collector.py را اجرا کنید")
        
        return True
        
    except ImportError:
        print("❌ پکیج python-telegram-bot نصب نیست")
        print("\\n📦 برای نصب:")
        print("pip install python-telegram-bot")
        return False
        
    except Exception as e:
        print(f"❌ خطا: {e}")
        print("\\n💡 راهنمایی:")
        print("- Token را بررسی کنید")
        print("- اتصال اینترنت را بررسی کنید")
        print("- VPN خود را فعال کنید (اگر در ایران هستید)")
        return False

if __name__ == "__main__":
    print("🚀 تست Telegram Bot\\n")
    asyncio.run(test_telegram_bot())
