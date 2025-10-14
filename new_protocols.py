#!/usr/bin/env python3
"""
New Protocol Support for V2Ray Collector
پشتیبانی از پروتکل‌های جدید
"""

import re
import base64
import json
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class NewProtocolConfig:
    """کانفیگ پروتکل جدید"""
    protocol: str
    address: str
    port: int
    uuid: str
    raw_config: str
    additional_params: Dict[str, Any] = None


class NewProtocolParser:
    """پارسکننده پروتکل‌های جدید"""

    def __init__(self):
        self.protocol_patterns = {
            # Reality Protocol
            'reality': r'reality://([^#]+)(#.*)?',

            # Tuic Protocol v5
            'tuic5': r'tuic5://([^#]+)(#.*)?',

            # Naive Protocol
            'naive': r'naive://([^#]+)(#.*)?',

            # Hysteria v3
            'hysteria3': r'hysteria3://([^#]+)(#.*)?',

            # VMess over WebSocket
            'vmess-ws': r'vmess-ws://([^#]+)(#.*)?',

            # VLESS over WebSocket
            'vless-ws': r'vless-ws://([^#]+)(#.*)?',

            # Trojan over WebSocket
            'trojan-ws': r'trojan-ws://([^#]+)(#.*)?',

            # Xray Reality
            'xray-reality': r'xray-reality://([^#]+)(#.*)?',

            # SingBox Universal
            'sing-box': r'sing-box://([^#]+)(#.*)?',

            # Clash Meta
            'clash-meta': r'clash-meta://([^#]+)(#.*)?',
        }

    def parse_reality_config(self, config_str: str) -> Optional[NewProtocolConfig]:
        """تجزیه کانفیگ Reality"""
        try:
            if not config_str.startswith('reality://'):
                return None

            # حذف پروتکل prefix
            encoded = config_str[9:]

            # حذف fragment
            if '#' in encoded:
                encoded = encoded.split('#')[0]

            # decode Base64
            decoded = base64.b64decode(encoded + '==').decode('utf-8')

            # تجزیه پارامترها
            params = self._parse_url_params(decoded)

            return NewProtocolConfig(
                protocol='reality',
                address=params.get('server', ''),
                port=int(params.get('port', 443)),
                uuid=params.get('uuid', ''),
                raw_config=config_str,
                additional_params=params
            )

        except Exception as e:
            logger.debug(f"خطا در تجزیه Reality: {e}")
            return None

    def parse_tuic5_config(self, config_str: str) -> Optional[NewProtocolConfig]:
        """تجزیه کانفیگ Tuic v5"""
        try:
            if not config_str.startswith('tuic5://'):
                return None

            # حذف پروتکل prefix
            encoded = config_str[8:]

            # حذف fragment
            if '#' in encoded:
                encoded = encoded.split('#')[0]

            # decode Base64
            decoded = base64.b64decode(encoded + '==').decode('utf-8')

            # تجزیه پارامترها
            params = self._parse_url_params(decoded)

            return NewProtocolConfig(
                protocol='tuic5',
                address=params.get('server', ''),
                port=int(params.get('port', 443)),
                uuid=params.get('uuid', ''),
                raw_config=config_str,
                additional_params=params
            )

        except Exception as e:
            logger.debug(f"خطا در تجزیه Tuic v5: {e}")
            return None

    def parse_naive_config(self, config_str: str) -> Optional[NewProtocolConfig]:
        """تجزیه کانفیگ Naive"""
        try:
            if not config_str.startswith('naive://'):
                return None

            # حذف پروتکل prefix
            encoded = config_str[8:]

            # حذف fragment
            if '#' in encoded:
                encoded = encoded.split('#')[0]

            # decode Base64
            decoded = base64.b64decode(encoded + '==').decode('utf-8')

            # تجزیه پارامترها
            params = self._parse_url_params(decoded)

            return NewProtocolConfig(
                protocol='naive',
                address=params.get('server', ''),
                port=int(params.get('port', 443)),
                uuid=params.get('username', ''),
                raw_config=config_str,
                additional_params=params
            )

        except Exception as e:
            logger.debug(f"خطا در تجزیه Naive: {e}")
            return None

    def parse_hysteria3_config(self, config_str: str) -> Optional[NewProtocolConfig]:
        """تجزیه کانفیگ Hysteria v3"""
        try:
            if not config_str.startswith('hysteria3://'):
                return None

            # حذف پروتکل prefix
            encoded = config_str[12:]

            # حذف fragment
            if '#' in encoded:
                encoded = encoded.split('#')[0]

            # decode Base64
            decoded = base64.b64decode(encoded + '==').decode('utf-8')

            # تجزیه پارامترها
            params = self._parse_url_params(decoded)

            return NewProtocolConfig(
                protocol='hysteria3',
                address=params.get('server', ''),
                port=int(params.get('port', 443)),
                uuid=params.get('auth', ''),
                raw_config=config_str,
                additional_params=params
            )

        except Exception as e:
            logger.debug(f"خطا در تجزیه Hysteria v3: {e}")
            return None

    def parse_singbox_config(self, config_str: str) -> Optional[NewProtocolConfig]:
        """تجزیه کانفیگ SingBox Universal"""
        try:
            if not config_str.startswith('sing-box://'):
                return None

            # حذف پروتکل prefix
            encoded = config_str[11:]

            # حذف fragment
            if '#' in encoded:
                encoded = encoded.split('#')[0]

            # decode Base64
            decoded = base64.b64decode(encoded + '==').decode('utf-8')

            # تجزیه JSON
            config_data = json.loads(decoded)

            # استخراج اطلاعات اصلی
            server = config_data.get('server', '')
            port = config_data.get('server_port', 443)
            uuid = config_data.get('uuid', '')
            protocol = config_data.get('type', 'unknown')

            return NewProtocolConfig(
                protocol=f'singbox-{protocol}',
                address=server,
                port=port,
                uuid=uuid,
                raw_config=config_str,
                additional_params=config_data
            )

        except Exception as e:
            logger.debug(f"خطا در تجزیه SingBox: {e}")
            return None

    def _parse_url_params(self, url: str) -> Dict[str, str]:
        """تجزیه پارامترهای URL"""
        params = {}

        if '?' in url:
            base_url, query = url.split('?', 1)
            for param in query.split('&'):
                if '=' in param:
                    key, value = param.split('=', 1)
                    params[key] = value

        # استخراج server و port از base URL
        if '://' in url:
            protocol, rest = url.split('://', 1)
            if '@' in rest:
                auth, server_port = rest.split('@', 1)
                if ':' in server_port:
                    server, port = server_port.split(':', 1)
                    params['server'] = server
                    params['port'] = port
                    params['auth'] = auth

        return params

    def parse_config(self, config_str: str) -> Optional[NewProtocolConfig]:
        """تجزیه کانفیگ بر اساس پروتکل"""

        # بررسی هر پروتکل
        for protocol, pattern in self.protocol_patterns.items():
            if re.match(pattern, config_str):
                if protocol == 'reality':
                    return self.parse_reality_config(config_str)
                elif protocol == 'tuic5':
                    return self.parse_tuic5_config(config_str)
                elif protocol == 'naive':
                    return self.parse_naive_config(config_str)
                elif protocol == 'hysteria3':
                    return self.parse_hysteria3_config(config_str)
                elif protocol == 'sing-box':
                    return self.parse_singbox_config(config_str)

        return None

    def get_supported_protocols(self) -> list:
        """لیست پروتکل‌های پشتیبانی شده"""
        return list(self.protocol_patterns.keys())

