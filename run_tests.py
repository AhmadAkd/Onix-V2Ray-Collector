#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V2Ray Config Collector - Test Runner
اجرای تست‌های سیستم جمع‌آوری کانفیگ‌های V2Ray
"""

import sys
import os
import asyncio
import time
import json
from datetime import datetime

def test_imports():
    """تست import کردن ماژول‌ها"""
    print("🧪 تست import کردن ماژول‌ها...")
    
    try:
        import requests
        import aiohttp
        import flask
        import schedule
        import yaml
        print("✅ تمام وابستگی‌ها به درستی import شدند")
        return True
    except ImportError as e:
        print(f"❌ خطا در import: {e}")
        return False

def test_config_collector():
    """تست کلاس V2RayCollector"""
    print("🧪 تست V2RayCollector...")
    
    try:
        from config_collector import V2RayCollector
        
        collector = V2RayCollector()
        
        # تست تنظیمات اولیه
        assert hasattr(collector, 'configs')
        assert hasattr(collector, 'working_configs')
        assert hasattr(collector, 'failed_configs')
        assert hasattr(collector, 'config_sources')
        
        print("✅ V2RayCollector کلاس به درستی ایجاد شد")
        return True
    except Exception as e:
        print(f"❌ خطا در تست V2RayCollector: {e}")
        return False

def test_config_parsing():
    """تست تجزیه کانفیگ‌ها"""
    print("🧪 تست تجزیه کانفیگ‌ها...")
    
    try:
        from config_collector import V2RayCollector
        
        collector = V2RayCollector()
        
        # تست کانفیگ VMess نمونه
        vmess_config = "vmess://eyJ2IjoiMiIsInBzIjoiVGVzdCIsImFkZCI6InRlc3QuY29tIiwicG9ydCI6IjQ0MyIsImlkIjoiMTIzNDU2Nzg5MCIsImFpZCI6IjAiLCJzY3kiOiJhdXRvIiwibmV0Ijoid3MiLCJ0eXBlIjoibm9uZSIsImhvc3QiOiIiLCJwYXRoIjoiL3dzIiwidGxzIjoidGxzIn0="
        
        parsed = collector.parse_config(vmess_config)
        assert parsed is not None
        assert parsed.protocol == "vmess"
        
        print("✅ تجزیه کانفیگ VMess موفق بود")
        return True
    except Exception as e:
        print(f"❌ خطا در تست تجزیه کانفیگ: {e}")
        return False

async def test_connectivity():
    """تست اتصال به منابع"""
    print("🧪 تست اتصال به منابع...")
    
    try:
        import aiohttp
        from config_collector import V2RayCollector
        
        collector = V2RayCollector()
        
        # تست اتصال به یک منبع
        test_source = "https://httpbin.org/json"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(test_source, timeout=10) as response:
                if response.status == 200:
                    print("✅ اتصال به منابع موفق بود")
                    return True
        
        print("❌ خطا در اتصال به منابع")
        return False
    except Exception as e:
        print(f"❌ خطا در تست اتصال: {e}")
        return False

def test_automation():
    """تست سیستم اتوماسیون"""
    print("🧪 تست سیستم اتوماسیون...")
    
    try:
        from automation import AutomationManager
        
        automation = AutomationManager()
        
        # تست تنظیمات اولیه
        assert hasattr(automation, 'collector')
        assert hasattr(automation, 'stats')
        
        print("✅ سیستم اتوماسیون به درستی ایجاد شد")
        return True
    except Exception as e:
        print(f"❌ خطا در تست اتوماسیون: {e}")
        return False

def test_web_server():
    """تست سرور وب"""
    print("🧪 تست سرور وب...")
    
    try:
        from web_server import V2RayWebServer
        
        web_server = V2RayWebServer()
        
        # تست تنظیمات اولیه
        assert hasattr(web_server, 'subscriptions_dir')
        
        # تست دریافت آمار
        stats = web_server.get_stats()
        assert isinstance(stats, dict)
        
        print("✅ سرور وب به درستی ایجاد شد")
        return True
    except Exception as e:
        print(f"❌ خطا در تست سرور وب: {e}")
        return False

def test_config_file():
    """تست فایل تنظیمات"""
    print("🧪 تست فایل تنظیمات...")
    
    try:
        from config import get_config, get_source_config, get_protocol_config
        
        # تست دریافت تنظیمات
        configs = get_config()
        assert isinstance(configs, dict)
        
        sources = get_source_config()
        assert isinstance(sources, list)
        assert len(sources) > 0
        
        protocols = get_protocol_config()
        assert isinstance(protocols, dict)
        assert len(protocols) > 0
        
        print("✅ فایل تنظیمات به درستی کار می‌کند")
        return True
    except Exception as e:
        print(f"❌ خطا در تست تنظیمات: {e}")
        return False

def test_file_structure():
    """تست ساختار فایل‌ها"""
    print("🧪 تست ساختار فایل‌ها...")
    
    required_files = [
        'config_collector.py',
        'automation.py',
        'web_server.py',
        'config.py',
        'start.py',
        'requirements.txt',
        'README.md',
        'README_EN.md',
        'LICENSE',
        '.gitignore'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ فایل‌های مفقود: {missing_files}")
        return False
    
    print("✅ تمام فایل‌های ضروری موجود هستند")
    return True

def create_test_report(results):
    """ایجاد گزارش تست"""
    report = {
        'timestamp': datetime.now().isoformat(),
        'total_tests': len(results),
        'passed_tests': sum(results.values()),
        'failed_tests': len(results) - sum(results.values()),
        'success_rate': f"{(sum(results.values()) / len(results)) * 100:.1f}%",
        'test_results': results
    }
    
    with open('test_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    return report

async def main():
    """تابع اصلی تست"""
    print("🚀 شروع تست‌های سیستم V2Ray Config Collector")
    print("=" * 60)
    
    results = {}
    
    # اجرای تست‌ها
    results['imports'] = test_imports()
    results['file_structure'] = test_file_structure()
    results['config_file'] = test_config_file()
    results['config_collector'] = test_config_collector()
    results['config_parsing'] = test_config_parsing()
    results['connectivity'] = await test_connectivity()
    results['automation'] = test_automation()
    results['web_server'] = test_web_server()
    
    # نمایش نتایج
    print("\n" + "=" * 60)
    print("📊 نتایج تست‌ها:")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    # ایجاد گزارش
    report = create_test_report(results)
    
    print(f"\n📈 آمار کلی:")
    print(f"تعداد کل تست‌ها: {report['total_tests']}")
    print(f"تست‌های موفق: {report['passed_tests']}")
    print(f"تست‌های ناموفق: {report['failed_tests']}")
    print(f"نرخ موفقیت: {report['success_rate']}")
    
    # نتیجه نهایی
    if all(results.values()):
        print("\n🎉 تمام تست‌ها با موفقیت انجام شد!")
        print("✅ سیستم آماده استفاده است")
        return True
    else:
        print("\n⚠️ برخی تست‌ها ناموفق بودند")
        print("❌ لطفاً مشکلات را بررسی کنید")
        return False

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️ تست‌ها متوقف شد")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ خطای کلی در تست‌ها: {e}")
        sys.exit(1)
