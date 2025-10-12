#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V2Ray Config Web Server
سرور وب برای نمایش و ارائه کانفیگ‌های V2Ray
"""

from flask import Flask, render_template_string, jsonify, send_file, request
import os
import json
import glob
from datetime import datetime
import logging

# تنظیم لاگ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# HTML template برای صفحه اصلی
MAIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>V2Ray Configs - کانفیگ‌های رایگان V2Ray</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }
        
        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
        }
        
        .stat-number {
            font-size: 2.5em;
            font-weight: bold;
            color: #4facfe;
            margin-bottom: 10px;
        }
        
        .stat-label {
            color: #666;
            font-size: 1.1em;
        }
        
        .subscriptions {
            padding: 30px;
        }
        
        .section-title {
            font-size: 1.8em;
            margin-bottom: 20px;
            color: #333;
            border-bottom: 3px solid #4facfe;
            padding-bottom: 10px;
        }
        
        .subscription-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .subscription-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            border: 2px solid #e9ecef;
            transition: all 0.3s ease;
        }
        
        .subscription-card:hover {
            border-color: #4facfe;
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }
        
        .protocol-name {
            font-size: 1.5em;
            font-weight: bold;
            color: #4facfe;
            margin-bottom: 10px;
            text-transform: uppercase;
        }
        
        .config-count {
            color: #666;
            margin-bottom: 15px;
        }
        
        .copy-btn {
            background: #4facfe;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1em;
            transition: background 0.3s ease;
            width: 100%;
        }
        
        .copy-btn:hover {
            background: #3d8bfe;
        }
        
        .url-input {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin-bottom: 10px;
            font-family: monospace;
            background: #f8f9fa;
        }
        
        .footer {
            background: #333;
            color: white;
            text-align: center;
            padding: 20px;
        }
        
        .last-update {
            background: #e9ecef;
            padding: 15px;
            margin: 20px 30px;
            border-radius: 10px;
            text-align: center;
            color: #666;
        }
        
        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-left: 10px;
        }
        
        .status-active {
            background: #28a745;
        }
        
        .status-inactive {
            background: #dc3545;
        }
        
        @media (max-width: 768px) {
            .header h1 {
                font-size: 2em;
            }
            
            .stats {
                grid-template-columns: 1fr;
            }
            
            .subscription-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔒 V2Ray Configs</h1>
            <p>کانفیگ‌های رایگان و تست شده V2Ray برای دسترسی امن</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number" id="total-configs">{{ stats.total_configs }}</div>
                <div class="stat-label">کانفیگ کل</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="working-configs">{{ stats.working_configs }}</div>
                <div class="stat-label">کانفیگ سالم</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="success-rate">{{ stats.success_rate }}</div>
                <div class="stat-label">نرخ موفقیت</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ stats.protocols_count }}</div>
                <div class="stat-label">پروتکل پشتیبانی شده</div>
            </div>
        </div>
        
        <div class="last-update">
            <span class="status-indicator status-active"></span>
            آخرین به‌روزرسانی: {{ stats.last_update }}
        </div>
        
        <div class="subscriptions">
            <h2 class="section-title">📡 لینک‌های اشتراک</h2>
            
            <div class="subscription-grid">
                {% for protocol, info in subscriptions.items() %}
                <div class="subscription-card">
                    <div class="protocol-name">{{ protocol.upper() }}</div>
                    <div class="config-count">{{ info.count }} کانفیگ</div>
                    <input type="text" class="url-input" value="{{ info.url }}" readonly>
                    <button class="copy-btn" onclick="copyToClipboard('{{ info.url }}')">
                        📋 کپی لینک
                    </button>
                </div>
                {% endfor %}
            </div>
            
            <h2 class="section-title">📱 نحوه استفاده</h2>
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                <h3>برای موبایل (Android):</h3>
                <ol style="margin: 10px 0; padding-right: 20px;">
                    <li>نرم‌افزار v2rayNG را دانلود و نصب کنید</li>
                    <li>روی + کلیک کنید و "Subscription" را انتخاب کنید</li>
                    <li>لینک مورد نظر را وارد کنید</li>
                    <li>روی "OK" کلیک کنید</li>
                </ol>
                
                <h3>برای کامپیوتر (Windows):</h3>
                <ol style="margin: 10px 0; padding-right: 20px;">
                    <li>نرم‌افزار v2rayN را دانلود کنید</li>
                    <li>روی "Subscribe" کلیک کنید</li>
                    <li>"Subscribe Settings" را انتخاب کنید</li>
                    <li>لینک را اضافه کنید</li>
                </ol>
            </div>
        </div>
        
        <div class="footer">
            <p>🔄 این کانفیگ‌ها هر 30 دقیقه به‌روزرسانی می‌شوند</p>
            <p>⚡ تمام کانفیگ‌ها تست شده و سالم هستند</p>
        </div>
    </div>
    
    <script>
        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(function() {
                alert('لینک کپی شد!');
            }, function(err) {
                console.error('خطا در کپی: ', err);
            });
        }
        
        // به‌روزرسانی خودکار آمار هر 5 دقیقه
        setInterval(function() {
            fetch('/api/stats')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('total-configs').textContent = data.total_configs;
                    document.getElementById('working-configs').textContent = data.working_configs;
                    document.getElementById('success-rate').textContent = data.success_rate;
                })
                .catch(error => console.error('خطا در به‌روزرسانی آمار:', error));
        }, 300000); // 5 دقیقه
    </script>
</body>
</html>
"""


