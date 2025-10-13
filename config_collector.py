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
from typing import List, Dict, Optional, Tuple
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
    speed_test_result: float = 0.0


class V2RayCollector:
    """کلاس اصلی برای جمع‌آوری و تست کانفیگ‌های V2Ray"""

    def __init__(self):
        self.configs: List[V2RayConfig] = []
        self.working_configs: List[V2RayConfig] = []
        self.failed_configs: List[V2RayConfig] = []
        
        # اضافه کردن Cache Manager
        try:
            from cache_manager import CacheManager
            self.cache = CacheManager(cache_dir="cache", max_size=2000)
            logger.info("Cache Manager initialized successfully")
        except ImportError:
            logger.warning("Cache Manager not available, running without cache")
            self.cache = None
        
        # اضافه کردن Advanced Analytics
        try:
            from analytics import AdvancedAnalytics
            self.analytics = AdvancedAnalytics()
            logger.info("Advanced Analytics initialized successfully")
        except ImportError:
            logger.warning("Advanced Analytics not available, running without analytics")
            self.analytics = None

        # منابع کانفیگ‌های رایگان
        self.config_sources = [
            "https://github.com/Epodonios/v2ray-configs/raw/main/All_Configs_Sub.txt",
            "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt",
            "https://raw.githubusercontent.com/peasoft/NoMoreWalls/master/list.txt",
            "https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/V2RAY_BASE64.txt",
            "https://raw.githubusercontent.com/Epodonios/v2ray-configs/refs/heads/main/All_Configs_base64_Sub.txt",
            "https://raw.githubusercontent.com/itsyebekhe/PSG/main/subscriptions/singbox/ss.json",
            "https://raw.githubusercontent.com/itsyebekhe/PSG/main/subscriptions/singbox/mix.json"
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
        """دریافت کانفیگ‌ها از یک منبع با کش"""
        # بررسی کش
        if self.cache:
            cached_configs = self.cache.get(source_url)
            if cached_configs is not None:
                logger.info(f"Cache hit for {source_url} - {len(cached_configs)} configs")
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
                                    self.cache.set(source_url, configs, ttl=1800)  # 30 دقیقه
                                
                                return configs
                            except json.JSONDecodeError:
                                logger.warning(
                                    f"فرمت JSON نامعتبر در {source_url}")

                        # تجزیه کانفیگ‌ها از متن معمولی
                        configs = []
                        for line in content.strip().split('\n'):
                            if line.strip() and not line.startswith('#'):
                                configs.append(line.strip())
                        
                        logger.info(f"دریافت {len(configs)} کانفیگ از {source_url}")
                        
                        # ذخیره در کش
                        if self.cache:
                            self.cache.set(source_url, configs, ttl=1800)  # 30 دقیقه
                        
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
            logger.debug(f"خطا در تست {config.protocol} {config.address}:{config.port} - {e}")
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
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                
                tls_sock = context.wrap_socket(sock, server_hostname=config.address)
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
            logger.debug(f"خطا در تست سریع {config.protocol} {config.address}:{config.port} - {e}")
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

    def extract_country_from_tag(self, tag: str) -> str:
        """استخراج کشور از تگ"""
        country_flags = {
            '🇺🇸': 'US', '🇩🇪': 'DE', '🇮🇷': 'IR', '🇨🇦': 'CA',
            '🇳🇱': 'NL', '🇹🇷': 'TR', '🇸🇪': 'SE', '🇮🇳': 'IN',
            '🇷🇺': 'RU', '🇪🇸': 'ES', '🇳🇴': 'NO', '🇱🇹': 'LT',
            '🇭🇰': 'HK', '🇨🇳': 'CN', '🚩': 'CF'
        }

        for flag, country in country_flags.items():
            if flag in tag:
                return country

        return 'unknown'

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

    async def test_all_configs(self, configs: List[str], max_concurrent: int = 20):
        """تست تمام کانفیگ‌ها با بهینه‌سازی پیشرفته"""
        logger.info(f"🧪 شروع تست {len(configs)} کانفیگ...")

        # حذف تکراری‌های پیشرفته
        unique_configs = self.remove_duplicate_configs_advanced(configs)
        logger.info(f"🔄 حذف تکراری‌ها: {len(configs)} → {len(unique_configs)} کانفیگ منحصر به فرد")

        # بهینه‌سازی تعداد همزمان بر اساس تعداد کانفیگ
        optimal_concurrent = min(max_concurrent, max(5, len(unique_configs) // 10))
        logger.info(f"⚡ تست موازی با {optimal_concurrent} thread")

        # فیلتر جغرافیایی
        if hasattr(self, 'geo_filter_enabled') and self.geo_filter_enabled:
            unique_configs = self.apply_geo_filter(unique_configs)

        semaphore = asyncio.Semaphore(optimal_concurrent)

        async def test_single_config_fast(config_str: str):
            async with semaphore:
                try:
                    config = self.parse_config(config_str)
                    if config:
                        # تست سریع‌تر با timeout کوتاه‌تر
                        is_working, latency = await self.test_config_connectivity_fast(config)
                        config.is_working = is_working
                        config.latency = latency

                        if is_working:
                            self.working_configs.append(config)
                            logger.debug(f"✅ {config.protocol.upper()} {config.address}:{config.port} - {latency:.0f}ms")
                        else:
                            self.failed_configs.append(config)
                except Exception as e:
                    logger.debug(f"❌ خطا در تست کانفیگ: {e}")

        # تقسیم به batch های کوچک‌تر برای مدیریت بهتر
        batch_size = max_concurrent * 2
        batches = [unique_configs[i:i + batch_size]
                   for i in range(0, len(unique_configs), batch_size)]

        total_working = len(self.working_configs)
        total_failed = len(self.failed_configs)

        for batch_idx, batch in enumerate(batches):
            logger.info(
                f"تست batch {batch_idx + 1}/{len(batches)} ({len(batch)} کانفیگ)")

            # اجرای موازی تست‌ها
            tasks = [test_single_config_fast(config) for config in batch]
            await asyncio.gather(*tasks, return_exceptions=True)

            # استراحت کوتاه بین batch ها
            if batch_idx < len(batches) - 1:
                await asyncio.sleep(0.5)

        logger.info(
            f"تست کامل شد: {len(self.working_configs)} کانفیگ سالم، {len(self.failed_configs)} کانفیگ ناسالم")

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
            'ssr': []
        }

        # دسته‌بندی بر اساس پروتکل
        for config in self.working_configs:
            if config.protocol in categories:
                categories[config.protocol].append(config)

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
                    country = config.country or 'unknown'
                    if country not in country_categories:
                        country_categories[country] = []
                    country_categories[country].append(config)

            logger.info(f"دسته‌بندی کشورها: {list(country_categories.keys())}")

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
        
        # تولید گزارش تحلیلی پیشرفته
        if self.analytics:
            try:
                analytics_report = self.analytics.generate_report(self.working_configs, self.failed_configs)
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
            
            logger.info("Analytics report saved to subscriptions/analytics_report.json")
            
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

if __name__ == "__main__":
    asyncio.run(main())
