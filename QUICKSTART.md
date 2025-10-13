# 🚀 راهنمای شروع سریع (Quick Start Guide)

## 📋 پیش‌نیازها

قبل از شروع، اطمینان حاصل کنید که موارد زیر را نصب کرده‌اید:

- Python 3.8 یا بالاتر
- pip (مدیر بسته‌های Python)
- Git (اختیاری)

### نصب Python

#### Windows

```bash
# دانلود از python.org و نصب
# یا با chocolatey:
choco install python
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip
```

#### macOS

```bash
brew install python3
```

---

## ⚡ نصب سریع (5 دقیقه)

### روش 1: نصب معمولی

#### 1️⃣ دانلود پروژه

```bash
# با Git:
git clone https://github.com/AhmadAkd/V2Ray_Collector.git
cd V2Ray_Collector

# یا دانلود ZIP و استخراج
```

#### 2️⃣ نصب وابستگی‌ها

```bash
pip install -r requirements.txt
```

#### 3️⃣ اجرای برنامه

```bash
# اجرای یکباره:
python config_collector.py

# یا اتوماسیون (هر 30 دقیقه):
python automation.py --mode auto
```

---

### روش 2: با Docker (پیشنهادی) 🐳

#### 1️⃣ نصب Docker

```bash
# Windows/Mac: دانلود Docker Desktop
# Linux:
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

#### 2️⃣ اجرای با Docker Compose

```bash
# دانلود پروژه
git clone https://github.com/AhmadAkd/V2Ray_Collector.git
cd V2Ray_Collector

# اجرا
docker-compose up -d

# مشاهده لاگ‌ها
docker-compose logs -f

# توقف
docker-compose down
```

---

## 🎯 اولین استفاده

### تست سریع

```bash
# تست وابستگی‌ها
python run_tests.py

# جمع‌آوری کانفیگ‌ها (یکباره)
python config_collector.py

# مشاهده نتایج
ls -la subscriptions/
```

### فایل‌های تولید شده

بعد از اجرا، فایل‌های زیر در پوشه `subscriptions/` ایجاد می‌شود:

```
subscriptions/
├── all_subscription.txt          # همه کانفیگ‌ها
├── vmess_subscription.txt        # فقط VMess
├── vless_subscription.txt        # فقط VLESS
├── trojan_subscription.txt       # فقط Trojan
├── ss_subscription.txt           # فقط Shadowsocks
├── ssr_subscription.txt          # فقط ShadowsocksR
└── report.json                   # گزارش جامع
```

---

## 📱 استفاده در کلاینت

### 1️⃣ دریافت لینک اشتراک

لینک‌های GitHub Pages:

```
https://github.com/[USERNAME]/V2Ray_Collector/raw/main/subscriptions/all_subscription.txt
https://github.com/[USERNAME]/V2Ray_Collector/raw/main/subscriptions/vmess_subscription.txt
https://github.com/[USERNAME]/V2Ray_Collector/raw/main/subscriptions/vless_subscription.txt
```

### 2️⃣ افزودن به کلاینت

#### v2rayN (Windows)

1. باز کردن v2rayN
2. `اشتراک` → `تنظیمات اشتراک`
3. افزودن URL اشتراک
4. `به‌روزرسانی اشتراک`

#### v2rayNG (Android)

1. باز کردن v2rayNG
2. `+` → `Import config from URL`
3. وارد کردن URL اشتراک
4. `تایید`

#### Fair (iOS)

1. کپی کردن لینک اشتراک
2. باز کردن Fair
3. کلیک روی `+`
4. انتخاب `Import from URL`

---

## 🔧 تنظیمات اولیه

### تنظیم فاصله زمانی اتوماسیون

در `automation.py`:

```bash
python automation.py --mode auto --interval 30  # هر 30 دقیقه
```

یا در `config.py`:

```python
AUTOMATION_CONFIG = {
    'collection_interval_minutes': 30,  # تغییر دهید
}
```

### تنظیم منابع کانفیگ

در `config.py`:

```python
CONFIG_SOURCES = [
    "https://your-source-1.com/configs.txt",
    "https://your-source-2.com/configs.txt",
    # منابع خود را اضافه کنید
]
```

### فعال‌سازی اعلان‌ها (اختیاری)

در `config.py`:

```python
NOTIFICATION_CONFIG = {
    'telegram_enabled': True,
    'telegram_bot_token': "YOUR_BOT_TOKEN",
    'telegram_chat_id': "YOUR_CHAT_ID",
}
```

---

## 🌐 استفاده از API

### اجرای API Server

```bash
python api_server.py
```

API در `http://localhost:8000` در دسترس است.

