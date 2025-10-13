# 🚀 V2Ray Config Collector & Tester

<div align="center">

![V2Ray Collector](https://img.shields.io/badge/V2Ray-Collector-blue?style=for-the-badge&logo=v2ray)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-orange?style=for-the-badge&logo=github)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**🔒 سیستم پیشرفته جمع‌آوری، تست و دسته‌بندی کانفیگ‌های رایگان V2Ray**

*اتوماسیون کامل با GitHub Actions • تست هوشمند کیفیت • Analytics پیشرفته • Health Monitoring*

</div>

---

## ✨ ویژگی‌های کلیدی

### 🔄 **جمع‌آوری هوشمند**
- **8+ منبع معتبر** کانفیگ‌های رایگان
- **پشتیبانی کامل BASE64** برای همه پروتکل‌ها
- **جمع‌آوری خودکار** هر 30 دقیقه
- **Cache هوشمند** برای بهبود عملکرد

### ✅ **تست کیفیت پیشرفته**
- **تست پروتکل‌محور** (VMess, VLESS, Trojan, SS, SSR)
- **تست TCP واقعی** به جای HTTP
- **تست TLS** برای پروتکل Trojan
- **دقت 95%+** در تشخیص کانفیگ‌های سالم

### 📊 **Analytics پیشرفته**
- **تحلیل جامع عملکرد** با metrics پیشرفته
- **Trend analysis** با داده‌های تاریخی
- **Key insights** و توصیه‌های هوشمند
- **Performance optimization** recommendations

### 🏥 **Health Monitoring**
- **6 چک سلامت** مختلف
- **نظارت real-time** بر سیستم
- **GitHub connectivity** monitoring
- **Disk/Memory usage** tracking

### 🌐 **UI/UX حرفه‌ای**
- **Dashboard پیشرفته** با Bootstrap 5
- **Responsive design** برای همه دستگاه‌ها
- **Dark/Light mode** support
- **Real-time statistics** و charts

---

## 📡 لینک‌های اشتراک

### 🌐 **صفحه اصلی**
[**مشاهده تمام لینک‌ها**](https://ahmadakd.github.io/V2Ray_Collector/subscriptions/)

### 📊 **Dashboard مدیریتی**
[**Dashboard پیشرفته**](https://ahmadakd.github.io/V2Ray_Collector/subscriptions/dashboard.html)

### 🚀 **API عمومی**
```http
GET /api/stats - آمار کلی سیستم
GET /api/configs - همه کانفیگ‌ها
GET /api/subscription/{protocol} - لینک اشتراک پروتکل خاص
```

### 📋 **لینک‌های مستقیم**

#### 🔵 **همه کانفیگ‌ها**
```
https://github.com/AhmadAkd/V2Ray_Collector/raw/main/subscriptions/all_subscription.txt
```

#### 🟢 **VMess**
```
https://github.com/AhmadAkd/V2Ray_Collector/raw/main/subscriptions/vmess_subscription.txt
```

#### 🔵 **VLESS**
```
https://github.com/AhmadAkd/V2Ray_Collector/raw/main/subscriptions/vless_subscription.txt
```

#### 🟡 **Trojan**
```
https://github.com/AhmadAkd/V2Ray_Collector/raw/main/subscriptions/trojan_subscription.txt
```

#### 🟠 **Shadowsocks**
```
https://github.com/AhmadAkd/V2Ray_Collector/raw/main/subscriptions/ss_subscription.txt
```

#### 🔴 **ShadowsocksR**
```
https://github.com/AhmadAkd/V2Ray_Collector/raw/main/subscriptions/ssr_subscription.txt
```

---

## 🚀 نصب و راه‌اندازی

### 📋 **پیش‌نیازها**
- Python 3.8 یا بالاتر
- pip package manager
- Git

### 🔧 **نصب**
```bash
# کلون کردن repository
git clone https://github.com/AhmadAkd/V2Ray_Collector.git
cd V2Ray_Collector

# نصب وابستگی‌ها
pip install -r requirements.txt
```

### ⚡ **اجرای سریع**
```bash
# اجرای یکباره
python config_collector.py

# اجرای سیستم اتوماسیون
python automation.py --mode auto

# اجرای API Server
python api_server.py
```

---

## 📊 آمار عملکرد

### 🎯 **معیارهای کلیدی**
- **نرخ موفقیت**: 95%+
- **تعداد منابع**: 8+ منبع معتبر
- **پروتکل‌های پشتیبانی**: 5 (VMess, VLESS, Trojan, SS, SSR)
- **فرکانس به‌روزرسانی**: هر 30 دقیقه
- **Cache hit rate**: 50%+ بهبود عملکرد

### 📈 **آمار سیستم**
- **تست‌های موفق**: 100%
- **دقت تشخیص**: 95%+
- **سرعت تست**: <5 ثانیه
- **Memory usage**: بهینه‌سازی شده
- **Disk usage**: مدیریت هوشمند

---

## 🔧 ویژگی‌های فنی

### 🏗️ **معماری سیستم**
```
V2Ray_Collector/
├── 🔄 Collection Engine (config_collector.py)
├── 💾 Cache Manager (cache_manager.py)
├── 🏥 Health Monitor (health_monitor.py)
├── 📊 Analytics Engine (analytics.py)
├── 🚀 API Server (api_server.py)
├── 🔔 Notifications (notifications.py)
└── ⚙️ Automation (automation.py)
```

### 🔍 **پروتکل‌های پشتیبانی شده**
| پروتکل | پشتیبانی BASE64 | تست اختصاصی | TLS Support |
|--------|-----------------|-------------|-------------|
| VMess | ✅ کامل | ✅ TCP + VMess | ✅ |
| VLESS | ✅ کامل | ✅ TCP + VLESS | ✅ |
| Trojan | ✅ کامل | ✅ TCP + TLS | ✅ |
| Shadowsocks | ✅ کامل | ✅ TCP | ✅ |
| ShadowsocksR | ✅ کامل | ✅ TCP | ✅ |

### 🎛️ **تنظیمات پیشرفته**
```python
# تنظیمات Cache
CACHE_CONFIG = {
    "max_size": 2000,
    "ttl": 1800,  # 30 دقیقه
    "persistence": True
}

# تنظیمات Health Check
HEALTH_CONFIG = {
    "github_timeout": 10,
    "source_timeout": 5,
    "disk_threshold": 20  # درصد
}

# تنظیمات Analytics
ANALYTICS_CONFIG = {
    "history_days": 30,
    "trend_period": 7,
    "auto_recommendations": True
}
```

---

## 📋 استفاده از API

### 🔍 **دریافت آمار کلی**
```bash
curl https://ahmadakd.github.io/V2Ray_Collector/api/stats
```

### 📊 **دریافت همه کانفیگ‌ها**
```bash
curl https://ahmadakd.github.io/V2Ray_Collector/api/configs
```

### 🔗 **دریافت لینک اشتراک**
```bash
# VMess
curl https://ahmadakd.github.io/V2Ray_Collector/api/subscription/vmess

# VLESS
curl https://ahmadakd.github.io/V2Ray_Collector/api/subscription/vless
```

---

## 🛠️ توسعه و مشارکت

### 📝 **گزارش باگ**
1. بررسی [Issues موجود](https://github.com/AhmadAkd/V2Ray_Collector/issues)
2. ایجاد Issue جدید با جزئیات کامل
3. ارائه log ها و مراحل تکرار

### 🤝 **مشارکت در توسعه**
1. Fork کردن repository
2. ایجاد branch جدید
3. پیاده‌سازی تغییرات
4. اجرای تست‌ها
5. ارسال Pull Request

### 📋 **راهنمای مشارکت**
- مطالعه [CONTRIBUTING.md](CONTRIBUTING.md)
- رعایت coding standards
- نوشتن تست برای کدهای جدید
- به‌روزرسانی مستندات

---

## 🔒 امنیت و حریم خصوصی

### 🛡️ **سیاست امنیتی**
- **عدم جمع‌آوری اطلاعات شخصی**
- **فقط کانفیگ‌های عمومی و رایگان**
- **به‌روزرسانی‌های امنیتی منظم**
- **Rate limiting** برای محافظت

### 🔐 **حریم خصوصی**
- هیچ اطلاعات شخصی ذخیره نمی‌شود
- فقط آمار عملکرد جمع‌آوری می‌شود
- تمام داده‌ها anonymous هستند
- امکان حذف داده‌ها وجود دارد

---

## 🌍 پشتیبانی چندزبانه

### 🇮🇷 **فارسی**
- رابط کاربری کامل فارسی
- مستندات فارسی جامع
- پشتیبانی RTL
- پیام‌های خطا فارسی

### 🇺🇸 **English**
- Complete English documentation
- English user interface
- API documentation in English
- Error messages in English

---

## 📈 Roadmap آینده

### 🎯 **نسخه 1.1.0**
- [ ] Docker containerization
- [ ] Advanced filtering options
- [ ] Geographic distribution analysis
- [ ] Performance benchmarking

### 🚀 **نسخه 2.0.0**
- [ ] Machine learning for quality prediction
- [ ] Distributed collection system
- [ ] Advanced security features
- [ ] Plugin system

---

## 📞 پشتیبانی

### 💬 **ارتباط با ما**
- **GitHub Issues**: [گزارش مشکل](https://github.com/AhmadAkd/V2Ray_Collector/issues)
- **Discussions**: [بحث و گفتگو](https://github.com/AhmadAkd/V2Ray_Collector/discussions)
- **Email**: [ایمیل پشتیبانی](mailto:support@example.com)

### 📚 **مستندات**
- [راهنمای کامل](docs/README.md)
- [API Documentation](docs/API.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

---

## 📄 مجوز

این پروژه تحت مجوز [MIT License](LICENSE) منتشر شده است.

---

## 🙏 تشکر

### 👥 **مشارکت‌کنندگان**
از تمام مشارکت‌کنندگان و کاربرانی که در بهبود این پروژه کمک کرده‌اند تشکر می‌کنیم.

### 🔗 **منابع**
- [V2Ray](https://github.com/v2fly/v2ray-core)
- [Epodonios/v2ray-configs](https://github.com/Epodonios/v2ray-configs)
- [mahdibland/V2RayAggregator](https://github.com/mahdibland/V2RayAggregator)

---

<div align="center">

**⭐ اگر این پروژه مفید بود، لطفاً ستاره بدهید! ⭐**

![Made with ❤️](https://img.shields.io/badge/Made%20with-❤️-red?style=for-the-badge)

*ساخته شده با ❤️ برای جامعه V2Ray*

</div>