# مثال استفاده


def main():
    parser = NewProtocolParser()

    # تست کانفیگ‌های مختلف
    test_configs = [
        'reality://eyJhZGQiOiIxMjcuMC4wLjEiLCJhaWQiOjAsImhvc3QiOiIiLCJpZCI6IjQ5YjQ2YjY0LTY1YjctNDQ2Yy04YjY0LTY1YjY0NjU2NDY1NjQiLCJuZXQiOiJ0Y3AiLCJwYXRoIjoiLyIsInBvcnQiOjgwLCJwcyI6IlJlYWxpdHkgVGVzdCIsInNjeSI6ImF1dG8iLCJzbmkiOiIiLCJ0bHMiOiIiLCJ0eXBlIjoiaHR0cCJ9',
        'tuic5://eyJhZGQiOiIxMjcuMC4wLjEiLCJhaWQiOjAsImhvc3QiOiIiLCJpZCI6IjQ5YjQ2YjY0LTY1YjctNDQ2Yy04YjY0LTY1YjY0NjU2NDY1NjQiLCJuZXQiOiJ0Y3AiLCJwYXRoIjoiLyIsInBvcnQiOjgwLCJwcyI6IlR1aWMgVGVzdCIsInNjeSI6ImF1dG8iLCJzbmkiOiIiLCJ0bHMiOiIiLCJ0eXBlIjoiaHR0cCJ9',
        'naive://dXNlcm5hbWU6cGFzc3dvcmRAc2VydmVyLmNvbTo0NDM=',
    ]

    for config in test_configs:
        result = parser.parse_config(config)
        if result:
            print(f"✅ {result.protocol}: {result.address}:{result.port}")
        else:
            print(f"❌ Failed to parse: {config[:50]}...")


if __name__ == "__main__":
    main()
