#!/usr/bin/env python3
"""
Telegram Collector Only - بدون Polling
جمع‌آوری کانفیگ‌ها از تلگرام بدون ربات
"""

import asyncio
import logging
import os
from datetime import datetime
from telegram_collector import TelegramCollector

# تنظیم logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TelegramCollectorOnly:
    """جمع‌آورنده کانفیگ‌ها از تلگرام (بدون ربات)"""

    def __init__(self, bot_token: str):
        self.telegram_collector = TelegramCollector(bot_token)
        self.is_running = False

        # اضافه کردن منابع تلگرام
        from telegram_collector import TELEGRAM_SOURCES
        for source in TELEGRAM_SOURCES:
            self.telegram_collector.add_source(source)

    async def collect_configs_periodically(self, interval_minutes: int = 30):
        """جمع‌آوری دوره‌ای کانفیگ‌ها"""
        self.is_running = True
        logger.info("🚀 Starting Telegram Config Collector...")

        while self.is_running:
            try:
                logger.info("📱 Starting config collection...")

                # جمع‌آوری از تلگرام
                configs = await self.telegram_collector.collect_all_sources()
                logger.info(
                    f"✅ Collected {len(configs)} configs from Telegram")

                if len(configs) > 0:
                    logger.info(f"📊 Config collection completed successfully!")
                    logger.info(f"📁 Configs saved to subscription files")
                else:
                    logger.info("ℹ️ No new configs found")

            except Exception as e:
                logger.error(f"❌ Collection error: {e}")

            # انتظار برای دور بعد
            logger.info(
                f"⏰ Waiting {interval_minutes} minutes for next collection...")
            await asyncio.sleep(interval_minutes * 60)

    async def run_once(self):
        """اجرای یکباره جمع‌آوری"""
        try:
            logger.info("🚀 Starting one-time config collection...")

            # جمع‌آوری از تلگرام
            configs = await self.telegram_collector.collect_all_sources()
            logger.info(f"✅ Collected {len(configs)} configs from Telegram")

            if len(configs) > 0:
                logger.info(f"📊 Collection completed successfully!")
                logger.info(f"📁 Configs saved to subscription files")
            else:
                logger.info("ℹ️ No configs found")

        except Exception as e:
            logger.error(f"❌ Collection error: {e}")

    async def run(self, mode: str = "once"):
        """اجرای جمع‌آورنده"""
        try:
            if mode == "once":
                await self.run_once()
            else:
                await self.collect_configs_periodically(30)
        except KeyboardInterrupt:
            logger.info("⏹️ Collector stopped by user")
        except Exception as e:
            logger.error(f"❌ Collector error: {e}")
        finally:
            self.is_running = False


async def main():
    """تابع اصلی"""
    print("🤖 Starting V2Ray Telegram Config Collector...")

    # Bot Token from environment
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN',
                          '8474552244:AAERRNE4n7_aFIeqxRlwEmutYn9jUvd9yUQ')

    # تنظیم Bot Token برای TelegramCollector
    os.environ['TELEGRAM_BOT_TOKEN'] = BOT_TOKEN

    # ایجاد جمع‌آورنده
    collector = TelegramCollectorOnly(BOT_TOKEN)

    print("📱 Config collector is now running...")
    print("🔄 Running one-time collection...")
    print("⏹️ Press Ctrl+C to stop")

    # اجرای جمع‌آورنده
    await collector.run("once")

if __name__ == "__main__":
    asyncio.run(main())
