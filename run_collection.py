#!/usr/bin/env python3
"""
Run full collection cycle to collect more configs
"""

import asyncio
import json
from datetime import datetime
from config_collector import V2RayCollector


async def run_full_cycle():
    print("🚀 شروع Collection Cycle کامل...")
    print(f"⏰ زمان شروع: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    collector = V2RayCollector()

    print(f"📊 تعداد منابع: {len(collector.config_sources)}")

    try:
        # اجرای collection cycle
        subscription_files = await collector.run_collection_cycle()

        print("\n✅ Collection Cycle با موفقیت تکمیل شد!")
        print(f"📁 فایل‌های تولید شده: {len(subscription_files)}")

        # نمایش آمار
        for protocol, file_info in subscription_files.items():
            if 'count' in file_info:
                print(f"   📄 {protocol}: {file_info['count']} کانفیگ")

        # تولید گزارش نهایی
        report = collector.generate_report()

        # ذخیره گزارش
        with open('subscriptions/latest_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print(f"\n📊 گزارش نهایی:")
        print(
            f"   🔢 کل کانفیگ‌های تست شده: {report.get('total_configs_tested', 0):,}")
        print(f"   ✅ کانفیگ‌های سالم: {report.get('working_configs', 0):,}")
        print(f"   ❌ کانفیگ‌های ناسالم: {report.get('failed_configs', 0):,}")
        print(f"   📈 نرخ موفقیت: {report.get('success_rate', '0%')}")

        # آمار AI Quality
        ai_quality = report.get('ai_quality', {})
        if ai_quality:
            print(f"\n🤖 آمار AI Quality:")
            print(f"   📊 میانگین امتیاز: {ai_quality.get('average_score', 0):.3f}")
            print(f"   🏆 کیفیت بالا: {ai_quality.get('high_quality_count', 0)}")
            print(f"   ⚠️ کیفیت متوسط: {ai_quality.get('medium_quality_count', 0)}")
            print(f"   ❌ کیفیت پایین: {ai_quality.get('low_quality_count', 0)}")
            
            # نمایش دسته‌بندی‌های کیفیت
            categories = ai_quality.get('quality_categories', {})
            if categories:
                print(f"   📋 دسته‌بندی‌ها:")
                for category, count in categories.items():
                    print(f"      {category}: {count}")

        # آمار پروتکل‌ها
        protocols = report.get('protocols', {})
        print(f"\n🔌 آمار پروتکل‌ها:")
        for protocol, stats in protocols.items():
            count = stats.get('count', 0)
            latency = stats.get('avg_latency', '-')
            print(f"   {protocol.upper()}: {count:,} کانفیگ - {latency}")

        # آمار کشورها
        countries = report.get('countries', {})
        print(f"\n🌍 آمار کشورها:")
        sorted_countries = sorted(
            countries.items(), key=lambda x: x[1].get('count', 0), reverse=True)
        for country, stats in sorted_countries[:10]:  # Top 10
            count = stats.get('count', 0)
            latency = stats.get('avg_latency', '-')
            print(f"   {country}: {count:,} کانفیگ - {latency}")

        print(
            f"\n⏰ زمان پایان: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Auto-update UI with new protocols and countries
        print("\n🔄 بروزرسانی خودکار UI...")
        try:
            from auto_update_ui import UIAutoUpdater
            ui_updater = UIAutoUpdater()
            ui_updater.run_auto_update()
        except Exception as e:
            print(f"⚠️ خطا در بروزرسانی UI: {e}")

        return True

    except Exception as e:
        print(f"❌ خطا در Collection Cycle: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(run_full_cycle())
    if success:
        print("\n🎉 Collection Cycle با موفقیت تکمیل شد!")
    else:
        print("\n💥 Collection Cycle با خطا مواجه شد!")
