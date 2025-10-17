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
        """دریافت پیام‌های کانال از طریق web scraping"""
        try:
            # استفاده از web scraping به جای Bot API
            return await self._scrape_channel_web(channel_id, limit)

        except Exception as e:
            logger.error(f"خطا در دریافت پیام‌های تلگرام: {e}")

        return []
    
    async def _scrape_channel_web(self, channel_id: str, limit: int = 100) -> List[Dict]:
        """Web scraping از کانال تلگرام"""
        try:
            # حذف @ از channel_id
            channel_username = channel_id[1:] if channel_id.startswith('@') else channel_id
            
            # URL کانال در t.me
            url = f"https://t.me/s/{channel_username}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        html = await response.text()
                        
                        # استخراج کانفیگ‌ها از HTML
                        configs = self._extract_configs_from_html(html)
                        
                        # تبدیل به فرمت پیام
                        messages = []
                        for i, config in enumerate(configs[:limit]):
                            messages.append({
                                'message_id': i + 1,
                                'text': config,
                                'date': int(time.time())
                            })
                        
                        return messages
                    else:
                        logger.warning(f"HTTP {response.status} for {channel_id}")
                        return []
                        
        except Exception as e:
            logger.debug(f"خطا در scraping {channel_id}: {e}")
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
        """ذخیره کانفیگ‌ها در فایل‌های اصلی (فقط سالم‌ها)"""
        try:
            if not configs:
                logger.info("هیچ کانفیگی برای ذخیره وجود ندارد")
                return
            
            # تست کانفیگ‌ها قبل از ذخیره
            logger.info(f"🧪 شروع تست {len(configs)} کانفیگ از تلگرام...")
            working_configs = await self._test_configs(configs)
            
            if not working_configs:
                logger.warning("❌ هیچ کانفیگ سالمی از تلگرام یافت نشد")
                return
                
            logger.info(f"✅ {len(working_configs)} کانفیگ سالم از {len(configs)} کانفیگ تست شده")
            
            # ذخیره در فایل اصلی all_subscription.txt
            await self._append_to_file("subscriptions/all_subscription.txt", working_configs)
            
            # ذخیره در فایل‌های پروتکل
            await self._categorize_and_save_configs(working_configs)
            
            # ذخیره در فایل‌های کشور
            await self._save_by_country(working_configs)
            
            # ذخیره گزارش
            await self._save_telegram_report(working_configs, len(configs))
            
            logger.info(f"✅ {len(working_configs)} کانفیگ سالم از تلگرام ذخیره شد")

        except Exception as e:
            logger.error(f"خطا در ذخیره کانفیگ‌ها: {e}")
    
    async def _test_configs(self, configs: List[str]) -> List[str]:
        """تست کانفیگ‌ها و برگرداندن سالم‌ها"""
        try:
            # Import V2RayCollector برای تست
            from config_collector import V2RayCollector
            
            # ایجاد instance از V2RayCollector
            collector = V2RayCollector()
            
            # تست کانفیگ‌ها
            logger.info("🔍 شروع تست کانفیگ‌های تلگرام...")
            await collector.test_all_configs_ultra_fast(configs, max_concurrent=20)
            
            # دریافت کانفیگ‌های سالم
            working_configs = []
            for config in collector.working_configs:
                if config.is_working:
                    working_configs.append(config.raw_config)
            
            logger.info(f"🧪 تست کامل: {len(working_configs)} کانفیگ سالم از {len(configs)} کانفیگ")
            
            return working_configs
            
        except Exception as e:
            logger.error(f"خطا در تست کانفیگ‌ها: {e}")
            # در صورت خطا، کانفیگ‌ها را بدون تست ذخیره کن
            return configs
    
    async def _append_to_file(self, filename: str, configs: List[str]):
        """اضافه کردن کانفیگ‌ها به فایل"""
        try:
            import os
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            with open(filename, 'a', encoding='utf-8') as f:
                for config in configs:
                    f.write(f"{config}\\n")

        except Exception as e:
            logger.error(f"خطا در اضافه کردن به {filename}: {e}")
    
    async def _categorize_and_save_configs(self, configs: List[str]):
        """دسته‌بندی و ذخیره کانفیگ‌ها بر اساس پروتکل"""
        try:
            protocols = {
                'vmess': [],
                'vless': [],
                'trojan': [],
                'ss': [],
                'ssr': [],
                'hysteria': [],
                'hy2': [],
                'tuic': []
            }
            
            for config in configs:
                config_lower = config.lower()
                if 'vmess://' in config_lower:
                    protocols['vmess'].append(config)
                elif 'vless://' in config_lower:
                    protocols['vless'].append(config)
                elif 'trojan://' in config_lower:
                    protocols['trojan'].append(config)
                elif 'ss://' in config_lower and 'ssr://' not in config_lower:
                    protocols['ss'].append(config)
                elif 'ssr://' in config_lower:
                    protocols['ssr'].append(config)
                elif 'hysteria://' in config_lower:
                    protocols['hysteria'].append(config)
                elif 'hy2://' in config_lower:
                    protocols['hy2'].append(config)
                elif 'tuic://' in config_lower:
                    protocols['tuic'].append(config)
            
            # ذخیره در فایل‌های پروتکل
            for protocol, protocol_configs in protocols.items():
                if protocol_configs:
                    filename = f"subscriptions/by_protocol/{protocol}.txt"
                    await self._append_to_file(filename, protocol_configs)
                    logger.info(f"📁 {len(protocol_configs)} کانفیگ {protocol} ذخیره شد")
                    
        except Exception as e:
            logger.error(f"خطا در دسته‌بندی کانفیگ‌ها: {e}")
    
    async def _save_by_country(self, configs: List[str]):
        """ذخیره کانفیگ‌ها بر اساس کشور"""
        try:
            # دسته‌بندی بر اساس کشور
            country_configs = await self._categorize_by_country(configs)
            
            # ذخیره در فایل‌های کشور
            for country, country_configs_list in country_configs.items():
                if country_configs_list:
                    filename = f"subscriptions/by_country/{country}.txt"
                    await self._append_to_file(filename, country_configs_list)
                    logger.info(f"🌍 {len(country_configs_list)} کانفیگ {country} ذخیره شد")
            
            # ذخیره در فایل عمومی تلگرام
            filename = "subscriptions/telegram_collected.txt"
            await self._append_to_file(filename, configs)
            
        except Exception as e:
            logger.error(f"خطا در ذخیره بر اساس کشور: {e}")
    
    async def _categorize_by_country(self, configs: List[str]) -> Dict[str, List[str]]:
        """دسته‌بندی کانفیگ‌ها بر اساس کشور"""
        try:
            country_configs = {}
            
            for config in configs:
                country = await self._detect_country_from_config(config)
                
                if country not in country_configs:
                    country_configs[country] = []
                
                country_configs[country].append(config)
            
            return country_configs
            
        except Exception as e:
            logger.error(f"خطا در دسته‌بندی بر اساس کشور: {e}")
            return {"UNKNOWN": configs}
    
    async def _detect_country_from_config(self, config: str) -> str:
        """تشخیص کشور از کانفیگ"""
        try:
            # استخراج آدرس سرور از کانفیگ
            server_address = self._extract_server_address(config)
            
            if not server_address:
                return "UNKNOWN"
            
            # تشخیص کشور بر اساس آدرس IP یا دامنه
            country = await self._get_country_from_address(server_address)
            
            return country
            
        except Exception as e:
            logger.debug(f"خطا در تشخیص کشور: {e}")
            return "UNKNOWN"
    
    def _extract_server_address(self, config: str) -> str:
        """استخراج آدرس سرور از کانفیگ"""
        try:
            config_lower = config.lower()
            
            if 'vmess://' in config_lower:
                return self._extract_vmess_address(config)
            elif 'vless://' in config_lower:
                return self._extract_vless_address(config)
            elif 'trojan://' in config_lower:
                return self._extract_trojan_address(config)
            elif 'ss://' in config_lower:
                return self._extract_ss_address(config)
            elif 'ssr://' in config_lower:
                return self._extract_ssr_address(config)
            elif 'hysteria://' in config_lower or 'hy2://' in config_lower:
                return self._extract_hysteria_address(config)
            elif 'tuic://' in config_lower:
                return self._extract_tuic_address(config)
            
            return ""
            
        except Exception as e:
            logger.debug(f"خطا در استخراج آدرس: {e}")
            return ""
    
    def _extract_vmess_address(self, config: str) -> str:
        """استخراج آدرس از VMess"""
        try:
            import base64
            import json
            
            # حذف پیشوند vmess://
            encoded_part = config[8:]
            
            # اضافه کردن padding
            missing_padding = len(encoded_part) % 4
            if missing_padding:
                encoded_part += '=' * (4 - missing_padding)
            
            # decode base64
            decoded = base64.b64decode(encoded_part).decode('utf-8')
            data = json.loads(decoded)
            
            return data.get('add', '')
            
        except Exception:
            return ""
    
    def _extract_vless_address(self, config: str) -> str:
        """استخراج آدرس از VLESS"""
        try:
            # فرمت: vless://uuid@server:port?params
            if '@' in config:
                server_part = config.split('@')[1]
                if ':' in server_part:
                    return server_part.split(':')[0]
            return ""
        except Exception:
            return ""
    
    def _extract_trojan_address(self, config: str) -> str:
        """استخراج آدرس از Trojan"""
        try:
            # فرمت: trojan://password@server:port?params
            if '@' in config:
                server_part = config.split('@')[1]
                if ':' in server_part:
                    return server_part.split(':')[0]
            return ""
        except Exception:
            return ""
    
    def _extract_ss_address(self, config: str) -> str:
        """استخراج آدرس از Shadowsocks"""
        try:
            import base64
            
            # فرمت: ss://method:password@server:port
            if '@' in config:
                server_part = config.split('@')[1]
                if ':' in server_part:
                    return server_part.split(':')[0]
            return ""
        except Exception:
            return ""
    
    def _extract_ssr_address(self, config: str) -> str:
        """استخراج آدرس از ShadowsocksR"""
        try:
            import base64
            
            # حذف پیشوند ssr://
            encoded_part = config[6:]
            
            # اضافه کردن padding
            missing_padding = len(encoded_part) % 4
            if missing_padding:
                encoded_part += '=' * (4 - missing_padding)
            
            # decode base64
            decoded = base64.b64decode(encoded_part).decode('utf-8')
            
            # فرمت: server:port:protocol:method:obfs:password
            parts = decoded.split(':')
            if len(parts) >= 1:
                return parts[0]
            
            return ""
        except Exception:
            return ""
    
    def _extract_hysteria_address(self, config: str) -> str:
        """استخراج آدرس از Hysteria"""
        try:
            # فرمت: hysteria://server:port?params
            if '://' in config:
                server_part = config.split('://')[1]
                if ':' in server_part:
                    return server_part.split(':')[0]
            return ""
        except Exception:
            return ""
    
    def _extract_tuic_address(self, config: str) -> str:
        """استخراج آدرس از TUIC"""
        try:
            # فرمت: tuic://uuid:password@server:port?params
            if '@' in config:
                server_part = config.split('@')[1]
                if ':' in server_part:
                    return server_part.split(':')[0]
            return ""
        except Exception:
            return ""
    
    async def _get_country_from_address(self, address: str) -> str:
        """تشخیص کشور از آدرس IP یا دامنه"""
        try:
            # لیست کشورهای رایج بر اساس دامنه
            domain_countries = {
                '.us': 'US', '.com': 'US', '.org': 'US', '.net': 'US',
                '.de': 'DE', '.uk': 'GB', '.fr': 'FR', '.ca': 'CA',
                '.nl': 'NL', '.jp': 'JP', '.kr': 'KR', '.sg': 'SG',
                '.hk': 'HK', '.tw': 'TW', '.au': 'AU', '.ch': 'CH',
                '.se': 'SE', '.no': 'NO', '.dk': 'DK', '.fi': 'FI',
                '.it': 'IT', '.es': 'ES', '.pl': 'PL', '.ru': 'RU',
                '.cn': 'CN', '.in': 'IN', '.br': 'BR', '.mx': 'MX',
                '.tr': 'TR', '.ir': 'IR', '.ae': 'AE', '.sa': 'SA'
            }
            
            # بررسی دامنه
            for domain, country in domain_countries.items():
                if domain in address.lower():
                    return country
            
            # اگر آدرس IP بود، از GeoIP استفاده کن
            if self._is_ip_address(address):
                return await self._get_country_from_ip(address)
            
            # پیش‌فرض
            return "UNKNOWN"
            
        except Exception as e:
            logger.debug(f"خطا در تشخیص کشور از آدرس: {e}")
            return "UNKNOWN"
    
    def _is_ip_address(self, address: str) -> bool:
        """بررسی اینکه آیا آدرس یک IP است"""
        try:
            import socket
            socket.inet_aton(address)
            return True
        except socket.error:
            return False
    
    async def _get_country_from_ip(self, ip: str) -> str:
        """تشخیص کشور از IP (ساده‌سازی شده)"""
        try:
            # برای سادگی، از یک سرویس عمومی استفاده می‌کنیم
            # در تولید واقعی، از یک کتابخانه GeoIP استفاده کنید
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://ip-api.com/json/{ip}") as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('countryCode', 'UNKNOWN')
            
            return "UNKNOWN"
            
        except Exception as e:
            logger.debug(f"خطا در تشخیص کشور از IP: {e}")
            return "UNKNOWN"
    
    async def _save_telegram_report(self, configs: List[str], total_tested: int = None):
        """ذخیره گزارش جمع‌آوری تلگرام"""
        try:
            import json
            from datetime import datetime
            
            # محاسبه آمار تست
            tested_count = total_tested or len(configs)
            success_rate = (len(configs) / tested_count * 100) if tested_count > 0 else 0
            
            report = {
                "source": "telegram",
                "timestamp": datetime.now().isoformat(),
                "testing_stats": {
                    "total_tested": tested_count,
                    "working_configs": len(configs),
                    "failed_configs": tested_count - len(configs),
                    "success_rate": round(success_rate, 2)
                },
                "protocols": {
                    "vmess": len([c for c in configs if 'vmess://' in c.lower()]),
                    "vless": len([c for c in configs if 'vless://' in c.lower()]),
                    "trojan": len([c for c in configs if 'trojan://' in c.lower()]),
                    "ss": len([c for c in configs if 'ss://' in c.lower() and 'ssr://' not in c.lower()]),
                    "ssr": len([c for c in configs if 'ssr://' in c.lower()]),
                    "hysteria": len([c for c in configs if 'hysteria://' in c.lower()]),
                    "hy2": len([c for c in configs if 'hy2://' in c.lower()]),
                    "tuic": len([c for c in configs if 'tuic://' in c.lower()])
                },
                "sources_count": len(self.sources),
                "status": "success" if len(configs) > 0 else "no_working_configs"
            }
            
            with open("subscriptions/telegram_report.json", 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"خطا در ذخیره گزارش تلگرام: {e}")


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
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')

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
