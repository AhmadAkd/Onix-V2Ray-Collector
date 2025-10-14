#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Security Validator
اعتبارسنجی و امنیت برای ورودی‌ها
"""

import re
import logging
from typing import Optional
from urllib.parse import urlparse
import hashlib

logger = logging.getLogger(__name__)

class SecurityValidator:
    """اعتبارسنجی امنیتی"""
    
    # Allowed protocols
    ALLOWED_PROTOCOLS = ['vmess', 'vless', 'trojan', 'ss', 'ssr', 'hysteria', 'hysteria2', 'tuic', 'wireguard']
    
    # Max lengths
    MAX_CONFIG_LENGTH = 10000
    MAX_URL_LENGTH = 2048
    MAX_TAG_LENGTH = 200
    
    # Patterns
    DOMAIN_PATTERN = re.compile(r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$')
    IP_PATTERN = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
    UUID_PATTERN = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.blocked_ips = set()
        self.blocked_domains = set()
    
    def validate_config_string(self, config: str) -> bool:
        """
        اعتبارسنجی رشته کانفیگ
        
        Args:
            config: رشته کانفیگ
            
        Returns:
            True اگر معتبر باشد
        """
        if not config or not isinstance(config, str):
            return False
        
        # Check length
        if len(config) > self.MAX_CONFIG_LENGTH:
            self.logger.warning(f"⚠️ Config too long: {len(config)} chars")
            return False
        
        # Check for malicious patterns
        malicious_patterns = [
            '<script', 'javascript:', 'data:', 'vbscript:',
            '../', '..\\', 'file://', 'ftp://'
        ]
        
        config_lower = config.lower()
        for pattern in malicious_patterns:
            if pattern in config_lower:
                self.logger.warning(f"⚠️ Malicious pattern detected: {pattern}")
                return False
        
        return True
    
    def validate_url(self, url: str) -> bool:
        """
        اعتبارسنجی URL
        
        Args:
            url: آدرس URL
            
        Returns:
            True اگر معتبر باشد
        """
        if not url or len(url) > self.MAX_URL_LENGTH:
            return False
        
        try:
            parsed = urlparse(url)
            
            # Check scheme
            if parsed.scheme not in ['http', 'https']:
                return False
            
            # Check netloc
            if not parsed.netloc:
                return False
            
            return True
        except:
            return False
    
    def validate_domain(self, domain: str) -> bool:
        """اعتبارسنجی domain"""
        if not domain or len(domain) > 255:
            return False
        return bool(self.DOMAIN_PATTERN.match(domain))
    
    def validate_ip(self, ip: str) -> bool:
        """اعتبارسنجی IP"""
        if not ip:
            return False
        
        if not self.IP_PATTERN.match(ip):
            return False
        
        # Check if IP is in valid range
        parts = ip.split('.')
        for part in parts:
            if int(part) > 255:
                return False
        
        # Block private IPs
        if ip.startswith('127.') or ip.startswith('0.') or ip.startswith('192.168.') or ip.startswith('10.'):
            self.logger.warning(f"⚠️ Private IP blocked: {ip}")
            return False
        
        return True
    
    def validate_port(self, port: int) -> bool:
        """اعتبارسنجی port"""
        return isinstance(port, int) and 1 <= port <= 65535
    
    def validate_uuid(self, uuid: str) -> bool:
        """اعتبارسنجی UUID"""
        if not uuid:
            return False
        return bool(self.UUID_PATTERN.match(uuid))
    
    def sanitize_tag(self, tag: str) -> str:
        """پاکسازی tag از کاراکترهای خطرناک"""
        if not tag:
            return ""
        
        # Remove HTML tags
        tag = re.sub(r'<[^>]+>', '', tag)
        
        # Remove special chars
        tag = re.sub(r'[<>"\'/\\]', '', tag)
        
        # Limit length
        if len(tag) > self.MAX_TAG_LENGTH:
            tag = tag[:self.MAX_TAG_LENGTH]
        
        return tag.strip()
    
    def generate_config_hash(self, config: str) -> str:
        """ایجاد hash برای کانفیگ (برای deduplication)"""
        return hashlib.sha256(config.encode()).hexdigest()
    
    def is_rate_limited(self, identifier: str, max_requests: int = 100, window: int = 3600) -> bool:
        """
        بررسی Rate Limiting (placeholder)
        
        Args:
            identifier: شناسه (IP, User, etc)
            max_requests: حداکثر درخواست
            window: بازه زمانی (ثانیه)
            
        Returns:
            True اگر محدود شده باشد
        """
        # TODO: Implement with Redis or memory cache
        return False

class InputSanitizer:
    """پاکسازی ورودی‌ها"""
    
    @staticmethod
    def sanitize_html(text: str) -> str:
        """حذف HTML tags"""
        return re.sub(r'<[^>]+>', '', text)
    
    @staticmethod
    def sanitize_sql(text: str) -> str:
        """جلوگیری از SQL Injection"""
        dangerous = ["'", '"', ';', '--', '/*', '*/', 'xp_', 'sp_']
        for char in dangerous:
            text = text.replace(char, '')
        return text
    
    @staticmethod
    def escape_special_chars(text: str) -> str:
        """Escape کردن کاراکترهای خاص"""
        replacements = {
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#x27;',
            '/': '&#x2F;'
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    validator = SecurityValidator()
    
    # Tests
    print("✅ URL valid:", validator.validate_url("https://example.com/config"))
    print("✅ Domain valid:", validator.validate_domain("example.com"))
    print("✅ IP valid:", validator.validate_ip("1.1.1.1"))
    print("✅ Port valid:", validator.validate_port(443))
    print("✅ UUID valid:", validator.validate_uuid("12345678-1234-1234-1234-123456789012"))

