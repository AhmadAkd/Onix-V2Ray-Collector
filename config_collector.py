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
import hashlib
import socket
import concurrent.futures
from typing import List, Dict, Optional, Tuple, Set
from dataclasses import dataclass
from urllib.parse import urlparse

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


class UltraFastConnectionPool:
    """Connection Pool برای تست فوق سریع"""

    def __init__(self, max_workers: int = 100):
        self.max_workers = max_workers
        self.executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=max_workers)
        self.connection_cache = {}
        self.test_results = {}

    def test_connection_sync(self, address: str, port: int, timeout: float = 2.0) -> Tuple[bool, float]:
        """تست همزمان اتصال"""
        try:
            start_time = time.time()

            # استفاده از socket برای تست سریع‌تر
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)

            result = sock.connect_ex((address, port))
            sock.close()

            latency = (time.time() - start_time) * 1000

            if result == 0:
                return True, latency
            return False, 0.0

        except Exception:
            return False, 0.0

    async def test_multiple_connections(self, configs: List[V2RayConfig]) -> List[Tuple[V2RayConfig, bool, float]]:
        """تست چندگانه اتصالات"""
        loop = asyncio.get_event_loop()

        # ایجاد tasks برای تست موازی
        tasks = []
        for config in configs:
            task = loop.run_in_executor(
                self.executor,
                self.test_connection_sync,
                config.address,
                config.port,
                2.0  # timeout کوتاه
            )
            tasks.append((config, task))

        # اجرای موازی
        results = []
        for config, task in tasks:
            try:
                is_working, latency = await task
                results.append((config, is_working, latency))
            except Exception:
                results.append((config, False, 0.0))

        return results

    def close(self):
        """بستن executor"""
        self.executor.shutdown(wait=True)


class SmartConfigFilter:
    """فیلتر هوشمند برای حذف کانفیگ‌های نامناسب قبل از تست"""

    def __init__(self):
        self.blacklisted_ips = set()
        self.blacklisted_ports = {22, 23, 25, 53, 80,
                                  110, 143, 993, 995, 3389, 5432, 6379, 27017}
        self.valid_ports = set(range(1024, 65536))  # پورت‌های کاربری

    def is_valid_config(self, config: V2RayConfig) -> bool:
        """بررسی اعتبار کانفیگ"""
        # بررسی IP
        if config.address in self.blacklisted_ips:
            return False

        # بررسی پورت
        if config.port in self.blacklisted_ports:
            return False

        # بررسی محدوده پورت
        if config.port not in self.valid_ports:
            return False

        # بررسی آدرس IP خصوصی (معمولاً غیرقابل دسترس)
        if config.address.startswith(('127.', '192.168.', '10.', '172.')):
            return False

        # بررسی UUID خالی
        if not config.uuid or len(config.uuid) < 10:
            return False

        return True

    def filter_configs(self, configs: List[V2RayConfig]) -> List[V2RayConfig]:
        """فیلتر کردن کانفیگ‌ها"""
        valid_configs = []
        filtered_count = 0

        for config in configs:
            if self.is_valid_config(config):
                valid_configs.append(config)
            else:
                filtered_count += 1

        logger.info(f"🔍 فیلتر هوشمند: {filtered_count} کانفیگ نامناسب حذف شد")
        return valid_configs


