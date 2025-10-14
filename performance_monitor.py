#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Performance Monitoring System
سیستم نظارت بر عملکرد
"""

import time
import logging
from functools import wraps
from typing import Callable, Dict, List
import json
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """نظارت بر عملکرد"""
    
    def __init__(self):
        self.metrics = defaultdict(list)
        self.logger = logging.getLogger(__name__)
    
    def measure_time(self, operation_name: str = None):
        """
        Decorator برای اندازه‌گیری زمان اجرا
        
        Args:
            operation_name: نام عملیات
        """
        def decorator(func: Callable):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                op_name = operation_name or func.__name__
                start_time = time.time()
                
                try:
                    result = await func(*args, **kwargs)
                    duration = time.time() - start_time
                    
                    self.record_metric(op_name, duration, success=True)
                    self.logger.debug(f"⏱️ {op_name}: {duration:.2f}s")
                    
                    return result
                except Exception as e:
                    duration = time.time() - start_time
                    self.record_metric(op_name, duration, success=False)
                    raise e
            
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                op_name = operation_name or func.__name__
                start_time = time.time()
                
                try:
                    result = func(*args, **kwargs)
                    duration = time.time() - start_time
                    
                    self.record_metric(op_name, duration, success=True)
                    self.logger.debug(f"⏱️ {op_name}: {duration:.2f}s")
                    
                    return result
                except Exception as e:
                    duration = time.time() - start_time
                    self.record_metric(op_name, duration, success=False)
                    raise e
            
            # Return appropriate wrapper
            import asyncio
            if asyncio.iscoroutinefunction(func):
                return async_wrapper
            else:
                return sync_wrapper
        
        return decorator
    
    def record_metric(self, operation: str, duration: float, success: bool = True):
        """
        ثبت metric
        
        Args:
            operation: نام عملیات
            duration: مدت زمان
            success: موفق بود یا نه
        """
        self.metrics[operation].append({
            'timestamp': datetime.now().isoformat(),
            'duration': duration,
            'success': success
        })
    
    def get_statistics(self, operation: str = None) -> Dict:
        """
        دریافت آمار عملکرد
        
        Args:
            operation: نام عملیات (None برای همه)
            
        Returns:
            آمار عملکرد
        """
        if operation:
            metrics = self.metrics.get(operation, [])
            return self._calculate_stats(operation, metrics)
        else:
            stats = {}
            for op, metrics in self.metrics.items():
                stats[op] = self._calculate_stats(op, metrics)
            return stats
    
    def _calculate_stats(self, operation: str, metrics: List[Dict]) -> Dict:
        """محاسبه آمار برای یک عملیات"""
        if not metrics:
            return {
                'operation': operation,
                'count': 0,
                'avg_duration': 0,
                'min_duration': 0,
                'max_duration': 0,
                'success_rate': 0
            }
        
        durations = [m['duration'] for m in metrics]
        successes = sum(1 for m in metrics if m['success'])
        
        return {
            'operation': operation,
            'count': len(metrics),
            'avg_duration': sum(durations) / len(durations),
            'min_duration': min(durations),
            'max_duration': max(durations),
            'success_rate': (successes / len(metrics)) * 100
        }
    
    def export_metrics(self, filename: str = 'performance_metrics.json'):
        """Export metrics به فایل"""
        stats = self.get_statistics()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"✅ Metrics exported to {filename}")
    
    def print_summary(self):
        """چاپ خلاصه عملکرد"""
        stats = self.get_statistics()
        
        print("\n" + "="*80)
        print("📊 PERFORMANCE SUMMARY")
        print("="*80)
        
        for operation, data in stats.items():
            print(f"\n🔧 {operation}:")
            print(f"   Count: {data['count']}")
            print(f"   Avg Duration: {data['avg_duration']:.2f}s")
            print(f"   Min Duration: {data['min_duration']:.2f}s")
            print(f"   Max Duration: {data['max_duration']:.2f}s")
            print(f"   Success Rate: {data['success_rate']:.1f}%")
        
        print("\n" + "="*80)
    
    def clear_metrics(self):
        """پاک کردن تمام metrics"""
        self.metrics.clear()
        self.logger.info("🗑️ Metrics cleared")

# Global instance
performance_monitor = PerformanceMonitor()

# Convenience decorator
def measure_performance(operation_name: str = None):
    """Decorator ساده برای اندازه‌گیری عملکرد"""
    return performance_monitor.measure_time(operation_name)

# Example usage
if __name__ == "__main__":
    import asyncio
    
    monitor = PerformanceMonitor()
    
    @monitor.measure_time("test_operation")
    async def test_function():
        await asyncio.sleep(0.5)
        return "Done"
    
    async def main():
        for i in range(5):
            await test_function()
        
        monitor.print_summary()
        monitor.export_metrics()
    
    asyncio.run(main())

