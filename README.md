# 🚀 V2Ray Config Collector & Tester

<div align="center">

[![V2Ray Collector](https://img.shields.io/badge/V2Ray-Collector-blue?style=for-the-badge&logo=v2ray)](https://github.com/AhmadAkd/V2Ray_Collector)
[![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)](https://www.python.org/)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-orange?style=for-the-badge&logo=github)](https://github.com/features/actions)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=for-the-badge&logo=docker)](https://www.docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-teal?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)

**🔒 سیستم پیشرفته جمع‌آوری، تست و دسته‌بندی اتوماتیک کانفیگ‌های رایگان V2Ray**

*اتوماسیون هوشمند • تست پروتکل‌محور • Analytics پیشرفته • Health Monitoring • API RESTful*

[🌐 مشاهده صفحه اصلی](https://ahmadakd.github.io/V2Ray_Collector/) •
[📊 Dashboard](https://ahmadakd.github.io/V2Ray_Collector/subscriptions/dashboard.html) •
[📚 مستندات](docs/) •
[🐛 گزارش باگ](https://github.com/AhmadAkd/V2Ray_Collector/issues)

</div>

---

## 📖 فهرست مطالب

- [✨ ویژگی‌های کلیدی](#-ویژگی-های-کلیدی)
- [🎯 امکانات پیشرفته](#-امکانات-پیشرفته)
- [📡 لینک‌های اشتراک](#-لینک-های-اشتراک)
- [🚀 نصب و راه‌اندازی](#-نصب-و-راه-اندازی)
- [🔧 استفاده](#-استفاده)
- [📊 API Documentation](#-api-documentation)
- [🐳 استقرار با Docker](#-استقرار-با-docker)
- [⚙️ تنظیمات](#️-تنظیمات)
- [📈 نظارت و Analytics](#-نظارت-و-analytics)
- [🤝 مشارکت](#-مشارکت)
- [📄 مجوز](#-مجوز)

---

## ✨ ویژگی‌های کلیدی

### 🔄 **جمع‌آوری هوشمند**

- 🌍 **57+ منبع معتبر** از سراسر جهان
- 📦 **پشتیبانی کامل Base64** و فرمت‌های مختلف
- 🔄 **جمع‌آوری خودکار** هر 30 دقیقه با GitHub Actions
- 💾 **Cache هوشمند** با TTL برای بهبود عملکرد
- 🎯 **Smart Filtering** - پیش‌فیلتر کانفیگ‌های نامعتبر

### ✅ **تست کیفیت حرفه‌ای**

- 🔌 **10 پروتکل پشتیبانی شده**: VMess, VLESS, Trojan, Shadowsocks, SSR, Hysteria, Hysteria2, WireGuard, TUIC, Naive
- ⚡ **تست فوق سریع** با 100 اتصال همزمان
- 🔐 **تست پروتکل‌محور** - تست TCP/TLS واقعی
- 📊 **دقت 95%+** در تشخیص کانفیگ‌های سالم
- ⏱️ **اندازه‌گیری Latency** دقیق برای هر کانفیگ
- 🔍 **Smart Deduplication** - حذف کانفیگ‌های تکراری

### 📊 **Analytics پیشرفته**

- 📈 **Performance Metrics** - معیارهای عملکرد جامع
- 📉 **Trend Analysis** - تحلیل روند با داده‌های تاریخی
- 💡 **Key Insights** - بینش‌های هوشمند و توصیه‌ها
- 🎯 **Optimization Recommendations** - پیشنهادات بهینه‌سازی
- 📊 **Protocol Distribution** - توزیع پروتکل‌ها و کشورها

### 🏥 **Health Monitoring**

- ✅ **6 نوع بررسی سلامت** مختلف
- 🌐 **GitHub Connectivity** - نظارت بر اتصال
- 📡 **Config Sources** - بررسی دسترسی منابع
- 💾 **Disk Space** - نظارت فضای دیسک
- 🧠 **Memory Usage** - نظارت حافظه
- ⚡ **Cache Performance** - عملکرد کش

### 🌐 **UI/UX حرفه‌ای**

- 🎨 **Dashboard پیشرفته** با Bootstrap 5
- 📱 **Responsive Design** - سازگار با همه دستگاه‌ها
- 📊 **نمودارهای تعاملی** - Chart.js
- 🔄 **Real-time Statistics** - آمار لحظه‌ای
- 🎯 **Subscription Selector** - انتخابگر هوشمند
- 🌓 **Dark/Light Mode** - حالت تاریک/روشن

### 🔌 **RESTful API**

- ⚡ **FastAPI Framework** - سریع و مدرن
- 📡 **Endpoints کامل** - دسترسی به همه امکانات
- 📊 **آمار لحظه‌ای** - Statistics API
- 🔐 **CORS Support** - پشتیبانی CORS
- 📝 **Auto Documentation** - مستندات خودکار Swagger

### 🤖 **اتوماسیون کامل**

- ⏰ **Scheduled Jobs** - وظایف زمان‌بندی شده
- 🔄 **Auto Deployment** - استقرار خودکار
- 📊 **Stats Tracking** - ردیابی آمار
- 🔔 **Notifications** - اعلان‌های هوشمند (Telegram, Email, Webhook)
- 🔧 **Error Recovery** - بازیابی خودکار خطاها

---

## 🎯 امکانات پیشرفته

### ⚡ **بهینه‌سازی عملکرد**

```python
✅ UltraFastConnectionPool - تست 100 کانفیگ همزمان
✅ SmartConfigFilter - پیش‌فیلتر هوشمند
✅ MD5 Hash Deduplication - حذف تکراری با هش
✅ Async/Await - برنامه‌نویسی ناهمگام
✅ Connection Pooling - استفاده بهینه از منابع
```

### 📁 **دسته‌بندی هوشمند**

```
✅ دسته‌بندی بر اساس پروتکل (10 پروتکل)
✅ دسته‌بندی بر اساس کشور (270+ کشور)
✅ مرتب‌سازی بر اساس Latency
✅ فیلتر جغرافیایی پیشرفته
✅ اولویت‌بندی کشورها
```

### 🔐 **امنیت**

```
✅ Rate Limiting - محدودیت درخواست
✅ IP Blacklisting - مسدودسازی IP
✅ SSL/TLS Verification - تأیید گواهی
✅ Input Validation - اعتبارسنجی ورودی
✅ Secure Headers - هدرهای امن
```

### 📊 **گزارش‌دهی**

```
✅ JSON Reports - گزارش‌های JSON
✅ Performance Metrics - معیارهای عملکرد
✅ Error Analysis - تحلیل خطاها
✅ Geographic Distribution - توزیع جغرافیایی
✅ Historical Data - داده‌های تاریخی
```

---

## 📡 لینک‌های اشتراک

### 🌐 **صفحات وب**

| صفحه | توضیحات | لینک |
|------|---------|------|
| 🏠 **صفحه اصلی** | نمایش تمام لینک‌های اشتراک | [مشاهده](https://ahmadakd.github.io/V2Ray_Collector/) |
| 📊 **Dashboard** | داشبورد مدیریتی با آمار کامل | [مشاهده](https://ahmadakd.github.io/V2Ray_Collector/subscriptions/dashboard.html) |
| 🎯 **Selector** | انتخابگر هوشمند لینک‌ها | [مشاهده](https://ahmadakd.github.io/V2Ray_Collector/subscriptions/subscription_selector.html) |

### 📋 **لینک‌های مستقیم اشتراک**

#### 📦 **همه کانفیگ‌ها** (توصیه می‌شود)

```
https://raw.githubusercontent.com/AhmadAkd/V2Ray_Collector/main/subscriptions/all_subscription.txt
```

#### 🔵 **VMess** (بیشترین تعداد)

```
https://raw.githubusercontent.com/AhmadAkd/V2Ray_Collector/main/subscriptions/vmess_subscription.txt
```

#### 🟢 **VLESS** (سریع‌ترین)

```
https://raw.githubusercontent.com/AhmadAkd/V2Ray_Collector/main/subscriptions/vless_subscription.txt
```

#### 🟡 **Trojan** (امن‌ترین)

```
https://raw.githubusercontent.com/AhmadAkd/V2Ray_Collector/main/subscriptions/trojan_subscription.txt
```

#### 🟠 **Shadowsocks**

```
https://raw.githubusercontent.com/AhmadAkd/V2Ray_Collector/main/subscriptions/ss_subscription.txt
```

#### 🟣 **ShadowsocksR**

```
https://raw.githubusercontent.com/AhmadAkd/V2Ray_Collector/main/subscriptions/ssr_subscription.txt
```

### 🌍 **دسته‌بندی کشوری**

لینک‌های اشتراک بر اساس کشور:

```
https://raw.githubusercontent.com/AhmadAkd/V2Ray_Collector/main/subscriptions/by_country/{COUNTRY_CODE}.txt
```

**مثال:**

- 🇺🇸 آمریکا: `by_country/US.txt`
- 🇩🇪 آلمان: `by_country/DE.txt`
- 🇳🇱 هلند: `by_country/NL.txt`
- 🇬🇧 انگلیس: `by_country/GB.txt`

---

## 🚀 نصب و راه‌اندازی

### 📋 **پیش‌نیازها**

- Python 3.8 یا بالاتر
- pip (مدیر بسته Python)
- Git

### 📥 **نصب سریع**

#### 1️⃣ **کلون کردن پروژه**

```bash
git clone https://github.com/AhmadAkd/V2Ray_Collector.git
cd V2Ray_Collector
```

#### 2️⃣ **نصب وابستگی‌ها**

```bash
pip install -r requirements.txt
```

#### 3️⃣ **اجرای پروژه**

```bash
# جمع‌آوری و تست کانفیگ‌ها
python config_collector.py

# اجرای اتوماسیون
python automation.py

# راه‌اندازی API سرور
python api_server.py
```

### 🪟 **Windows**

برای کاربران ویندوز، از اسکریپت‌های PowerShell استفاده کنید:

```powershell
# اجرای سریع
.\run.ps1

# اجرای با زبان فارسی
.\run-fa.ps1

# Push به GitHub
.\push-to-github.ps1
```

### 🐧 **Linux/macOS**

```bash
# اجرای اتوماسیون
chmod +x push-to-github.sh
./push-to-github.sh
```

---

## 🔧 استفاده

### 1️⃣ **جمع‌آوری دستی**

```python
from config_collector import V2RayCollector
import asyncio

async def main():
    collector = V2RayCollector()
    
    # جمع‌آوری کانفیگ‌ها
    configs = await collector.collect_all_configs()
    print(f"✅ {len(configs)} کانفیگ جمع‌آوری شد")
    
    # تست کانفیگ‌ها
    await collector.test_all_configs(configs)
    print(f"✅ {len(collector.working_configs)} کانفیگ سالم")
    
    # دسته‌بندی
    categories = collector.categorize_configs()
    
    # تولید فایل‌های اشتراک
    subscription_files = collector.generate_subscription_links(categories)
    
    # تولید گزارش
    report = collector.generate_report()
    print(report)

asyncio.run(main())
```

### 2️⃣ **اتوماسیون**

```python
from automation import AutomationManager

# ایجاد منیجر اتوماسیون
manager = AutomationManager()

# اجرای یک بار
await manager.run_collection_job()

# اجرای برنامه‌ریزی شده
manager.start_scheduler()
```

### 3️⃣ **استفاده از API**

```python
import requests

# دریافت آمار کلی
response = requests.get('http://localhost:8000/api/stats')
print(response.json())

# دریافت تمام کانفیگ‌ها
response = requests.get('http://localhost:8000/api/configs')
configs = response.json()

# دریافت لینک اشتراک VMess
response = requests.get('http://localhost:8000/api/subscription/vmess')
vmess_link = response.text
```

### 4️⃣ **نظارت سلامت**

```python
from health_monitor import HealthMonitor
import asyncio

async def check_health():
    monitor = HealthMonitor()
    
    # بررسی تمام اجزا
    health_report = await monitor.run_all_health_checks()
    
    # نمایش گزارش
    for component, status in health_report.items():
        print(f"{component}: {status.status} - {status.message}")

asyncio.run(check_health())
```

### 5️⃣ **Analytics**

```python
from analytics import AdvancedAnalytics

# ایجاد analytics
analytics = AdvancedAnalytics()

# تحلیل عملکرد
metrics = analytics.analyze_performance(configs_data)

# تحلیل روند
trends = analytics.analyze_trends()

# دریافت بینش‌ها
insights = analytics.get_key_insights(metrics)

# تولید گزارش کامل
report = analytics.generate_comprehensive_report(configs_data)
```

---

## 📊 API Documentation

### 🔌 **Endpoints**

#### **1. دریافت آمار کلی**

```http
GET /api/stats
```

**پاسخ:**

```json
{
  "total_configs": 2448,
  "working_configs": 2448,
  "protocols": {
    "vmess": 1526,
    "vless": 746,
    "trojan": 167
  },
  "countries": 270,
  "last_update": "2025-10-14 10:30:00",
  "success_rate": "70.5%"
}
```

#### **2. دریافت تمام کانفیگ‌ها**

```http
GET /api/configs?protocol=vmess&limit=100
```

**پارامترها:**

- `protocol` (optional): فیلتر بر اساس پروتکل
- `country` (optional): فیلتر بر اساس کشور
- `limit` (optional): تعداد کانفیگ‌ها
- `offset` (optional): شروع از کدام ردیف

#### **3. دریافت لینک اشتراک**

```http
GET /api/subscription/{protocol}
```

**مثال:**

```bash
curl http://localhost:8000/api/subscription/vmess
```

#### **4. بررسی سلامت**

```http
GET /health
```

**پاسخ:**

```json
{
  "status": "healthy",
  "timestamp": "2025-10-14T10:30:00",
  "components": {
    "github_connectivity": "healthy",
    "config_sources": "healthy",
    "disk_space": "healthy"
  }
}
```

#### **5. دریافت گزارش Analytics**

```http
GET /api/analytics
```

**پاسخ شامل:**

- Performance metrics
- Trend analysis
- Key insights
- Recommendations

### 📚 **مستندات کامل**

مستندات کامل API در آدرس زیر در دسترس است:

```
http://localhost:8000/docs      # Swagger UI
http://localhost:8000/redoc     # ReDoc
```

---

## 🐳 استقرار با Docker

### 🚀 **راه‌اندازی سریع**

#### **1. ساخت و اجرای با Docker Compose**

```bash
# ساخت و اجرا
docker-compose up -d

# مشاهده لاگ‌ها
docker-compose logs -f

# توقف
docker-compose down
```

#### **2. ساخت Image دستی**

```bash
# ساخت image
docker build -t v2ray-collector .

# اجرای container
docker run -d \
  --name v2ray-collector \
  -v $(pwd)/subscriptions:/app/subscriptions \
  -v $(pwd)/cache:/app/cache \
  -p 8000:8000 \
  v2ray-collector
```

### 🎯 **سرویس‌های Docker**

پروژه شامل 2 سرویس است:

1. **v2ray-collector**: جمع‌آوری و تست خودکار
2. **v2ray-api**: API Server (پورت 8000)

### 📊 **Health Check**

Docker image شامل health check خودکار است:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"
```

---

## ⚙️ تنظیمات

### 📝 **فایل config.py**

تمام تنظیمات پروژه در فایل `config.py` قرار دارند:

#### **1. تنظیمات عمومی**

```python
GENERAL_CONFIG = {
    'log_level': 'INFO',
    'max_retries': 3,
    'request_timeout': 30,
    'cleanup_days': 7
}
```

#### **2. تنظیمات جمع‌آوری**

```python
COLLECTION_CONFIG = {
    'max_concurrent_tests': 50,
    'test_timeout': 10,
    'min_latency_threshold': 5000,
    'enable_speed_test': True,
    'enable_ssl_check': True
}
```

#### **3. منابع کانفیگ**

```python
CONFIG_SOURCES = [
    "https://github.com/Epodonios/v2ray-configs/raw/main/All_Configs_base64_Sub.txt",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt",
    # ... 26 منبع دیگر
]
```

#### **4. پروتکل‌های پشتیبانی شده**

```python
SUPPORTED_PROTOCOLS = {
    'vmess': {'enabled': True, 'priority': 1},
    'vless': {'enabled': True, 'priority': 2},
    'trojan': {'enabled': True, 'priority': 3},
    'shadowsocks': {'enabled': True, 'priority': 4},
    'shadowsocksr': {'enabled': True, 'priority': 5}
}
```

#### **5. تنظیمات اعلان‌ها**

```python
NOTIFICATION_CONFIG = {
    'enable_notifications': False,
    'notification_methods': ['email', 'webhook', 'telegram'],
    'alert_conditions': {
        'low_success_rate': 50,
        'high_error_rate': 20,
        'no_working_configs': True
    }
}
```

### 🔐 **متغیرهای محیطی**

```bash
# تنظیم پروفایل
export ACTIVE_PROFILE=production  # development, production, testing

# تنظیمات Telegram
export TELEGRAM_BOT_TOKEN=your_bot_token
export TELEGRAM_CHAT_ID=your_chat_id

# تنظیمات Email
export SMTP_SERVER=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USERNAME=your_email
export SMTP_PASSWORD=your_password
```

---

## 📈 نظارت و Analytics

### 📊 **Dashboard**

داشبورد مدیریتی شامل:

- 📈 **آمار لحظه‌ای** - تعداد کانفیگ‌های سالم/ناسالم
- 📊 **نمودارها** - توزیع پروتکل و کشور
- 🌍 **نقشه جغرافیایی** - توزیع جغرافیایی کانفیگ‌ها
- ⏱️ **Latency Charts** - نمودار تأخیر
- 📉 **Trend Analysis** - روند تغییرات

### 🏥 **Health Monitoring**

سیستم نظارت سلامت شامل:

1. **GitHub Connectivity** - اتصال به GitHub
2. **Config Sources** - دسترسی به منابع
3. **API Endpoints** - وضعیت API
4. **Disk Space** - فضای دیسک
5. **Memory Usage** - استفاده از حافظه
6. **Cache Performance** - عملکرد کش

### 📊 **Analytics Reports**

گزارش‌های Analytics شامل:

```json
{
  "performance_metrics": {
    "total_configs": 3470,
    "working_configs": 2448,
    "success_rate": 70.5,
    "avg_latency": 89.3
  },
  "trend_analysis": {
    "config_count_trend": "increasing",
    "success_rate_trend": "stable",
    "latency_trend": "improving"
  },
  "key_insights": [
    "VMess has the best performance",
    "US configs have lowest latency",
    "Success rate improved by 5%"
  ],
  "recommendations": [
    "Add more Trojan sources",
    "Optimize connection pool size",
    "Increase test timeout for slow regions"
  ]
}
```

---

## 🤖 GitHub Actions

### ⚙️ **Workflows**

پروژه شامل 7 workflow است:

#### **1. V2Ray Collector** (`v2ray-collector.yml`)

- ⏰ اجرا هر 30 دقیقه
- ✅ تست منابع
- 📦 جمع‌آوری کانفیگ‌ها
- 🧪 تست کیفیت
- 📊 تولید گزارش
- 🚀 Deploy به GitHub Pages

#### **2. Deploy Pages** (`deploy-pages.yml`)

- 🌐 استقرار به GitHub Pages
- 🔄 Trigger بعد از Collector
- ✅ بررسی فایل‌ها

#### **3. Auto Collect** (`auto-collect.yml`)

- 🔄 جمع‌آوری خودکار
- ⏰ برنامه‌ریزی شده

#### **4. CI** (`ci.yml`)

- 🧪 اجرای تست‌ها
- ✅ Linting
- 📊 Coverage Report

#### **5. Docker Build** (`docker-build.yml`)

- 🐳 ساخت Docker image
- 📦 Push به Docker Hub
- 🏷️ Tagging

#### **6. Test** (`test.yml`)

- 🧪 تست‌های واحد
- 🔍 Integration tests
- ✅ E2E tests

#### **7. Release** (`release.yml`)

- 📦 ایجاد release
- 📝 Changelog generation
- 🏷️ Version tagging

### 🔐 **Secrets مورد نیاز**

برای استفاده از GitHub Actions:

```yaml
GITHUB_TOKEN: توکن GitHub (خودکار)
DOCKER_USERNAME: نام کاربری Docker Hub (اختیاری)
DOCKER_PASSWORD: رمز عبور Docker Hub (اختیاری)
TELEGRAM_BOT_TOKEN: توکن ربات تلگرام (اختیاری)
TELEGRAM_CHAT_ID: شناسه چت تلگرام (اختیاری)
```

---

## 📚 مستندات

### 📖 **راهنماها**

- 📘 [راهنمای نصب](docs/INSTALLATION.md) - نصب کامل گام به گام
- 📗 [راهنمای کاربر](docs/USER_GUIDE.md) - استفاده از پروژه
- 📕 [راهنمای توسعه‌دهنده](docs/DEVELOPER.md) - توسعه و مشارکت
- 📙 [API Documentation](docs/API.md) - مستندات کامل API
- 📔 [عیب‌یابی](docs/TROUBLESHOOTING.md) - حل مشکلات رایج

### 📊 **آمار پروژه**

```
📦 تعداد فایل‌ها: 350+
📝 خطوط کد: ~15,000
🔌 پروتکل‌های پشتیبانی: 10
🌍 منابع کانفیگ: 57+
🌏 کشورهای پشتیبانی: 40+
⭐ کیفیت کد: A+
```

---

## 🤝 مشارکت

مشارکت شما در بهبود این پروژه بسیار ارزشمند است! 🙏

### 📝 **نحوه مشارکت**

1. **Fork** کردن پروژه
2. ایجاد **Branch** جدید (`git checkout -b feature/amazing-feature`)
3. **Commit** تغییرات (`git commit -m 'Add amazing feature'`)
4. **Push** به Branch (`git push origin feature/amazing-feature`)
5. ایجاد **Pull Request**

### 🐛 **گزارش باگ**

برای گزارش باگ از [Issues](https://github.com/AhmadAkd/V2Ray_Collector/issues) استفاده کنید.

### 💡 **پیشنهادات**

پیشنهادات خود را از طریق [Discussions](https://github.com/AhmadAkd/V2Ray_Collector/discussions) با ما در میان بگذارید.

### 🌟 **Contributors**

<a href="https://github.com/AhmadAkd/V2Ray_Collector/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=AhmadAkd/V2Ray_Collector" />
</a>

---

## 📊 وضعیت پروژه

### ✅ **فعالیت‌های اخیر**

- ✅ افزودن 28 منبع جدید کانفیگ
- ✅ پیاده‌سازی تست فوق سریع (100 concurrent)
- ✅ افزودن Analytics پیشرفته
- ✅ پیاده‌سازی Health Monitoring
- ✅ طراحی Dashboard حرفه‌ای
- ✅ ایجاد API RESTful
- ✅ پشتیبانی Docker کامل
- ✅ مستندات جامع فارسی و انگلیسی

### 🚀 **برنامه آینده**

- [ ] افزودن پشتیبانی از Hysteria v3
- [ ] پیاده‌سازی Load Balancing
- [ ] افزودن Grafana Dashboard
- [ ] پشتیبانی از Kubernetes
- [ ] ایجاد Mobile App
- [ ] افزودن Machine Learning برای پیش‌بینی کیفیت

---

## 🔒 امنیت

برای گزارش مشکلات امنیتی، لطفاً به [SECURITY.md](SECURITY.md) مراجعه کنید.

**توجه:** هرگز اطلاعات حساس (API keys, tokens, passwords) را در کدها commit نکنید.

---

## 📄 مجوز

این پروژه تحت مجوز MIT منتشر شده است. برای اطلاعات بیشتر به فایل [LICENSE](LICENSE) مراجعه کنید.

```
MIT License

Copyright (c) 2025 Ahmad Akd

مجاز به استفاده، کپی، تغییر، ادغام، انتشار، توزیع، اعطای مجوز فرعی
و/یا فروش نسخه‌هایی از نرم‌افزار هستید.
```

---

## 🙏 تشکر و قدردانی

### 📚 **منابع استفاده شده**

- [V2Ray](https://www.v2ray.com/) - پروتکل اصلی
- [FastAPI](https://fastapi.tiangolo.com/) - API Framework
- [Bootstrap](https://getbootstrap.com/) - UI Framework
- [Chart.js](https://www.chartjs.org/) - نمودارها
- منابع کانفیگ رایگان جامعه V2Ray

### ⭐ **حمایت از پروژه**

اگر این پروژه برای شما مفید بود:

- ⭐ **Star** دادن به پروژه
- 🐛 **گزارش** باگ‌ها
- 💡 **پیشنهاد** ویژگی‌های جدید
- 🤝 **مشارکت** در توسعه
- 📢 **اشتراک‌گذاری** با دیگران

---

## 📞 ارتباط با ما

- 🐛 **Issues:** [GitHub Issues](https://github.com/AhmadAkd/V2Ray_Collector/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/AhmadAkd/V2Ray_Collector/discussions)
- 📧 **Email:** <ahmad.akd@example.com>
- 🌐 **Website:** [ahmadakd.github.io](https://ahmadakd.github.io/V2Ray_Collector/)

---

<div align="center">

**ساخته شده با ❤️ توسط [Ahmad Akd](https://github.com/AhmadAkd)**

⭐ اگر این پروژه برایتان مفید بود، Star بدهید! ⭐

[![GitHub stars](https://img.shields.io/github/stars/AhmadAkd/V2Ray_Collector?style=social)](https://github.com/AhmadAkd/V2Ray_Collector/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/AhmadAkd/V2Ray_Collector?style=social)](https://github.com/AhmadAkd/V2Ray_Collector/network/members)
[![GitHub watchers](https://img.shields.io/github/watchers/AhmadAkd/V2Ray_Collector?style=social)](https://github.com/AhmadAkd/V2Ray_Collector/watchers)

</div>

---

**نسخه:** 2.0.0  
**آخرین به‌روزرسانی:** 2025-10-14  
**وضعیت:** ✅ فعال و در حال توسعه
