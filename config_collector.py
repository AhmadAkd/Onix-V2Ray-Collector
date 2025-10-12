#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V2Ray Config Collector & Tester
جمع‌آوری، تست و دسته‌بندی کانفیگ‌های رایگان V2Ray
"""

import asyncio
import aiohttp
import json
import base64
import re
import time
import logging
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from urllib.parse import urlparse
import yaml

# تنظیم لاگ
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('v2ray_collector.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class V2RayConfig:
    """کلاس برای ذخیره اطلاعات کانفیگ V2Ray"""
    protocol: str
    address: str
    port: int
    uuid: str
    alter_id: Optional[int] = None
    network: str = "tcp"
    tls: bool = False
    raw_config: str = ""
    latency: float = 0.0
    is_working: bool = False
    country: str = "unknown"
    speed_test_result: float = 0.0


class V2RayCollector:
    """کلاس اصلی برای جمع‌آوری و تست کانفیگ‌های V2Ray"""

    def __init__(self):
        self.configs: List[V2RayConfig] = []
        self.working_configs: List[V2RayConfig] = []
        self.failed_configs: List[V2RayConfig] = []

        # منابع کانفیگ‌های رایگان
        self.config_sources = [
            "https://github.com/Epodonios/v2ray-configs/raw/main/All_Configs_Sub.txt",
            "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt",
            "https://raw.githubusercontent.com/peasoft/NoMoreWalls/master/list.txt",
            "https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2"
        ]

        # الگوهای regex برای تشخیص پروتکل‌ها
        self.protocol_patterns = {
            'vmess': r'vmess://([A-Za-z0-9+/=]+)',
            'vless': r'vless://([^@]+)@([^:]+):(\d+)(\?[^#]*)?(#.*)?',
            'trojan': r'trojan://([^@]+)@([^:]+):(\d+)(\?[^#]*)?(#.*)?',
            'ss': r'ss://([A-Za-z0-9+/=]+)',
            'ssr': r'ssr://([A-Za-z0-9+/=]+)'
        }

    async def fetch_configs_from_source(self, source_url: str) -> List[str]:
        """دریافت کانفیگ‌ها از یک منبع"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(source_url, timeout=30) as response:
                    if response.status == 200:
                        content = await response.text()
                        # تجزیه کانفیگ‌ها از متن
                        configs = []
                        for line in content.strip().split('\n'):
                            if line.strip() and not line.startswith('#'):
                                configs.append(line.strip())
                        logger.info(
                            f"دریافت {len(configs)} کانفیگ از {source_url}")
                        return configs
        except Exception as e:
            logger.error(f"خطا در دریافت از {source_url}: {e}")
        return []

    async def collect_all_configs(self) -> List[str]:
        """جمع‌آوری کانفیگ‌ها از تمام منابع"""
        all_configs = []

        tasks = [self.fetch_configs_from_source(
            source) for source in self.config_sources]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, list):
                all_configs.extend(result)
            elif isinstance(result, Exception):
                logger.error(f"خطا در جمع‌آوری: {result}")

        # حذف کانفیگ‌های تکراری
        unique_configs = list(set(all_configs))
        logger.info(
            f"مجموع {len(unique_configs)} کانفیگ منحصر به فرد جمع‌آوری شد")

        return unique_configs

    def parse_vmess_config(self, config_str: str) -> Optional[V2RayConfig]:
        """تجزیه کانفیگ VMess"""
        try:
            # حذف پیشوند vmess://
            if config_str.startswith('vmess://'):
                encoded = config_str[8:]
            else:
                encoded = config_str

            # دیکد کردن base64
            decoded = base64.b64decode(encoded + '==').decode('utf-8')
            config_data = json.loads(decoded)

            return V2RayConfig(
                protocol="vmess",
                address=config_data.get('add', ''),
                port=int(config_data.get('port', 0)),
                uuid=config_data.get('id', ''),
                alter_id=config_data.get('aid', 0),
                network=config_data.get('net', 'tcp'),
                tls=config_data.get('tls') == 'tls',
                raw_config=config_str,
                country=config_data.get('ps', '').split(
                    '-')[-1] if '-' in config_data.get('ps', '') else 'unknown'
            )
        except Exception as e:
            logger.debug(f"خطا در تجزیه VMess: {e}")
            return None

    def parse_vless_config(self, config_str: str) -> Optional[V2RayConfig]:
        """تجزیه کانفیگ VLESS"""
        try:
            match = re.match(self.protocol_patterns['vless'], config_str)
            if match:
                uuid, address, port, params, fragment = match.groups()

                # تجزیه پارامترها
                tls = False
                if params and 'security=tls' in params:
                    tls = True

                return V2RayConfig(
                    protocol="vless",
                    address=address,
                    port=int(port),
                    uuid=uuid,
                    raw_config=config_str,
                    tls=tls,
                    country="unknown"
                )
        except Exception as e:
            logger.debug(f"خطا در تجزیه VLESS: {e}")
        return None

    def parse_trojan_config(self, config_str: str) -> Optional[V2RayConfig]:
        """تجزیه کانفیگ Trojan"""
        try:
            match = re.match(self.protocol_patterns['trojan'], config_str)
            if match:
                password, address, port, params, fragment = match.groups()

                return V2RayConfig(
                    protocol="trojan",
                    address=address,
                    port=int(port),
                    uuid=password,  # در Trojan از password به عنوان uuid استفاده می‌کنیم
                    raw_config=config_str,
                    tls=True,  # Trojan همیشه TLS دارد
                    country="unknown"
                )
        except Exception as e:
            logger.debug(f"خطا در تجزیه Trojan: {e}")
        return None

    def parse_ss_config(self, config_str: str) -> Optional[V2RayConfig]:
        """تجزیه کانفیگ Shadowsocks"""
        try:
            if config_str.startswith('ss://'):
                encoded = config_str[5:]
            else:
                encoded = config_str

            # تجزیه کانفیگ SS
            decoded = base64.b64decode(encoded + '==').decode('utf-8')
            if '@' in decoded:
                method_password, address_port = decoded.split('@')
                method, password = method_password.split(':')
                address, port = address_port.split(':')

                return V2RayConfig(
                    protocol="ss",
                    address=address,
                    port=int(port),
                    uuid=f"{method}:{password}",
                    raw_config=config_str,
                    country="unknown"
                )
        except Exception as e:
            logger.debug(f"خطا در تجزیه SS: {e}")
        return None

    async def test_config_connectivity(self, config: V2RayConfig) -> Tuple[bool, float]:
        """تست اتصال کانفیگ"""
        try:
            start_time = time.time()

            # تست ping به سرور
            async with aiohttp.ClientSession() as session:
                # تست HTTP connection
                test_url = f"http://{config.address}:{config.port}"
                try:
                    async with session.get(test_url, timeout=10) as response:
                        latency = (time.time() - start_time) * 1000
                        return True, latency
                except:
                    # تست HTTPS
                    test_url = f"https://{config.address}:{config.port}"
                    try:
                        async with session.get(test_url, timeout=10) as response:
                            latency = (time.time() - start_time) * 1000
                            return True, latency
                    except:
                        return False, 0.0

        except Exception as e:
            logger.debug(f"خطا در تست {config.address}:{config.port} - {e}")
            return False, 0.0

    def parse_config(self, config_str: str) -> Optional[V2RayConfig]:
        """تجزیه کانفیگ بر اساس نوع پروتکل"""
        config_str = config_str.strip()

        if config_str.startswith('vmess://'):
            return self.parse_vmess_config(config_str)
        elif config_str.startswith('vless://'):
            return self.parse_vless_config(config_str)
        elif config_str.startswith('trojan://'):
            return self.parse_trojan_config(config_str)
        elif config_str.startswith('ss://'):
            return self.parse_ss_config(config_str)

        return None

    async def test_all_configs(self, configs: List[str], max_concurrent: int = 50):
        """تست تمام کانفیگ‌ها"""
        logger.info(f"شروع تست {len(configs)} کانفیگ...")

        semaphore = asyncio.Semaphore(max_concurrent)

        async def test_single_config(config_str: str):
            async with semaphore:
                config = self.parse_config(config_str)
                if config:
                    is_working, latency = await self.test_config_connectivity(config)
                    config.is_working = is_working
                    config.latency = latency

                    if is_working:
                        self.working_configs.append(config)
                        logger.info(
                            f"✅ {config.protocol.upper()} {config.address}:{config.port} - {latency:.0f}ms")
                    else:
                        self.failed_configs.append(config)
                        logger.debug(
                            f"❌ {config.protocol.upper()} {config.address}:{config.port} - فیل شد")
                else:
                    logger.debug(
                        f"❌ خطا در تجزیه کانفیگ: {config_str[:50]}...")

        # اجرای موازی تست‌ها
        tasks = [test_single_config(config) for config in configs]
        await asyncio.gather(*tasks, return_exceptions=True)

        logger.info(
            f"تست کامل شد: {len(self.working_configs)} کانفیگ سالم، {len(self.failed_configs)} کانفیگ ناسالم")

    def categorize_configs(self):
        """دسته‌بندی کانفیگ‌ها"""
        categories = {
            'vmess': [],
            'vless': [],
            'trojan': [],
            'ss': [],
            'ssr': []
        }

        for config in self.working_configs:
            if config.protocol in categories:
                categories[config.protocol].append(config)

        return categories

    def generate_subscription_links(self, categories: Dict[str, List[V2RayConfig]]):
        """تولید لینک‌های اشتراک"""
        subscription_files = {}

        # تولید فایل برای هر پروتکل
        for protocol, configs in categories.items():
            if configs:
                # مرتب‌سازی بر اساس سرعت
                configs.sort(key=lambda x: x.latency)

                # تولید محتوای اشتراک
                subscription_content = '\n'.join(
                    [config.raw_config for config in configs])

                # ذخیره در فایل
                filename = f"subscriptions/{protocol}_subscription.txt"
                subscription_files[protocol] = {
                    'filename': filename,
                    'content': subscription_content,
                    'count': len(configs)
                }

                logger.info(f"تولید شد: {filename} با {len(configs)} کانفیگ")

        # تولید فایل ترکیبی
        all_configs = []
        for configs in categories.values():
            all_configs.extend(configs)

        if all_configs:
            all_configs.sort(key=lambda x: x.latency)
            all_content = '\n'.join(
                [config.raw_config for config in all_configs])

            subscription_files['all'] = {
                'filename': 'subscriptions/all_subscription.txt',
                'content': all_content,
                'count': len(all_configs)
            }

        return subscription_files

    async def run_collection_cycle(self):
        """اجرای یک سیکل کامل جمع‌آوری و تست"""
        logger.info("🚀 شروع سیکل جمع‌آوری کانفیگ‌ها...")

        # جمع‌آوری کانفیگ‌ها
        raw_configs = await self.collect_all_configs()

        # تست کانفیگ‌ها
        await self.test_all_configs(raw_configs)

        # دسته‌بندی
        categories = self.categorize_configs()

        # تولید لینک‌های اشتراک
        subscription_files = self.generate_subscription_links(categories)

        # ذخیره فایل‌ها
        import os
        os.makedirs('subscriptions', exist_ok=True)

        for protocol, file_info in subscription_files.items():
            with open(file_info['filename'], 'w', encoding='utf-8') as f:
                f.write(file_info['content'])

        logger.info(
            f"✅ سیکل کامل شد - {len(self.working_configs)} کانفیگ سالم ذخیره شد")

        return subscription_files

    def generate_report(self):
        """تولید گزارش عملکرد"""
        total_tested = len(self.working_configs) + len(self.failed_configs)
        success_rate = (len(self.working_configs) /
                        total_tested * 100) if total_tested > 0 else 0

        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_configs_tested': total_tested,
            'working_configs': len(self.working_configs),
            'failed_configs': len(self.failed_configs),
            'success_rate': f"{success_rate:.1f}%",
            'protocols': {}
        }

        # آمار پروتکل‌ها
        for config in self.working_configs:
            if config.protocol not in report['protocols']:
                report['protocols'][config.protocol] = {
                    'count': 0, 'avg_latency': 0}
            report['protocols'][config.protocol]['count'] += 1

        # محاسبه میانگین تأخیر
        for protocol in report['protocols']:
            protocol_configs = [
                c for c in self.working_configs if c.protocol == protocol]
            if protocol_configs:
                avg_latency = sum(
                    c.latency for c in protocol_configs) / len(protocol_configs)
                report['protocols'][protocol]['avg_latency'] = f"{avg_latency:.1f}ms"

        return report


async def main():
    """تابع اصلی"""
    collector = V2RayCollector()

    try:
        # اجرای سیکل جمع‌آوری
        subscription_files = await collector.run_collection_cycle()

        # تولید گزارش
        report = collector.generate_report()

        # ذخیره گزارش
        with open('subscriptions/report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print("\n" + "="*50)
        print("📊 گزارش نهایی:")
        print(f"تعداد کل کانفیگ‌های تست شده: {report['total_configs_tested']}")
        print(f"کانفیگ‌های سالم: {report['working_configs']}")
        print(f"کانفیگ‌های ناسالم: {report['failed_configs']}")
        print(f"نرخ موفقیت: {report['success_rate']}")
        print("\n📁 فایل‌های تولید شده:")
        for protocol, file_info in subscription_files.items():
            print(
                f"  {protocol}: {file_info['count']} کانفیگ - {file_info['filename']}")
        print("="*50)

    except Exception as e:
        logger.error(f"خطای کلی در اجرا: {e}")

if __name__ == "__main__":
    asyncio.run(main())
