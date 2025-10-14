#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GeoIP Lookup Module
استخراج کشور از IP یا دامنه
"""

import re
import socket
import logging
from typing import Optional
from functools import lru_cache

logger = logging.getLogger(__name__)


class GeoIPLookup:
    """کلاس برای lookup کشور از IP یا دامنه"""

    def __init__(self):
        # نقشه دامنه‌های ملی به کد کشور
        self.domain_to_country = {
            '.ir': 'IR',  # ایران
            '.us': 'US',  # آمریکا
            '.uk': 'GB',  # انگلیس
            '.de': 'DE',  # آلمان
            '.fr': 'FR',  # فرانسه
            '.ca': 'CA',  # کانادا
            '.jp': 'JP',  # ژاپن
            '.sg': 'SG',  # سنگاپور
            '.nl': 'NL',  # هلند
            '.tr': 'TR',  # ترکیه
            '.ru': 'RU',  # روسیه
            '.cn': 'CN',  # چین
            '.kr': 'KR',  # کره جنوبی
            '.br': 'BR',  # برزیل
            '.au': 'AU',  # استرالیا
            '.in': 'IN',  # هند
            '.es': 'ES',  # اسپانیا
            '.it': 'IT',  # ایتالیا
            '.se': 'SE',  # سوئد
            '.no': 'NO',  # نروژ
            '.fi': 'FI',  # فنلاند
            '.pl': 'PL',  # لهستان
            '.ch': 'CH',  # سوئیس
        }

        # نقشه رنج‌های IP به کشور (ساده‌سازی شده)
        self.ip_ranges = {
            # Cloudflare IPs (معمولاً US)
            '104.': 'US',
            '172.': 'US',
            '198.': 'US',
            '205.': 'US',
            '216.': 'US',
            
            # Digital Ocean (US, NL, SG, DE)
            '159.': 'NL',
            '165.': 'SG',
            '167.': 'US',
            '178.': 'DE',
            '154.': 'US',
            
            # Hetzner (DE)
            '78.': 'DE',
            '88.': 'DE',
            '95.': 'DE',
            
            # OVH (FR, CA)
            '51.': 'FR',
            '54.': 'CA',
            
            # Linode & US ranges
            '45.': 'US',
            '66.': 'US',
            '192.': 'US',
            '193.': 'EU',
            '194.': 'EU',
            '195.': 'EU',
            
            # ایران
            '2.': 'IR',
            '5.': 'IR',
            '31.': 'IR',
            '37.': 'IR',
            '46.': 'IR',
            '79.': 'IR',
            '80.': 'IR',
            '81.': 'IR',
            '82.': 'IR',
            '83.': 'IR',
            '84.': 'IR',
            '85.': 'IR',
            '86.': 'IR',
            '87.': 'IR',
            '89.': 'IR',
            '91.': 'IR',
            '92.': 'IR',
            '93.': 'IR',
            '94.': 'IR',
            '95.': 'IR',
            '151.': 'IR',
            '176.': 'IR',
            '185.': 'IR',
        }

    @lru_cache(maxsize=1000)
    def get_country_from_domain(self, domain: str) -> Optional[str]:
        """استخراج کشور از دامنه"""
        try:
            domain = domain.lower()

            # بررسی TLD های ملی
            for tld, country in self.domain_to_country.items():
                if domain.endswith(tld):
                    return country

            # بررسی الگوهای خاص
            if 'iran' in domain or 'persian' in domain or 'farsi' in domain:
                return 'IR'
            elif 'german' in domain or 'deutschland' in domain:
                return 'DE'
            elif 'french' in domain or 'france' in domain:
                return 'FR'
            elif 'american' in domain or 'usa' in domain:
                return 'US'
            elif 'british' in domain or 'england' in domain:
                return 'GB'
            elif 'canadian' in domain or 'canada' in domain:
                return 'CA'
            elif 'japanese' in domain or 'japan' in domain:
                return 'JP'
            elif 'singapore' in domain:
                return 'SG'
            elif 'dutch' in domain or 'netherlands' in domain:
                return 'NL'
            elif 'turkish' in domain or 'turkey' in domain:
                return 'TR'

        except Exception as e:
            logger.debug(f"خطا در استخراج کشور از دامنه {domain}: {e}")

        return None

    @lru_cache(maxsize=1000)
    def get_country_from_ip(self, ip: str) -> Optional[str]:
        """استخراج کشور از IP با استفاده از رنج‌های ساده"""
        try:
            # بررسی اینکه آیا IP معتبر است
            if not self._is_valid_ip(ip):
                return None

            # بررسی رنج‌های شناخته شده
            for prefix, country in self.ip_ranges.items():
                if ip.startswith(prefix):
                    return country

            # اگر هیچ کدام نبود، Unknown
            return None

        except Exception as e:
            logger.debug(f"خطا در استخراج کشور از IP {ip}: {e}")
            return None

    def _is_valid_ip(self, ip: str) -> bool:
        """بررسی اعتبار IP"""
        try:
            parts = ip.split('.')
            if len(parts) != 4:
                return False
            for part in parts:
                if not 0 <= int(part) <= 255:
                    return False
            return True
        except:
            return False

    def get_country(self, address: str) -> Optional[str]:
        """
        استخراج کشور از آدرس (IP یا دامنه)
        اول دامنه را چک می‌کند، بعد IP
        """
        try:
            # اگر IP است
            if self._is_valid_ip(address):
                return self.get_country_from_ip(address)

            # اگر دامنه است
            return self.get_country_from_domain(address)

        except Exception as e:
            logger.debug(f"خطا در استخراج کشور از {address}: {e}")
            return None


# نمونه استفاده
if __name__ == '__main__':
    geoip = GeoIPLookup()

    # تست IP ها
    test_ips = [
        '104.18.114.228',  # Cloudflare (US)
        '89.44.242.222',   # ایران
        '185.143.233.120',  # ایران
        '45.85.118.234',   # US
    ]

    print('🧪 تست IP ها:')
    for ip in test_ips:
        country = geoip.get_country(ip)
        print(f'  {ip} → {country}')

    # تست دامنه‌ها
    test_domains = [
        'example.ir',
        'google.de',
        'amazon.com',
        'test.sg',
    ]

    print('\n🧪 تست دامنه‌ها:')
    for domain in test_domains:
        country = geoip.get_country(domain)
        print(f'  {domain} → {country}')