### Endpoints مفید

```bash
# آمار کلی
curl http://localhost:8000/stats

# همه کانفیگ‌ها
curl http://localhost:8000/configs

# کانفیگ‌های VMess
curl http://localhost:8000/configs/vmess

# دریافت اشتراک
curl http://localhost:8000/subscription/all

# مستندات API
# باز کردن در مرورگر: http://localhost:8000/docs
```

---

## 📊 مشاهده نتایج

### گزارش JSON

```bash
# مشاهده گزارش
cat subscriptions/report.json

# با jq (زیباتر):
cat subscriptions/report.json | jq .
```

### لاگ‌ها

```bash
# لاگ اصلی
tail -f v2ray_collector.log

# لاگ اتوماسیون
tail -f automation.log

# همه لاگ‌ها (با سیستم جدید)
tail -f logs/v2ray_collector.log
tail -f logs/automation.log
```

---

## 🔄 اتوماسیون با GitHub Actions

### فعال‌سازی GitHub Actions

1. **Fork کردن repository**
2. **فعال‌سازی GitHub Pages**:
   - Settings → Pages
   - Source: main branch
   - Folder: / (root)

3. **بررسی Actions**:
   - رفتن به تب Actions
   - اطمینان از اجرای workflow ها

### تنظیمات دستی اتوماسیون

فایل `.github/workflows/ci.yml` را ویرایش کنید:

```yaml
on:
  schedule:
    # هر 30 دقیقه
    - cron: '*/30 * * * *'
```

---

## ❓ حل مشکلات رایج

### مشکل 1: خطای نصب وابستگی‌ها

```bash
# آپگرید pip
python -m pip install --upgrade pip

# نصب مجدد
pip install -r requirements.txt --force-reinstall
```

### مشکل 2: دسترسی به منابع

```bash
# بررسی اتصال
curl https://github.com

# استفاده از proxy (اگر نیاز است)
export HTTP_PROXY="http://proxy:port"
export HTTPS_PROXY="http://proxy:port"
```

### مشکل 3: خطای Permission

```bash
# Linux/Mac:
chmod +x *.py

# Windows: اجرا با PowerShell به عنوان Administrator
```

### مشکل 4: فضای دیسک کم

```bash
# پاکسازی cache
rm -rf cache/*

# پاکسازی لاگ‌های قدیمی
rm -rf logs/*.log.old
```

---

## 📈 بهینه‌سازی

### افزایش سرعت

در `config.py`:

```python
COLLECTION_CONFIG = {
    'max_concurrent_tests': 100,  # افزایش تعداد تست همزمان
    'test_timeout': 5,  # کاهش timeout
}
```

### کاهش استفاده از منابع

```python
COLLECTION_CONFIG = {
    'max_concurrent_tests': 20,  # کاهش تعداد تست همزمان
}
```

### Cache بیشتر

```python
CACHE_CONFIG = {
    "max_size": 5000,  # افزایش اندازه cache
    "ttl": 3600,  # افزایش مدت زمان cache
}
```

---

## 🎓 آموزش‌های بیشتر

- [راهنمای کامل (USER_GUIDE.md)](docs/USER_GUIDE.md)
- [مستندات توسعه‌دهنده (DEVELOPER.md)](docs/DEVELOPER.md)
- [راهنمای نصب (INSTALLATION.md)](docs/INSTALLATION.md)
- [رفع مشکلات (TROUBLESHOOTING.md)](docs/TROUBLESHOOTING.md)
- [API Documentation (API.md)](docs/API.md)

---

## 💬 پشتیبانی

اگر مشکلی داشتید:

1. **مستندات** را بخوانید
2. **GitHub Issues** را جستجو کنید
3. **Issue جدید** ایجاد کنید
4. **Discussions** را بررسی کنید

---

## ⭐ قدم بعدی

- ⭐ به پروژه Star بدهید
- 🔀 Fork کنید و سفارشی‌سازی کنید
- 🤝 در توسعه مشارکت کنید
- 📢 به دیگران معرفی کنید

---

**موفق باشید! 🎉**

---

**نکته**: این راهنما برای شروع سریع طراحی شده. برای جزئیات بیشتر به مستندات کامل مراجعه کنید.
