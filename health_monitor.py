#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Health Monitor for V2Ray Collector
نظارت بر سلامت سیستم V2Ray Collector
"""

import asyncio
import aiohttp
import time
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class HealthStatus:
    """وضعیت سلامت"""
    component: str
    status: str  # healthy, warning, critical
    message: str
    timestamp: float
    response_time: float = 0.0
    details: Dict = None

class HealthMonitor:
    """نظارت بر سلامت سیستم"""
    
    def __init__(self):
        self.health_checks: Dict[str, callable] = {}
        self.last_health_report: Dict[str, HealthStatus] = {}
        self.health_history: List[HealthStatus] = []
        
        # ثبت چک‌های سلامت
        self._register_health_checks()
        
        logger.info("Health Monitor initialized")
    
    def _register_health_checks(self):
        """ثبت چک‌های سلامت"""
        self.health_checks = {
            'github_connectivity': self._check_github_connectivity,
            'config_sources': self._check_config_sources,
            'api_endpoints': self._check_api_endpoints,
            'disk_space': self._check_disk_space,
            'memory_usage': self._check_memory_usage,
            'cache_performance': self._check_cache_performance
        }
    
    async def _check_github_connectivity(self) -> HealthStatus:
        """بررسی اتصال به GitHub"""
        start_time = time.time()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://api.github.com", 
                    timeout=10
                ) as response:
                    response_time = (time.time() - start_time) * 1000
                    
                    if response.status == 200:
                        return HealthStatus(
                            component="github_connectivity",
                            status="healthy",
                            message="GitHub API accessible",
                            timestamp=time.time(),
                            response_time=response_time,
                            details={"status_code": response.status}
                        )
                    else:
                        return HealthStatus(
                            component="github_connectivity",
                            status="warning",
                            message=f"GitHub API returned {response.status}",
                            timestamp=time.time(),
                            response_time=response_time,
                            details={"status_code": response.status}
                        )
        
        except asyncio.TimeoutError:
            return HealthStatus(
                component="github_connectivity",
                status="critical",
                message="GitHub API timeout",
                timestamp=time.time(),
                response_time=10000
            )
        except Exception as e:
            return HealthStatus(
                component="github_connectivity",
                status="critical",
                message=f"GitHub API error: {str(e)}",
                timestamp=time.time(),
                response_time=(time.time() - start_time) * 1000
            )
    
    async def _check_config_sources(self) -> HealthStatus:
        """بررسی منابع کانفیگ"""
        from config_collector import V2RayCollector
        
        collector = V2RayCollector()
        total_sources = len(collector.config_sources)
        accessible_sources = 0
        
        try:
            async with aiohttp.ClientSession() as session:
                for source_url in collector.config_sources[:5]:  # تست 5 منبع اول
                    try:
                        async with session.get(source_url, timeout=5) as response:
                            if response.status == 200:
                                accessible_sources += 1
                    except:
                        pass
            
            accessibility_rate = (accessible_sources / min(5, total_sources)) * 100
            
            if accessibility_rate >= 80:
                status = "healthy"
                message = f"{accessible_sources}/{min(5, total_sources)} sources accessible"
            elif accessibility_rate >= 50:
                status = "warning"
                message = f"Only {accessible_sources}/{min(5, total_sources)} sources accessible"
            else:
                status = "critical"
                message = f"Most sources inaccessible ({accessible_sources}/{min(5, total_sources)})"
            
            return HealthStatus(
                component="config_sources",
                status=status,
                message=message,
                timestamp=time.time(),
                details={
                    "total_sources": total_sources,
                    "accessible": accessible_sources,
                    "accessibility_rate": f"{accessibility_rate:.1f}%"
                }
            )
            
        except Exception as e:
            return HealthStatus(
                component="config_sources",
                status="critical",
                message=f"Error checking sources: {str(e)}",
                timestamp=time.time()
            )
    
    async def _check_api_endpoints(self) -> HealthStatus:
        """بررسی endpoint های API"""
        try:
            # این چک فقط در صورت اجرای API Server کار می‌کند
            return HealthStatus(
                component="api_endpoints",
                status="healthy",
                message="API endpoints check skipped (not running)",
                timestamp=time.time(),
                details={"note": "API server not running"}
            )
        except Exception as e:
            return HealthStatus(
                component="api_endpoints",
                status="warning",
                message=f"API check error: {str(e)}",
                timestamp=time.time()
            )
    
    async def _check_disk_space(self) -> HealthStatus:
        """بررسی فضای دیسک"""
        try:
            import shutil
            
            total, used, free = shutil.disk_usage(".")
            free_percent = (free / total) * 100
            
            if free_percent >= 20:
                status = "healthy"
                message = f"Disk space OK ({free_percent:.1f}% free)"
            elif free_percent >= 10:
                status = "warning"
                message = f"Low disk space ({free_percent:.1f}% free)"
            else:
                status = "critical"
                message = f"Critical disk space ({free_percent:.1f}% free)"
            
            return HealthStatus(
                component="disk_space",
                status=status,
                message=message,
                timestamp=time.time(),
                details={
                    "free_gb": round(free / (1024**3), 2),
                    "total_gb": round(total / (1024**3), 2),
                    "free_percent": round(free_percent, 1)
                }
            )
            
        except Exception as e:
            return HealthStatus(
                component="disk_space",
                status="critical",
                message=f"Disk space check failed: {str(e)}",
                timestamp=time.time()
            )
    
    async def _check_memory_usage(self) -> HealthStatus:
        """بررسی استفاده از حافظه"""
        try:
            import psutil
            
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            if memory_percent <= 80:
                status = "healthy"
                message = f"Memory usage OK ({memory_percent:.1f}%)"
            elif memory_percent <= 90:
                status = "warning"
                message = f"High memory usage ({memory_percent:.1f}%)"
            else:
                status = "critical"
                message = f"Critical memory usage ({memory_percent:.1f}%)"
            
            return HealthStatus(
                component="memory_usage",
                status=status,
                message=message,
                timestamp=time.time(),
                details={
                    "used_gb": round(memory.used / (1024**3), 2),
                    "total_gb": round(memory.total / (1024**3), 2),
                    "percent": round(memory_percent, 1)
                }
            )
            
        except Exception as e:
            return HealthStatus(
                component="memory_usage",
                status="warning",
                message=f"Memory check failed: {str(e)}",
                timestamp=time.time()
            )
    
    async def _check_cache_performance(self) -> HealthStatus:
        """بررسی عملکرد کش"""
        try:
            from cache_manager import CacheManager
            
            cache = CacheManager()
            stats = cache.get_stats()
            hit_rate = float(stats['hit_rate'].replace('%', ''))
            
            if hit_rate >= 70:
                status = "healthy"
                message = f"Cache performance good ({stats['hit_rate']} hit rate)"
            elif hit_rate >= 50:
                status = "warning"
                message = f"Cache performance moderate ({stats['hit_rate']} hit rate)"
            else:
                status = "warning"
                message = f"Cache performance low ({stats['hit_rate']} hit rate)"
            
            return HealthStatus(
                component="cache_performance",
                status=status,
                message=message,
                timestamp=time.time(),
                details=stats
            )
            
        except Exception as e:
            return HealthStatus(
                component="cache_performance",
                status="warning",
                message=f"Cache check failed: {str(e)}",
                timestamp=time.time()
            )
    
    async def run_health_checks(self) -> Dict[str, HealthStatus]:
        """اجرای تمام چک‌های سلامت"""
        logger.info("Running health checks...")
        
        health_results = {}
        
        for check_name, check_func in self.health_checks.items():
            try:
                result = await check_func()
                health_results[check_name] = result
                self.last_health_report[check_name] = result
                self.health_history.append(result)
                
                # نگه داشتن فقط 100 رکورد آخر
                if len(self.health_history) > 100:
                    self.health_history = self.health_history[-100:]
                
                logger.debug(f"Health check {check_name}: {result.status} - {result.message}")
                
            except Exception as e:
                error_result = HealthStatus(
                    component=check_name,
                    status="critical",
                    message=f"Health check failed: {str(e)}",
                    timestamp=time.time()
                )
                health_results[check_name] = error_result
                logger.error(f"Health check {check_name} failed: {e}")
        
        logger.info("Health checks completed")
        return health_results
    
    def get_overall_status(self) -> str:
        """دریافت وضعیت کلی سیستم"""
        if not self.last_health_report:
            return "unknown"
        
        statuses = [status.status for status in self.last_health_report.values()]
        
        if "critical" in statuses:
            return "critical"
        elif "warning" in statuses:
            return "warning"
        else:
            return "healthy"
    
    def get_health_summary(self) -> Dict:
        """دریافت خلاصه وضعیت سلامت"""
        overall_status = self.get_overall_status()
        
        summary = {
            "overall_status": overall_status,
            "timestamp": datetime.now().isoformat(),
            "components": {},
            "statistics": {
                "total_checks": len(self.last_health_report),
                "healthy": len([s for s in self.last_health_report.values() if s.status == "healthy"]),
                "warning": len([s for s in self.last_health_report.values() if s.status == "warning"]),
                "critical": len([s for s in self.last_health_report.values() if s.status == "critical"])
            }
        }
        
        for name, status in self.last_health_report.items():
            summary["components"][name] = {
                "status": status.status,
                "message": status.message,
                "response_time": status.response_time,
                "details": status.details
            }
        
        return summary

# نمونه استفاده
async def main():
    """نمونه استفاده از Health Monitor"""
    logging.basicConfig(level=logging.INFO)
    
    monitor = HealthMonitor()
    
    # اجرای چک‌های سلامت
    results = await monitor.run_health_checks()
    
    # نمایش نتایج
    print("\n🏥 Health Check Results:")
    print("=" * 50)
    
    for name, status in results.items():
        emoji = "✅" if status.status == "healthy" else "⚠️" if status.status == "warning" else "❌"
        print(f"{emoji} {name}: {status.status.upper()}")
        print(f"   {status.message}")
        if status.response_time > 0:
            print(f"   Response time: {status.response_time:.1f}ms")
        print()
    
    # نمایش خلاصه
    summary = monitor.get_health_summary()
    print(f"Overall Status: {summary['overall_status'].upper()}")
    print(f"Statistics: {summary['statistics']}")

if __name__ == "__main__":
    asyncio.run(main())
