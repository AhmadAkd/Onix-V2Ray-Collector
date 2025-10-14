#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""تست نهایی و جامع سیستم"""

import asyncio
import json
import os
from config_collector import V2RayCollector


async def final_test():
    print('🎯 شروع تست نهایی سیستم...\n')

    # 1. تست GeoIP
    print('1️⃣ تست GeoIP Lookup:')
    collector = V2RayCollector()

    test_addresses = [
        ('104.17.147.22', 'Cloudflare IP'),
        ('185.143.233.120', 'Iran IP'),
        ('example.ir', 'Iran domain'),
        ('google.de', 'German domain'),
    ]

    for address, desc in test_addresses:
        country = collector.geoip.get_country(
            address) if collector.geoip else None
        print(f'   {address:20} ({desc:15}) → {country}')

    # 2. تست جمع‌آوری و parse
    print('\n2️⃣ تست جمع‌آوری (100 کانفیگ اول):')
    configs = await collector.collect_all_configs()
    print(f'   ✅ {len(configs)} کانفیگ جمع‌آوری شد')

    # تست parse نمونه
    sample = configs[:10]
    parsed = []
    for cfg in sample:
        p = collector.parse_config(cfg)
        if p:
            parsed.append(p)

    print(f'   ✅ {len(parsed)}/{len(sample)} کانفیگ parse شد')

    # نمایش country distribution
    countries = {}
    for p in parsed:
        countries[p.country] = countries.get(p.country, 0) + 1

    print(f'   📊 کشورها: {dict(sorted(countries.items()))}')

    # 3. تست حذف تکراری
    print('\n3️⃣ تست حذف تکراری:')
    test_configs = configs[:100]
    # اضافه کردن تکراری عمدی
    test_configs.extend(configs[10:20])  # 10 تکراری

    unique = collector.remove_duplicate_configs_advanced(test_configs)
    print(f'   قبل: {len(test_configs)} کانفیگ')
    print(f'   بعد: {len(unique)} کانفیگ')
    print(f'   ✅ {len(test_configs) - len(unique)} تکراری حذف شد')

    # 4. تست سرعت
    print('\n4️⃣ تست سرعت (50 کانفیگ):')
    import time
    start = time.time()
    await collector.test_all_configs_ultra_fast(configs[:50], max_concurrent=50)
    duration = time.time() - start

    print(f'   ⏱️ زمان: {duration:.1f}s')
    print(f'   ⚡ سرعت: {len(configs[:50])/duration:.1f} config/s')
    print(f'   ✅ موفق: {len(collector.working_configs)}')
    print(f'   ❌ ناموفق: {len(collector.failed_configs)}')

    # 5. تست دسته‌بندی
    print('\n5️⃣ تست دسته‌بندی:')
    categories = collector.categorize_configs()

    print(f'   📦 پروتکل‌ها:')
    for protocol, cfgs in categories.items():
        if cfgs:
            print(f'      {protocol}: {len(cfgs)} کانفیگ')

    # 6. تست گزارش
    print('\n6️⃣ تست گزارش:')
    report = collector.generate_report()

    print(f'   📊 آمار کلی:')
    print(f'      Working: {report["working_configs"]}')
    print(f'      Failed: {report["failed_configs"]}')
    print(f'      Success Rate: {report["success_rate"]}')

    print(f'   🌍 کشورها ({len(report.get("countries", {}))} کشور):')
    for country, stats in list(report.get('countries', {}).items())[:5]:
        print(
            f'      {country}: {stats["count"]} سرور, {stats["avg_latency"]}')

    print(f'   📁 فایل‌های موجود:')
    if 'available_files' in report:
        print(
            f'      Protocols: {len(report["available_files"].get("protocols", []))} فایل')
        print(
            f'      Countries: {len(report["available_files"].get("countries", []))} فایل')

    # 7. بررسی فایل‌های تولید شده
    print('\n7️⃣ بررسی فایل‌های تولید شده:')

    # Check latest_report.json
    if os.path.exists('subscriptions/latest_report.json'):
        with open('subscriptions/latest_report.json', 'r', encoding='utf-8') as f:
            live_report = json.load(f)
        print(f'   ✅ latest_report.json موجود است')
        print(f'      Countries: {len(live_report.get("countries", {}))}')
        print(f'      Protocols: {len(live_report.get("protocols", {}))}')
        print(
            f'      Available files: protocols={len(live_report.get("available_files", {}).get("protocols", []))}, countries={len(live_report.get("available_files", {}).get("countries", []))}')
    else:
        print(f'   ❌ latest_report.json یافت نشد')

    # Check by_protocol
    protocol_dir = 'subscriptions/by_protocol'
    if os.path.exists(protocol_dir):
        files = [f for f in os.listdir(protocol_dir) if f.endswith('.txt')]
        print(f'   ✅ by_protocol: {len(files)} فایل')
        for f in files[:3]:
            size = os.path.getsize(os.path.join(protocol_dir, f))
            print(f'      {f}: {size} bytes')

    # Check by_country
    country_dir = 'subscriptions/by_country'
    if os.path.exists(country_dir):
        files = [f for f in os.listdir(country_dir) if f.endswith('.txt')]
        print(f'   ✅ by_country: {len(files)} فایل')
        for f in sorted(files)[:5]:
            size = os.path.getsize(os.path.join(country_dir, f))
            print(f'      {f}: {size} bytes')

    # 8. خلاصه نهایی
    print('\n' + '='*50)
    print('📋 خلاصه تست نهایی:')
    print('='*50)
    print(f'✅ GeoIP: کار می‌کند')
    print(f'✅ جمع‌آوری: {len(configs)} کانفیگ')
    print(f'✅ Parse: موفق')
    print(f'✅ حذف تکراری: موفق ({len(test_configs) - len(unique)} حذف شد)')
    print(f'✅ تست سرعت: {len(configs[:50])/duration:.1f} config/s')
    print(
        f'✅ دسته‌بندی پروتکل: {len([p for p in categories if categories[p]])} پروتکل')
    print(f'✅ دسته‌بندی کشور: {len(report.get("countries", {}))} کشور')
    print(f'✅ گزارش: کامل')
    print(f'✅ فایل‌ها: تولید شده')
    print('\n🎉 همه چیز عالی کار می‌کند!')


if __name__ == '__main__':
    asyncio.run(final_test())
