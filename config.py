#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V2Ray Config Collector - Configuration File
فایل تنظیمات سیستم جمع‌آوری کانفیگ‌های V2Ray
"""

# تنظیمات عمومی
GENERAL_CONFIG = {
    'log_level': 'INFO',
    'max_retries': 3,
    'request_timeout': 30,
    'cleanup_days': 7,  # حذف فایل‌های قدیمی‌تر از 7 روز
}

# تنظیمات جمع‌آوری
COLLECTION_CONFIG = {
    'max_concurrent_tests': 50,  # حداکثر تست همزمان
    'test_timeout': 10,  # زمان انتظار تست (ثانیه)
    'min_latency_threshold': 5000,  # حداقل تأخیر قابل قبول (میلی‌ثانیه)
    'enable_speed_test': True,  # فعال‌سازی تست سرعت
    'enable_ssl_check': True,  # بررسی گواهی SSL
}

# منابع کانفیگ‌ها - منابع فعال و معتبر (بهینه‌سازی شده)
CONFIG_SOURCES = [
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

    # منابع بیشتر Leon406
    "https://raw.githubusercontent.com/Leon406/SubCrawler/main/sub/share/vmess",
    "https://raw.githubusercontent.com/Leon406/SubCrawler/main/sub/share/trojan",
    "https://raw.githubusercontent.com/Leon406/SubCrawler/main/sub/share/ssr",

    # منابع yebekhe/TelegramV2rayCollector
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/base64/mix",
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/normal/vmess",
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/normal/vless",
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/normal/trojan",
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/normal/ss",

    # منابع barry-far/V2ray-Configs
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub1.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub2.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub3.txt",

    # منابع mfuu/v2ray
    "https://raw.githubusercontent.com/mfuu/v2ray/master/v2ray",

    # منابع ts-sf/fly
    "https://raw.githubusercontent.com/ts-sf/fly/main/v2",

    # منابع ermaozi/get_subscribe
    "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/v2ray.txt",

    # منابع AzadNetCH/Clash
    "https://raw.githubusercontent.com/AzadNetCH/Clash/main/V2Ray.txt",

    # منابع soroushmirzaei/telegram-configs-collector
    "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/vmess",
    "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/vless",
    "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/trojan",
    "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/shadowsocks",

    # منابع MhdiTaheri/V2rayCollector
    "https://raw.githubusercontent.com/MhdiTaheri/V2rayCollector/main/sub/Mix/mix.txt",
    "https://raw.githubusercontent.com/MhdiTaheri/V2rayCollector/main/sub/Mix/base64/mix",

    # منابع sashalsk/V2Ray
    "https://raw.githubusercontent.com/sashalsk/V2Ray/main/V2Config",

    # منابع freefq/free
    "https://raw.githubusercontent.com/freefq/free/master/v2",

    # منابع ripaojiedian/freenode
    "https://raw.githubusercontent.com/ripaojiedian/freenode/main/sub",

    # منابع mianfeifq/share
    "https://raw.githubusercontent.com/mianfeifq/share/main/data2024",

    # منابع اضافی برای SS و SSR
    "https://raw.githubusercontent.com/freefq/free/master/ss",
    "https://raw.githubusercontent.com/freefq/free/master/ssr",
    "https://raw.githubusercontent.com/ripaojiedian/freenode/main/ss",
    "https://raw.githubusercontent.com/ripaojiedian/freenode/main/ssr",
    
    # منابع Hysteria و Hysteria2
    "https://raw.githubusercontent.com/freefq/free/master/hysteria",
    "https://raw.githubusercontent.com/ripaojiedian/freenode/main/hysteria",
    
    # منابع Wireguard و TUIC
    "https://raw.githubusercontent.com/freefq/free/master/wireguard",
    "https://raw.githubusercontent.com/ripaojiedian/freenode/main/tuic",
    
    # منابع جامع
    "https://raw.githubusercontent.com/peasoft/NoMoreWalls/master/list.txt",
    "https://raw.githubusercontent.com/Alvin9999/new-pac/master/ss-sub",
    "https://raw.githubusercontent.com/ripaojiedian/freenode/main/sub",
]

# تنظیمات اتوماسیون
AUTOMATION_CONFIG = {
    'collection_interval_minutes': 30,  # فاصله جمع‌آوری (دقیقه)
    'health_check_interval_minutes': 60,  # فاصله بررسی سلامت (دقیقه)
    'cleanup_hour': 2,  # ساعت تمیزکاری (24 ساعته)
    'weekly_report_day': 'monday',  # روز گزارش هفتگی
    'weekly_report_hour': 8,  # ساعت گزارش هفتگی
}

# تنظیمات سرور وب
WEB_SERVER_CONFIG = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': False,
    'enable_cors': True,
    'max_content_length': 16 * 1024 * 1024,  # 16MB
}

# تنظیمات دسته‌بندی
CATEGORIZATION_CONFIG = {
    'sort_by_latency': True,  # مرتب‌سازی بر اساس تأخیر
    'group_by_protocol': True,  # دسته‌بندی بر اساس پروتکل
    'group_by_country': True,  # دسته‌بندی بر اساس کشور
    'max_configs_per_protocol': 2000,  # حداکثر کانفیگ در هر پروتکل
    'max_configs_per_country': 1000,  # حداکثر کانفیگ در هر کشور
    'min_configs_per_protocol': 10,  # حداقل کانفیگ برای ایجاد فایل
}

# تنظیمات فیلتر جغرافیایی
GEO_FILTER_CONFIG = {
    'enabled': True,  # فعال‌سازی فیلتر جغرافیایی
    'priority_countries': ['US', 'DE', 'NL', 'CA', 'UK'],  # کشورهای اولویت‌دار
    'blocked_countries': ['CN', 'RU'],  # کشورهای مسدود
    'prefer_nearby': True,  # اولویت کشورهای نزدیک به ایران
    'nearby_countries': ['TR', 'AM', 'AZ', 'GE'],  # کشورهای نزدیک
    'min_country_diversity': 3,  # حداقل تنوع کشوری
}

# تنظیمات لاگ‌گیری
LOGGING_CONFIG = {
    'log_file': 'v2ray_collector.log',
    'automation_log_file': 'automation.log',
    'max_log_size_mb': 10,
    'backup_count': 5,
    'log_format': '%(asctime)s - %(levelname)s - %(message)s',
}

# تنظیمات امنیتی
SECURITY_CONFIG = {
    'enable_rate_limiting': True,
    'max_requests_per_minute': 60,
    'blocked_ips': [],  # IP های مسدود شده
    'allowed_user_agents': [
        'Mozilla/5.0',
        'v2rayNG',
        'v2rayN',
        'Fair',
        'Streisand'
    ],
}

# تنظیمات تست کیفیت
QUALITY_TEST_CONFIG = {
    'ping_test_enabled': True,
    'http_test_enabled': True,
    'https_test_enabled': True,
    'dns_test_enabled': False,  # تست DNS (نیاز به تنظیمات اضافی)
    'bandwidth_test_enabled': False,  # تست پهنای باند (نیاز به سرور تست)

    # آستانه‌های کیفیت
    'excellent_latency': 100,  # زیر 100ms عالی
    'good_latency': 300,  # زیر 300ms خوب
    'acceptable_latency': 500,  # زیر 500ms قابل قبول

    'min_uptime_percentage': 95,  # حداقل 95% uptime
}

# تنظیمات پروتکل‌های پشتیبانی شده
SUPPORTED_PROTOCOLS = {
    'vmess': {
        'enabled': True,
        'priority': 1,
        'min_alter_id': 0,
        'max_alter_id': 100,
    },
    'vless': {
        'enabled': True,
        'priority': 2,
        'require_tls': False,
    },
    'trojan': {
        'enabled': True,
        'priority': 3,
        'require_tls': True,
    },
    'shadowsocks': {
        'enabled': True,
        'priority': 4,
        'supported_methods': [
            'aes-256-gcm',
            'aes-128-gcm',
            'chacha20-poly1305',
            'chacha20-ietf-poly1305'
        ],
    },
    'shadowsocksr': {
        'enabled': True,
        'priority': 5,
    },
    'hysteria': {
        'enabled': True,
        'priority': 6,
        'require_tls': True,
    },
    'hysteria2': {
        'enabled': True,
        'priority': 7,
        'require_tls': True,
    },
    'wireguard': {
        'enabled': True,
        'priority': 8,
    },
    'tuic': {
        'enabled': True,
        'priority': 9,
        'require_tls': True,
    },
    'naive': {
        'enabled': True,
        'priority': 10,
    }
}

# تنظیمات تولید فایل‌های اشتراک
SUBSCRIPTION_CONFIG = {
    'generate_base64': True,  # تولید فرمت base64
    'generate_raw': True,  # تولید فرمت خام
    'generate_by_protocol': True,  # تولید فایل‌های جداگانه برای هر پروتکل
    'generate_combined': True,  # تولید فایل ترکیبی
    'max_configs_per_file': 250,  # حداکثر کانفیگ در هر فایل
    'file_naming_pattern': '{protocol}_subscription_{timestamp}.txt',
}

# تنظیمات گزارش‌گیری
REPORTING_CONFIG = {
    'generate_json_report': True,
    'generate_html_report': False,  # گزارش HTML (نیاز به template)
    'include_performance_metrics': True,
    'include_error_analysis': True,
    'include_geographic_distribution': False,  # توزیع جغرافیایی
    'report_retention_days': 30,
}

# تنظیمات API
API_CONFIG = {
    'enable_api': True,
    'api_version': 'v1',
    'rate_limit_per_minute': 100,
    'require_authentication': False,  # احراز هویت API
    'api_key_header': 'X-API-Key',
    'allowed_origins': ['*'],  # CORS origins
}

# تنظیمات پشتیبان‌گیری
BACKUP_CONFIG = {
    'enable_backup': True,
    'backup_interval_hours': 24,
    'backup_retention_days': 7,
    'backup_location': 'backups/',
    'compress_backups': True,
}

# تنظیمات اعلان‌ها
NOTIFICATION_CONFIG = {
    'enable_notifications': False,
    'notification_methods': ['email', 'webhook'],  # email, webhook, telegram
    'email_config': {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'username': '',
        'password': '',
        'to_addresses': [],
    },
    'webhook_config': {
        'url': '',
        'headers': {},
    },
    'alert_conditions': {
        'low_success_rate': 50,  # کمتر از 50% موفقیت
        'high_error_rate': 20,  # بیش از 20% خطا
        'no_working_configs': True,  # عدم وجود کانفیگ سالم
    }
}

# تنظیمات جغرافیایی (اختیاری)
GEO_CONFIG = {
    'enable_geo_detection': False,  # تشخیص موقعیت جغرافیایی
    'geo_api_key': '',  # کلید API برای سرویس جغرافیایی
    'preferred_countries': ['US', 'EU', 'ASIA'],  # کشورهای ترجیحی
    'blocked_countries': [],  # کشورهای مسدود شده
}

# تنظیمات بهینه‌سازی
OPTIMIZATION_CONFIG = {
    'enable_caching': True,
    'cache_ttl_seconds': 300,  # 5 دقیقه
    'enable_compression': True,
    'enable_connection_pooling': True,
    'max_connections': 100,
    'connection_timeout': 10,
}

# تنظیمات پروفایل‌های مختلف
PROFILES = {
    'development': {
        'log_level': 'DEBUG',
        'debug': True,
        'collection_interval_minutes': 5,
        'max_concurrent_tests': 10,
    },
    'production': {
        'log_level': 'INFO',
        'debug': False,
        'collection_interval_minutes': 30,
        'max_concurrent_tests': 50,
    },
    'testing': {
        'log_level': 'WARNING',
        'debug': False,
        'collection_interval_minutes': 60,
        'max_concurrent_tests': 5,
        'test_mode': True,
    }
}

# انتخاب پروفایل فعال
ACTIVE_PROFILE = 'production'  # development, production, testing


def get_config(section_name=None):
    """دریافت تنظیمات"""
    if section_name:
        return globals().get(section_name.upper() + '_CONFIG', {})

    # ترکیب تمام تنظیمات
    all_configs = {}
    for name, value in globals().items():
        if name.endswith('_CONFIG'):
            section = name[:-7].lower()
            all_configs[section] = value

    # اعمال پروفایل فعال
    if ACTIVE_PROFILE in PROFILES:
        profile_config = PROFILES[ACTIVE_PROFILE]
        for section, config in all_configs.items():
            for key, value in profile_config.items():
                if key in config:
                    config[key] = value

    return all_configs


def update_config(section_name, key, value):
    """به‌روزرسانی تنظیمات"""
    config_name = section_name.upper() + '_CONFIG'
    if config_name in globals():
        globals()[config_name][key] = value
        return True
    return False


def get_source_config():
    """دریافت تنظیمات منابع"""
    return CONFIG_SOURCES


def get_protocol_config():
    """دریافت تنظیمات پروتکل‌ها"""
    return SUPPORTED_PROTOCOLS


def get_active_profile():
    """دریافت پروفایل فعال"""
    return ACTIVE_PROFILE


def set_active_profile(profile_name):
    """تغییر پروفایل فعال"""
    global ACTIVE_PROFILE
    if profile_name in PROFILES:
        ACTIVE_PROFILE = profile_name
        return True
    return False


# تنظیمات پیش‌فرض برای تست
if __name__ == "__main__":
    print("📋 تنظیمات سیستم V2Ray Config Collector")
    print("=" * 50)

    configs = get_config()
    for section, config in configs.items():
        print(f"\n🔧 {section.upper()}:")
        for key, value in config.items():
            print(f"  {key}: {value}")

    print(f"\n🎯 پروفایل فعال: {ACTIVE_PROFILE}")
    print(f"📡 تعداد منابع: {len(CONFIG_SOURCES)}")
    print(f"🔌 پروتکل‌های پشتیبانی شده: {len(SUPPORTED_PROTOCOLS)}")
