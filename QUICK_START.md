# 🚀 راهنمای سریع شروع کار

## 📦 نصب

### **1. نصب پکیج‌های اصلی**
```bash
pip install -r requirements.txt
```

### **2. نصب ویژگی‌های پیشرفته (اختیاری)**
```bash
# پکیج‌های ضروری
pip install -r requirements_core.txt

# Telegram Bot (اختیاری)
pip install python-telegram-bot

# Monitoring (اختیاری)
pip install prometheus-client
```

---

## ⚙️ تنظیمات اولیه

### **1. کپی فایل تنظیمات**
```bash
cp config.env.example config.env
```

### **2. ویرایش تنظیمات (اختیاری)**
```bash
# ویرایش config.env و تنظیم:
# - TELEGRAM_BOT_TOKEN (برای Telegram)
# - سایر تنظیمات مورد نیاز
```

---

## 🎯 استفاده از ویژگی‌های جدید

### **تست اصلی سیستم**
```bash
python config_collector.py
```

### **تست پیشرفته پروتکل‌ها**
```python
from config_collector import UltraFastConnectionPool

pool = UltraFastConnectionPool()
is_working, latency, details = pool.test_connection_advanced(
    address='1.1.1.1',
    port=443
)
print(f"Working: {is_working}, Latency: {latency}ms")
```

### **Telegram Bot**

#### **راه‌اندازی:**
```bash
# 1. دریافت Token از @BotFather
# 2. تنظیم در config.env:
#    TELEGRAM_BOT_TOKEN=your_token_here

# 3. تست اتصال
python test_telegram.py

# 4. جمع‌آوری از تلگرام
python telegram_collector.py
```

#### **استفاده در کد:**
```python
from telegram_collector import TelegramCollector, TelegramSource

collector = TelegramCollector(bot_token="YOUR_TOKEN")

source = TelegramSource(
    channel_id="@v2rayngvpn",
    channel_name="V2RayNG VPN"
)
collector.add_source(source)

# جمع‌آوری
configs = await collector.collect_all_sources()
print(f"جمع‌آوری شد: {len(configs)} کانفیگ")
```

### **Monitoring پیشرفته**
```bash
python advanced_monitoring.py
```

```python
from advanced_monitoring import AdvancedMonitor

monitor = AdvancedMonitor()

# نظارت بر کانفیگ‌ها
health_data = await monitor.monitor_config_health(configs)

# نظارت بر سیستم
metrics = await monitor.monitor_system_metrics()

# بررسی هشدارها
alerts = monitor.check_alerts(health_data, metrics)

# گزارش سلامت
report = monitor.generate_health_report()
```

### **پروتکل‌های جدید**
```python
from new_protocols import NewProtocolParser

parser = NewProtocolParser()

# تجزیه Reality
config = parser.parse_reality_config("reality://...")

# تجزیه Tuic v5
config = parser.parse_tuic5_config("tuic5://...")

# لیست پروتکل‌ها
protocols = parser.get_supported_protocols()
```

---

## 🔧 عیب‌یابی

### **مشکل: uvloop نصب نمی‌شود**
```bash
# uvloop فقط برای Linux/Mac است
# در Windows نیازی به آن نیست
```

### **مشکل: sqlite3 پیدا نمی‌شود**
```bash
# sqlite3 داخلی پایتون است
# نیازی به نصب ندارد
```

### **مشکل: Telegram Bot کار نمی‌کند**
```bash
# 1. Token را بررسی کنید
# 2. اتصال اینترنت را بررسی کنید
# 3. VPN فعال کنید (اگر در ایران هستید)
# 4. test_telegram.py را اجرا کنید
```

---

## 📊 ساختار پروژه

```
V2Ray-Checker/
├── config_collector.py         # سیستم اصلی
├── config.py                   # تنظیمات
├── advanced_protocol_tester.py # تست پیشرفته
├── advanced_monitoring.py      # نظارت پیشرفته
├── telegram_collector.py       # جمع‌آوری از تلگرام
├── new_protocols.py           # پروتکل‌های جدید
├── test_telegram.py           # تست Telegram Bot
├── config.env.example         # نمونه تنظیمات
├── requirements.txt           # وابستگی‌های اصلی
├── requirements_core.txt      # وابستگی‌های ضروری
├── requirements_optional.txt  # وابستگی‌های اختیاری
├── IMPROVEMENTS.md            # مستندات کامل
└── QUICK_START.md            # این فایل
```

---

## 🎓 آموزش‌ها

### **دریافت Telegram Bot Token**
1. به [@BotFather](https://t.me/BotFather) پیام دهید
2. دستور `/newbot` را بزنید
3. نام ربات را وارد کنید (مثلاً: My V2Ray Bot)
4. Username منحصر به فرد انتخاب کنید (باید به bot ختم شود)
5. Token دریافتی را کپی کنید
6. در فایل `config.env` قرار دهید

### **اضافه کردن ربات به کانال**
1. به کانال مورد نظر بروید
2. Settings → Administrators
3. Add Administrator
4. ربات خود را انتخاب کنید
5. دسترسی "Post Messages" را بدهید

---

## 📈 عملکرد

### **سیستم فعلی:**
- ⏱️ سرعت: 50 کانفیگ/ثانیه
- ✅ نرخ موفقیت: 68.8%
- 🔌 پروتکل‌ها: 17
- 🌍 منابع: 68+

### **با ویژگی‌های جدید:**
- ⏱️ سرعت: 100+ کانفیگ/ثانیه (انتظار)
- ✅ نرخ موفقیت: 75%+ (انتظار)
- 🔌 پروتکل‌ها: 17
- 🌍 منابع: 100+ (با Telegram)

---

## 🆘 کمک

- **Issues**: [GitHub Issues](https://github.com/AhmadAkd/Onix-V2Ray-Collector/issues)
- **Discussions**: [GitHub Discussions](https://github.com/AhmadAkd/Onix-V2Ray-Collector/discussions)
- **Documentation**: [IMPROVEMENTS.md](IMPROVEMENTS.md)

---

**🎉 موفق باشید!**
