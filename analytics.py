#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Analytics for V2Ray Collector
تحلیل‌های پیشرفته برای V2Ray Collector
"""

import json
import time
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter

@dataclass
class PerformanceMetrics:
    """معیارهای عملکرد"""
    total_configs: int
    working_configs: int
    failed_configs: int
    success_rate: float
    avg_latency: float
    median_latency: float
    protocol_distribution: Dict[str, int]
    country_distribution: Dict[str, int]
    latency_distribution: Dict[str, int]
    top_performing_protocols: List[Dict[str, Any]]
    top_performing_countries: List[Dict[str, Any]]

@dataclass
class TrendAnalysis:
    """تحلیل روند"""
    period: str
    config_count_trend: str  # increasing, decreasing, stable
    success_rate_trend: str
    latency_trend: str
    top_growing_protocols: List[str]
    top_declining_protocols: List[str]

class AdvancedAnalytics:
    """تحلیل‌های پیشرفته سیستم"""
    
    def __init__(self, data_dir: str = "analytics"):
        self.data_dir = data_dir
        self.historical_data: List[Dict] = []
        self.load_historical_data()
    
    def load_historical_data(self):
        """بارگذاری داده‌های تاریخی"""
        try:
            with open(f"{self.data_dir}/historical_data.json", 'r', encoding='utf-8') as f:
                self.historical_data = json.load(f)
        except FileNotFoundError:
            self.historical_data = []
    
    def save_historical_data(self):
        """ذخیره داده‌های تاریخی"""
        import os
        os.makedirs(self.data_dir, exist_ok=True)
        
        with open(f"{self.data_dir}/historical_data.json", 'w', encoding='utf-8') as f:
            json.dump(self.historical_data, f, ensure_ascii=False, indent=2)
    
    def analyze_current_performance(self, working_configs: List, failed_configs: List) -> PerformanceMetrics:
        """تحلیل عملکرد فعلی"""
        
        all_configs = working_configs + failed_configs
        total_configs = len(all_configs)
        working_count = len(working_configs)
        failed_count = len(failed_configs)
        success_rate = (working_count / total_configs * 100) if total_configs > 0 else 0
        
        # تحلیل تأخیر
        latencies = [config.latency for config in working_configs if config.latency > 0]
        avg_latency = statistics.mean(latencies) if latencies else 0
        median_latency = statistics.median(latencies) if latencies else 0
        
        # توزیع پروتکل‌ها
        protocol_counts = Counter(config.protocol for config in all_configs)
        protocol_distribution = dict(protocol_counts)
        
        # توزیع کشورها
        country_counts = Counter(config.country for config in working_configs)
        country_distribution = dict(country_counts)
        
        # توزیع تأخیر
        latency_ranges = {
            "0-100ms": 0,
            "100-300ms": 0,
            "300-500ms": 0,
            "500-1000ms": 0,
            "1000ms+": 0
        }
        
        for latency in latencies:
            if latency <= 100:
                latency_ranges["0-100ms"] += 1
            elif latency <= 300:
                latency_ranges["100-300ms"] += 1
            elif latency <= 500:
                latency_ranges["300-500ms"] += 1
            elif latency <= 1000:
                latency_ranges["500-1000ms"] += 1
            else:
                latency_ranges["1000ms+"] += 1
        
        # بهترین پروتکل‌ها بر اساس عملکرد
        protocol_performance = {}
        for protocol in protocol_distribution.keys():
            protocol_configs = [c for c in working_configs if c.protocol == protocol]
            if protocol_configs:
                protocol_latencies = [c.latency for c in protocol_configs if c.latency > 0]
                if protocol_latencies:
                    protocol_performance[protocol] = {
                        "count": len(protocol_configs),
                        "avg_latency": statistics.mean(protocol_latencies),
                        "success_rate": (len(protocol_configs) / protocol_distribution[protocol]) * 100
                    }
        
        top_performing_protocols = sorted(
            protocol_performance.items(),
            key=lambda x: (x[1]["success_rate"], -x[1]["avg_latency"]),
            reverse=True
        )[:5]
        
        # بهترین کشورها
        country_performance = {}
        for country in country_distribution.keys():
            country_configs = [c for c in working_configs if c.country == country]
            if country_configs:
                country_latencies = [c.latency for c in country_configs if c.latency > 0]
                if country_latencies:
                    country_performance[country] = {
                        "count": len(country_configs),
                        "avg_latency": statistics.mean(country_latencies)
                    }
        
        top_performing_countries = sorted(
            country_performance.items(),
            key=lambda x: (-x[1]["count"], x[1]["avg_latency"])
        )[:5]
        
        return PerformanceMetrics(
            total_configs=total_configs,
            working_configs=working_count,
            failed_configs=failed_count,
            success_rate=success_rate,
            avg_latency=avg_latency,
            median_latency=median_latency,
            protocol_distribution=protocol_distribution,
            country_distribution=country_distribution,
            latency_distribution=latency_ranges,
            top_performing_protocols=[{"protocol": k, **v} for k, v in top_performing_protocols],
            top_performing_countries=[{"country": k, **v} for k, v in top_performing_countries]
        )
    
    def analyze_trends(self, days: int = 7) -> TrendAnalysis:
        """تحلیل روندها"""
        if len(self.historical_data) < 2:
            return TrendAnalysis(
                period=f"{days} days",
                config_count_trend="stable",
                success_rate_trend="stable",
                latency_trend="stable",
                top_growing_protocols=[],
                top_declining_protocols=[]
            )
        
        # فیلتر داده‌های روزهای اخیر
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_data = [
            d for d in self.historical_data 
            if datetime.fromisoformat(d['timestamp']) >= cutoff_date
        ]
        
        if len(recent_data) < 2:
            return TrendAnalysis(
                period=f"{days} days",
                config_count_trend="stable",
                success_rate_trend="stable",
                latency_trend="stable",
                top_growing_protocols=[],
                top_declining_protocols=[]
            )
        
        # تحلیل روند تعداد کانفیگ‌ها
        config_counts = [d['total_configs'] for d in recent_data]
        config_trend = self._calculate_trend(config_counts)
        
        # تحلیل روند نرخ موفقیت
        success_rates = [d['success_rate'] for d in recent_data]
        success_trend = self._calculate_trend(success_rates)
        
        # تحلیل روند تأخیر
        avg_latencies = [d['avg_latency'] for d in recent_data]
        latency_trend = self._calculate_trend(avg_latencies, reverse=True)  # کمتر = بهتر
        
        # تحلیل روند پروتکل‌ها
        protocol_trends = self._analyze_protocol_trends(recent_data)
        growing_protocols = [p for p, trend in protocol_trends.items() if trend > 0.1]
        declining_protocols = [p for p, trend in protocol_trends.items() if trend < -0.1]
        
        return TrendAnalysis(
            period=f"{days} days",
            config_count_trend=config_trend,
            success_rate_trend=success_trend,
            latency_trend=latency_trend,
            top_growing_protocols=growing_protocols[:3],
            top_declining_protocols=declining_protocols[:3]
        )
    
    def _calculate_trend(self, values: List[float], reverse: bool = False) -> str:
        """محاسبه روند"""
        if len(values) < 2:
            return "stable"
        
        # محاسبه شیب خط روند
        n = len(values)
        x = list(range(n))
        
        # رگرسیون خطی ساده
        sum_x = sum(x)
        sum_y = sum(values)
        sum_xy = sum(x[i] * values[i] for i in range(n))
        sum_x2 = sum(x[i] ** 2 for i in range(n))
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        
        if reverse:
            slope = -slope
        
        if slope > 0.1:
            return "increasing"
        elif slope < -0.1:
            return "decreasing"
        else:
            return "stable"
    
    def _analyze_protocol_trends(self, data: List[Dict]) -> Dict[str, float]:
        """تحلیل روند پروتکل‌ها"""
        if len(data) < 2:
            return {}
        
        protocol_trends = {}
        
        # جمع‌آوری داده‌های پروتکل‌ها
        for entry in data:
            for protocol, count in entry.get('protocol_distribution', {}).items():
                if protocol not in protocol_trends:
                    protocol_trends[protocol] = []
                protocol_trends[protocol].append(count)
        
        # محاسبه روند هر پروتکل
        result = {}
        for protocol, counts in protocol_trends.items():
            if len(counts) >= 2:
                trend = self._calculate_trend(counts)
                if trend == "increasing":
                    result[protocol] = 0.2
                elif trend == "decreasing":
                    result[protocol] = -0.2
                else:
                    result[protocol] = 0.0
        
        return result
    
    def generate_report(self, working_configs: List, failed_configs: List) -> Dict[str, Any]:
        """تولید گزارش جامع"""
        
        # تحلیل عملکرد فعلی
        current_performance = self.analyze_current_performance(working_configs, failed_configs)
        
        # تحلیل روندها
        trends = self.analyze_trends()
        
        # ذخیره داده‌های فعلی
        current_data = {
            "timestamp": datetime.now().isoformat(),
            "total_configs": current_performance.total_configs,
            "working_configs": current_performance.working_configs,
            "failed_configs": current_performance.failed_configs,
            "success_rate": current_performance.success_rate,
            "avg_latency": current_performance.avg_latency,
            "median_latency": current_performance.median_latency,
            "protocol_distribution": current_performance.protocol_distribution,
            "country_distribution": current_performance.country_distribution,
            "latency_distribution": current_performance.latency_distribution
        }
        
        self.historical_data.append(current_data)
        
        # نگه داشتن فقط 30 روز داده
        cutoff_date = datetime.now() - timedelta(days=30)
        self.historical_data = [
            d for d in self.historical_data 
            if datetime.fromisoformat(d['timestamp']) >= cutoff_date
        ]
        
        # ذخیره داده‌های تاریخی
        self.save_historical_data()
        
        # تولید گزارش
        report = {
            "generated_at": datetime.now().isoformat(),
            "current_performance": asdict(current_performance),
            "trends": asdict(trends),
            "summary": {
                "overall_status": "excellent" if current_performance.success_rate > 80 else "good" if current_performance.success_rate > 60 else "needs_improvement",
                "key_insights": self._generate_key_insights(current_performance, trends),
                "recommendations": self._generate_recommendations(current_performance, trends)
            }
        }
        
        return report
    
    def _generate_key_insights(self, performance: PerformanceMetrics, trends: TrendAnalysis) -> List[str]:
        """تولید بینش‌های کلیدی"""
        insights = []
        
        if performance.success_rate > 80:
            insights.append(f"عالی! نرخ موفقیت {performance.success_rate:.1f}% است")
        elif performance.success_rate > 60:
            insights.append(f"خوب، اما نرخ موفقیت {performance.success_rate:.1f}% قابل بهبود است")
        else:
            insights.append(f"نرخ موفقیت {performance.success_rate:.1f}% نیاز به بهبود دارد")
        
        if performance.avg_latency < 300:
            insights.append(f"تأخیر متوسط {performance.avg_latency:.0f}ms عالی است")
        elif performance.avg_latency < 500:
            insights.append(f"تأخیر متوسط {performance.avg_latency:.0f}ms قابل قبول است")
        else:
            insights.append(f"تأخیر متوسط {performance.avg_latency:.0f}ms بالا است")
        
        top_protocol = max(performance.protocol_distribution.items(), key=lambda x: x[1])
        insights.append(f"پروتکل محبوب: {top_protocol[0]} با {top_protocol[1]} کانفیگ")
        
        if trends.config_count_trend == "increasing":
            insights.append("روند مثبت: تعداد کانفیگ‌ها در حال افزایش است")
        elif trends.config_count_trend == "decreasing":
            insights.append("هشدار: تعداد کانفیگ‌ها در حال کاهش است")
        
        return insights
    
    def _generate_recommendations(self, performance: PerformanceMetrics, trends: TrendAnalysis) -> List[str]:
        """تولید توصیه‌ها"""
        recommendations = []
        
        if performance.success_rate < 70:
            recommendations.append("افزایش منابع کانفیگ با کیفیت بالا")
        
        if performance.avg_latency > 500:
            recommendations.append("بهینه‌سازی تست‌های اتصال و فیلتر کردن سرورهای کند")
        
        if len(performance.protocol_distribution) < 3:
            recommendations.append("افزایش تنوع پروتکل‌ها")
        
        if trends.latency_trend == "increasing":
            recommendations.append("بررسی و بهینه‌سازی منابع کند")
        
        if trends.success_rate_trend == "decreasing":
            recommendations.append("بررسی کیفیت منابع و حذف منابع ناسالم")
        
        return recommendations

# نمونه استفاده
if __name__ == "__main__":
    from config_collector import V2RayConfig
    
    # نمونه داده‌ها
    working_configs = [
        V2RayConfig("vmess", "test1.com", 443, "uuid1", latency=200, country="US"),
        V2RayConfig("vless", "test2.com", 443, "uuid2", latency=150, country="DE"),
        V2RayConfig("trojan", "test3.com", 443, "uuid3", latency=300, country="US"),
    ]
    
    failed_configs = [
        V2RayConfig("vmess", "bad1.com", 443, "uuid4", country="CN"),
        V2RayConfig("vless", "bad2.com", 443, "uuid5", country="RU"),
    ]
    
    # ایجاد تحلیلگر
    analytics = AdvancedAnalytics()
    
    # تولید گزارش
    report = analytics.generate_report(working_configs, failed_configs)
    
    print("📊 Advanced Analytics Report:")
    print("=" * 50)
    print(f"Success Rate: {report['current_performance']['success_rate']:.1f}%")
    print(f"Average Latency: {report['current_performance']['avg_latency']:.0f}ms")
    print(f"Total Configs: {report['current_performance']['total_configs']}")
    print(f"Working Configs: {report['current_performance']['working_configs']}")
    
    print("\n🔍 Key Insights:")
    for insight in report['summary']['key_insights']:
        print(f"• {insight}")
    
    print("\n💡 Recommendations:")
    for rec in report['summary']['recommendations']:
        print(f"• {rec}")
