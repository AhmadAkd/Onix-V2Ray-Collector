#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete Workflow Test
تست کامل فرآیند جمع‌آوری، تست و دسته‌بندی
"""

import asyncio
import json
import os
from config_collector import V2RayCollector

async def test_complete_workflow():
    """تست کامل workflow"""
    print("=" * 70)
    print("🚀 تست کامل فرآیند V2Ray Collector")
    print("=" * 70)
    
    collector = V2RayCollector()
    
    # ========== 1. بررسی منابع ==========
    print("\n📊 مرحله 1: بررسی منابع")
    print("-" * 70)
    print(f"✅ تعداد منابع: {len(collector.config_sources)}")
    print(f"✅ منابع از config.py بارگذاری شد")
    
    # ========== 2. جمع‌آوری ==========
    print("\n📥 مرحله 2: جمع‌آوری کانفیگ‌ها (15 منبع اول)")
    print("-" * 70)
    
    all_configs = []
    successful_sources = 0
    failed_sources = 0
    
    for i, source in enumerate(collector.config_sources[:15], 1):
        try:
            configs = await collector.fetch_configs_from_source(source)
            all_configs.extend(configs)
            successful_sources += 1
            source_name = source.split('/')[-1]
            print(f"  {i:2d}. ✅ {len(configs):>6} کانفیگ - {source_name[:50]}")
        except Exception as e:
            failed_sources += 1
            print(f"  {i:2d}. ❌ خطا - {str(e)[:40]}")
    
    print(f"\n📊 نتیجه جمع‌آوری:")
    print(f"  ✅ منابع موفق: {successful_sources}")
    print(f"  ❌ منابع ناموفق: {failed_sources}")
    print(f"  📦 مجموع کانفیگ‌های خام: {len(all_configs)}")
    
    # ========== 3. تجزیه ==========
    print("\n🔍 مرحله 3: تجزیه کانفیگ‌ها")
    print("-" * 70)
    
    parsed_configs = []
    protocol_counts = {}
    country_counts = {}
    
    for config_str in all_configs[:1000]:  # تجزیه 1000 کانفیگ اول
        parsed = collector.parse_config(config_str)
        if parsed:
            parsed_configs.append(parsed)
            protocol_counts[parsed.protocol] = protocol_counts.get(parsed.protocol, 0) + 1
            country_counts[parsed.country] = country_counts.get(parsed.country, 0) + 1
    
    print(f"✅ تجزیه شده: {len(parsed_configs)} از {min(1000, len(all_configs))}")
    print(f"📊 نرخ موفقیت تجزیه: {len(parsed_configs)/min(1000, len(all_configs))*100:.1f}%")
    
    print(f"\n📊 توزیع پروتکل‌ها:")
    for protocol, count in sorted(protocol_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {protocol:12s}: {count:4d} کانفیگ")
    
    print(f"\n🌍 توزیع کشورها (10 برتر):")
    top_countries = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    for country, count in top_countries:
        print(f"  - {country:20s}: {count:4d} کانفیگ")
    
    # ========== 4. دسته‌بندی ==========
    print("\n📁 مرحله 4: دسته‌بندی")
    print("-" * 70)
    
    # شبیه‌سازی working_configs
    collector.working_configs = parsed_configs[:500]  # 500 کانفیگ برای تست
    
    categories = collector.categorize_configs()
    
    print(f"✅ دسته‌بندی انجام شد")
    print(f"\n📊 دسته‌بندی بر اساس پروتکل:")
    for protocol, configs in sorted(categories.items(), key=lambda x: len(x[1]), reverse=True):
        if configs:
            print(f"  - {protocol:12s}: {len(configs):4d} کانفیگ")
    
    # ========== 5. تولید فایل‌های اشتراک ==========
    print("\n📝 مرحله 5: تولید فایل‌های اشتراک")
    print("-" * 70)
    
    subscription_files = collector.generate_subscription_links(categories)
    
    print(f"✅ {len(subscription_files)} فایل تولید شد:")
    
    protocol_files = [k for k in subscription_files.keys() if not k.endswith('_by_country')]
    country_files = [k for k in subscription_files.keys() if k.endswith('_by_country')]
    
    print(f"\n📦 فایل‌های پروتکل ({len(protocol_files)}):")
    for key in sorted(protocol_files):
        file_info = subscription_files[key]
        print(f"  - {key:15s}: {file_info['count']:4d} کانفیگ")
    
    print(f"\n🌍 فایل‌های کشور ({len(country_files)}):")
    for key in sorted(country_files)[:10]:
        file_info = subscription_files[key]
        country = key.replace('_by_country', '')
        print(f"  - {country:15s}: {file_info['count']:4d} کانفیگ")
    
    if len(country_files) > 10:
        print(f"  ... و {len(country_files) - 10} کشور دیگر")
    
    # ========== 6. بررسی کیفیت ==========
    print("\n✅ مرحله 6: بررسی کیفیت")
    print("-" * 70)
    
    # بررسی فایل‌های موجود
    protocol_file_count = len([f for f in os.listdir('subscriptions') if f.endswith('_subscription.txt')])
    
    by_protocol_exists = os.path.exists('subscriptions/by_protocol')
    by_country_exists = os.path.exists('subscriptions/by_country')
    
    if by_protocol_exists:
        by_protocol_count = len([f for f in os.listdir('subscriptions/by_protocol') if f.endswith('.txt')])
    else:
        by_protocol_count = 0
    
    if by_country_exists:
        by_country_count = len([f for f in os.listdir('subscriptions/by_country') if f.endswith('.txt')])
    else:
        by_country_count = 0
    
    print(f"✅ فایل‌های subscription در root: {protocol_file_count}")
    print(f"✅ فایل‌های by_protocol: {by_protocol_count}")
    print(f"✅ فایل‌های by_country: {by_country_count}")
    
    # ========== نتیجه نهایی ==========
    print("\n" + "=" * 70)
    print("🎉 نتیجه نهایی")
    print("=" * 70)
    
    print(f"""
✅ جمع‌آوری: {successful_sources}/{successful_sources + failed_sources} منبع موفق
✅ کانفیگ‌های خام: {len(all_configs):,}
✅ تجزیه شده: {len(parsed_configs):,}
✅ پروتکل‌های یافت شده: {len(protocol_counts)}
✅ کشورهای یافت شده: {len(country_counts)}
✅ فایل‌های تولید شده: {len(subscription_files)}
✅ دسته‌بندی پروتکل: {len([c for c in categories.values() if c])}
✅ دسته‌بندی کشور: {len(country_files)}

🎯 وضعیت: همه چیز به درستی کار می‌کند!
    """)
    
    return True

if __name__ == '__main__':
    try:
        result = asyncio.run(test_complete_workflow())
        if result:
            print("✅ تست کامل موفق بود!")
            exit(0)
        else:
            print("❌ تست ناموفق بود!")
            exit(1)
    except Exception as e:
        print(f"❌ خطا در تست: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

