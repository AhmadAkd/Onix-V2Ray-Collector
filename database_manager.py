#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Manager for V2Ray Collector
مدیریت پایگاه داده برای ذخیره تاریخچه و آمار
"""

import sqlite3
import logging
from datetime import datetime, timedelta
from typing import List, Dict
from contextlib import contextmanager
import json

logger = logging.getLogger(__name__)

class DatabaseManager:
    """مدیریت پایگاه داده SQLite"""
    
    def __init__(self, db_path: str = 'v2ray_collector.db'):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self._init_database()
    
    @contextmanager
    def get_connection(self):
        """Context manager برای اتصال"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            self.logger.error(f"❌ Database error: {e}")
            raise
        finally:
            conn.close()
    
    def _init_database(self):
        """ایجاد جداول"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS collection_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    total_configs INTEGER,
                    working_configs INTEGER,
                    failed_configs INTEGER,
                    success_rate REAL,
                    duration INTEGER
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS protocol_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    protocol TEXT NOT NULL,
                    count INTEGER,
                    avg_latency REAL
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS country_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    country TEXT NOT NULL,
                    count INTEGER,
                    avg_latency REAL
                )
            ''')
            
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_collection_timestamp ON collection_history(timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_protocol_timestamp ON protocol_stats(timestamp, protocol)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_country_timestamp ON country_stats(timestamp, country)')
            
            self.logger.info("✅ Database initialized")
    
    def save_collection_snapshot(self, report: Dict) -> int:
        """ذخیره snapshot از جمع‌آوری"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO collection_history 
                (timestamp, total_configs, working_configs, failed_configs, success_rate, duration)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                report.get('timestamp', datetime.now().isoformat()),
                report.get('total_configs_tested', 0),
                report.get('working_configs', 0),
                report.get('failed_configs', 0),
                float(report.get('success_rate', '0%').replace('%', '')),
                0
            ))
            
            snapshot_id = cursor.lastrowid
            timestamp = report.get('timestamp', datetime.now().isoformat())
            
            # Save protocols
            for protocol, stats in report.get('protocols', {}).items():
                cursor.execute('''
                    INSERT INTO protocol_stats (timestamp, protocol, count, avg_latency)
                    VALUES (?, ?, ?, ?)
                ''', (timestamp, protocol, stats.get('count', 0), float(stats.get('avg_latency', '0ms').replace('ms', ''))))
            
            # Save countries
            for country, stats in report.get('countries', {}).items():
                cursor.execute('''
                    INSERT INTO country_stats (timestamp, country, count, avg_latency)
                    VALUES (?, ?, ?, ?)
                ''', (timestamp, country, stats.get('count', 0), float(stats.get('avg_latency', '0ms').replace('ms', ''))))
            
            self.logger.info(f"✅ Snapshot saved: {snapshot_id}")
            return snapshot_id
    
    def get_history(self, hours: int = 24) -> List[Dict]:
        """دریافت تاریخچه"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            since = (datetime.now() - timedelta(hours=hours)).isoformat()
            cursor.execute('SELECT * FROM collection_history WHERE timestamp >= ? ORDER BY timestamp DESC', (since,))
            return [dict(row) for row in cursor.fetchall()]
    
    def cleanup_old_data(self, days: int = 30):
        """پاک‌سازی داده‌های قدیمی"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cutoff = (datetime.now() - timedelta(days=days)).isoformat()
            
            for table in ['collection_history', 'protocol_stats', 'country_stats']:
                cursor.execute(f'DELETE FROM {table} WHERE timestamp < ?', (cutoff,))
                self.logger.info(f"🗑️ Cleaned {cursor.rowcount} old records from {table}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Database Manager module loaded successfully")