class V2RayCollector:
    """کلاس اصلی برای جمع‌آوری و تست کانفیگ‌های V2Ray"""

    def __init__(self):
        self.configs: List[V2RayConfig] = []
        self.working_configs: List[V2RayConfig] = []
        self.failed_configs: List[V2RayConfig] = []

        # اضافه کردن سیستم‌های جدید
        self.connection_pool = UltraFastConnectionPool(max_workers=200)
        self.smart_filter = SmartConfigFilter()

        # اضافه کردن Cache Manager
        try:
            from cache_manager import CacheManager
            self.cache = CacheManager(cache_dir="cache", max_size=2000)
            logger.info("Cache Manager initialized successfully")
        except ImportError:
            logger.warning(
                "Cache Manager not available, running without cache")
            self.cache = None

        # اضافه کردن Advanced Analytics
        try:
            from analytics import AdvancedAnalytics
            self.analytics = AdvancedAnalytics()
            logger.info("Advanced Analytics initialized successfully")
        except ImportError:
            logger.warning(
                "Advanced Analytics not available, running without analytics")
            self.analytics = None

        # منابع کانفیگ‌های رایگان - منابع فعال و معتبر (بهینه‌سازی شده)
        self.config_sources = [
            # منابع اصلی Epodonios (تست شده)
            "https://github.com/Epodonios/v2ray-configs/raw/main/All_Configs_base64_Sub.txt",

            # منابع تقسیم شده بر اساس پروتکل (Epodonios)
            "https://github.com/Epodonios/v2ray-configs/raw/main/Splitted-By-Protocol/vless.txt",
            "https://github.com/Epodonios/v2ray-configs/raw/main/Splitted-By-Protocol/vmess.txt",
            "https://github.com/Epodonios/v2ray-configs/raw/main/Splitted-By-Protocol/ss.txt",
            "https://github.com/Epodonios/v2ray-configs/raw/main/Splitted-By-Protocol/ssr.txt",
            "https://github.com/Epodonios/v2ray-configs/raw/main/Splitted-By-Protocol/trojan.txt",

            # منابع تقسیم شده (Epodonios - 250 کانفیگ در هر فایل)
            "https://raw.githubusercontent.com/Epodonios/v2ray-configs/refs/heads/main/Sub1.txt",
            "https://raw.githubusercontent.com/Epodonios/v2ray-configs/refs/heads/main/Sub2.txt",
            "https://raw.githubusercontent.com/Epodonios/v2ray-configs/refs/heads/main/Sub3.txt",
            "https://raw.githubusercontent.com/Epodonios/v2ray-configs/refs/heads/main/Sub4.txt",
            "https://raw.githubusercontent.com/Epodonios/v2ray-configs/refs/heads/main/Sub5.txt",

            # منابع معتبر دیگر (تست شده)
            "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt",
            "https://raw.githubusercontent.com/peasoft/NoMoreWalls/master/list.txt",
            "https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2",

            # منابع SingBox (تست شده)
            "https://raw.githubusercontent.com/itsyebekhe/PSG/main/subscriptions/singbox/ss.json",
            "https://raw.githubusercontent.com/itsyebekhe/PSG/main/subscriptions/singbox/mix.json",
            "https://raw.githubusercontent.com/itsyebekhe/PSG/main/subscriptions/singbox/vmess.json",
            "https://raw.githubusercontent.com/itsyebekhe/PSG/main/subscriptions/singbox/vless.json",
            "https://raw.githubusercontent.com/itsyebekhe/PSG/main/subscriptions/singbox/trojan.json",
            "https://raw.githubusercontent.com/itsyebekhe/PSG/main/subscriptions/singbox/hy2.json",

            # منابع Leon406 SubCrawler (تست شده)
            "https://raw.githubusercontent.com/Leon406/SubCrawler/main/sub/share/vless",
            "https://raw.githubusercontent.com/Leon406/SubCrawler/main/sub/share/ss",

            # منابع Shadowsocks (تست شده)
            "https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/sub/sub_merge.txt",

            # منابع Argh94/V2RayAutoConfig (تست شده)
            "https://raw.githubusercontent.com/Argh94/V2RayAutoConfig/refs/heads/main/configs/USA.txt",
            "https://raw.githubusercontent.com/Argh94/V2RayAutoConfig/refs/heads/main/configs/UK.txt",
            "https://raw.githubusercontent.com/Argh94/V2RayAutoConfig/refs/heads/main/configs/Germany.txt",
            "https://raw.githubusercontent.com/Argh94/V2RayAutoConfig/refs/heads/main/configs/France.txt",
            "https://raw.githubusercontent.com/Argh94/V2RayAutoConfig/refs/heads/main/configs/Canada.txt",
            "https://raw.githubusercontent.com/Argh94/V2RayAutoConfig/refs/heads/main/configs/Japan.txt",
            "https://raw.githubusercontent.com/Argh94/V2RayAutoConfig/refs/heads/main/configs/Singapore.txt",
            "https://raw.githubusercontent.com/Argh94/V2RayAutoConfig/refs/heads/main/configs/Iran.txt",
        ]

        # الگوهای regex برای تشخیص پروتکل‌ها
        self.protocol_patterns = {
            'vmess': r'vmess://([A-Za-z0-9+/=]+)',
            'vless': r'vless://([^@]+)@([^:]+):(\d+)(\?[^#]*)?(#.*)?',
            'trojan': r'trojan://([^@]+)@([^:]+):(\d+)(\?[^#]*)?(#.*)?',
            'ss': r'ss://([A-Za-z0-9+/=]+)',
            'ssr': r'ssr://([A-Za-z0-9+/=]+)',
            'hysteria': r'hysteria://([^#]+)(#.*)?',
            'hy2': r'hy2://([^#]+)(#.*)?',
            'wireguard': r'wireguard://([^#]+)(#.*)?',
            'tuic': r'tuic://([^#]+)(#.*)?',
            'naive': r'naive://([^#]+)(#.*)?',
            'hysteria2': r'hysteria2://([^#]+)(#.*)?'
        }

    async def fetch_configs_from_source(self, source_url: str) -> List[str]:
        """دریافت کانفیگ‌ها از یک منبع با کش"""
        # بررسی کش
        if self.cache:
            cached_configs = self.cache.get(source_url)
            if cached_configs is not None:
                logger.info(
                    f"Cache hit for {source_url} - {len(cached_configs)} configs")
                return cached_configs

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(source_url, timeout=30) as response:
                    if response.status == 200:
                        content = await response.text()

                        # بررسی فرمت JSON (SingBox)
                        if source_url.endswith('.json') or content.strip().startswith('{'):
                            try:
                                import json
                                json_data = json.loads(content)
                                singbox_configs = self.parse_singbox_config(
                                    json_data)
                                # تبدیل به فرمت استاندارد
                                configs = [
                                    config.raw_config for config in singbox_configs]
                                logger.info(
                                    f"دریافت {len(configs)} کانفیگ از SingBox JSON: {source_url}")

                                # ذخیره در کش
                                if self.cache:
                                    self.cache.set(
                                        source_url, configs, ttl=1800)  # 30 دقیقه

                                return configs
                            except json.JSONDecodeError:
                                logger.warning(
                                    f"فرمت JSON نامعتبر در {source_url}")

                        # تجزیه کانفیگ‌ها از متن معمولی
                        configs = []
                        for line in content.strip().split('\n'):
                            if line.strip() and not line.startswith('#'):
                                configs.append(line.strip())

                        logger.info(
                            f"دریافت {len(configs)} کانفیگ از {source_url}")

                        # ذخیره در کش
                        if self.cache:
                            self.cache.set(source_url, configs,
                                           ttl=1800)  # 30 دقیقه

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

    def parse_ssr_config(self, config_str: str) -> Optional[V2RayConfig]:
        """تجزیه کانفیگ ShadowsocksR"""
        try:
            # حذف پیشوند ssr://
            encoded_part = config_str[6:]

            # اضافه کردن padding اگر لازم باشد
            missing_padding = len(encoded_part) % 4
            if missing_padding:
                encoded_part += '=' * (4 - missing_padding)

            # decode base64
            decoded = base64.b64decode(encoded_part).decode('utf-8')

            # تجزیه پارامترها - SSR format: server:port:protocol:method:obfs:password/base64
            parts = decoded.split('/')
            if len(parts) < 1:
                return None

            # تجزیه بخش اول (server info)
            server_info_parts = parts[0].split(':')
            if len(server_info_parts) < 6:
                return None

            server = server_info_parts[0]
            port = int(server_info_parts[1])
            protocol = server_info_parts[2]
            method = server_info_parts[3]
            obfs = server_info_parts[4]
            password_encoded = server_info_parts[5]

            # decode password
            try:
                password_missing_padding = len(password_encoded) % 4
                if password_missing_padding:
                    password_encoded += '=' * (4 - password_missing_padding)
                password = base64.b64decode(password_encoded).decode('utf-8')
            except:
                password = password_encoded

            return V2RayConfig(
                protocol="ssr",
                address=server,
                port=port,
                uuid=f"{method}:{password}",
                raw_config=config_str,
                country="unknown"
            )

        except Exception as e:
            logger.debug(f"خطا در تجزیه SSR: {e}")
            return None

    async def test_config_connectivity(self, config: V2RayConfig) -> Tuple[bool, float]:
        """تست اتصال کانفیگ با روش‌های پیشرفته"""
        try:
            start_time = time.time()

            # تست‌های مختلف برای پروتکل‌های مختلف
            if config.protocol == "vmess":
                return await self._test_vmess_connection(config, start_time)
            elif config.protocol == "vless":
                return await self._test_vless_connection(config, start_time)
            elif config.protocol == "trojan":
                return await self._test_trojan_connection(config, start_time)
            elif config.protocol in ["ss", "ssr"]:
                return await self._test_ss_connection(config, start_time)
            else:
                return await self._test_generic_connection(config, start_time)

        except Exception as e:
            logger.debug(
                f"خطا در تست {config.protocol} {config.address}:{config.port} - {e}")
            return False, 0.0

    async def _test_vmess_connection(self, config: V2RayConfig, start_time: float) -> Tuple[bool, float]:
        """تست اتصال VMess"""
        try:
            import socket

            # تست اتصال TCP
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            result = sock.connect_ex((config.address, config.port))
            sock.close()

            if result == 0:
                latency = (time.time() - start_time) * 1000
                return True, latency
            return False, 0.0

        except Exception:
            return False, 0.0

    async def _test_vless_connection(self, config: V2RayConfig, start_time: float) -> Tuple[bool, float]:
        """تست اتصال VLESS"""
        try:
            import socket

            # تست اتصال TCP
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            result = sock.connect_ex((config.address, config.port))
            sock.close()

            if result == 0:
                latency = (time.time() - start_time) * 1000
                return True, latency
            return False, 0.0

        except Exception:
            return False, 0.0

    async def _test_trojan_connection(self, config: V2RayConfig, start_time: float) -> Tuple[bool, float]:
        """تست اتصال Trojan"""
        try:
            import socket
            import ssl

            # تست اتصال TCP + TLS
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)

            try:
                sock.connect((config.address, config.port))

                # تست TLS
                context = ssl.create_default_context()
                # برای تست فقط hostname check رو غیرفعال می‌کنیم
                context.check_hostname = False
                # اما certificate verification رو نگه می‌داریم برای امنیت بیشتر
                context.verify_mode = ssl.CERT_OPTIONAL

                try:
                    tls_sock = context.wrap_socket(
                        sock, server_hostname=config.address)
                    tls_sock.close()
                except ssl.SSLError:
                    # اگر TLS verification ناموفق بود، با CERT_NONE امتحان می‌کنیم
                    context.verify_mode = ssl.CERT_NONE
                    tls_sock = context.wrap_socket(
                        sock, server_hostname=config.address)
                    tls_sock.close()

                latency = (time.time() - start_time) * 1000
                return True, latency

            except:
                sock.close()
                return False, 0.0

        except Exception:
            return False, 0.0

    async def _test_ss_connection(self, config: V2RayConfig, start_time: float) -> Tuple[bool, float]:
        """تست اتصال Shadowsocks"""
        try:
            import socket

            # تست اتصال TCP
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            result = sock.connect_ex((config.address, config.port))
            sock.close()

            if result == 0:
                latency = (time.time() - start_time) * 1000
                return True, latency
            return False, 0.0

        except Exception:
            return False, 0.0

    async def _test_generic_connection(self, config: V2RayConfig, start_time: float) -> Tuple[bool, float]:
        """تست اتصال عمومی"""
        try:
            import socket

            # تست اتصال TCP ساده
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            result = sock.connect_ex((config.address, config.port))
            sock.close()

            if result == 0:
                latency = (time.time() - start_time) * 1000
                return True, latency
            return False, 0.0

        except Exception:
            return False, 0.0

    async def test_config_connectivity_fast(self, config: V2RayConfig) -> Tuple[bool, float]:
        """تست سریع اتصال کانفیگ با timeout کوتاه‌تر"""
        try:
            start_time = time.time()

            # تست سریع با timeout کوتاه‌تر
            if config.protocol == "vmess":
                return await self._test_vmess_connection_fast(config, start_time)
            elif config.protocol == "vless":
                return await self._test_vless_connection_fast(config, start_time)
            elif config.protocol == "trojan":
                return await self._test_trojan_connection_fast(config, start_time)
            elif config.protocol in ["ss", "ssr"]:
                return await self._test_ss_connection_fast(config, start_time)
            else:
                return await self._test_generic_connection_fast(config, start_time)

        except Exception as e:
            logger.debug(
                f"خطا در تست سریع {config.protocol} {config.address}:{config.port} - {e}")
            return False, 0.0

    async def _test_vmess_connection_fast(self, config: V2RayConfig, start_time: float) -> Tuple[bool, float]:
        """تست سریع اتصال VMess"""
        try:
            import socket

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)  # timeout کوتاه‌تر
            result = sock.connect_ex((config.address, config.port))
            sock.close()

            if result == 0:
                latency = (time.time() - start_time) * 1000
                return True, latency
            return False, 0.0

        except Exception:
            return False, 0.0

    async def _test_vless_connection_fast(self, config: V2RayConfig, start_time: float) -> Tuple[bool, float]:
        """تست سریع اتصال VLESS"""
        try:
            import socket

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((config.address, config.port))
            sock.close()

            if result == 0:
                latency = (time.time() - start_time) * 1000
                return True, latency
            return False, 0.0

        except Exception:
            return False, 0.0

    async def _test_trojan_connection_fast(self, config: V2RayConfig, start_time: float) -> Tuple[bool, float]:
        """تست سریع اتصال Trojan"""
        try:
            import socket

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((config.address, config.port))
            sock.close()

            if result == 0:
                latency = (time.time() - start_time) * 1000
                return True, latency
            return False, 0.0

        except Exception:
            return False, 0.0

    async def _test_ss_connection_fast(self, config: V2RayConfig, start_time: float) -> Tuple[bool, float]:
        """تست سریع اتصال Shadowsocks"""
        try:
            import socket

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((config.address, config.port))
            sock.close()

            if result == 0:
                latency = (time.time() - start_time) * 1000
                return True, latency
            return False, 0.0

        except Exception:
            return False, 0.0

    async def _test_generic_connection_fast(self, config: V2RayConfig, start_time: float) -> Tuple[bool, float]:
        """تست سریع اتصال عمومی"""
        try:
            import socket

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((config.address, config.port))
            sock.close()

            if result == 0:
                latency = (time.time() - start_time) * 1000
                return True, latency
            return False, 0.0

        except Exception:
            return False, 0.0

    def parse_singbox_config(self, json_data: dict) -> List[V2RayConfig]:
        """تجزیه کانفیگ SingBox JSON"""
        configs = []

        try:
            outbounds = json_data.get('outbounds', [])

            for outbound in outbounds:
                if isinstance(outbound, dict) and 'outbounds' in outbound:
                    # این یک selector است که خودش outbounds دارد
                    for sub_outbound in outbound['outbounds']:
                        config = self.parse_singbox_outbound(sub_outbound)
                        if config:
                            configs.append(config)
                else:
                    # این یک outbound مستقیم است
                    config = self.parse_singbox_outbound(outbound)
                    if config:
                        configs.append(config)

            logger.info(f"تجزیه شد {len(configs)} کانفیگ از فرمت SingBox")
            return configs

        except Exception as e:
            logger.error(f"خطا در تجزیه SingBox: {e}")
            return []

    def parse_singbox_outbound(self, outbound: dict) -> Optional[V2RayConfig]:
        """تجزیه یک outbound SingBox"""
        try:
            outbound_type = outbound.get('type', '')
            tag = outbound.get('tag', '')

            if outbound_type == 'vmess':
                return V2RayConfig(
                    protocol="vmess",
                    address=outbound.get('server', ''),
                    port=int(outbound.get('server_port', 0)),
                    uuid=outbound.get('uuid', ''),
                    alter_id=int(outbound.get('alter_id', 0)),
                    network=outbound.get('transport', {}).get('type', 'tcp'),
                    tls=outbound.get('transport', {}).get('tls', False),
                    raw_config=f"vmess://{self.encode_vmess_config(outbound)}",
                    country=self.extract_country_from_tag(tag)
                )

            elif outbound_type == 'vless':
                return V2RayConfig(
                    protocol="vless",
                    address=outbound.get('server', ''),
                    port=int(outbound.get('server_port', 0)),
                    uuid=outbound.get('uuid', ''),
                    network=outbound.get('transport', {}).get('type', 'tcp'),
                    tls=outbound.get('transport', {}).get('tls', False),
                    raw_config=f"vless://{self.encode_vless_config(outbound)}",
                    country=self.extract_country_from_tag(tag)
                )

            elif outbound_type == 'trojan':
                return V2RayConfig(
                    protocol="trojan",
                    address=outbound.get('server', ''),
                    port=int(outbound.get('server_port', 0)),
                    uuid=outbound.get('password', ''),
                    tls=True,
                    raw_config=f"trojan://{self.encode_trojan_config(outbound)}",
                    country=self.extract_country_from_tag(tag)
                )

            elif outbound_type == 'shadowsocks':
                return V2RayConfig(
                    protocol="ss",
                    address=outbound.get('server', ''),
                    port=int(outbound.get('server_port', 0)),
                    uuid=f"{outbound.get('method', '')}:{outbound.get('password', '')}",
                    raw_config=f"ss://{self.encode_ss_config(outbound)}",
                    country=self.extract_country_from_tag(tag)
                )

        except Exception as e:
            logger.debug(f"خطا در تجزیه outbound: {e}")

        return None

    def validate_country_name(self, country: str) -> str:
        """اعتبارسنجی و نرمال‌سازی نام کشور"""
        if not country:
            return 'Unknown'

        # لیست کدهای معتبر کشور (ISO 3166-1 alpha-2)
        valid_country_codes = {
            'US', 'DE', 'IR', 'CA', 'NL', 'TR', 'SE', 'IN', 'RU',
            'ES', 'NO', 'LT', 'HK', 'CN', 'GB', 'FR', 'JP', 'SG',
            'AU', 'BR', 'KR', 'IT', 'CH', 'PL', 'UA', 'TW', 'FI',
            'AT', 'BE', 'DK', 'IE', 'PT', 'GR', 'CZ', 'RO', 'BG',
            'HR', 'SK', 'SI', 'EE', 'LV', 'IS', 'LU', 'MT', 'CY'
        }

        # نرمال‌سازی
        country = country.strip().upper()

        # اگر شروع با عدد می‌شود، نامعتبر است
        if country and country[0].isdigit():
            return 'Unknown'

        # اگر شامل ms یا latency است، نامعتبر است
        if 'MS' in country or 'LATENCY' in country or '_' in country:
            return 'Unknown'

        # اگر طول بیش از 30 کاراکتر است، نامعتبر است
        if len(country) > 30:
            return 'Unknown'

        # اگر کد 2-3 حرفی معتبر است
        if len(country) <= 3 and country in valid_country_codes:
            return country

        # اگر نام کامل کشور است، آن را به کد تبدیل کن
        country_name_to_code = {
            'UNITED STATES': 'US', 'AMERICA': 'US', 'USA': 'US',
            'GERMANY': 'DE', 'DEUTSCHLAND': 'DE',
            'IRAN': 'IR', 'PERSIA': 'IR',
            'CANADA': 'CA',
            'NETHERLANDS': 'NL', 'HOLLAND': 'NL',
            'TURKEY': 'TR', 'TURKIYE': 'TR',
            'SWEDEN': 'SE',
            'INDIA': 'IN',
            'RUSSIA': 'RU',
            'SPAIN': 'ES',
            'NORWAY': 'NO',
            'LITHUANIA': 'LT',
            'HONG KONG': 'HK', 'HONGKONG': 'HK',
            'CHINA': 'CN',
            'UNITED KINGDOM': 'GB', 'UK': 'GB', 'BRITAIN': 'GB',
            'FRANCE': 'FR',
            'JAPAN': 'JP',
            'SINGAPORE': 'SG',
            'AUSTRALIA': 'AU',
            'BRAZIL': 'BR',
            'SOUTH KOREA': 'KR', 'KOREA': 'KR',
            'ITALY': 'IT',
            'SWITZERLAND': 'CH',
            'POLAND': 'PL',
            'UKRAINE': 'UA',
            'TAIWAN': 'TW',
            'FINLAND': 'FI'
        }

        country_upper = country.upper().replace('_', ' ')
        if country_upper in country_name_to_code:
            return country_name_to_code[country_upper]

        # در غیر این صورت Unknown
        return 'Unknown'

    def extract_country_from_tag(self, tag: str) -> str:
        """استخراج کشور از تگ"""
        country_flags = {
            '🇺🇸': 'US', '🇩🇪': 'DE', '🇮🇷': 'IR', '🇨🇦': 'CA',
            '🇳🇱': 'NL', '🇹🇷': 'TR', '🇸🇪': 'SE', '🇮🇳': 'IN',
            '🇷🇺': 'RU', '🇪🇸': 'ES', '🇳🇴': 'NO', '🇱🇹': 'LT',
            '🇭🇰': 'HK', '🇨🇳': 'CN', '🚩': 'CF', '🇬🇧': 'GB',
            '🇫🇷': 'FR', '🇯🇵': 'JP', '🇸🇬': 'SG', '🇦🇺': 'AU',
            '🇧🇷': 'BR', '🇰🇷': 'KR', '🇮🇹': 'IT', '🇨🇭': 'CH',
            '🇵🇱': 'PL', '🇺🇦': 'UA', '🇹🇼': 'TW', '🇫🇮': 'FI'
        }

        # بررسی flag در تگ
        for flag, country in country_flags.items():
            if flag in tag:
                return country

        # بررسی کد کشور (2-3 حرف بزرگ)
        country_match = re.search(r'\b([A-Z]{2,3})\b', tag)
        if country_match:
            country_code = country_match.group(1)
            # لیست کدهای معتبر کشور
            valid_codes = ['US', 'DE', 'IR', 'CA', 'NL', 'TR', 'SE', 'IN', 'RU',
                           'ES', 'NO', 'LT', 'HK', 'CN', 'GB', 'FR', 'JP', 'SG',
                           'AU', 'BR', 'KR', 'IT', 'CH', 'PL', 'UA', 'TW', 'FI']
            if country_code in valid_codes:
                return country_code

        return 'Unknown'

    def encode_vmess_config(self, outbound: dict) -> str:
        """کدگذاری کانفیگ VMess به base64"""
        vmess_config = {
            "v": "2",
            "ps": outbound.get('tag', ''),
            "add": outbound.get('server', ''),
            "port": str(outbound.get('server_port', 0)),
            "id": outbound.get('uuid', ''),
            "aid": str(outbound.get('alter_id', 0)),
            "net": outbound.get('transport', {}).get('type', 'tcp'),
            "type": "none",
            "host": "",
            "path": "",
            "tls": "tls" if outbound.get('transport', {}).get('tls') else ""
        }

        import json
        return base64.b64encode(json.dumps(vmess_config).encode()).decode()

    def encode_vless_config(self, outbound: dict) -> str:
        """کدگذاری کانفیگ VLESS"""
        uuid = outbound.get('uuid', '')
        server = outbound.get('server', '')
        port = outbound.get('server_port', 0)

        params = []
        if outbound.get('transport', {}).get('tls'):
            params.append('security=tls')

        params_str = '&'.join(params) if params else ''
        fragment = f"#{outbound.get('tag', '')}"

        return f"{uuid}@{server}:{port}?{params_str}{fragment}"

    def encode_trojan_config(self, outbound: dict) -> str:
        """کدگذاری کانفیگ Trojan"""
        password = outbound.get('password', '')
        server = outbound.get('server', '')
        port = outbound.get('server_port', 0)
        fragment = f"#{outbound.get('tag', '')}"

        return f"{password}@{server}:{port}{fragment}"

    def encode_ss_config(self, outbound: dict) -> str:
        """کدگذاری کانفیگ Shadowsocks"""
        method = outbound.get('method', '')
        password = outbound.get('password', '')
        server = outbound.get('server', '')
        port = outbound.get('server_port', 0)

        encoded = base64.b64encode(f"{method}:{password}".encode()).decode()
        return f"{encoded}@{server}:{port}"

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
        elif config_str.startswith('ssr://'):
            return self.parse_ssr_config(config_str)
        elif config_str.startswith('hysteria://') or config_str.startswith('hy2://') or config_str.startswith('hysteria2://'):
            return self.parse_hysteria_config(config_str)
        elif config_str.startswith('wireguard://'):
            return self.parse_wireguard_config(config_str)
        elif config_str.startswith('tuic://'):
            return self.parse_tuic_config(config_str)
        elif config_str.startswith('naive://'):
            return self.parse_naive_config(config_str)

        return None

    def parse_hysteria_config(self, config_str: str) -> Optional[V2RayConfig]:
        """تجزیه کانفیگ Hysteria"""
        try:
            # استخراج بخش اصلی
            if '://' in config_str:
                main_part = config_str.split('://', 1)[1]
            else:
                return None

            # تجزیه پارامترها
            parts = main_part.split('?')
            server_info = parts[0]

            # استخراج آدرس و پورت
            if '@' in server_info:
                server_part = server_info.split('@')[1]
            else:
                server_part = server_info

            if ':' in server_part:
                address, port = server_part.rsplit(':', 1)
                port = int(port)
            else:
                return None

            # استخراج UUID از query params
            uuid = "hysteria-uuid"
            if len(parts) > 1:
                params = parts[1].split('#')[0]
                for param in params.split('&'):
                    if '=' in param:
                        key, value = param.split('=', 1)
                        if key == 'auth' or key == 'password':
                            uuid = value
                            break

            return V2RayConfig(
                protocol="hysteria",
                address=address,
                port=port,
                uuid=uuid,
                raw_config=config_str
            )
        except Exception as e:
            logger.debug(f"خطا در تجزیه Hysteria: {e}")
            return None

    def parse_wireguard_config(self, config_str: str) -> Optional[V2RayConfig]:
        """تجزیه کانفیگ WireGuard"""
        try:
            # استخراج بخش اصلی
            if '://' in config_str:
                main_part = config_str.split('://', 1)[1]
            else:
                return None

            # تجزیه پارامترها
            parts = main_part.split('?')
            server_info = parts[0]

            # استخراج آدرس و پورت
            if '@' in server_info:
                server_part = server_info.split('@')[1]
            else:
                server_part = server_info

            if ':' in server_part:
                address, port = server_part.rsplit(':', 1)
                port = int(port)
            else:
                return None

            # استخراج Public Key
            public_key = "wireguard-key"
            if len(parts) > 1:
                params = parts[1].split('#')[0]
                for param in params.split('&'):
                    if '=' in param:
                        key, value = param.split('=', 1)
                        if key == 'publickey':
                            public_key = value
                            break

            return V2RayConfig(
                protocol="wireguard",
                address=address,
                port=port,
                uuid=public_key,
                raw_config=config_str
            )
        except Exception as e:
            logger.debug(f"خطا در تجزیه WireGuard: {e}")
            return None

    def parse_tuic_config(self, config_str: str) -> Optional[V2RayConfig]:
        """تجزیه کانفیگ TUIC"""
        try:
            # استخراج بخش اصلی
            if '://' in config_str:
                main_part = config_str.split('://', 1)[1]
            else:
                return None

            # تجزیه پارامترها
            parts = main_part.split('?')
            server_info = parts[0]

            # استخراج آدرس و پورت
            if '@' in server_info:
                server_part = server_info.split('@')[1]
            else:
                server_part = server_info

            if ':' in server_part:
                address, port = server_part.rsplit(':', 1)
                port = int(port)
            else:
                return None

            # استخراج UUID
            uuid = "tuic-uuid"
            if len(parts) > 1:
                params = parts[1].split('#')[0]
                for param in params.split('&'):
                    if '=' in param:
                        key, value = param.split('=', 1)
                        if key == 'uuid':
                            uuid = value
                            break

            return V2RayConfig(
                protocol="tuic",
                address=address,
                port=port,
                uuid=uuid,
                raw_config=config_str
            )
        except Exception as e:
            logger.debug(f"خطا در تجزیه TUIC: {e}")
            return None

    def parse_naive_config(self, config_str: str) -> Optional[V2RayConfig]:
        """تجزیه کانفیگ Naive"""
        try:
            # استخراج بخش اصلی
            if '://' in config_str:
                main_part = config_str.split('://', 1)[1]
            else:
                return None

            # تجزیه پارامترها
            parts = main_part.split('?')
            server_info = parts[0]

            # استخراج آدرس و پورت
            if '@' in server_info:
                server_part = server_info.split('@')[1]
            else:
                server_part = server_info

            if ':' in server_part:
                address, port = server_part.rsplit(':', 1)
                port = int(port)
            else:
                return None

            # استخراج username
            username = "naive-user"
            if '@' in server_info:
                username = server_info.split('@')[0]

            return V2RayConfig(
                protocol="naive",
                address=address,
                port=port,
                uuid=username,
                raw_config=config_str
            )
        except Exception as e:
            logger.debug(f"خطا در تجزیه Naive: {e}")
            return None

    def remove_duplicate_configs_advanced(self, configs: List[str]) -> List[str]:
        """حذف تکراری‌های پیشرفته بر اساس محتوا"""
        logger.info("🔍 شروع حذف تکراری‌های پیشرفته...")

        unique_configs = []
        seen_hashes = set()
        duplicate_count = 0

        for config_str in configs:
            if not config_str or len(config_str.strip()) == 0:
                continue

            # ایجاد hash از محتوای کانفیگ
            config_hash = hashlib.md5(config_str.encode('utf-8')).hexdigest()

            if config_hash not in seen_hashes:
                # بررسی تکراری بر اساس آدرس و پورت
                config = self.parse_config(config_str)
                if config:
                    server_key = f"{config.address}:{config.port}:{config.protocol}"
                    if server_key not in seen_hashes:
                        unique_configs.append(config_str)
                        seen_hashes.add(config_hash)
                        seen_hashes.add(server_key)
                    else:
                        duplicate_count += 1
                else:
                    unique_configs.append(config_str)
                    seen_hashes.add(config_hash)
            else:
                duplicate_count += 1

        logger.info(f"🔄 حذف {duplicate_count} کانفیگ تکراری")
        return unique_configs

    async def test_all_configs_ultra_fast(self, configs: List[str], max_concurrent: int = 50):
        """تست فوق سریع کانفیگ‌ها با بهینه‌سازی پیشرفته"""
        start_time = time.time()
        logger.info(f"🚀 شروع تست فوق سریع {len(configs)} کانفیگ...")

        # مرحله 1: حذف تکراری‌های پیشرفته
        unique_configs = self.remove_duplicate_configs_advanced(configs)
        logger.info(
            f"🔄 حذف تکراری‌ها: {len(configs)} → {len(unique_configs)} کانفیگ")

        # مرحله 2: تبدیل به V2RayConfig و فیلتر هوشمند
        parsed_configs = []
        parse_start = time.time()

        for config_str in unique_configs:
            config = self.parse_config(config_str)
            if config:
                parsed_configs.append(config)

        # فیلتر هوشمند
        valid_configs = self.smart_filter.filter_configs(parsed_configs)
        parse_time = time.time() - parse_start
        logger.info(
            f"🔍 فیلتر هوشمند: {len(parsed_configs)} → {len(valid_configs)} کانفیگ معتبر ({parse_time:.1f}s)")

        if not valid_configs:
            logger.warning("❌ هیچ کانفیگ معتبری یافت نشد")
            return

        # مرحله 3: تست فوق سریع با Connection Pool
        test_start = time.time()
        logger.info(
            f"⚡ شروع تست فوق سریع با {self.connection_pool.max_workers} worker")

        # تقسیم به batch های بزرگ برای تست موازی
        batch_size = 500  # batch بزرگ‌تر
        batches = [valid_configs[i:i + batch_size]
                   for i in range(0, len(valid_configs), batch_size)]

        total_tested = 0
        for batch_idx, batch in enumerate(batches):
            logger.info(
                f"🧪 تست batch {batch_idx + 1}/{len(batches)} ({len(batch)} کانفیگ)")

            # تست موازی با Connection Pool
            results = await self.connection_pool.test_multiple_connections(batch)

            # پردازش نتایج
            for config, is_working, latency in results:
                config.is_working = is_working
                config.latency = latency

                if is_working:
                    self.working_configs.append(config)
                    logger.debug(
                        f"✅ {config.protocol.upper()} {config.address}:{config.port} - {latency:.0f}ms")
                else:
                    self.failed_configs.append(config)

            total_tested += len(batch)

            # گزارش پیشرفت
            if batch_idx % 5 == 0 or batch_idx == len(batches) - 1:
                success_rate = (len(self.working_configs) /
                                total_tested * 100) if total_tested > 0 else 0
                logger.info(
                    f"📊 پیشرفت: {total_tested}/{len(valid_configs)} - موفقیت: {success_rate:.1f}%")

        test_time = time.time() - test_start
        total_time = time.time() - start_time

        # گزارش نهایی
        success_rate = (len(self.working_configs) /
                        len(valid_configs) * 100) if valid_configs else 0
        configs_per_second = len(valid_configs) / \
            test_time if test_time > 0 else 0

        logger.info(f"🎉 تست فوق سریع کامل شد:")
        logger.info(f"   ⏱️ زمان کل: {total_time:.1f}s")
        logger.info(f"   🧪 زمان تست: {test_time:.1f}s")
        logger.info(f"   ⚡ سرعت: {configs_per_second:.1f} کانفیگ/ثانیه")
        logger.info(
            f"   ✅ موفق: {len(self.working_configs)} ({success_rate:.1f}%)")
        logger.info(f"   ❌ ناموفق: {len(self.failed_configs)}")

    def cleanup_resources(self):
        """پاکسازی منابع"""
        if hasattr(self, 'connection_pool'):
            self.connection_pool.close()
        logger.info("🧹 منابع پاکسازی شدند")

    async def test_all_configs(self, configs: List[str], max_concurrent: int = 50):
        """Wrapper برای تست فوق سریع"""
        await self.test_all_configs_ultra_fast(configs, max_concurrent)

    def apply_geo_filter(self, configs: List[str]) -> List[str]:
        """اعمال فیلتر جغرافیایی"""
        from config import GEO_FILTER_CONFIG

        if not GEO_FILTER_CONFIG['enabled']:
            return configs

        filtered_configs = []
        country_counts = {}

        for config_str in configs:
            config = self.parse_config(config_str)
            if not config:
                continue

            country = config.country or 'unknown'

            # بررسی کشورهای مسدود
            if country in GEO_FILTER_CONFIG['blocked_countries']:
                continue

            # محدودیت تعداد کانفیگ در هر کشور
            max_per_country = GEO_FILTER_CONFIG.get(
                'max_configs_per_country', 500)
            if country_counts.get(country, 0) >= max_per_country:
                continue

            filtered_configs.append(config_str)
            country_counts[country] = country_counts.get(country, 0) + 1

        logger.info(
            f"فیلتر جغرافیایی: {len(configs)} -> {len(filtered_configs)} کانفیگ")
        return filtered_configs

    def categorize_configs(self):
        """دسته‌بندی کانفیگ‌ها با فیلتر جغرافیایی"""
        from config import CATEGORIZATION_CONFIG, GEO_FILTER_CONFIG

        categories = {
            'vmess': [],
            'vless': [],
            'trojan': [],
            'ss': [],
            'ssr': [],
            'hysteria': [],
            'hysteria2': [],
            'hy2': [],  # alias for hysteria2
            'wireguard': [],
            'tuic': [],
            'naive': []
        }

        # دسته‌بندی بر اساس پروتکل
        for config in self.working_configs:
            protocol = config.protocol.lower()
            
            # Normalize protocol names
            if protocol == 'shadowsocks':
                protocol = 'ss'
            elif protocol == 'shadowsocksr':
                protocol = 'ssr'
            
            if protocol in categories:
                categories[protocol].append(config)
            else:
                # اگر پروتکل جدیدی بود، آن را اضافه کن
                logger.warning(f"پروتکل ناشناخته: {protocol}")
                if protocol not in categories:
                    categories[protocol] = []
                categories[protocol].append(config)

        # اعمال محدودیت‌ها
        max_per_protocol = CATEGORIZATION_CONFIG.get(
            'max_configs_per_protocol', 1000)
        max_per_country = CATEGORIZATION_CONFIG.get(
            'max_configs_per_country', 500)

        for protocol, configs in categories.items():
            # مرتب‌سازی بر اساس تأخیر
            if CATEGORIZATION_CONFIG.get('sort_by_latency', True):
                configs.sort(key=lambda x: x.latency or float('inf'))

            # محدودیت تعداد
            if len(configs) > max_per_protocol:
                categories[protocol] = configs[:max_per_protocol]
                logger.info(
                    f"محدود کردن {protocol}: {len(configs)} -> {max_per_protocol}")

        # دسته‌بندی بر اساس کشور
        if CATEGORIZATION_CONFIG.get('group_by_country', True):
            country_categories = {}
            for protocol, configs in categories.items():
                for config in configs:
                    country = config.country or 'Unknown'

                    # اعتبارسنجی نام کشور
                    country = self.validate_country_name(country)

                    if country not in country_categories:
                        country_categories[country] = []
                    country_categories[country].append(config)

            logger.info(f"دسته‌بندی {len(country_categories)} کشور")

        return categories

    def generate_subscription_links(self, categories: Dict[str, List[V2RayConfig]]):
        """تولید لینک‌های اشتراک"""
        subscription_files = {}

        # ایجاد پوشه‌های مورد نیاز
        import os
        os.makedirs('subscriptions/by_protocol', exist_ok=True)
        os.makedirs('subscriptions/by_country', exist_ok=True)

        # تولید فایل برای هر پروتکل
        for protocol, configs in categories.items():
            if configs:
                # مرتب‌سازی بر اساس سرعت
                configs.sort(key=lambda x: x.latency)

                # تولید محتوای اشتراک
                subscription_content = '\n'.join(
                    [config.raw_config for config in configs])

                # فایل اصلی پروتکل
                filename = f"subscriptions/{protocol}_subscription.txt"
                subscription_files[protocol] = {
                    'filename': filename,
                    'content': subscription_content,
                    'count': len(configs)
                }

                # فایل در پوشه by_protocol
                protocol_filename = f"subscriptions/by_protocol/{protocol}.txt"
                subscription_files[f"{protocol}_by_protocol"] = {
                    'filename': protocol_filename,
                    'content': subscription_content,
                    'count': len(configs)
                }

                logger.info(f"تولید شد: {filename} با {len(configs)} کانفیگ")

        # تولید فایل‌های بر اساس کشور
        country_files = self.generate_country_subscriptions(categories)
        subscription_files.update(country_files)

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

    def generate_country_subscriptions(self, categories: dict) -> dict:
        """تولید فایل‌های اشتراک بر اساس کشور"""
        country_files = {}

        # جمع‌آوری کانفیگ‌ها بر اساس کشور
        country_configs = {}

        for protocol, configs in categories.items():
            for config in configs:
                # اعتبارسنجی و نرمال‌سازی کشور
                country = self.validate_country_name(
                    config.country or 'Unknown')

                if country not in country_configs:
                    country_configs[country] = []
                country_configs[country].append(config)

        # تولید فایل برای هر کشور
        for country, configs in country_configs.items():
            # فقط کشورهای معتبر (نه Unknown)
            if configs and country != "Unknown" and len(configs) >= 1:
                # مرتب‌سازی بر اساس سرعت
                configs.sort(key=lambda x: x.latency)

                # تولید محتوای اشتراک
                subscription_content = '\n'.join(
                    [config.raw_config for config in configs])

                # نام فایل با کد کشور
                filename = f"subscriptions/by_country/{country}.txt"

                country_files[f"{country}_by_country"] = {
                    'filename': filename,
                    'content': subscription_content,
                    'count': len(configs)
                }

                logger.info(f"تولید شد: {filename} با {len(configs)} کانفیگ")

        return country_files

    def sanitize_filename(self, filename: str) -> str:
        """پاک‌سازی نام فایل از کاراکترهای غیرمجاز"""
        import re

        # بررسی اینکه آیا نام فایل یک کد کشور معتبر است
        # کدهای کشور باید 2-3 حرف بزرگ باشند یا نام‌های شناخته شده
        valid_country_pattern = r'^[A-Z]{2,3}$|^[A-Za-z\-\s]{2,30}$'

        # اگر نام فایل یک عدد یا شامل اعداد زیاد است، آن را unknown کن
        if re.match(r'^\d+', filename) or '_' in filename and 'ms' in filename.lower():
            return 'Unknown'

        # حذف کاراکترهای غیرمجاز
        safe_filename = re.sub(r'[<>:"/\\|?*]', '', filename)

        # حذف فاصله‌ها و کاراکترهای خاص
        safe_filename = re.sub(r'\s+', '_', safe_filename)
        safe_filename = safe_filename.replace(
            '|', '_').replace('&', '_').replace('@', '_')

        # اگر نام خیلی عجیب است، unknown کن
        if not re.match(valid_country_pattern, safe_filename.replace('_', ' ')):
            if len(safe_filename) > 30 or any(char.isdigit() for char in safe_filename[:5]):
                return 'Unknown'

        # محدود کردن طول نام فایل
        if len(safe_filename) > 50:
            safe_filename = safe_filename[:50]

        # اگر نام فایل خالی شد، نام پیش‌فرض
        if not safe_filename or safe_filename == '_':
            safe_filename = 'unknown'

        return safe_filename

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

        # تولید گزارش تحلیلی پیشرفته
        if self.analytics:
            try:
                analytics_report = self.analytics.generate_report(
                    self.working_configs, self.failed_configs)
                self.save_analytics_report(analytics_report)
                logger.info("Advanced analytics report generated successfully")
            except Exception as e:
                logger.error(f"Error generating analytics report: {e}")

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

    def save_analytics_report(self, analytics_report: Dict) -> None:
        """ذخیره گزارش تحلیلی"""
        try:
            import os
            os.makedirs('subscriptions', exist_ok=True)

            with open('subscriptions/analytics_report.json', 'w', encoding='utf-8') as f:
                json.dump(analytics_report, f, ensure_ascii=False, indent=2)

            logger.info(
                "Analytics report saved to subscriptions/analytics_report.json")

        except Exception as e:
            logger.error(f"Error saving analytics report: {e}")


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
    finally:
        # پاکسازی منابع
        collector.cleanup_resources()
        logger.info("منابع پاکسازی شدند")

if __name__ == "__main__":
    asyncio.run(main())
