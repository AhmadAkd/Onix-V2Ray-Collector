#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Webhook Bot for GitHub Pages
ربات تلگرام با Webhook برای GitHub Pages
"""

import asyncio
import json
import logging
from typing import Dict, Any
from telegram_bot_enhanced import EnhancedTelegramBot

# تنظیم logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebhookTelegramBot:
    """ربات تلگرام با Webhook"""
    
    def __init__(self, bot_token: str):
        self.bot = EnhancedTelegramBot(bot_token)
        self.webhook_url = "https://ahmadakd.github.io/Onix-V2Ray-Collector/webhook"
        
    async def setup_webhook(self) -> bool:
        """تنظیم Webhook"""
        try:
            # حذف webhook قبلی
            await self.bot.delete_webhook()
            
            # تنظیم webhook جدید
            success = await self.bot.set_webhook(self.webhook_url)
            
            if success:
                logger.info("✅ Webhook configured successfully")
                return True
            else:
                logger.error("❌ Failed to configure webhook")
                return False
                
        except Exception as e:
            logger.error(f"❌ Webhook setup error: {e}")
            return False
    
    async def handle_webhook(self, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """پردازش Webhook"""
        try:
            if 'message' not in update_data:
                return {"status": "ok", "message": "No message in update"}
            
            message = update_data['message']
            chat_id = message.get('chat', {}).get('id')
            text = message.get('text', '')
            
            if not chat_id:
                return {"status": "error", "message": "No chat_id"}
            
            # دریافت جلسه کاربر
            from_user = message.get('from', {})
            user_id = from_user.get('id')
            username = from_user.get('username', '')
            first_name = from_user.get('first_name', '')
            
            user_session = self.bot.get_user_session(user_id, username, first_name)
            
            # پردازش پیام
            await self.bot.process_message(chat_id, text, user_session)
            
            return {"status": "ok", "message": "Message processed"}
            
        except Exception as e:
            logger.error(f"❌ Webhook processing error: {e}")
            return {"status": "error", "message": str(e)}
    
    async def send_notification(self, chat_id: int, message: str) -> bool:
        """ارسال اطلاعیه"""
        try:
            return await self.bot.send_message(chat_id, message)
        except Exception as e:
            logger.error(f"❌ Notification error: {e}")
            return False

async def main():
    """تابع اصلی"""
    print("🤖 Setting up Telegram Webhook Bot...")
    
    # Bot Token
    BOT_TOKEN = "8474552244:AAERRNE4n7_aFIeqxRlwEmutYn9jUvd9yUQ"
    
    # ایجاد ربات
    webhook_bot = WebhookTelegramBot(BOT_TOKEN)
    
    # تنظیم Webhook
    success = await webhook_bot.setup_webhook()
    
    if success:
        print("✅ Webhook configured successfully!")
        print("📱 Bot is ready to receive messages")
        print("🔗 Webhook URL: https://ahmadakd.github.io/Onix-V2Ray-Collector/webhook")
        
        # ارسال پیام تست به ادمین
        admin_id = 6563143907
        test_message = """
🤖 **ربات تلگرام فعال شد!**

✅ Webhook تنظیم شد
📱 آماده دریافت پیام‌ها
👑 ادمین: @Deltamax (6563143907)

**دستورات موجود:**
/start - شروع کار
/help - راهنما
/stats - آمار سیستم
/admin - دستورات ادمین
        """
        
        await webhook_bot.send_notification(admin_id, test_message)
        
    else:
        print("❌ Failed to configure webhook")
        return False
    
    return True

if __name__ == "__main__":
    asyncio.run(main())
