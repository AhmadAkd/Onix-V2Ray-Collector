#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V2Ray Collector Notifications System
سیستم اعلان‌های V2Ray Collector
"""

import json
import logging
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class NotificationConfig:
    """تنظیمات اعلان‌ها"""
    telegram_enabled: bool = False
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""
    
    email_enabled: bool = False
    email_smtp_server: str = ""
    email_smtp_port: int = 587
    email_username: str = ""
    email_password: str = ""
    email_recipients: List[str] = None
    
    webhook_enabled: bool = False
    webhook_url: str = ""
    
    alert_thresholds: Dict[str, int] = None
    
    def __post_init__(self):
        if self.email_recipients is None:
            self.email_recipients = []
        if self.alert_thresholds is None:
            self.alert_thresholds = {
                'min_healthy_configs': 10,
                'max_failed_percentage': 80,
                'min_sources_active': 3
            }

class NotificationManager:
    """مدیریت اعلان‌ها"""
    
    def __init__(self, config: NotificationConfig):
        self.config = config
        self.last_notification = {}
        
    async def send_telegram_message(self, message: str) -> bool:
        """ارسال پیام تلگرام"""
        if not self.config.telegram_enabled:
            return False
            
        try:
            url = f"https://api.telegram.org/bot{self.config.telegram_bot_token}/sendMessage"
            data = {
                'chat_id': self.config.telegram_chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, data=data, timeout=10)
            return response.status_code == 200
            
        except Exception as e:
            logger.error(f"خطا در ارسال تلگرام: {e}")
            return False
    
    async def send_email(self, subject: str, message: str) -> bool:
        """ارسال ایمیل"""
        if not self.config.email_enabled:
            return False
            
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config.email_username
            msg['To'] = ', '.join(self.config.email_recipients)
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'html', 'utf-8'))
            
            server = smtplib.SMTP(self.config.email_smtp_server, self.config.email_smtp_port)
            server.starttls()
            server.login(self.config.email_username, self.config.email_password)
            
            text = msg.as_string()
            server.sendmail(self.config.email_username, self.config.email_recipients, text)
            server.quit()
            
            return True
            
        except Exception as e:
            logger.error(f"خطا در ارسال ایمیل: {e}")
            return False
    
    async def send_webhook(self, data: Dict) -> bool:
        """ارسال webhook"""
        if not self.config.webhook_enabled:
            return False
            
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(
                self.config.webhook_url, 
                json=data, 
                headers=headers, 
                timeout=10
            )
            return response.status_code in [200, 201]
            
        except Exception as e:
            logger.error(f"خطا در ارسال webhook: {e}")
            return False
    
    async def check_and_send_alerts(self, report: Dict) -> None:
        """بررسی و ارسال اعلان‌های لازم"""
        current_time = datetime.now()
        
        # بررسی آستانه‌ها
        alerts = []
        
        # بررسی تعداد کانفیگ‌های سالم
        healthy_count = len(report.get('working_configs', []))
        if healthy_count < self.config.alert_thresholds['min_healthy_configs']:
            alerts.append(f"⚠️ تعداد کانفیگ‌های سالم کمتر از حد انتظار: {healthy_count}")
        
        # بررسی درصد کانفیگ‌های ناسالم
        total_configs = healthy_count + len(report.get('failed_configs', []))
        if total_configs > 0:
            failed_percentage = (len(report.get('failed_configs', [])) / total_configs) * 100
            if failed_percentage > self.config.alert_thresholds['max_failed_percentage']:
                alerts.append(f"⚠️ درصد کانفیگ‌های ناسالم بالا: {failed_percentage:.1f}%")
        
        # بررسی منابع فعال
        sources_checked = report.get('sources_checked', 0)
        if sources_checked < self.config.alert_thresholds['min_sources_active']:
            alerts.append(f"⚠️ تعداد منابع فعال کم: {sources_checked}")
        
        # ارسال اعلان‌ها
        if alerts:
            await self._send_alert_notifications(alerts, report)
    
    async def _send_alert_notifications(self, alerts: List[str], report: Dict) -> None:
        """ارسال اعلان‌های هشدار"""
        current_time = datetime.now()
        
        # جلوگیری از ارسال مکرر (حداکثر هر 30 دقیقه)
        alert_key = "general_alert"
        if alert_key in self.last_notification:
            if current_time - self.last_notification[alert_key] < timedelta(minutes=30):
                return
        
        # آماده‌سازی پیام
        message = self._format_alert_message(alerts, report)
        
        # ارسال از طریق کانال‌های مختلف
        tasks = []
        if self.config.telegram_enabled:
            tasks.append(self.send_telegram_message(message))
        
        if self.config.email_enabled:
            tasks.append(self.send_email("V2Ray Collector Alert", message))
        
        if self.config.webhook_enabled:
            webhook_data = {
                'type': 'alert',
                'timestamp': current_time.isoformat(),
                'alerts': alerts,
                'report': report
            }
            tasks.append(self.send_webhook(webhook_data))
        
        # اجرای همزمان
        if tasks:
            import asyncio
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # ثبت زمان آخرین اعلان
            self.last_notification[alert_key] = current_time
            
            # لاگ نتایج
            logger.info(f"ارسال اعلان‌ها: {results}")
    
    def _format_alert_message(self, alerts: List[str], report: Dict) -> str:
        """فرمت‌بندی پیام اعلان"""
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        message = f"""
🚨 <b>V2Ray Collector Alert</b>
📅 زمان: {current_time}

