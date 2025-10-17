#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Get Telegram User ID
دریافت Telegram User ID برای پیکربندی ادمین
"""

import asyncio
import aiohttp
import logging
from datetime import datetime

# تنظیم logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TelegramUserIDGetter:
    """دریافت User ID از Telegram"""

    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.api_url = f"https://api.telegram.org/bot{bot_token}"

    async def get_updates(self, offset: int = 0):
        """دریافت آخرین پیام‌ها"""
        try:
            url = f"{self.api_url}/getUpdates"
            params = {
                'offset': offset,
                'timeout': 30,
                'limit': 100
            }

            # ایجاد connector بدون SSL verification
            connector = aiohttp.TCPConnector(ssl=False)

            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('ok'):
                            return data.get('result', [])

            return []

        except Exception as e:
            logger.error(f"Error getting updates: {e}")
            return []

    async def send_message(self, chat_id: int, text: str) -> bool:
        """ارسال پیام"""
        try:
            url = f"{self.api_url}/sendMessage"
            data = {
                "chat_id": chat_id,
                "text": text
            }

            connector = aiohttp.TCPConnector(ssl=False)

            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.post(url, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get('ok', False)

            return False

        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False


async def main():
    """تابع اصلی"""
    print("🔍 Telegram User ID Getter")
    print("=" * 50)

    # Bot Token from environment
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8474552244:AAERRNE4n7_aFIeqxRlwEmutYn9jUvd9yUQ')

    # ایجاد کلاس
    user_getter = TelegramUserIDGetter(BOT_TOKEN)

    print("📱 مراحل:")
    print("1. به ربات @onixdev_bot در تلگرام پیام دهید")
    print("2. دستور /start یا هر پیامی ارسال کنید")
    print("3. اینجا Enter را فشار دهید")
    print("4. User ID شما نمایش داده خواهد شد")
    print()

    input("آماده‌اید؟ Enter را فشار دهید...")

    print("🔍 در حال دریافت پیام‌ها...")

    # دریافت آخرین پیام‌ها
    updates = await user_getter.get_updates()

    if not updates:
        print("❌ هیچ پیامی یافت نشد!")
        print("💡 لطفاً ابتدا به ربات پیام دهید و دوباره تلاش کنید.")
        return

    print(f"✅ {len(updates)} پیام دریافت شد")
    print()

    # نمایش اطلاعات کاربران
    users = {}

    for update in updates:
        if 'message' in update:
            message = update['message']
            from_user = message.get('from', {})

            user_id = from_user.get('id')
            username = from_user.get('username', 'بدون username')
            first_name = from_user.get('first_name', 'بدون نام')
            last_name = from_user.get('last_name', '')

            if user_id:
                users[user_id] = {
                    'username': username,
                    'first_name': first_name,
                    'last_name': last_name,
                    'message': message.get('text', 'بدون متن')
                }

    if not users:
        print("❌ هیچ کاربری یافت نشد!")
        return

    print("👥 کاربران یافت شده:")
    print("=" * 50)

    for i, (user_id, info) in enumerate(users.items(), 1):
        print(f"{i}. User ID: {user_id}")
        print(f"   نام: {info['first_name']} {info['last_name']}")
        print(f"   Username: @{info['username']}")
        print(f"   آخرین پیام: {info['message'][:50]}...")
        print()

    print("🔧 برای تنظیم ادمین:")
    print("=" * 50)

    for user_id in users.keys():
        print(f"# در فایل telegram_bot_enhanced.py:")
        print(f"self.admin_users.add({user_id})")
        print()

    # ارسال پیام تایید
    print("📨 ارسال پیام تایید به کاربران...")

    for user_id in users.keys():
        confirm_message = f"""
✅ User ID شما: {user_id}

🔧 برای تنظیم ادمین، این کد را در فایل telegram_bot_enhanced.py قرار دهید:

self.admin_users.add({user_id})

🎉 حالا می‌توانید از دستورات ادمین استفاده کنید:
/admin stats - آمار تفصیلی
/admin users - لیست کاربران
/admin broadcast - ارسال پیام به همه
        """

        sent = await user_getter.send_message(user_id, confirm_message)
        if sent:
            print(f"✅ پیام تایید به User ID {user_id} ارسال شد")
        else:
            print(f"❌ خطا در ارسال پیام به User ID {user_id}")

        await asyncio.sleep(1)  # تأخیر بین ارسال‌ها

    print()
    print("🎉 تمام شد!")
    print("💡 حالا می‌توانید User ID را در فایل telegram_bot_enhanced.py قرار دهید.")

if __name__ == "__main__":
    asyncio.run(main())
