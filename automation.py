#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V2Ray Config Automation System
سیستم اتوماسیون برای اجرای خودکار جمع‌آوری کانفیگ‌ها
"""

import schedule
import time
import asyncio
import logging
import os
import json
from datetime import datetime
from config_collector import V2RayCollector

# تنظیم لاگ
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automation.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AutomationManager:
    """مدیریت اتوماسیون سیستم جمع‌آوری کانفیگ‌ها"""

    def __init__(self):
        self.collector = V2RayCollector()
        self.is_running = False
        self.stats = {
            'total_runs': 0,
            'successful_runs': 0,
            'failed_runs': 0,
            'last_run': None,
            'last_successful_run': None
        }

        # بارگذاری آمار قبلی
        self.load_stats()

    def load_stats(self):
        """بارگذاری آمار از فایل"""
        try:
            if os.path.exists('automation_stats.json'):
                with open('automation_stats.json', 'r', encoding='utf-8') as f:
                    self.stats = json.load(f)
        except Exception as e:
            logger.error(f"خطا در بارگذاری آمار: {e}")

    def save_stats(self):
        """ذخیره آمار در فایل"""
        try:
            with open('automation_stats.json', 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"خطا در ذخیره آمار: {e}")

    async def run_collection_job(self):
        """اجرای کار جمع‌آوری کانفیگ‌ها"""
        logger.info("🔄 شروع کار خودکار جمع‌آوری کانفیگ‌ها...")

        self.stats['total_runs'] += 1
        self.stats['last_run'] = datetime.now().isoformat()

        try:
            # اجرای سیکل جمع‌آوری
            subscription_files = await self.collector.run_collection_cycle()

            # تولید گزارش
            report = self.collector.generate_report()

            # ذخیره گزارش با timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_filename = f'subscriptions/report_{timestamp}.json'

            os.makedirs('subscriptions', exist_ok=True)
            with open(report_filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)

            # به‌روزرسانی آمار موفقیت
            self.stats['successful_runs'] += 1
            self.stats['last_successful_run'] = datetime.now().isoformat()

            logger.info(
                f"✅ کار خودکار با موفقیت انجام شد - {report['working_configs']} کانفیگ سالم")

            # ذخیره آمار
            self.save_stats()

            return True

        except Exception as e:
            logger.error(f"❌ خطا در کار خودکار: {e}")
            self.stats['failed_runs'] += 1
            self.save_stats()
            return False

    def setup_schedule(self):
        """تنظیم زمان‌بندی کارها"""

        # اجرای هر 30 دقیقه
        schedule.every(30).minutes.do(self.run_scheduled_job)

        # اجرای هر ساعت
        schedule.every().hour.do(self.run_health_check)

        # اجرای روزانه در ساعت 2 صبح برای تمیزکاری
        schedule.every().day.at("02:00").do(self.cleanup_old_files)

        # اجرای هفتگی برای گزارش کلی
        schedule.every().monday.at("08:00").do(self.generate_weekly_report)

        logger.info("⏰ زمان‌بندی کارها تنظیم شد:")
        logger.info("  - هر 30 دقیقه: جمع‌آوری کانفیگ‌ها")
        logger.info("  - هر ساعت: بررسی سلامت سیستم")
        logger.info("  - هر روز ساعت 2 صبح: تمیزکاری فایل‌های قدیمی")
        logger.info("  - هر دوشنبه ساعت 8 صبح: گزارش هفتگی")

    def run_scheduled_job(self):
        """اجرای کار زمان‌بندی شده"""
        if not self.is_running:
            self.is_running = True
            try:
                # اجرای async در loop جدید
                asyncio.run(self.run_collection_job())
            finally:
                self.is_running = False

    def run_health_check(self):
        """بررسی سلامت سیستم"""
        logger.info("🏥 بررسی سلامت سیستم...")

        # بررسی وجود فایل‌های ضروری
        required_dirs = ['subscriptions']
        for directory in required_dirs:
            if not os.path.exists(directory):
                os.makedirs(directory)
                logger.info(f"📁 پوشه {directory} ایجاد شد")

        # بررسی فضای دیسک
        import shutil
        total, used, free = shutil.disk_usage('.')
        free_gb = free // (1024**3)

        if free_gb < 1:  # کمتر از 1 گیگابایت فضای آزاد
            logger.warning(f"⚠️ فضای دیسک کم: {free_gb}GB باقی‌مانده")
        else:
            logger.info(f"💾 فضای دیسک: {free_gb}GB آزاد")

    def cleanup_old_files(self):
        """تمیزکاری فایل‌های قدیمی"""
        logger.info("🧹 شروع تمیزکاری فایل‌های قدیمی...")

        import glob
        from datetime import datetime, timedelta

        # حذف گزارش‌های قدیمی (بیش از 7 روز)
        old_reports = glob.glob('subscriptions/report_*.json')
        cutoff_date = datetime.now() - timedelta(days=7)

        deleted_count = 0
        for report_file in old_reports:
            try:
                file_time = datetime.fromtimestamp(
                    os.path.getctime(report_file))
                if file_time < cutoff_date:
                    os.remove(report_file)
                    deleted_count += 1
                    logger.info(f"🗑️ حذف گزارش قدیمی: {report_file}")
            except Exception as e:
                logger.error(f"خطا در حذف {report_file}: {e}")

        logger.info(f"✅ تمیزکاری کامل شد - {deleted_count} فایل حذف شد")

    def generate_weekly_report(self):
        """تولید گزارش هفتگی"""
        logger.info("📊 تولید گزارش هفتگی...")

        try:
            # جمع‌آوری آمار هفته
            weekly_stats = {
                'period': 'هفته گذشته',
                'generated_at': datetime.now().isoformat(),
                'automation_stats': self.stats,
                'summary': {
                    'total_runs': self.stats['total_runs'],
                    'success_rate': f"{(self.stats['successful_runs'] / max(self.stats['total_runs'], 1)) * 100:.1f}%",
                    'average_configs_per_run': 0  # محاسبه از گزارش‌های روزانه
                }
            }

            # ذخیره گزارش هفتگی
            os.makedirs('subscriptions', exist_ok=True)
            weekly_filename = f'subscriptions/weekly_report_{datetime.now().strftime("%Y%m%d")}.json'

            with open(weekly_filename, 'w', encoding='utf-8') as f:
                json.dump(weekly_stats, f, ensure_ascii=False, indent=2)

            logger.info(f"📈 گزارش هفتگی ذخیره شد: {weekly_filename}")

        except Exception as e:
            logger.error(f"خطا در تولید گزارش هفتگی: {e}")

    def start_automation(self):
        """شروع اتوماسیون"""
        logger.info("🚀 شروع سیستم اتوماسیون...")

        # تنظیم زمان‌بندی
        self.setup_schedule()

        # اجرای اولیه
        logger.info("🔄 اجرای اولیه...")
        self.run_scheduled_job()

        # حلقه اصلی
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # بررسی هر دقیقه

        except KeyboardInterrupt:
            logger.info("⏹️ توقف سیستم اتوماسیون...")
        except Exception as e:
            logger.error(f"خطای کلی در اتوماسیون: {e}")
        finally:
            self.save_stats()
            logger.info("💾 آمار نهایی ذخیره شد")

    def run_once(self):
        """اجرای یکباره (بدون اتوماسیون)"""
        logger.info("🔄 اجرای یکباره جمع‌آوری کانفیگ‌ها...")

        try:
            asyncio.run(self.run_collection_job())
            logger.info("✅ اجرای یکباره با موفقیت انجام شد")
        except Exception as e:
            logger.error(f"❌ خطا در اجرای یکباره: {e}")


def main():
    """تابع اصلی"""
    import argparse

    parser = argparse.ArgumentParser(
        description='سیستم اتوماسیون V2Ray Config Collector')
    parser.add_argument('--mode', choices=['auto', 'once'], default='auto',
                        help='حالت اجرا: auto (خودکار) یا once (یکباره)')
    parser.add_argument('--interval', type=int, default=30,
                        help='فاصله زمانی اجرا به دقیقه (فقط در حالت auto)')

    args = parser.parse_args()

    automation = AutomationManager()

    if args.mode == 'once':
        automation.run_once()
    else:
        # تنظیم فاصله زمانی سفارشی
        if args.interval != 30:
            schedule.every(args.interval).minutes.do(
                automation.run_scheduled_job)

        automation.start_automation()


if __name__ == "__main__":
    main()
