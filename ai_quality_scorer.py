#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Quality Scorer - سیستم هوش مصنوعی برای ارزیابی کیفیت کانفیگ‌های V2Ray
AI-Powered Quality Assessment System for V2Ray Configurations
"""

import json
import re
import time
import hashlib
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os

# تنظیمات لاگ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class QualityMetrics:
    """متریک‌های کیفیت کانفیگ"""
    latency_score: float = 0.0
    stability_score: float = 0.0
    security_score: float = 0.0
    performance_score: float = 0.0
    reliability_score: float = 0.0
    overall_score: float = 0.0
    confidence_level: float = 0.0


@dataclass
class ConfigFeatures:
    """ویژگی‌های استخراج شده از کانفیگ"""
    protocol: str
    encryption: str
    network_type: str
    port: int
    has_tls: bool
    has_reality: bool
    has_ws: bool
    has_grpc: bool
    has_quic: bool
    server_country: str
    latency: float
    uptime_percentage: float
    error_rate: float
    bandwidth_utilization: float
    connection_attempts: int
    success_rate: float


class AIQualityScorer:
    """سیستم هوش مصنوعی برای ارزیابی کیفیت کانفیگ‌ها"""

    def __init__(self, model_path: str = "models/quality_model.pkl"):
        self.model_path = model_path
        self.model = None
        self.scaler = StandardScaler()
        self.feature_importance = {}
        self.quality_thresholds = {
            'excellent': 0.85,
            'good': 0.70,
            'average': 0.50,
            'poor': 0.30
        }

        # ایجاد پوشه models اگر وجود نداشته باشد
        os.makedirs(os.path.dirname(model_path), exist_ok=True)

        # بارگذاری یا ایجاد مدل
        self._load_or_create_model()

    def _load_or_create_model(self):
        """بارگذاری یا ایجاد مدل ML"""
        try:
            if os.path.exists(self.model_path):
                logger.info("🔄 بارگذاری مدل موجود...")
                model_data = joblib.load(self.model_path)
                self.model = model_data['model']
                self.scaler = model_data['scaler']
                self.feature_importance = model_data.get(
                    'feature_importance', {})
                logger.info("✅ مدل با موفقیت بارگذاری شد")
            else:
                logger.info("🆕 ایجاد مدل جدید...")
                self._create_new_model()
        except Exception as e:
            logger.error(f"❌ خطا در بارگذاری مدل: {e}")
            self._create_new_model()

    def _create_new_model(self):
        """ایجاد مدل جدید با داده‌های نمونه"""
        logger.info("🧠 آموزش مدل جدید...")

        # تولید داده‌های نمونه برای آموزش
        training_data = self._generate_training_data()

        if len(training_data) < 10:
            logger.warning(
                "⚠️ داده‌های آموزشی کافی نیست، استفاده از مدل پیش‌فرض")
            self._create_default_model()
            return

        # استخراج ویژگی‌ها و برچسب‌ها
        X = np.array([self._extract_features_vector(data['features'])
                     for data in training_data])
        y = np.array([data['quality_score'] for data in training_data])

        # تقسیم داده‌ها
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # نرمال‌سازی ویژگی‌ها
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # آموزش مدل
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )

        self.model.fit(X_train_scaled, y_train)

        # محاسبه اهمیت ویژگی‌ها
        self.feature_importance = dict(zip(
            self._get_feature_names(),
            self.model.feature_importances_
        ))

        # ذخیره مدل
        self._save_model()

        # ارزیابی مدل
        train_score = self.model.score(X_train_scaled, y_train)
        test_score = self.model.score(X_test_scaled, y_test)

        logger.info(f"📊 امتیاز آموزش: {train_score:.3f}")
        logger.info(f"📊 امتیاز تست: {test_score:.3f}")
        logger.info("✅ مدل جدید با موفقیت ایجاد شد")

    def _create_default_model(self):
        """ایجاد مدل پیش‌فرض ساده"""
        self.model = RandomForestRegressor(n_estimators=10, random_state=42)
        # آموزش با داده‌های پیش‌فرض
        X_dummy = np.random.rand(50, len(self._get_feature_names()))
        y_dummy = np.random.rand(50)
        X_scaled = self.scaler.fit_transform(X_dummy)
        self.model.fit(X_scaled, y_dummy)
        self._save_model()

    def _generate_training_data(self) -> List[Dict]:
        """تولید داده‌های آموزشی نمونه"""
        training_data = []

        # نمونه‌های مختلف کانفیگ
        sample_configs = [
            {
                'protocol': 'vless',
                'encryption': 'none',
                'network_type': 'ws',
                'port': 443,
                'has_tls': True,
                'has_reality': True,
                'latency': 50.0,
                'uptime': 99.5,
                'quality_score': 0.95
            },
            {
                'protocol': 'vmess',
                'encryption': 'auto',
                'network_type': 'tcp',
                'port': 80,
                'has_tls': False,
                'has_reality': False,
                'latency': 200.0,
                'uptime': 85.0,
                'quality_score': 0.65
            },
            {
                'protocol': 'trojan',
                'encryption': 'aes-256-gcm',
                'network_type': 'grpc',
                'port': 443,
                'has_tls': True,
                'has_reality': False,
                'latency': 80.0,
                'uptime': 95.0,
                'quality_score': 0.85
            }
        ]

        # تولید داده‌های بیشتر
        for base_config in sample_configs:
            for _ in range(20):  # 20 نمونه از هر نوع
                config = base_config.copy()
                # تغییرات تصادفی
                config['latency'] += np.random.normal(0, 20)
                config['uptime'] += np.random.normal(0, 5)
                config['quality_score'] = self._calculate_manual_score(config)

                features = ConfigFeatures(
                    protocol=config['protocol'],
                    encryption=config['encryption'],
                    network_type=config['network_type'],
                    port=config['port'],
                    has_tls=config['has_tls'],
                    has_reality=config['has_reality'],
                    has_ws=config['network_type'] == 'ws',
                    has_grpc=config['network_type'] == 'grpc',
                    has_quic=config['network_type'] == 'quic',
                    server_country='US',
                    latency=config['latency'],
                    uptime_percentage=config['uptime'],
                    error_rate=100 - config['uptime'],
                    bandwidth_utilization=50.0,
                    connection_attempts=100,
                    success_rate=config['uptime'] / 100
                )

                training_data.append({
                    'features': features,
                    'quality_score': config['quality_score']
                })

        return training_data

    def _calculate_manual_score(self, config: Dict) -> float:
        """محاسبه دستی امتیاز کیفیت"""
        score = 0.5  # امتیاز پایه

        # تأخیر (0-0.3)
        if config['latency'] < 100:
            score += 0.3
        elif config['latency'] < 200:
            score += 0.2
        elif config['latency'] < 500:
            score += 0.1

        # Uptime (0-0.3)
        if config['uptime'] > 95:
            score += 0.3
        elif config['uptime'] > 90:
            score += 0.2
        elif config['uptime'] > 80:
            score += 0.1

        # پروتکل (0-0.2)
        if config['protocol'] in ['vless', 'trojan']:
            score += 0.2
        elif config['protocol'] == 'vmess':
            score += 0.15
        else:
            score += 0.1

        # امنیت (0-0.2)
        if config['has_tls'] and config['has_reality']:
            score += 0.2
        elif config['has_tls']:
            score += 0.15
        else:
            score += 0.05

        return min(1.0, max(0.0, score))

    def _extract_features_vector(self, features: ConfigFeatures) -> List[float]:
        """استخراج بردار ویژگی‌ها"""
        # تبدیل ویژگی‌های کیفی به عددی
        protocol_map = {'vless': 1.0, 'vmess': 0.8,
                        'trojan': 0.9, 'ss': 0.6, 'ssr': 0.7}
        encryption_map = {'none': 0.3, 'auto': 0.5,
                          'aes-256-gcm': 0.9, 'chacha20-poly1305': 0.8}
        network_map = {'ws': 0.8, 'tcp': 0.6,
                       'grpc': 0.9, 'quic': 0.7, 'h2': 0.8}

        return [
            protocol_map.get(features.protocol, 0.5),
            encryption_map.get(features.encryption, 0.5),
            network_map.get(features.network_type, 0.5),
            features.port / 65535.0,  # نرمال‌سازی پورت
            float(features.has_tls),
            float(features.has_reality),
            float(features.has_ws),
            float(features.has_grpc),
            float(features.has_quic),
            features.latency / 1000.0,  # نرمال‌سازی تأخیر
            features.uptime_percentage / 100.0,
            features.error_rate / 100.0,
            features.bandwidth_utilization / 100.0,
            features.connection_attempts / 1000.0,
            features.success_rate
        ]

    def _get_feature_names(self) -> List[str]:
        """نام‌های ویژگی‌ها"""
        return [
            'protocol_score', 'encryption_score', 'network_score', 'port_normalized',
            'has_tls', 'has_reality', 'has_ws', 'has_grpc', 'has_quic',
            'latency_normalized', 'uptime_normalized', 'error_rate_normalized',
            'bandwidth_normalized', 'attempts_normalized', 'success_rate'
        ]

    def _save_model(self):
        """ذخیره مدل"""
        try:
            model_data = {
                'model': self.model,
                'scaler': self.scaler,
                'feature_importance': self.feature_importance,
                'timestamp': datetime.now().isoformat()
            }
            joblib.dump(model_data, self.model_path)
            logger.info(f"💾 مدل در {self.model_path} ذخیره شد")
        except Exception as e:
            logger.error(f"❌ خطا در ذخیره مدل: {e}")

    def extract_config_features(self, config_data: Dict) -> ConfigFeatures:
        """استخراج ویژگی‌های کانفیگ"""
        try:
            # استخراج اطلاعات پایه
            protocol = config_data.get('protocol', 'unknown')
            port = config_data.get('port', 443)
            server = config_data.get('server', '')

            # تشخیص نوع شبکه
            network_type = 'tcp'
            if 'ws' in config_data.get('network', '').lower():
                network_type = 'ws'
            elif 'grpc' in config_data.get('network', '').lower():
                network_type = 'grpc'
            elif 'quic' in config_data.get('network', '').lower():
                network_type = 'quic'

            # تشخیص TLS و Reality
            has_tls = config_data.get(
                'tls', False) or 'tls' in str(config_data).lower()
            has_reality = 'reality' in str(config_data).lower()

            # تشخیص رمزنگاری
            encryption = config_data.get('encryption', 'auto')
            if not encryption or encryption == 'auto':
                if protocol == 'vless':
                    encryption = 'none'
                elif protocol == 'vmess':
                    encryption = 'auto'
                elif protocol == 'trojan':
                    encryption = 'aes-256-gcm'

            return ConfigFeatures(
                protocol=protocol,
                encryption=encryption,
                network_type=network_type,
                port=port,
                has_tls=has_tls,
                has_reality=has_reality,
                has_ws=network_type == 'ws',
                has_grpc=network_type == 'grpc',
                has_quic=network_type == 'quic',
                server_country=config_data.get('country', 'unknown'),
                latency=config_data.get('latency', 0.0),
                uptime_percentage=config_data.get('uptime', 0.0),
                error_rate=config_data.get('error_rate', 0.0),
                bandwidth_utilization=config_data.get(
                    'bandwidth_utilization', 0.0),
                connection_attempts=config_data.get('connection_attempts', 0),
                success_rate=config_data.get('success_rate', 0.0)
            )
        except Exception as e:
            logger.error(f"❌ خطا در استخراج ویژگی‌ها: {e}")
            return ConfigFeatures()

    def predict_quality(self, config_data: Dict) -> QualityMetrics:
        """پیش‌بینی کیفیت کانفیگ"""
        try:
            # استخراج ویژگی‌ها
            features = self.extract_config_features(config_data)

            # تبدیل به بردار
            feature_vector = np.array(
                [self._extract_features_vector(features)]).reshape(1, -1)

            # نرمال‌سازی
            feature_vector_scaled = self.scaler.transform(feature_vector)

            # پیش‌بینی
            overall_score = self.model.predict(feature_vector_scaled)[0]
            # محدود کردن به [0,1]
            overall_score = max(0.0, min(1.0, overall_score))

            # محاسبه متریک‌های جزئی
            metrics = self._calculate_detailed_metrics(features, overall_score)

            return metrics

        except Exception as e:
            logger.error(f"❌ خطا در پیش‌بینی کیفیت: {e}")
            return QualityMetrics()

    def _calculate_detailed_metrics(self, features: ConfigFeatures, overall_score: float) -> QualityMetrics:
        """محاسبه متریک‌های تفصیلی"""
        # امتیاز تأخیر
        if features.latency <= 50:
            latency_score = 1.0
        elif features.latency <= 100:
            latency_score = 0.8
        elif features.latency <= 200:
            latency_score = 0.6
        elif features.latency <= 500:
            latency_score = 0.4
        else:
            latency_score = 0.2

        # امتیاز پایداری
        stability_score = features.uptime_percentage / 100.0

        # امتیاز امنیت
        security_score = 0.3  # پایه
        if features.has_tls:
            security_score += 0.3
        if features.has_reality:
            security_score += 0.2
        if features.encryption in ['aes-256-gcm', 'chacha20-poly1305']:
            security_score += 0.2

        # امتیاز عملکرد
        performance_score = 0.5  # پایه
        if features.protocol in ['vless', 'trojan']:
            performance_score += 0.3
        elif features.protocol == 'vmess':
            performance_score += 0.2
        if features.network_type in ['grpc', 'quic']:
            performance_score += 0.2

        # امتیاز قابلیت اطمینان
        reliability_score = features.success_rate

        # سطح اطمینان
        confidence_level = min(1.0, len([f for f in [
                               features.latency, features.uptime_percentage, features.success_rate] if f > 0]) / 3.0)

        return QualityMetrics(
            latency_score=latency_score,
            stability_score=stability_score,
            security_score=security_score,
            performance_score=performance_score,
            reliability_score=reliability_score,
            overall_score=overall_score,
            confidence_level=confidence_level
        )

    def get_quality_category(self, score: float) -> str:
        """دریافت دسته‌بندی کیفیت"""
        if score >= self.quality_thresholds['excellent']:
            return 'excellent'
        elif score >= self.quality_thresholds['good']:
            return 'good'
        elif score >= self.quality_thresholds['average']:
            return 'average'
        else:
            return 'poor'

    def get_feature_importance(self) -> Dict[str, float]:
        """دریافت اهمیت ویژگی‌ها"""
        return self.feature_importance.copy()

    def retrain_model(self, new_data: List[Dict]):
        """بازآموزی مدل با داده‌های جدید"""
        logger.info("🔄 شروع بازآموزی مدل...")

        try:
            # استخراج ویژگی‌ها از داده‌های جدید
            X_new = []
            y_new = []

            for data in new_data:
                features = self.extract_config_features(data['config'])
                quality_score = data.get('quality_score', 0.5)

                X_new.append(self._extract_features_vector(features))
                y_new.append(quality_score)

            if len(X_new) < 5:
                logger.warning("⚠️ داده‌های جدید کافی نیست")
                return False

            # ترکیب با داده‌های موجود
            X_new = np.array(X_new)
            y_new = np.array(y_new)

            # نرمال‌سازی
            X_new_scaled = self.scaler.transform(X_new)

            # بازآموزی مدل
            self.model.fit(X_new_scaled, y_new)

            # ذخیره مدل جدید
            self._save_model()

            logger.info("✅ مدل با موفقیت بازآموزی شد")
            return True

        except Exception as e:
            logger.error(f"❌ خطا در بازآموزی مدل: {e}")
            return False


# نمونه استفاده
if __name__ == "__main__":
    # ایجاد نمونه AI Scorer
    scorer = AIQualityScorer()

    # نمونه کانفیگ برای تست
    sample_config = {
        'protocol': 'vless',
        'server': 'example.com',
        'port': 443,
        'network': 'ws',
        'tls': True,
        'encryption': 'none',
        'latency': 45.0,
        'uptime': 98.5,
        'success_rate': 0.95
    }

    # پیش‌بینی کیفیت
    quality = scorer.predict_quality(sample_config)

    print(f"🎯 امتیاز کلی: {quality.overall_score:.3f}")
    print(f"⚡ امتیاز تأخیر: {quality.latency_score:.3f}")
    print(f"🛡️ امتیاز امنیت: {quality.security_score:.3f}")
    print(f"📊 دسته‌بندی: {scorer.get_quality_category(quality.overall_score)}")
