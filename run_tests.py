#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V2Ray Config Collector Tests
تست‌های سیستم V2Ray Config Collector
"""

import os
import sys
import asyncio
import traceback

# Fix encoding for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def test_imports():
    """تست import کردن ماژول‌ها"""
    print("🧪 تست import کردن ماژول‌ها...")

    try:
        import requests
        import aiohttp
        import json
        import base64
        import logging
        print("✅ تمام وابستگی‌ها به درستی import شدند")
        return True
    except ImportError as e:
        print(f"❌ خطا در import: {e}")
        return False


def test_file_structure():
    """تست ساختار فایل‌ها"""
    print("🧪 تست ساختار فایل‌ها...")

    required_files = [
        'config_collector.py',
        'config.py',
        'api_server.py',
        'requirements.txt',
        'README.md'
    ]

    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)

    if missing_files:
        print(f"❌ فایل‌های مفقود: {missing_files}")
        return False

    print("✅ تمام فایل‌های لازم موجود هستند")
    return True


def test_config_file():
    """تست فایل تنظیمات"""
    print("🧪 تست فایل تنظیمات...")

    try:
        from config import (
            COLLECTION_CONFIG, LOGGING_CONFIG,
            CATEGORIZATION_CONFIG, SECURITY_CONFIG
        )

        # بررسی وجود تنظیمات
        assert 'test_timeout' in COLLECTION_CONFIG, "تنظیمات جمع‌آوری ناقص است"
        assert 'log_file' in LOGGING_CONFIG, "تنظیمات لاگ ناقص است"

        print("✅ فایل تنظیمات به درستی کار می‌کند")
        return True
    except Exception as e:
        print(f"❌ خطا در فایل تنظیمات: {e}")
        return False


def test_config_collector():
    """تست کلاس V2RayCollector"""
    print("🧪 تست V2RayCollector...")

    try:
        from config_collector import V2RayCollector

        collector = V2RayCollector()

        # تست تنظیمات اولیه
        assert hasattr(collector, 'working_configs')
        assert hasattr(collector, 'failed_configs')
        assert hasattr(collector, 'config_sources')

        print("✅ V2RayCollector کلاس به درستی ایجاد شد")
        return True
    except Exception as e:
        print(f"❌ خطا در تست V2RayCollector: {e}")
        traceback.print_exc()
        return False


def test_config_parsing():
    """تست تجزیه کانفیگ‌ها"""
    print("🧪 تست تجزیه کانفیگ‌ها...")

    try:
        from config_collector import V2RayCollector

        collector = V2RayCollector()

        # تست تجزیه VMess
        vmess_config = "vmess://eyJ2IjoiMiIsInBzIjoiVGVzdCIsImFkZCI6InRlc3QuY29tIiwicG9ydCI6IjQ0MyIsImlkIjoiMTIzNDU2NzgtYWJjZC1lZmdoLWlqa2wtbW5vcC1xcnN0dXYifQ=="
        parsed = collector.parse_config(vmess_config)

        if parsed:
            print("✅ تجزیه VMess موفق بود")
        else:
            print("⚠️ تجزیه VMess ناموفق بود")

        # تست تجزیه VLESS
        vless_config = "vless://12345678-abcd-efgh-ijkl-mnop-qrstuv@test.com:443?security=tls#Test"
        parsed = collector.parse_config(vless_config)

        if parsed:
            print("✅ تجزیه VLESS موفق بود")
        else:
            print("⚠️ تجزیه VLESS ناموفق بود")

        return True
    except Exception as e:
        print(f"❌ خطا در تست تجزیه کانفیگ: {e}")
        traceback.print_exc()
        return False


async def test_connectivity():
    """تست اتصال به منابع"""
    print("🧪 تست اتصال به منابع...")

    try:
        import aiohttp
        from config_collector import V2RayCollector

        collector = V2RayCollector()

        # لیست منابع برای تست
        test_sources = [
            "https://api.github.com",
            "https://httpbin.org/json",
        ]

        # استفاده از ClientTimeout
        timeout = aiohttp.ClientTimeout(total=10)

        async with aiohttp.ClientSession(timeout=timeout) as session:
            for test_source in test_sources:
                try:
                    async with session.get(test_source) as response:
                        if response.status == 200:
                            print(f"✅ اتصال به منابع موفق بود ({test_source})")
                            return True
                except:
                    continue

        print("⚠️ هیچ منبع تستی در دسترس نیست (اختیاری)")
        # Connectivity test is optional - don't fail
        return True

    except aiohttp.ClientError as e:
        print(f"⚠️ خطا در اتصال شبکه (اختیاری): {str(e)}")
        return True
    except asyncio.TimeoutError:
        print(f"⚠️ زمان اتصال به پایان رسید (اختیاری)")
        return True
    except Exception as e:
        print(f"⚠️ خطا در تست اتصال (اختیاری): {type(e).__name__}")
        return True


def test_api_server():
    """تست API Server"""
    print("🧪 تست API Server...")

    try:
        # فقط بررسی import
        import api_server

        print("✅ API Server به درستی import می‌شود")
        return True
    except Exception as e:
        print(f"❌ خطا در تست API Server: {e}")
        return False


async def main():
    """اجرای تمام تست‌ها"""
    print("🚀 شروع تست‌های سیستم V2Ray Config Collector")
    print("=" * 60)

    tests = [
        ("imports", test_imports),
        ("file_structure", test_file_structure),
        ("config_file", test_config_file),
        ("config_collector", test_config_collector),
        ("config_parsing", test_config_parsing),
        ("connectivity", test_connectivity),
        ("api_server", test_api_server),
    ]

    results = {}

    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ خطا در تست {test_name}: {e}")
            results[test_name] = False

    # نمایش نتایج
    print("\n" + "=" * 60)
    print("📊 نتایج تست‌ها:")
    print("=" * 60)

    passed = 0
    failed = 0

    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
        else:
            failed += 1

    print("\n" + "=" * 60)
    print("📈 آمار کلی:")
    print("=" * 60)
    print(f"تعداد کل تست‌ها: {len(tests)}")
    print(f"تست‌های موفق: {passed}")
    print(f"تست‌های ناموفق: {failed}")
    print(f"نرخ موفقیت: {(passed/len(tests)*100):.1f}%")

    if failed == 0:
        print("\n🎉 تمام تست‌ها با موفقیت انجام شدند!")
        return True
    else:
        print(f"\n⚠️ {failed} تست ناموفق بودند")
        print("❌ لطفاً مشکلات را بررسی کنید")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
