#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ML-based Config Scoring System
سیستم امتیازدهی هوشمند به کانفیگ‌ها
"""

import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
import json
import math

logger = logging.getLogger(__name__)

@dataclass
class ConfigScore:
    """امتیاز کانفیگ"""
    total_score: float
    latency_score: float
    reliability_score: float
    location_score: float
    protocol_score: float
    details: Dict

class MLConfigScorer:
    """امتیازدهی هوشمند به کانفیگ‌ها"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # وزن‌های امتیازدهی
        self.weights = {
            'latency': 0.35,      # 35% - مهم‌ترین فاکتور
            'reliability': 0.30,   # 30% - پایداری
            'location': 0.20,      # 20% - موقعیت جغرافیایی
            'protocol': 0.15       # 15% - نوع پروتکل
        }
        
        # امتیاز پروتکل‌ها (بر اساس عملکرد)
        self.protocol_scores = {
            'vless': 1.0,      # بهترین
            'vmess': 0.9,
            'trojan': 0.85,
            'hysteria': 0.95,
            'hysteria2': 0.95,
            'ss': 0.8,
            'ssr': 0.7,
            'tuic': 0.9,
            'wireguard': 0.95
        }
        
        # امتیاز کشورها (بر اساس proximity به ایران)
        self.country_scores = {
            'IR': 1.0,    # ایران - بهترین
            'TR': 0.95,   # ترکیه - نزدیک
            'AE': 0.9,    # امارات
            'DE': 0.8,    # آلمان
            'NL': 0.8,    # هلند
            'FR': 0.75,   # فرانسه
            'GB': 0.75,   # انگلیس
            'US': 0.6,    # آمریکا - دور
            'SG': 0.7,    # سنگاپور
            'JP': 0.65,   # ژاپن
            'HK': 0.7,    # هنگ کنگ
            'CA': 0.6,    # کانادا
            'AU': 0.5,    # استرالیا - خیلی دور
        }
        
        # تاریخچه عملکرد (می‌تواند از database بیاید)
        self.performance_history = {}
        
    def calculate_latency_score(self, latency_ms: float) -> float:
        """
        محاسبه امتیاز بر اساس تأخیر
        
        Args:
            latency_ms: تأخیر به میلی‌ثانیه
            
        Returns:
            امتیاز بین 0 تا 1
        """
        if latency_ms <= 0:
            return 0.0
        
        # فرمول: exp(-latency/200)
        # Latency 50ms → Score ~0.78
        # Latency 100ms → Score ~0.61
        # Latency 200ms → Score ~0.37
        # Latency 500ms → Score ~0.08
        
        score = math.exp(-latency_ms / 200)
        return max(0.0, min(1.0, score))
    
    def calculate_reliability_score(self, config_id: str, success_count: int = 0, total_tests: int = 1) -> float:
        """
        محاسبه امتیاز قابلیت اطمینان
        
        Args:
            config_id: شناسه کانفیگ
            success_count: تعداد موفقیت‌ها
            total_tests: کل تست‌ها
            
        Returns:
            امتیاز بین 0 تا 1
        """
        if total_tests == 0:
            return 0.5  # مقدار پیش‌فرض
        
        # استفاده از تاریخچه
        if config_id in self.performance_history:
            history = self.performance_history[config_id]
            success_count = history.get('success', 0)
            total_tests = history.get('total', 1)
        
        # فرمول: success_rate با وزن تاریخچه
        success_rate = success_count / total_tests
        
        # اضافه کردن وزن برای تعداد تست‌ها (اعتماد بیشتر با تست‌های بیشتر)
        confidence = min(1.0, total_tests / 10.0)  # تا 10 تست
        
        return success_rate * confidence + 0.5 * (1 - confidence)
    
    def calculate_location_score(self, country: str) -> float:
        """
        محاسبه امتیاز موقعیت جغرافیایی
        
        Args:
            country: کد کشور
            
        Returns:
            امتیاز بین 0 تا 1
        """
        return self.country_scores.get(country.upper(), 0.5)  # پیش‌فرض 0.5
    
    def calculate_protocol_score(self, protocol: str) -> float:
        """
        محاسبه امتیاز پروتکل
        
        Args:
            protocol: نوع پروتکل
            
        Returns:
            امتیاز بین 0 تا 1
        """
        return self.protocol_scores.get(protocol.lower(), 0.5)
    
    def score_config(self, config: Dict) -> ConfigScore:
        """
        امتیازدهی کامل به یک کانفیگ
        
        Args:
            config: اطلاعات کانفیگ
            
        Returns:
            ConfigScore
        """
        # استخراج اطلاعات
        latency = float(config.get('latency', '999ms').replace('ms', ''))
        protocol = config.get('protocol', 'unknown')
        country = config.get('country', 'XX')
        config_id = config.get('id', config.get('address', 'unknown'))
        
        # محاسبه امتیازها
        latency_score = self.calculate_latency_score(latency)
        reliability_score = self.calculate_reliability_score(config_id)
        location_score = self.calculate_location_score(country)
        protocol_score = self.calculate_protocol_score(protocol)
        
        # امتیاز نهایی (میانگین وزن‌دار)
        total_score = (
            latency_score * self.weights['latency'] +
            reliability_score * self.weights['reliability'] +
            location_score * self.weights['location'] +
            protocol_score * self.weights['protocol']
        )
        
        return ConfigScore(
            total_score=round(total_score, 3),
            latency_score=round(latency_score, 3),
            reliability_score=round(reliability_score, 3),
            location_score=round(location_score, 3),
            protocol_score=round(protocol_score, 3),
            details={
                'latency_ms': latency,
                'protocol': protocol,
                'country': country,
                'recommendation': self._get_recommendation(total_score)
            }
        )
    
    def _get_recommendation(self, score: float) -> str:
        """دریافت توصیه بر اساس امتیاز"""
        if score >= 0.8:
            return "🌟 عالی - بسیار توصیه می‌شود"
        elif score >= 0.6:
            return "✅ خوب - توصیه می‌شود"
        elif score >= 0.4:
            return "⚠️ متوسط - با احتیاط استفاده کنید"
        else:
            return "❌ ضعیف - توصیه نمی‌شود"
    
    def rank_configs(self, configs: List[Dict], top_n: int = 10) -> List[tuple]:
        """
        رتبه‌بندی کانفیگ‌ها
        
        Args:
            configs: لیست کانفیگ‌ها
            top_n: تعداد برترین‌ها
            
        Returns:
            لیست (config, score) مرتب شده
        """
        scored_configs = []
        
        for config in configs:
            score = self.score_config(config)
            scored_configs.append((config, score))
        
        # مرتب‌سازی بر اساس امتیاز
        scored_configs.sort(key=lambda x: x[1].total_score, reverse=True)
        
        return scored_configs[:top_n]
    
    def update_performance_history(self, config_id: str, success: bool):
        """
        بروزرسانی تاریخچه عملکرد
        
        Args:
            config_id: شناسه کانفیگ
            success: موفق بود یا نه
        """
        if config_id not in self.performance_history:
            self.performance_history[config_id] = {'success': 0, 'total': 0}
        
        self.performance_history[config_id]['total'] += 1
        if success:
            self.performance_history[config_id]['success'] += 1
    
    def save_performance_history(self, filename: str = 'performance_history.json'):
        """ذخیره تاریخچه عملکرد"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.performance_history, f, indent=2)
            self.logger.info(f"✅ Performance history saved")
        except Exception as e:
            self.logger.error(f"❌ Error saving history: {e}")
    
    def load_performance_history(self, filename: str = 'performance_history.json'):
        """بارگذاری تاریخچه عملکرد"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.performance_history = json.load(f)
            self.logger.info(f"✅ Performance history loaded")
        except Exception as e:
            self.logger.debug(f"No performance history found")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test
    scorer = MLConfigScorer()
    
    test_configs = [
        {'protocol': 'vless', 'country': 'TR', 'latency': '50ms', 'address': 'test1.com'},
        {'protocol': 'vmess', 'country': 'US', 'latency': '200ms', 'address': 'test2.com'},
        {'protocol': 'trojan', 'country': 'DE', 'latency': '100ms', 'address': 'test3.com'},
    ]
    
    print("\n🎯 ML CONFIG SCORING TEST")
    print("="*60)
    
    top_configs = scorer.rank_configs(test_configs, top_n=3)
    
    for i, (config, score) in enumerate(top_configs, 1):
        print(f"\n{i}. {config['protocol']} - {config['country']} ({config['latency']})")
        print(f"   Total Score: {score.total_score:.3f}")
        print(f"   Latency: {score.latency_score:.3f}")
        print(f"   Reliability: {score.reliability_score:.3f}")
        print(f"   Location: {score.location_score:.3f}")
        print(f"   Protocol: {score.protocol_score:.3f}")
        print(f"   {score.details['recommendation']}")

