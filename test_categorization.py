#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""تست دسته‌بندی و گزارش‌گیری"""

import asyncio
import json
from config_collector import V2RayCollector


async def main():
    print('🔍 شروع تست...')
    collector = V2RayCollector()

    # جمع‌آوری تعداد کمی از کانفیگ‌ها
    print('📥 جمع‌آوری کانفیگ‌ها...')
    configs = await collector.collect_all_configs()
    print(f'✅ {len(configs)} کانفیگ جمع‌آوری شد')

    # فقط 50 تا اول را تست کنیم
    test_configs = configs[:50] if len(configs) > 50 else configs

    # تست
    print(f'🧪 تست {len(test_configs)} کانفیگ...')
    await collector.test_all_configs_ultra_fast(test_configs, max_concurrent=20)
    print(f'✅ {len(collector.working_configs)} کانفیگ سالم')

    # نمایش نمونه‌ای از کانفیگ‌های سالم
    print('\n📊 نمونه کانفیگ‌های سالم:')
    for i, cfg in enumerate(collector.working_configs[:5]):
        print(
            f'  {i+1}. Protocol: {cfg.protocol}, Country: {cfg.country}, Address: {cfg.address}')

    # دسته‌بندی
    print('\n🗂️ دسته‌بندی...')
    categories = collector.categorize_configs()

    print(f'\n📦 دسته‌بندی پروتکل:')
    for protocol, configs_list in categories.items():
        if configs_list:
            print(f'  {protocol}: {len(configs_list)} کانفیگ')

    # گزارش
    print('\n📝 تولید گزارش...')
    report = collector.generate_report()

    print(f'\n🌍 کشورها در گزارش:')
    if 'countries' in report and report['countries']:
        for country, stats in list(report['countries'].items())[:10]:
            print(
                f'  {country}: {stats["count"]} سرور, {stats["avg_latency"]}')
    else:
        print('  ❌ هیچ کشوری یافت نشد!')

    print(f'\n📁 فایل‌های موجود:')
    if 'available_files' in report:
        print(f'  Protocols: {report["available_files"].get("protocols", [])}')
        print(f'  Countries: {report["available_files"].get("countries", [])}')
    else:
        print('  ❌ available_files موجود نیست!')

    # ذخیره گزارش
    with open('test_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print('\n✅ گزارش در test_report.json ذخیره شد')


if __name__ == '__main__':
    asyncio.run(main())
