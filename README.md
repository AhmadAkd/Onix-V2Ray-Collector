# V2Ray Config Collector & Tester

## 🔒 سیستم جمع‌آوری، تست و دسته‌بندی کانفیگ‌های رایگان V2Ray

این پروژه یک سیستم کامل برای جمع‌آوری خودکار کانفیگ‌های رایگان V2Ray، تست کیفیت آنها و ارائه لینک‌های اشتراک دسته‌بندی شده است.

## ✨ ویژگی‌ها

- 🔄 **جمع‌آوری خودکار** کانفیگ‌ها از منابع مختلف
- ✅ **تست کیفیت** و اعتبارسنجی کانفیگ‌ها
- 📊 **دسته‌بندی هوشمند** بر اساس پروتکل
- 🌐 **سرور وب** برای ارائه آسان
- ⏰ **اتوماسیون کامل** با زمان‌بندی
- 📈 **گزارش‌گیری دقیق** عملکرد

## 🚀 نصب و راه‌اندازی

### پیش‌نیازها

- Python 3.8 یا بالاتر
- pip

### نصب وابستگی‌ها

```bash
pip install -r requirements.txt
```

## 📖 نحوه استفاده

### 1. اجرای یکباره

```bash
python config_collector.py
```

### 2. اجرای سیستم اتوماسیون

```bash
# اجرای خودکار هر 30 دقیقه
python automation.py --mode auto

# اجرای خودکار با فاصله زمانی سفارشی
python automation.py --mode auto --interval 15

# اجرای یکباره
python automation.py --mode once
```

### 3. اجرای سرور وب

```bash
# اجرای سرور روی پورت پیش‌فرض (5000)
python web_server.py

# اجرای با تنظیمات سفارشی
python web_server.py --host 0.0.0.0 --port 8080
```

### 4. شروع سریع

```bash
python start.py
```

## 📁 ساختار پروژه

```
V2Ray_Collector/
├── config_collector.py      # هسته اصلی جمع‌آوری و تست
├── automation.py            # سیستم اتوماسیون
├── web_server.py           # سرور وب
├── config.py              # تنظیمات سیستم
├── start.py               # اسکریپت شروع سریع
├── run_tests.py           # اجرای تست‌ها
├── deploy.sh              # اسکریپت استقرار
├── requirements.txt       # وابستگی‌ها
├── README.md             # راهنمای فارسی
├── README_EN.md          # راهنمای انگلیسی
├── LICENSE               # مجوز MIT
├── Dockerfile            # کانتینر Docker
├── docker-compose.yml    # تنظیمات Docker
└── subscriptions/        # فایل‌های اشتراک تولید شده
    ├── vmess_subscription.txt
    ├── vless_subscription.txt
    ├── trojan_subscription.txt
    ├── ss_subscription.txt
    ├── ssr_subscription.txt
    ├── all_subscription.txt
    └── report_*.json     # گزارش‌های عملکرد
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
