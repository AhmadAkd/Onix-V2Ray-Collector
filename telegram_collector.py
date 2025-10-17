#!/usr/bin/env python3
"""
Telegram Config Collector
جمع‌آوری کانفیگ‌ها از کانال‌ها و گروه‌های تلگرام
"""

import asyncio
import aiohttp
import re
import logging
from typing import List, Dict, Optional
from dataclasses import dataclass
import json
import time

logger = logging.getLogger(__name__)


@dataclass
class TelegramSource:
    """منبع تلگرام برای جمع‌آوری کانفیگ"""
    channel_id: str
    channel_name: str
    last_message_id: int = 0
    config_patterns: List[str] = None

    def __post_init__(self):
        if self.config_patterns is None:
            self.config_patterns = [
                r'vmess://[A-Za-z0-9+/=]+',
                r'vless://[^\\s]+',
                r'trojan://[^\\s]+',
                r'ss://[A-Za-z0-9+/=]+',
                r'ssr://[A-Za-z0-9+/=]+',
                r'hysteria://[^\\s]+',
                r'hy2://[^\\s]+',
                r'tuic://[^\\s]+'
            ]


class TelegramCollector:
    """جمع‌آورنده کانفیگ‌ها از تلگرام"""

    def __init__(self, bot_token: Optional[str] = None):
        """
        Initialize Telegram Collector

        Args:
            bot_token: Telegram Bot Token (از env یا parameter)
        """
        import os
        self.bot_token = bot_token or os.getenv('TELEGRAM_BOT_TOKEN')

        if not self.bot_token:
            logger.warning(
                "⚠️ Telegram Bot Token not provided - using static sources only")
            logger.info(
                "💡 To enable real-time collection, set TELEGRAM_BOT_TOKEN environment variable")
            self.api_url = None
        else:
            self.api_url = f"https://api.telegram.org/bot{self.bot_token}"
            logger.info("✅ Telegram Collector initialized with Bot Token")
            logger.info(f"🔗 API URL: {self.api_url}")

        self.sources = []
        self.collected_configs = []

    def add_source(self, source: TelegramSource):
        """اضافه کردن منبع تلگرام"""
        self.sources.append(source)
        logger.info(f"منبع تلگرام اضافه شد: {source.channel_name}")

    async def get_channel_messages(self, channel_id: str, limit: int = 100) -> List[Dict]:
        """دریافت پیام‌های کانال"""
        try:
            url = f"{self.api_url}/getUpdates"
            params = {
                'offset': -limit,
                'limit': limit,
                'timeout': 30
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('result', [])

        except Exception as e:
            logger.error(f"خطا در دریافت پیام‌های تلگرام: {e}")

        return []

    async def get_channel_history(self, channel_id: str, limit: int = 100) -> List[Dict]:
        """دریافت تاریخچه کانال (نیاز به Bot API v6.0+)"""
        try:
            # استفاده از Bot API برای دریافت پیام‌های کانال
            url = f"{self.api_url}/getUpdates"
            params = {
                'chat_id': channel_id,
                'limit': limit
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        messages = data.get('result', [])

                        # فیلتر کردن پیام‌های کانال
                        channel_messages = []
                        for update in messages:
                            if 'channel_post' in update:
                                channel_messages.append(update['channel_post'])

                        return channel_messages

        except Exception as e:
            logger.error(f"خطا در دریافت تاریخچه کانال: {e}")

        return []

    def extract_configs_from_text(self, text: str, patterns: List[str]) -> List[str]:
        """استخراج کانفیگ‌ها از متن"""
        configs = []

        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            configs.extend(matches)

        return configs

    async def collect_from_source(self, source: TelegramSource) -> List[str]:
        """جمع‌آوری کانفیگ‌ها از یک منبع"""
        configs = []

        try:
            # دریافت پیام‌های کانال
            messages = await self.get_channel_messages(source.channel_id, 50)

            for message in messages:
                if 'message' in message:
                    msg = message['message']
                    text = msg.get('text', '')

                    # استخراج کانفیگ‌ها
                    found_configs = self.extract_configs_from_text(
                        text, source.config_patterns)
                    configs.extend(found_configs)

                    # بررسی caption در media
                    if 'caption' in msg:
                        caption_configs = self.extract_configs_from_text(
                            msg['caption'], source.config_patterns
                        )
                        configs.extend(caption_configs)

            logger.info(
                f"از {source.channel_name}: {len(configs)} کانفیگ جمع‌آوری شد")

        except Exception as e:
            logger.error(f"خطا در جمع‌آوری از {source.channel_name}: {e}")

        return configs

    async def collect_all_sources(self) -> List[str]:
        """جمع‌آوری از تمام منابع"""
        all_configs = []

        for source in self.sources:
            configs = await self.collect_from_source(source)
            all_configs.extend(configs)

            # تأخیر بین درخواست‌ها
            await asyncio.sleep(1)

        # حذف تکراری‌ها
        unique_configs = list(set(all_configs))
        logger.info(
            f"کل کانفیگ‌های جمع‌آوری شده از تلگرام: {len(unique_configs)}")

        return unique_configs

    async def monitor_channels(self, interval: int = 300):
        """نظارت مداوم بر کانال‌ها"""
        logger.info("شروع نظارت بر کانال‌های تلگرام...")

        while True:
            try:
                configs = await self.collect_all_sources()
                self.collected_configs = configs

                # ذخیره کانفیگ‌ها
                await self.save_configs(configs)

                logger.info(f"نظارت کامل شد. {len(configs)} کانفیگ جدید")

            except Exception as e:
                logger.error(f"خطا در نظارت: {e}")

            # انتظار برای دور بعدی
            await asyncio.sleep(interval)

    async def save_configs(self, configs: List[str]):
        """ذخیره کانفیگ‌ها در فایل"""
        try:
            timestamp = int(time.time())
            filename = f"telegram_configs_{timestamp}.txt"

            with open(filename, 'w', encoding='utf-8') as f:
                for config in configs:
                    f.write(f"{config}\\n")

            logger.info(f"کانفیگ‌ها در {filename} ذخیره شدند")

        except Exception as e:
            logger.error(f"خطا در ذخیره کانفیگ‌ها: {e}")


# تنظیمات منابع تلگرام - کانال‌های معروف V2Ray
TELEGRAM_SOURCES = [
    # کانال‌های اصلی V2Ray
    TelegramSource(
        channel_id="@v2rayngvpn",
        channel_name="V2RayNG VPN",
    ),
    TelegramSource(
        channel_id="@freev2ray",
        channel_name="Free V2Ray",
    ),
    TelegramSource(
        channel_id="@vpnconfigs",
        channel_name="VPN Configs",
    ),
    TelegramSource(
        channel_id="@proxynetwork",
        channel_name="Proxy Network",
    ),
    TelegramSource(
        channel_id="@v2raycollect",
        channel_name="V2Ray Collector",
    ),
    # کانال‌های تخصصی VLess
    TelegramSource(
        channel_id="@vlessvpn",
        channel_name="VLess VPN",
    ),
    TelegramSource(
        channel_id="@vlessconfigs",
        channel_name="VLess Configs",
    ),
    TelegramSource(
        channel_id="@vlessfree",
        channel_name="VLess Free",
    ),
    # کانال‌های تخصصی VMess
    TelegramSource(
        channel_id="@vmessvpn",
        channel_name="VMess VPN",
    ),
    TelegramSource(
        channel_id="@vmessconfigs",
        channel_name="VMess Configs",
    ),
    TelegramSource(
        channel_id="@vmessfree",
        channel_name="VMess Free",
    ),
    # کانال‌های تخصصی Shadowsocks
    TelegramSource(
        channel_id="@ssvpn",
        channel_name="Shadowsocks VPN",
    ),
    TelegramSource(
        channel_id="@ssconfigs",
        channel_name="Shadowsocks Configs",
    ),
    TelegramSource(
        channel_id="@ssfree",
        channel_name="Shadowsocks Free",
    ),
    # کانال‌های تخصصی Trojan
    TelegramSource(
        channel_id="@trojanvpn",
        channel_name="Trojan VPN",
    ),
    TelegramSource(
        channel_id="@trojanconfigs",
        channel_name="Trojan Configs",
    ),
    TelegramSource(
        channel_id="@trojanfree",
        channel_name="Trojan Free",
    ),
    # کانال‌های تخصصی Hysteria
    TelegramSource(
        channel_id="@hysteriavpn",
        channel_name="Hysteria VPN",
    ),
    TelegramSource(
        channel_id="@hysteriaconfigs",
        channel_name="Hysteria Configs",
    ),
    TelegramSource(
        channel_id="@hysteriafree",
        channel_name="Hysteria Free",
    ),
    # کانال‌های ایرانی
    TelegramSource(
        channel_id="@iranvpn",
        channel_name="Iran VPN",
    ),
    TelegramSource(
        channel_id="@iranconfigs",
        channel_name="Iran Configs",
    ),
    TelegramSource(
        channel_id="@iranfree",
        channel_name="Iran Free",
    ),
    # کانال‌های بین‌المللی
    TelegramSource(
        channel_id="@globalvpn",
        channel_name="Global VPN",
    ),
    TelegramSource(
        channel_id="@globalconfigs",
        channel_name="Global Configs",
    ),
    TelegramSource(
        channel_id="@globalfree",
        channel_name="Global Free",
    ),
    # کانال‌های پرمخاطب
    TelegramSource(
        channel_id="@vpnclub",
        channel_name="VPN Club",
    ),
    TelegramSource(
        channel_id="@vpnworld",
        channel_name="VPN World",
    ),
    TelegramSource(
        channel_id="@vpnking",
        channel_name="VPN King",
    ),
    TelegramSource(
        channel_id="@vpnmaster",
        channel_name="VPN Master",
    ),
    TelegramSource(
        channel_id="@vpnpro",
        channel_name="VPN Pro",
    ),
    # کانال‌های تخصصی پروتکل‌های جدید
    TelegramSource(
        channel_id="@tuicvpn",
        channel_name="TUIC VPN",
    ),
    TelegramSource(
        channel_id="@hy2vpn",
        channel_name="Hysteria2 VPN",
    ),
    TelegramSource(
        channel_id="@realityvpn",
        channel_name="Reality VPN",
    ),
    TelegramSource(
        channel_id="@singboxvpn",
        channel_name="SingBox VPN",
    ),
    TelegramSource(
        channel_id="@xrayvpn",
        channel_name="Xray VPN",
    ),
]

# مثال استفاده


async def main():
    # تنظیم Bot Token (باید از BotFather دریافت شود)
    BOT_TOKEN = "6942899950:AAEDV4iX8jh2zD8be2dPqcADnB7V4xWy7aE"

    collector = TelegramCollector(BOT_TOKEN)

    # اضافه کردن منابع
    for source in TELEGRAM_SOURCES:
        collector.add_source(source)

    # جمع‌آوری یکباره
    configs = await collector.collect_all_sources()
    print(f"جمع‌آوری شد: {len(configs)} کانفیگ")

    # شروع نظارت مداوم
    # await collector.monitor_channels(interval=600)  # هر 10 دقیقه

if __name__ == "__main__":
    asyncio.run(main())
