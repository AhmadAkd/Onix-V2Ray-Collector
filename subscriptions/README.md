# 📡 V2Ray Subscription Links

این پوشه شامل لینک‌های اشتراک V2Ray است که به صورت خودکار هر 30 دقیقه به‌روزرسانی می‌شوند.

## 📋 فایل‌های موجود

### 🌐 صفحات وب

- **[index.html](index.html)** - صفحه اصلی با لینک‌های مستقیم
- **[dashboard.html](dashboard.html)** - داشبورد مدیریتی با آمار کامل و AI Quality Metrics
- **[subscription_selector.html](subscription_selector.html)** - انتخابگر هوشمند لینک‌ها

### 📦 فایل‌های اشتراک

#### همه کانفیگ‌ها

- `all_subscription.txt` - تمام کانفیگ‌های سالم
- `latest_report.json` - آخرین گزارش جمع‌آوری با آمار AI

#### بر اساس پروتکل

- `vmess_subscription.txt` - کانفیگ‌های VMess
- `vless_subscription.txt` - کانفیگ‌های VLESS
- `trojan_subscription.txt` - کانفیگ‌های Trojan
- `ss_subscription.txt` - کانفیگ‌های Shadowsocks
- `ssr_subscription.txt` - کانفیگ‌های ShadowsocksR
- `hysteria_subscription.txt` - کانفیگ‌های Hysteria

#### دسته‌بندی شده

- `by_protocol/` - دسته‌بندی بر اساس پروتکل
- `by_country/` - دسته‌بندی بر اساس کشور (25+ فایل)

### 📊 گزارش‌ها

- `latest_report.json` - آخرین گزارش جمع‌آوری
- `report.json` - گزارش کامل
- `analytics_report.json` - گزارش تحلیلی با AI Quality Metrics

## 🔗 نحوه استفاده

### 1️⃣ استفاده مستقیم

کپی کردن لینک و وارد کردن در کلاینت V2Ray:

```
https://raw.githubusercontent.com/rpg-dev420/Onix-V2Ray-Collector/main/subscriptions/all_subscription.txt
```

### 2️⃣ استفاده از صفحات وب

- مراجعه به [index.html](https://rpg-dev420.github.io/Onix-V2Ray-Collector/)
- انتخاب پروتکل یا کشور مورد نظر
- کپی لینک با یک کلیک

### 3️⃣ استفاده از API

```bash
# دریافت آمار کامل
curl https://rpg-dev420.github.io/Onix-V2Ray-Collector/subscriptions/latest_report.json

# دریافت کانفیگ‌های VLESS
curl https://rpg-dev420.github.io/Onix-V2Ray-Collector/subscriptions/vless_subscription.txt

# دریافت کانفیگ‌های آمریکا
curl https://rpg-dev420.github.io/Onix-V2Ray-Collector/subscriptions/by_country/US.txt
```

## 🤖 ویژگی‌های AI

### 🧠 **AI Quality Scoring**

- **امتیازدهی هوشمند** کانفیگ‌ها بر اساس Machine Learning
- **دسته‌بندی کیفیت**: عالی، خوب، متوسط، ضعیف
- **سطح اطمینان** برای هر پیش‌بینی
- **تحلیل ویژگی‌ها** و اهمیت آن‌ها

### 📊 **AI Dashboard**

- **توزیع کیفیت AI** - نمایش دسته‌بندی‌های مختلف
- **امتیازات کیفیت** - مقایسه امتیازات مختلف
- **Feature Importance** - اهمیت ویژگی‌ها
- **Confidence Levels** - سطح اطمینان

## 📈 آمار

- 🔄 به‌روزرسانی: هر 30 دقیقه
- ✅ تست شده: تمام کانفیگ‌ها
- 🌍 کشورها: 25+
- 🔌 پروتکل‌ها: 17+
- 📊 نرخ موفقیت: ~70%
- 🤖 AI Quality: فعال
- 📊 میانگین AI Score: 0.75+

## ⚡ کلاینت‌های پشتیبانی شده

- v2rayNG (Android)
- v2rayN (Windows)
- Shadowrocket (iOS)
- Clash (همه پلتفرم‌ها)
- Qv2ray (همه پلتفرم‌ها)
- SingBox (همه پلتفرم‌ها)

## 🔒 امنیت

تمام کانفیگ‌ها:

- ✅ تست شده و سالم
- ✅ از منابع معتبر
- ✅ بدون malware
- ✅ به‌روزرسانی مداوم
- ✅ امتیازدهی AI برای کیفیت

## 🚀 ویژگی‌های جدید

### 🤖 **AI Quality System**

- **RandomForest Model** برای پیش‌بینی کیفیت
- **15+ ویژگی** برای تحلیل
- **Real-time Scoring** در هر بروزرسانی
- **Quality Categories** خودکار

### 📊 **Advanced Analytics**

- **SQLite Database** برای تاریخچه
- **Performance Monitoring** 
- **Trend Analysis**
- **Source Health Monitoring**

### 🎨 **Modern UI**

- **Responsive Design** 
- **Dark/Light Theme**
- **Real-time Updates**
- **Interactive Charts**

---

**نکته:** این فایل‌ها توسط GitHub Actions به صورت خودکار تولید می‌شوند و شامل AI Quality Scoring هستند.
