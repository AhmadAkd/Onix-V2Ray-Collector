#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced V2Ray Collector
نسخه پیشرفته collector با تمام قابلیت‌های جدید
"""

import asyncio
import logging
from typing import List, Dict, Optional
from datetime import datetime
import json

# Import core modules
from config_collector import V2RayCollector
from config import CONFIG_SOURCES

# Import advanced modules
try:
    from health_checker import HealthChecker, HealthStatus
    HEALTH_CHECK_AVAILABLE = True
except ImportError:
    HEALTH_CHECK_AVAILABLE = False
    logging.warning("Health Checker not available")

try:
    from error_recovery import ErrorRecovery
    ERROR_RECOVERY_AVAILABLE = True
except ImportError:
    ERROR_RECOVERY_AVAILABLE = False
    logging.warning("Error Recovery not available")

try:
    from database_manager import DatabaseManager
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False
    logging.warning("Database Manager not available")

try:
    from ml_config_scorer import MLConfigScorer
    ML_SCORING_AVAILABLE = True
except ImportError:
    ML_SCORING_AVAILABLE = False
    logging.warning("ML Scoring not available")

try:
    from telegram_collector import TelegramCollector
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    logging.warning("Telegram Collector not available")

logger = logging.getLogger(__name__)

class AdvancedCollector:
    """
    Collector پیشرفته با تمام قابلیت‌های جدید
    """
    
    def __init__(self, enable_all_features: bool = True):
        """
        Initialize Advanced Collector
        
        Args:
            enable_all_features: فعال‌سازی تمام قابلیت‌ها
        """
        self.logger = logging.getLogger(__name__)
        self.collector = V2RayCollector()
        
        # Initialize advanced modules
        self.health_checker = HealthChecker() if HEALTH_CHECK_AVAILABLE and enable_all_features else None
        self.error_recovery = ErrorRecovery() if ERROR_RECOVERY_AVAILABLE and enable_all_features else None
        self.database = DatabaseManager() if DATABASE_AVAILABLE and enable_all_features else None
        self.ml_scorer = MLConfigScorer() if ML_SCORING_AVAILABLE and enable_all_features else None
        self.telegram = TelegramCollector() if TELEGRAM_AVAILABLE and enable_all_features else None
        
        self.logger.info("🚀 Advanced Collector initialized")
        self.logger.info(f"   Health Check: {'✅' if self.health_checker else '❌'}")
        self.logger.info(f"   Error Recovery: {'✅' if self.error_recovery else '❌'}")
        self.logger.info(f"   Database: {'✅' if self.database else '❌'}")
        self.logger.info(f"   ML Scoring: {'✅' if self.ml_scorer else '❌'}")
        self.logger.info(f"   Telegram: {'✅' if self.telegram else '❌'}")
    
    async def run_with_health_check(self) -> Dict:
        """
        اجرای collection با health check
        
        Returns:
            گزارش کامل
        """
        start_time = datetime.now()
        
        # Pre-flight health check
        if self.health_checker:
            health_status = await self.health_checker.perform_full_health_check(CONFIG_SOURCES)
            self.health_checker.save_health_report(health_status)
            
            if not health_status.is_healthy:
                self.logger.error("❌ System is not healthy, proceeding with caution...")
        
        # Run collection with error recovery
        if self.error_recovery:
            @self.error_recovery.retry_with_backoff(max_retries=3)
            async def collect_with_retry():
                return await self.collector.collect_all()
            
            all_configs = await collect_with_retry()
        else:
            all_configs = await self.collector.collect_all()
        
        # Generate report
        report = self.collector.generate_report()
        
        # Save to database
        if self.database:
            try:
                self.database.save_collection_snapshot(report)
                self.logger.info("✅ Snapshot saved to database")
            except Exception as e:
                self.logger.error(f"❌ Error saving to database: {e}")
        
        # ML Scoring for top configs
        if self.ml_scorer and all_configs:
            try:
                # Score working configs
                working_configs_data = [
                    {
                        'protocol': c.protocol,
                        'country': c.country,
                        'latency': f"{c.latency}ms" if hasattr(c, 'latency') else '999ms',
                        'address': c.address,
                        'id': f"{c.address}:{c.port}"
                    }
                    for c in all_configs[:100]  # Score first 100
                ]
                
                top_configs = self.ml_scorer.rank_configs(working_configs_data, top_n=10)
                
                # Add to report
                report['top_configs'] = [
                    {
                        'config': config,
                        'score': score.total_score,
                        'recommendation': score.details['recommendation']
                    }
                    for config, score in top_configs
                ]
                
                self.logger.info(f"✅ ML scoring completed for top {len(top_configs)} configs")
            except Exception as e:
                self.logger.error(f"❌ Error in ML scoring: {e}")
        
        # Calculate duration
        duration = (datetime.now() - start_time).total_seconds()
        report['collection_duration'] = f"{duration:.1f}s"
        
        return report
    
    async def run_scheduled(self, interval_minutes: int = 30):
        """
        اجرای دوره‌ای
        
        Args:
            interval_minutes: فاصله زمانی (دقیقه)
        """
        self.logger.info(f"🔄 Starting scheduled collection (every {interval_minutes} minutes)")
        
        while True:
            try:
                report = await self.run_with_health_check()
                self.logger.info(f"✅ Collection completed: {report.get('working_configs', 0)} working configs")
                
                # Wait for next run
                await asyncio.sleep(interval_minutes * 60)
                
            except KeyboardInterrupt:
                self.logger.info("⏹️ Scheduled collection stopped by user")
                break
            except Exception as e:
                self.logger.error(f"❌ Error in scheduled collection: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retry

async def main():
    """تست Advanced Collector"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("\n" + "="*80)
    print("🚀 ADVANCED V2RAY COLLECTOR")
    print("="*80)
    
    collector = AdvancedCollector(enable_all_features=True)
    
    print("\n📊 Running collection with all advanced features...")
    report = await collector.run_with_health_check()
    
    print("\n" + "="*80)
    print("📈 COLLECTION REPORT")
    print("="*80)
    print(f"⏱️  Duration: {report.get('collection_duration', 'N/A')}")
    print(f"📊 Total tested: {report.get('total_configs_tested', 0):,}")
    print(f"✅ Working: {report.get('working_configs', 0):,}")
    print(f"❌ Failed: {report.get('failed_configs', 0):,}")
    print(f"📈 Success rate: {report.get('success_rate', 'N/A')}")
    
    if 'top_configs' in report:
        print(f"\n🌟 Top {len(report['top_configs'])} Configs:")
        for i, item in enumerate(report['top_configs'][:5], 1):
            config = item['config']
            print(f"   {i}. {config['protocol']} - {config['country']} ({config['latency']}) - Score: {item['score']:.3f}")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    asyncio.run(main())

