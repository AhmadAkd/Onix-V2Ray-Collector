# V2Ray Config Collector & Tester

## 🔒 سیستم جمع‌آوری، تست و دسته‌بندی کانفیگ‌های رایگان V2Ray

این پروژه یک سیستم کامل برای جمع‌آوری خودکار کانفیگ‌های رایگان V2Ray، تست کیفیت آنها و ارائه لینک‌های اشتراک دسته‌بندی شده است که روی GitHub Actions اجرا می‌شود.

## ✨ ویژگی‌ها

- 🔄 **جمع‌آوری خودکار** کانفیگ‌ها از منابع مختلف
- ✅ **تست کیفیت** و اعتبارسنجی کانفیگ‌ها
- 📊 **دسته‌بندی هوشمند** بر اساس پروتکل
- ⏰ **اتوماسیون کامل** با GitHub Actions
- 📈 **گزارش‌گیری دقیق** عملکرد
- 🌐 **لینک‌های اشتراک آماده** برای استفاده

## 📡 لینک‌های اشتراک

### 🌐 صفحه اصلی
[**مشاهده تمام لینک‌ها**](https://ahmadakd.github.io/V2Ray_Collector/subscriptions/)

### 📊 Dashboard مدیریتی
[**Dashboard پیشرفته**](https://ahmadakd.github.io/V2Ray_Collector/subscriptions/dashboard.html)

### 🚀 API عمومی
```
GET /api/stats - آمار کلی
GET /api/configs - همه کانفیگ‌ها
GET /api/subscription/{protocol} - لینک اشتراک
```

### همه کانفیگ‌ها
```
https://github.com/AhmadAkd/V2Ray_Collector/raw/main/subscriptions/all_subscription.txt
```

### پروتکل‌های جداگانه

#### 🔵 VMess
```
https://github.com/AhmadAkd/V2Ray_Collector/raw/main/subscriptions/vmess_subscription.txt
```

#### 🟢 VLESS
```
https://github.com/AhmadAkd/V2Ray_Collector/raw/main/subscriptions/vless_subscription.txt
```

#### 🟡 Trojan
```
https://github.com/AhmadAkd/V2Ray_Collector/raw/main/subscriptions/trojan_subscription.txt
```

#### 🟠 Shadowsocks
```
https://github.com/AhmadAkd/V2Ray_Collector/raw/main/subscriptions/ss_subscription.txt
```

#### 🔴 ShadowsocksR
```
https://github.com/AhmadAkd/V2Ray_Collector/raw/main/subscriptions/ssr_subscription.txt
```

## 🚀 نحوه استفاده

### Android (v2rayNG)
1. نرم‌افزار v2rayNG را دانلود کنید
2. روی + کلیک کنید
3. "Subscription" را انتخاب کنید
4. یکی از لینک‌های بالا را وارد کنید
5. روی "OK" کلیک کنید

### iOS (Fair/Streisand)
1. نرم‌افزار Fair یا Streisand را دانلود کنید
2. بخش Subscription را باز کنید
3. لینک مورد نظر را اضافه کنید

### Windows (v2rayN)
1. نرم‌افزار v2rayN را دانلود کنید
2. روی "Subscribe" کلیک کنید
3. "Subscribe Settings" را انتخاب کنید
4. لینک را اضافه کنید

## 📁 ساختار پروژه

```
V2Ray_Collector/
├── .github/
│   └── workflows/
│       └── v2ray-collector.yml  # GitHub Actions workflow
├── config_collector.py           # هسته اصلی جمع‌آوری و تست
├── automation.py                 # سیستم اتوماسیون
├── config.py                    # تنظیمات سیستم
├── run_tests.py                 # اجرای تست‌ها
├── requirements.txt             # وابستگی‌ها
├── README.md                   # راهنمای فارسی
├── README_EN.md                # راهنمای انگلیسی
├── LICENSE                     # مجوز MIT
└── subscriptions/              # فایل‌های اشتراک تولید شده
    ├── index.html             # صفحه اصلی لینک‌ها
    ├── README.md             # راهنمای لینک‌ها
    ├── vmess_subscription.txt
    ├── vless_subscription.txt
    ├── trojan_subscription.txt
    ├── ss_subscription.txt
    ├── ssr_subscription.txt
    ├── all_subscription.txt
    └── latest_report.json    # آخرین گزارش عملکرد
```

## 🔧 تنظیمات

### منابع کانفیگ‌ها

می‌توانید منابع کانفیگ‌ها را در فایل `config.py` تغییر دهید:

```python
CONFIG_SOURCES = [
    "https://github.com/Epodonios/v2ray-configs/raw/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt",
    # اضافه کردن منابع جدید...
]
```

### تنظیمات تست

```python
# تعداد همزمان تست‌ها
max_concurrent_tests = 50

# زمان انتظار تست
test_timeout = 10
```

## 📊 گزارش‌گیری

### گزارش JSON

سیستم به صورت خودکار گزارش‌هایی با فرمت JSON تولید می‌کند:

```json
{
  "timestamp": "2024-01-15 14:30:00",
  "total_configs_tested": 1250,
  "working_configs": 850,
  "failed_configs": 400,
  "success_rate": "68.0%",
  "protocols": {
    "vmess": {
      "count": 400,
      "avg_latency": "245.5ms"
    },
    "vless": {
      "count": 300,
      "avg_latency": "180.2ms"
    }
  }
}
```

### API های وب

- `GET /` - صفحه اصلی
- `GET /api/stats` - آمار سیستم
- `GET /api/protocols` - لیست پروتکل‌ها
- `GET /api/health` - بررسی سلامت
- `GET /subscription/{protocol}` - دانلود فایل اشتراک

## 🔄 اتوماسیون

### زمان‌بندی پیش‌فرض

- **هر 30 دقیقه**: جمع‌آوری و تست کانفیگ‌ها
- **هر ساعت**: بررسی سلامت سیستم
- **هر روز ساعت 2 صبح**: تمیزکاری فایل‌های قدیمی
- **هر دوشنبه ساعت 8 صبح**: گزارش هفتگی

### تغییر زمان‌بندی

```python
# در فایل config.py
AUTOMATION_CONFIG = {
    'collection_interval_minutes': 15,  # هر 15 دقیقه
    'cleanup_hour': 1,  # ساعت 1 صبح
}
```

## 🛠️ تنظیمات پیشرفته

### اجرای در پس‌زمینه (Linux/Mac)

```bash
# اجرای در پس‌زمینه
nohup python automation.py --mode auto > automation.log 2>&1 &

# بررسی وضعیت
ps aux | grep automation.py
```

### اجرای با Docker

```bash
# ساخت و اجرای کانتینر
docker-compose up -d

# مشاهده لاگ‌ها
docker-compose logs -f
```

### اجرای با systemd (Linux)

```bash
# ایجاد سرویس
sudo ./deploy.sh --service

# فعال‌سازی سرویس
sudo systemctl enable v2ray-collector
sudo systemctl start v2ray-collector
```

## 📱 استفاده از لینک‌های اشتراک

### Android (v2rayNG)

1. نرم‌افزار v2rayNG را دانلود کنید
2. روی + کلیک کنید
3. "Subscription" را انتخاب کنید
4. لینک مورد نظر را وارد کنید
5. روی "OK" کلیک کنید

### iOS (Fair/Streisand)

1. نرم‌افزار Fair یا Streisand را دانلود کنید
2. بخش Subscription را باز کنید
3. لینک را اضافه کنید

### Windows (v2rayN)

1. نرم‌افزار v2rayN را دانلود کنید
2. روی "Subscribe" کلیک کنید
3. "Subscribe Settings" را انتخاب کنید
4. لینک را اضافه کنید

## 🧪 تست سیستم

```bash
# اجرای تمام تست‌ها
python run_tests.py

# تست یکباره
python automation.py --mode once

# تست سرور وب
python web_server.py --debug
```

## 🔍 عیب‌یابی

### مشکلات رایج

#### خطای اتصال

```
خطا: Connection timeout
راه‌حل: بررسی اتصال اینترنت و فایروال
```

#### خطای مجوز

```
خطا: Permission denied
راه‌حل: اجرای با دسترسی ادمین یا تغییر مجوز فایل‌ها
```

#### خطای وابستگی

```
خطا: Module not found
راه‌حل: pip install -r requirements.txt
```

### لاگ‌ها

- `v2ray_collector.log` - لاگ اصلی جمع‌آوری
- `automation.log` - لاگ اتوماسیون
- `test_report.json` - گزارش تست‌ها

## 🌟 ویژگی‌های کلیدی

1. **کیفیت بالاتر**: فقط کانفیگ‌های تست شده و سالم
2. **دسته‌بندی بهتر**: تفکیک بر اساس پروتکل
3. **رابط کاربری**: وب‌سایت فارسی و انگلیسی
4. **اتوماسیون**: به‌روزرسانی خودکار
5. **گزارش‌گیری**: آمار دقیق عملکرد
6. **API**: دسترسی برنامه‌نویسی
7. **قابلیت تنظیم**: تمام پارامترها قابل تغییر
8. **Docker**: پشتیبانی کامل از کانتینری‌سازی

## 🤝 مشارکت

برای مشارکت در پروژه:

1. Fork کنید
2. شاخه جدید بسازید
3. تغییرات را commit کنید
4. Pull Request ارسال کنید

## 📄 مجوز

این پروژه تحت مجوز MIT منتشر شده است.

## 📞 پشتیبانی

برای پشتیبانی و گزارش مشکل:

- GitHub Issues
- Email: your-email@example.com

---

**نکته مهم**: این سیستم فقط کانفیگ‌های رایگان را جمع‌آوری می‌کند و هیچ کانفیگ پولی یا خصوصی در آن ذخیره نمی‌شود.

---

Made with ❤️ for the V2Ray community
