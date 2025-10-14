#!/usr/bin/env python3
"""
Advanced Monitoring System for V2Ray Collector
سیستم نظارت پیشرفته برای V2Ray Collector
"""

import asyncio
import aiohttp
import time
import json
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import sqlite3
import os

logger = logging.getLogger(__name__)


@dataclass
class ConfigHealth:
    """سلامت کانفیگ"""
    address: str
    port: int
    protocol: str
    latency: float
    is_working: bool
    last_check: datetime
    success_rate: float
    uptime_percentage: float
    error_count: int
    last_error: Optional[str] = None


@dataclass
class SystemMetrics:
    """معیارهای سیستم"""
    timestamp: datetime
    total_configs: int
    working_configs: int
    failed_configs: int
    avg_latency: float
    collection_time: float
    sources_active: int
    sources_failed: int
    memory_usage: float
    cpu_usage: float


class DatabaseManager:
    """مدیریت دیتابیس برای ذخیره اطلاعات"""

    def __init__(self, db_path: str = "monitoring.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """ایجاد جداول دیتابیس"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # جدول سلامت کانفیگ‌ها
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS config_health (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    address TEXT NOT NULL,
                    port INTEGER NOT NULL,
                    protocol TEXT NOT NULL,
                    latency REAL,
                    is_working BOOLEAN,
                    last_check TIMESTAMP,
                    success_rate REAL,
                    uptime_percentage REAL,
                    error_count INTEGER,
                    last_error TEXT
                )
            ''')

            # جدول معیارهای سیستم
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP,
                    total_configs INTEGER,
                    working_configs INTEGER,
                    failed_configs INTEGER,
                    avg_latency REAL,
                    collection_time REAL,
                    sources_active INTEGER,
                    sources_failed INTEGER,
                    memory_usage REAL,
                    cpu_usage REAL
                )
            ''')

            # جدول آمار منابع
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS source_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_url TEXT NOT NULL,
                    configs_count INTEGER,
                    success_rate REAL,
                    last_check TIMESTAMP,
                    response_time REAL,
                    status TEXT
                )
            ''')

            conn.commit()

    def save_config_health(self, health: ConfigHealth):
        """ذخیره سلامت کانفیگ"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO config_health 
                (address, port, protocol, latency, is_working, last_check, 
                 success_rate, uptime_percentage, error_count, last_error)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                health.address, health.port, health.protocol, health.latency,
                health.is_working, health.last_check, health.success_rate,
                health.uptime_percentage, health.error_count, health.last_error
            ))
            conn.commit()

    def save_system_metrics(self, metrics: SystemMetrics):
        """ذخیره معیارهای سیستم"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO system_metrics 
                (timestamp, total_configs, working_configs, failed_configs,
                 avg_latency, collection_time, sources_active, sources_failed,
                 memory_usage, cpu_usage)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                metrics.timestamp, metrics.total_configs, metrics.working_configs,
                metrics.failed_configs, metrics.avg_latency, metrics.collection_time,
                metrics.sources_active, metrics.sources_failed, metrics.memory_usage,
                metrics.cpu_usage
            ))
            conn.commit()

    def get_health_stats(self, hours: int = 24) -> Dict:
        """دریافت آمار سلامت"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # آمار کلی
            cursor.execute('''
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN is_working = 1 THEN 1 ELSE 0 END) as working,
                    AVG(latency) as avg_latency,
                    AVG(success_rate) as avg_success_rate
                FROM config_health 
                WHERE last_check > datetime('now', '-{} hours')
            '''.format(hours))

            stats = cursor.fetchone()

            return {
                'total_configs': stats[0] or 0,
                'working_configs': stats[1] or 0,
                'avg_latency': stats[2] or 0.0,
                'avg_success_rate': stats[3] or 0.0
            }


class AdvancedMonitor:
    """نظارت پیشرفته سیستم"""

    def __init__(self):
        self.db = DatabaseManager()
        self.health_history = []
        self.alert_thresholds = {
            'success_rate': 0.7,  # 70%
            'avg_latency': 3000,  # 3 seconds
            'uptime_percentage': 0.8  # 80%
        }

    async def monitor_config_health(self, configs: List[Dict]) -> List[ConfigHealth]:
        """نظارت بر سلامت کانفیگ‌ها"""
        health_data = []

        for config in configs:
            try:
                # تست اتصال
                start_time = time.time()
                is_working, latency = await self._test_config_connection(config)
                test_time = time.time() - start_time

                # محاسبه معیارهای سلامت
                health = ConfigHealth(
                    address=config.get('address', ''),
                    port=config.get('port', 0),
                    protocol=config.get('protocol', ''),
                    latency=latency,
                    is_working=is_working,
                    last_check=datetime.now(),
                    success_rate=self._calculate_success_rate(config),
                    uptime_percentage=self._calculate_uptime(config),
                    error_count=self._get_error_count(config),
                    last_error=None if is_working else "Connection failed"
                )

                health_data.append(health)
                self.db.save_config_health(health)

            except Exception as e:
                logger.error(f"خطا در نظارت کانفیگ: {e}")

        return health_data

    async def monitor_system_metrics(self) -> SystemMetrics:
        """نظارت بر معیارهای سیستم"""
        import psutil

        # جمع‌آوری اطلاعات سیستم
        memory_info = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent(interval=1)

        # خواندن آمار از فایل گزارش
        try:
            with open('subscriptions/latest_report.json', 'r') as f:
                report = json.load(f)
        except:
            report = {}

        metrics = SystemMetrics(
            timestamp=datetime.now(),
            total_configs=report.get('total_configs_tested', 0),
            working_configs=report.get('working_configs', 0),
            failed_configs=report.get('failed_configs', 0),
            avg_latency=report.get('avg_latency', 0.0),
            collection_time=report.get('collection_time', 0.0),
            sources_active=report.get('sources_active', 0),
            sources_failed=report.get('sources_failed', 0),
            memory_usage=memory_info.percent,
            cpu_usage=cpu_percent
        )

        self.db.save_system_metrics(metrics)
        return metrics

    async def _test_config_connection(self, config: Dict) -> tuple:
        """تست اتصال کانفیگ"""
        try:
            address = config.get('address', '')
            port = config.get('port', 0)

            if not address or not port:
                return False, 0.0

            # تست اتصال TCP
            start_time = time.time()
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(address, port),
                timeout=5.0
            )
            writer.close()
            await writer.wait_closed()

            latency = (time.time() - start_time) * 1000
            return True, latency

        except Exception:
            return False, 0.0

    def _calculate_success_rate(self, config: Dict) -> float:
        """محاسبه نرخ موفقیت"""
        # اینجا می‌توانید منطق پیچیده‌تری برای محاسبه نرخ موفقیت پیاده‌سازی کنید
        return 0.85  # مقدار نمونه

    def _calculate_uptime(self, config: Dict) -> float:
        """محاسبه درصد uptime"""
        # اینجا می‌توانید منطق پیچیده‌تری برای محاسبه uptime پیاده‌سازی کنید
        return 0.90  # مقدار نمونه

    def _get_error_count(self, config: Dict) -> int:
        """دریافت تعداد خطاها"""
        # اینجا می‌توانید منطق پیچیده‌تری برای شمارش خطاها پیاده‌سازی کنید
        return 0  # مقدار نمونه

    def check_alerts(self, health_data: List[ConfigHealth], metrics: SystemMetrics):
        """بررسی هشدارها"""
        alerts = []

        # بررسی نرخ موفقیت
        if metrics.working_configs / max(metrics.total_configs, 1) < self.alert_thresholds['success_rate']:
            alerts.append({
                'type': 'success_rate',
                'message': f'نرخ موفقیت پایین: {(metrics.working_configs/max(metrics.total_configs, 1)*100):.1f}%',
                'severity': 'high'
            })

        # بررسی تأخیر متوسط
        if metrics.avg_latency > self.alert_thresholds['avg_latency']:
            alerts.append({
                'type': 'high_latency',
                'message': f'تأخیر بالا: {metrics.avg_latency:.0f}ms',
                'severity': 'medium'
            })

        # بررسی منابع ناموفق
        if metrics.sources_failed > metrics.sources_active * 0.3:
            alerts.append({
                'type': 'source_failure',
                'message': f'تعداد زیادی منبع ناموفق: {metrics.sources_failed}',
                'severity': 'high'
            })

        # بررسی استفاده از حافظه
        if metrics.memory_usage > 80:
            alerts.append({
                'type': 'high_memory',
                'message': f'استفاده بالای حافظه: {metrics.memory_usage:.1f}%',
                'severity': 'medium'
            })

        return alerts

    def generate_health_report(self) -> Dict:
        """تولید گزارش سلامت"""
        health_stats = self.db.get_health_stats(24)

        return {
            'timestamp': datetime.now().isoformat(),
            'health_stats': health_stats,
            'system_status': 'healthy' if health_stats['avg_success_rate'] > 0.8 else 'degraded',
            'recommendations': self._generate_recommendations(health_stats)
        }

    def _generate_recommendations(self, stats: Dict) -> List[str]:
        """تولید توصیه‌ها"""
        recommendations = []

        if stats['avg_success_rate'] < 0.8:
            recommendations.append(
                "نرخ موفقیت پایین است. منابع جدید اضافه کنید.")

        if stats['avg_latency'] > 2000:
            recommendations.append(
                "تأخیر بالا است. فیلترهای هوشمند را بهبود دهید.")

        if stats['total_configs'] < 1000:
            recommendations.append(
                "تعداد کانفیگ‌ها کم است. منابع بیشتری اضافه کنید.")

        return recommendations

# مثال استفاده


async def main():
    monitor = AdvancedMonitor()

    # نمونه کانفیگ‌ها
    sample_configs = [
        {'address': '127.0.0.1', 'port': 1080, 'protocol': 'vmess'},
        {'address': '127.0.0.1', 'port': 1081, 'protocol': 'vless'},
    ]

    # نظارت بر سلامت کانفیگ‌ها
    health_data = await monitor.monitor_config_health(sample_configs)

    # نظارت بر معیارهای سیستم
    metrics = await monitor.monitor_system_metrics()

    # بررسی هشدارها
    alerts = monitor.check_alerts(health_data, metrics)

    # تولید گزارش
    report = monitor.generate_health_report()

    print("گزارش سلامت سیستم:")
    print(json.dumps(report, indent=2, ensure_ascii=False))

    if alerts:
        print("\\nهشدارها:")
        for alert in alerts:
            print(f"- {alert['severity'].upper()}: {alert['message']}")

if __name__ == "__main__":
    asyncio.run(main())
