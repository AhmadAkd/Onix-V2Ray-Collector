#!/usr/bin/env python3
"""
Telegram MTProto Collector
جمع‌آوری کانفیگ‌ها از کانال‌های تلگرام با استفاده از MTProto API
"""

import asyncio
import logging
import re
import os
from typing import List, Dict, Optional
from dataclasses import dataclass

# تنظیم logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TelegramChannel:
    """کانال تلگرام"""
    username: str
    name: str
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

class TelegramMTProtoCollector:
    """جمع‌آورنده کانفیگ‌ها با MTProto API"""
    
    def __init__(self):
        self.collected_configs = []
        self.channels = []
        
    def add_channel(self, channel: TelegramChannel):
        """اضافه کردن کانال"""
        self.channels.append(channel)
        logger.info(f"کانال اضافه شد: {channel.name}")
    
    def extract_configs_from_text(self, text: str, patterns: List[str]) -> List[str]:
        """استخراج کانفیگ‌ها از متن"""
        configs = []
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            configs.extend(matches)
        
        return configs
    
    async def collect_from_web_scraping(self) -> List[str]:
        """جمع‌آوری از طریق web scraping (جایگزین MTProto)"""
        try:
            import aiohttp
            
            all_configs = []
            
            # لیست کانال‌های معروف V2Ray
            channels = [
                "@v2rayngvpn",
                "@freev2ray", 
                "@vpnconfigs",
                "@proxynetwork",
                "@v2raycollect",
                "@vlessvpn",
                "@vmessvpn",
                "@ssvpn",
                "@trojanvpn",
                "@hysteriavpn"
            ]
            
            logger.info(f"🔍 شروع جمع‌آوری از {len(channels)} کانال...")
            
            # استفاده از t.me برای دسترسی به کانال‌ها
            for channel in channels:
                try:
                    configs = await self._scrape_channel_web(channel)
                    all_configs.extend(configs)
                    logger.info(f"✅ {channel}: {len(configs)} کانفیگ")
                except Exception as e:
                    logger.warning(f"❌ {channel}: {e}")
                
                # تأخیر بین درخواست‌ها
                await asyncio.sleep(1)
            
            # حذف تکراری‌ها
            unique_configs = list(set(all_configs))
            logger.info(f"📊 کل کانفیگ‌های منحصر به فرد: {len(unique_configs)}")
            
            return unique_configs
            
        except Exception as e:
            logger.error(f"خطا در جمع‌آوری: {e}")
            return []
    
    async def _scrape_channel_web(self, channel: str) -> List[str]:
        """Web scraping از کانال تلگرام"""
        try:
            import aiohttp
            
            # URL کانال در t.me
            url = f"https://t.me/s/{channel[1:]}"  # حذف @
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        html = await response.text()
                        
                        # استخراج کانفیگ‌ها از HTML
                        configs = self._extract_configs_from_html(html)
                        return configs
                    else:
                        logger.warning(f"HTTP {response.status} for {channel}")
                        return []
                        
        except Exception as e:
            logger.debug(f"خطا در scraping {channel}: {e}")
            return []
    
    def _extract_configs_from_html(self, html: str) -> List[str]:
        """استخراج کانفیگ‌ها از HTML"""
        configs = []
        
        # الگوهای کانفیگ
        patterns = [
            r'vmess://[A-Za-z0-9+/=]+',
            r'vless://[^\\s]+',
            r'trojan://[^\\s]+',
            r'ss://[A-Za-z0-9+/=]+',
            r'ssr://[A-Za-z0-9+/=]+',
            r'hysteria://[^\\s]+',
            r'hy2://[^\\s]+',
            r'tuic://[^\\s]+'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            configs.extend(matches)
        
        return configs
    
    async def collect_all_sources(self) -> List[str]:
        """جمع‌آوری از تمام منابع"""
        try:
            logger.info("🚀 شروع جمع‌آوری از کانال‌های تلگرام...")
            
            # جمع‌آوری از web scraping
            configs = await self.collect_from_web_scraping()
            
            self.collected_configs = configs
            logger.info(f"✅ {len(configs)} کانفیگ از تلگرام جمع‌آوری شد")
            
            return configs
            
        except Exception as e:
            logger.error(f"خطا در جمع‌آوری: {e}")
            return []

# کانال‌های معروف V2Ray
TELEGRAM_CHANNELS = [
    TelegramChannel("@v2rayngvpn", "V2RayNG VPN"),
    TelegramChannel("@freev2ray", "Free V2Ray"),
    TelegramChannel("@vpnconfigs", "VPN Configs"),
    TelegramChannel("@proxynetwork", "Proxy Network"),
    TelegramChannel("@v2raycollect", "V2Ray Collector"),
    TelegramChannel("@vlessvpn", "VLess VPN"),
    TelegramChannel("@vmessvpn", "VMess VPN"),
    TelegramChannel("@ssvpn", "Shadowsocks VPN"),
    TelegramChannel("@trojanvpn", "Trojan VPN"),
    TelegramChannel("@hysteriavpn", "Hysteria VPN"),
]

async def main():
    """تابع اصلی"""
    print("🤖 Starting Telegram MTProto Config Collector...")
    
    # ایجاد جمع‌آورنده
    collector = TelegramMTProtoCollector()
    
    # اضافه کردن کانال‌ها
    for channel in TELEGRAM_CHANNELS:
        collector.add_channel(channel)
    
    # جمع‌آوری کانفیگ‌ها
    configs = await collector.collect_all_sources()
    
    if configs:
        print(f"✅ Collected {len(configs)} configs from Telegram")
        
        # ذخیره در فایل
        with open("telegram_configs.txt", "w", encoding="utf-8") as f:
            for config in configs:
                f.write(f"{config}\\n")
        
        print("📁 Configs saved to telegram_configs.txt")
    else:
        print("❌ No configs found")

if __name__ == "__main__":
    asyncio.run(main())