<b>هشدارها:</b>
{chr(10).join(f"• {alert}" for alert in alerts)}

<b>آمار فعلی:</b>
✅ کانفیگ‌های سالم: {len(report.get('working_configs', []))}
❌ کانفیگ‌های ناسالم: {len(report.get('failed_configs', []))}
🌐 منابع بررسی شده: {report.get('sources_checked', 0)}
📊 نرخ موفقیت: {report.get('success_rate', 0):.1f}%

<b>لینک‌های اشتراک:</b>
🔗 <a href="https://ahmadakd.github.io/Onix-V2Ray-Collector/subscriptions/">صفحه اصلی</a>
📱 <a href="https://github.com/AhmadAkd/Onix-V2Ray-Collector/raw/main/subscriptions/all_subscription.txt">همه کانفیگ‌ها</a>
        """
        
        return message.strip()
    
    async def send_daily_report(self, report: Dict) -> None:
        """ارسال گزارش روزانه"""
        current_time = datetime.now()
        
        # فقط یک بار در روز
        alert_key = "daily_report"
        if alert_key in self.last_notification:
            if current_time.date() == self.last_notification[alert_key].date():
                return
        
        message = self._format_daily_report(report)
        
        # ارسال گزارش
        tasks = []
        if self.config.telegram_enabled:
            tasks.append(self.send_telegram_message(message))
        
        if self.config.email_enabled:
            tasks.append(self.send_email("V2Ray Collector Daily Report", message))
        
        if tasks:
            import asyncio
            await asyncio.gather(*tasks, return_exceptions=True)
            self.last_notification[alert_key] = current_time
    
    def _format_daily_report(self, report: Dict) -> str:
        """فرمت‌بندی گزارش روزانه"""
        current_time = datetime.now().strftime('%Y-%m-%d')
        
        # آمار پروتکل‌ها
        protocol_stats = {}
        for config in report.get('working_configs', []):
            protocol = config.get('protocol', 'unknown')
            protocol_stats[protocol] = protocol_stats.get(protocol, 0) + 1
        
        protocol_text = ""
        for protocol, count in protocol_stats.items():
            protocol_text += f"• {protocol.upper()}: {count}\n"
        
        # آمار کشورها
        country_stats = {}
        for config in report.get('working_configs', []):
            country = config.get('country', 'unknown')
            country_stats[country] = country_stats.get(country, 0) + 1
        
        # 5 کشور برتر
        top_countries = sorted(country_stats.items(), key=lambda x: x[1], reverse=True)[:5]
        country_text = ""
        for country, count in top_countries:
            country_text += f"• {country}: {count}\n"
        
        message = f"""
📊 <b>گزارش روزانه V2Ray Collector</b>
📅 تاریخ: {current_time}

<b>آمار کلی:</b>
✅ کانفیگ‌های سالم: {len(report.get('working_configs', []))}
❌ کانفیگ‌های ناسالم: {len(report.get('failed_configs', []))}
🌐 منابع بررسی شده: {report.get('sources_checked', 0)}
📊 نرخ موفقیت: {report.get('success_rate', 0):.1f}%

<b>توزیع پروتکل‌ها:</b>
{protocol_text}

<b>کشورهای برتر:</b>
{country_text}

<b>لینک‌های اشتراک:</b>
🔗 <a href="https://ahmadakd.github.io/Onix-V2Ray-Collector/subscriptions/">صفحه اصلی</a>
📱 <a href="https://github.com/AhmadAkd/Onix-V2Ray-Collector/raw/main/subscriptions/all_subscription.txt">همه کانفیگ‌ها</a>
        """
        
        return message.strip()

# تنظیمات پیش‌فرض اعلان‌ها
DEFAULT_NOTIFICATION_CONFIG = NotificationConfig(
    telegram_enabled=False,
    email_enabled=False,
    webhook_enabled=False,
    alert_thresholds={
        'min_healthy_configs': 10,
        'max_failed_percentage': 80,
        'min_sources_active': 3
    }
)

# نمونه استفاده
async def main():
    """نمونه استفاده از سیستم اعلان‌ها"""
    config = DEFAULT_NOTIFICATION_CONFIG
    
    # فعال‌سازی تلگرام (اختیاری)
    # config.telegram_enabled = True
    # config.telegram_bot_token = "YOUR_BOT_TOKEN"
    # config.telegram_chat_id = "YOUR_CHAT_ID"
    
    notification_manager = NotificationManager(config)
    
    # نمونه گزارش
    sample_report = {
        'timestamp': datetime.now().isoformat(),
        'working_configs': [{'protocol': 'vmess', 'country': 'US'}],
        'failed_configs': [{'protocol': 'vless', 'country': 'DE'}],
        'sources_checked': 5,
        'success_rate': 50.0
    }
    
    # بررسی و ارسال اعلان‌ها
    await notification_manager.check_and_send_alerts(sample_report)
    
    # ارسال گزارش روزانه
    await notification_manager.send_daily_report(sample_report)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
