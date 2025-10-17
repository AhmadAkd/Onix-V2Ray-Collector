#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Polling Bot for V2Ray Collector
ربات تلگرام با Polling برای جمع‌آوری کانفیگ‌ها
"""

import asyncio
import logging
import os
from datetime import datetime
from telegram_bot_enhanced import EnhancedTelegramBot
from telegram_collector import TelegramCollector

# تنظیم logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PollingTelegramBot:
    """ربات تلگرام با Polling و جمع‌آوری کانفیگ"""
    
    def __init__(self, bot_token: str):
        self.bot = EnhancedTelegramBot(bot_token)
        self.telegram_collector = TelegramCollector(bot_token)
        self.is_running = False
        
    async def start_polling(self):
        """شروع Polling"""
        self.is_running = True
        logger.info("🚀 Starting Telegram Bot with Polling...")
        
        # حذف webhook قبلی
        await self.bot.delete_webhook()
        logger.info("✅ Webhook deleted")
        
        # شروع polling
        await self.bot.start_polling(interval=2)
    
    async def collect_configs_periodically(self, interval_minutes: int = 30):
        """جمع‌آوری دوره‌ای کانفیگ‌ها"""
        while self.is_running:
            try:
                logger.info("📱 Starting periodic config collection...")
                
                # جمع‌آوری از تلگرام
                configs = await self.telegram_collector.collect_all_sources()
                logger.info(f"✅ Collected {len(configs)} configs from Telegram")
                
                # فقط اگر کانفیگ جدیدی یافت شد، اطلاعیه ارسال کن
                if len(configs) > 0:
                    admin_id = 6563143907
                    message = f"""
📊 **گزارش جمع‌آوری دوره‌ای**

✅ کانفیگ‌های جمع‌آوری شده: {len(configs)}
🕐 زمان: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📱 منبع: تلگرام

**آمار کلی:**
• کل کانفیگ‌ها: {len(configs)}
• منابع فعال: {len(self.telegram_collector.sources)}
• آخرین بروزرسانی: {datetime.now().strftime('%H:%M')}
                    """
                    
                    await self.bot.send_message(admin_id, message)
                else:
                    logger.info("ℹ️ No new configs found, skipping notification")
                
            except Exception as e:
                logger.error(f"❌ Collection error: {e}")
                
            # انتظار برای دور بعد
            logger.info(f"⏰ Waiting {interval_minutes} minutes for next collection...")
            await asyncio.sleep(interval_minutes * 60)
    
    async def run(self):
        """اجرای ربات"""
        try:
            # شروع همزمان polling و جمع‌آوری
            await asyncio.gather(
                self.start_polling(),
                self.collect_configs_periodically(30)  # هر 30 دقیقه
            )
        except KeyboardInterrupt:
            logger.info("⏹️ Bot stopped by user")
        except Exception as e:
            logger.error(f"❌ Bot error: {e}")
        finally:
            self.is_running = False

async def main():
    """تابع اصلی"""
    print("🤖 Starting V2Ray Collector Telegram Bot with Polling...")
    
    # Bot Token from environment
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8474552244:AAERRNE4n7_aFIeqxRlwEmutYn9jUvd9yUQ')
    
    # ایجاد ربات
    bot = PollingTelegramBot(BOT_TOKEN)
    
    # دریافت اطلاعات ربات
    bot_info = await bot.bot.get_bot_info()
    if bot_info:
        print(f"✅ Bot: {bot_info.get('first_name')} (@{bot_info.get('username')})")
        print(f"👑 Admin: 6563143907 (@Deltamax)")
        print("📱 Bot is now running with polling...")
        print("🔄 Config collection every 30 minutes")
        print("⏹️ Press Ctrl+C to stop")
    
    # اجرای ربات
    await bot.run()

if __name__ == "__main__":
    asyncio.run(main())
