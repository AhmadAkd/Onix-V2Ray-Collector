# 📡 V2Ray Subscription Links

این پوشه شامل لینک‌های اشتراک V2Ray است که به صورت خودکار هر 30 دقیقه به‌روزرسانی می‌شوند.

## 📋 فایل‌های موجود

### 🌐 صفحات وب

- **[index.html](index.html)** - صفحه اصلی با لینک‌های مستقیم
- **[dashboard.html](dashboard.html)** - داشبورد مدیریتی با آمار کامل
- **[subscription_selector.html](subscription_selector.html)** - انتخابگر هوشمند لینک‌ها

### 📦 فایل‌های اشتراک

#### همه کانفیگ‌ها
- `all_subscription.txt` - تمام کانفیگ‌های سالم

#### بر اساس پروتکل
- `vmess_subscription.txt` - کانفیگ‌های VMess
- `vless_subscription.txt` - کانفیگ‌های VLESS
- `trojan_subscription.txt` - کانفیگ‌های Trojan
- `ss_subscription.txt` - کانفیگ‌های Shadowsocks
- `ssr_subscription.txt` - کانفیگ‌های ShadowsocksR

#### دسته‌بندی شده
- `by_protocol/` - دسته‌بندی بر اساس پروتکل
- `by_country/` - دسته‌بندی بر اساس کشور (270+ فایل)

### 📊 گزارش‌ها

- `latest_report.json` - آخرین گزارش جمع‌آوری
- `report.json` - گزارش کامل
- `analytics_report.json` - گزارش تحلیلی

## 🔗 نحوه استفاده

### 1️⃣ استفاده مستقیم
کپی کردن لینک و وارد کردن در کلاینت V2Ray:
```
https://raw.githubusercontent.com/AhmadAkd/V2Ray_Collector/main/subscriptions/all_subscription.txt
```

### 2️⃣ استفاده از صفحات وب
- مراجعه به [index.html](https://ahmadakd.github.io/V2Ray_Collector/)
- انتخاب پروتکل یا کشور مورد نظر
- کپی لینک با یک کلیک

### 3️⃣ استفاده از API
```bash
curl https://ahmadakd.github.io/V2Ray_Collector/subscriptions/latest_report.json
```

## 📈 آمار

- 🔄 به‌روزرسانی: هر 30 دقیقه
- ✅ تست شده: تمام کانفیگ‌ها
- 🌍 کشورها: 270+
- 🔌 پروتکل‌ها: 10
- 📊 نرخ موفقیت: ~70%

## ⚡ کلاینت‌های پشتیبانی شده

- v2rayNG (Android)
- v2rayN (Windows)
- Shadowrocket (iOS)
- Clash (همه پلتفرم‌ها)
- Qv2ray (همه پلتفرم‌ها)

## 🔒 امنیت

تمام کانفیگ‌ها:
- ✅ تست شده و سالم
- ✅ از منابع معتبر
- ✅ بدون malware
- ✅ به‌روزرسانی مداوم

---

**نکته:** این فایل‌ها توسط GitHub Actions به صورت خودکار تولید می‌شوند.

