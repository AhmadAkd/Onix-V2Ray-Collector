#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Telegram Bot Test
تست ساده ربات تلگرام
"""

import asyncio
import os
from telegram_bot_enhanced import EnhancedTelegramBot

async def test_bot():
    """تست ربات"""
    print("🤖 Testing Telegram Bot...")
    
    # Bot Token from environment
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8474552244:AAERRNE4n7_aFIeqxRlwEmutYn9jUvd9yUQ')
    
    # ایجاد ربات
    bot = EnhancedTelegramBot(BOT_TOKEN)
    
    # تست اطلاعات ربات
    print("📡 Getting bot info...")
    bot_info = await bot.get_bot_info()
    
    if bot_info:
        print(f"✅ Bot Name: {bot_info.get('first_name')}")
        print(f"✅ Bot Username: @{bot_info.get('username')}")
        print(f"✅ Bot ID: {bot_info.get('id')}")
        print(f"✅ Admin Users: {list(bot.admin_users)}")
        
        # تست ارسال پیام به ادمین
        admin_id = 6563143907
        test_message = """
🤖 **تست ربات تلگرام**

✅ ربات فعال است
📱 آماده دریافت دستورات
👑 ادمین: @Deltamax (6563143907)

**دستورات موجود:**
/start - شروع کار
/help - راهنما
/stats - آمار سیستم
/configs - دریافت کانفیگ‌ها
/admin - دستورات ادمین

**تست موفق!** 🎉
        """
        
        print("📤 Sending test message to admin...")
        success = await bot.send_message(admin_id, test_message)
        
        if success:
            print("✅ Test message sent successfully!")
        else:
            print("❌ Failed to send test message")
        
        return True
    else:
        print("❌ Failed to get bot info")
        return False

async def main():
    """تابع اصلی"""
    print("🚀 Telegram Bot Simple Test")
    print("=" * 50)
    
    success = await test_bot()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Test Result: SUCCESS")
        print("🎉 Bot is working correctly!")
    else:
        print("❌ Test Result: FAILED")
        print("💡 Check bot token and configuration")

if __name__ == "__main__":
    asyncio.run(main())