class V2RayWebServer:
    """کلاس مدیریت سرور وب"""

    def __init__(self):
        self.subscriptions_dir = 'subscriptions'

    def get_latest_report(self):
        """دریافت آخرین گزارش"""
        try:
            report_files = glob.glob(f'{self.subscriptions_dir}/report_*.json')
            if report_files:
                latest_file = max(report_files, key=os.path.getctime)
                with open(latest_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except Exception as e:
            logger.error(f"خطا در خواندن گزارش: {e}")
            return None

    def get_subscription_files(self):
        """دریافت فایل‌های اشتراک"""
        subscriptions = {}

        try:
            # فایل‌های پروتکل‌های مختلف
            protocols = ['vmess', 'vless', 'trojan', 'ss', 'ssr', 'all']

            for protocol in protocols:
                file_path = f'{self.subscriptions_dir}/{protocol}_subscription.txt'
                if os.path.exists(file_path):
                    # شمارش تعداد کانفیگ‌ها
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                        count = len(
                            [line for line in content.split('\n') if line.strip()])

                    subscriptions[protocol] = {
                        'count': count,
                        'url': f'/subscription/{protocol}',
                        'filename': f'{protocol}_subscription.txt'
                    }

            return subscriptions
        except Exception as e:
            logger.error(f"خطا در خواندن فایل‌های اشتراک: {e}")
            return {}

    def get_stats(self):
        """دریافت آمار سیستم"""
        report = self.get_latest_report()

        if report:
            return {
                'total_configs': report.get('total_configs_tested', 0),
                'working_configs': report.get('working_configs', 0),
                'failed_configs': report.get('failed_configs', 0),
                'success_rate': report.get('success_rate', '0%'),
                'last_update': report.get('timestamp', 'نامشخص'),
                'protocols_count': len(report.get('protocols', {}))
            }
        else:
            return {
                'total_configs': 0,
                'working_configs': 0,
                'failed_configs': 0,
                'success_rate': '0%',
                'last_update': 'هیچ گزارش یافت نشد',
                'protocols_count': 0
            }


@app.route('/')
def index():
    """صفحه اصلی"""
    web_server = V2RayWebServer()
    stats = web_server.get_stats()
    subscriptions = web_server.get_subscription_files()

    return render_template_string(MAIN_TEMPLATE, stats=stats, subscriptions=subscriptions)


@app.route('/api/stats')
def api_stats():
    """API آمار"""
    web_server = V2RayWebServer()
    return jsonify(web_server.get_stats())


@app.route('/subscription/<protocol>')
def get_subscription(protocol):
    """دریافت فایل اشتراک"""
    try:
        file_path = f'subscriptions/{protocol}_subscription.txt'
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True,
                             download_name=f'{protocol}_subscription.txt')
        else:
            return jsonify({'error': 'فایل اشتراک یافت نشد'}), 404
    except Exception as e:
        logger.error(f"خطا در ارسال فایل اشتراک: {e}")
        return jsonify({'error': 'خطا در سرور'}), 500


@app.route('/api/protocols')
def api_protocols():
    """API لیست پروتکل‌ها"""
    web_server = V2RayWebServer()
    subscriptions = web_server.get_subscription_files()

    protocols_info = []
    for protocol, info in subscriptions.items():
        protocols_info.append({
            'protocol': protocol,
            'count': info['count'],
            'url': info['url']
        })

    return jsonify(protocols_info)


@app.route('/api/health')
def api_health():
    """بررسی سلامت سیستم"""
    try:
        # بررسی وجود فایل‌های ضروری
        required_files = [
            'subscriptions/vmess_subscription.txt',
            'subscriptions/vless_subscription.txt'
        ]

        health_status = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'files_status': {},
            'total_subscriptions': 0
        }

        for file_path in required_files:
            exists = os.path.exists(file_path)
            health_status['files_status'][file_path] = 'exists' if exists else 'missing'
            if not exists:
                health_status['status'] = 'degraded'

        # شمارش کل اشتراک‌ها
        web_server = V2RayWebServer()
        subscriptions = web_server.get_subscription_files()
        health_status['total_subscriptions'] = len(subscriptions)

        return jsonify(health_status)

    except Exception as e:
        logger.error(f"خطا در بررسی سلامت: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


def run_server(host='0.0.0.0', port=5000, debug=False):
    """اجرای سرور وب"""
    logger.info(f"🚀 شروع سرور وب روی http://{host}:{port}")

    try:
        app.run(host=host, port=port, debug=debug)
    except Exception as e:
        logger.error(f"خطا در اجرای سرور: {e}")


def main():
    """تابع اصلی"""
    import argparse

    parser = argparse.ArgumentParser(description='سرور وب V2Ray Configs')
    parser.add_argument('--host', default='0.0.0.0', help='آدرس میزبان')
    parser.add_argument('--port', type=int, default=5000, help='پورت')
    parser.add_argument('--debug', action='store_true', help='حالت debug')

    args = parser.parse_args()

    run_server(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
