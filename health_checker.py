#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Health Check System for V2Ray Collector
بررسی سلامت سیستم، منابع و کانفیگ‌ها
"""

import asyncio
import aiohttp
import psutil
import logging
from datetime import datetime
from typing import Dict, List
from dataclasses import dataclass, field
import json

logger = logging.getLogger(__name__)

@dataclass
class HealthStatus:
    """وضعیت سلامت سیستم"""
    is_healthy: bool = True
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    disk_usage: float = 0.0
    active_sources: int = 0
    failed_sources: int = 0
    total_configs: int = 0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

class HealthChecker:
    """سیستم بررسی سلامت"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.last_check = None
        self.check_interval = 300  # 5 minutes
        
        # Thresholds
        self.cpu_threshold = 80.0
        self.memory_threshold = 80.0
        self.disk_threshold = 90.0
        self.min_working_sources = 20
        
    async def check_system_resources(self) -> Dict:
        """بررسی منابع سیستم"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            resources = {
                'cpu': {'usage': cpu_percent, 'healthy': cpu_percent < self.cpu_threshold},
                'memory': {'usage': memory.percent, 'available': memory.available // (1024 * 1024), 'healthy': memory.percent < self.memory_threshold},
                'disk': {'usage': disk.percent, 'free': disk.free // (1024 * 1024 * 1024), 'healthy': disk.percent < self.disk_threshold}
            }
            
            self.logger.info(f"✅ System resources checked")
            return resources
        except Exception as e:
            self.logger.error(f"❌ Error checking system resources: {e}")
            return {}
    
    async def check_sources(self, sources: List[str]) -> Dict:
        """بررسی دسترسی به منابع"""
        active = 0
        failed = 0
        failed_sources = []
        
        async with aiohttp.ClientSession() as session:
            for source in sources[:10]:
                try:
                    async with session.head(source, timeout=aiohttp.ClientTimeout(total=5)) as response:
                        if response.status == 200:
                            active += 1
                        else:
                            failed += 1
                            failed_sources.append(source)
                except:
                    failed += 1
                    failed_sources.append(source)
        
        return {
            'total': len(sources),
            'checked': 10,
            'active': active,
            'failed': failed,
            'failed_sources': failed_sources,
            'healthy': active >= 5
        }
    
    async def check_configs(self, config_file: str = 'subscriptions/latest_report.json') -> Dict:
        """بررسی وضعیت کانفیگ‌ها"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            working = data.get('working_configs', 0)
            success_rate = float(data.get('success_rate', '0%').replace('%', ''))
            
            return {
                'working': working,
                'total': data.get('total_configs_tested', 0),
                'success_rate': success_rate,
                'healthy': success_rate >= 60.0
            }
        except Exception as e:
            self.logger.error(f"❌ Error checking configs: {e}")
            return {'working': 0, 'total': 0, 'success_rate': 0, 'healthy': False}
    
    async def perform_full_health_check(self, sources: List[str]) -> HealthStatus:
        """بررسی کامل سلامت سیستم"""
        self.logger.info("🔍 Starting full health check...")
        status = HealthStatus()
        
        # Check resources
        resources = await self.check_system_resources()
        if resources:
            status.cpu_usage = resources['cpu']['usage']
            status.memory_usage = resources['memory']['usage']
            status.disk_usage = resources['disk']['usage']
            
            if not resources['cpu']['healthy']:
                status.warnings.append(f"⚠️ High CPU: {status.cpu_usage}%")
            if not resources['memory']['healthy']:
                status.warnings.append(f"⚠️ High memory: {status.memory_usage}%")
            if not resources['disk']['healthy']:
                status.warnings.append(f"⚠️ High disk: {status.disk_usage}%")
        
        # Check sources
        source_status = await self.check_sources(sources)
        status.active_sources = source_status['active']
        status.failed_sources = source_status['failed']
        
        if not source_status['healthy']:
            status.errors.append(f"❌ Too few active sources: {status.active_sources}")
            status.is_healthy = False
        
        # Check configs
        config_status = await self.check_configs()
        status.total_configs = config_status['total']
        
        if not config_status['healthy']:
            status.errors.append(f"❌ Low success rate: {config_status['success_rate']}%")
            status.is_healthy = False
        
        self.last_check = datetime.now()
        return status
    
    def save_health_report(self, status: HealthStatus, output_file: str = 'health_report.json'):
        """ذخیره گزارش سلامت"""
        try:
            report = {
                'timestamp': status.timestamp,
                'is_healthy': status.is_healthy,
                'system': {
                    'cpu_usage': f"{status.cpu_usage:.1f}%",
                    'memory_usage': f"{status.memory_usage:.1f}%",
                    'disk_usage': f"{status.disk_usage:.1f}%"
                },
                'sources': {'active': status.active_sources, 'failed': status.failed_sources},
                'configs': {'total': status.total_configs},
                'errors': status.errors,
                'warnings': status.warnings
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"✅ Health report saved")
        except Exception as e:
            self.logger.error(f"❌ Error saving health report: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Health Checker module loaded successfully")

