# 🚀 بهبودهای پیشرفته V2Ray Collector

## 📋 فهرست بهبودها

### **فاز 1: بهبودهای فوری (تکمیل شده)** ✅

#### **1. تست پیشرفته پروتکل‌ها** 
```python
# ویژگی‌های جدید:
- تست واقعی handshake برای هر پروتکل
- ارسال و دریافت داده برای تأیید کارکرد
- جمع‌آوری جزئیات بیشتر (response size, etc.)
- تست پیشرفته با timeout قابل تنظیم

# فایل: config_collector.py
# متد جدید: test_connection_advanced()
```

#### **2. پروتکل‌های جدید**
```python
# پروتکل‌های اضافه شده:
✅ Reality Protocol
✅ Tuic v5  
✅ Hysteria v3
✅ Xray Reality
✅ SingBox Universal
✅ Clash Meta

# فایل: new_protocols.py
# پارسرهای مختص هر پروتکل
```

#### **3. سیستم Monitoring پیشرفته**
```python
# امکانات:
✅ SQLite database برای تاریخچه
✅ Config Health Monitoring
✅ System Metrics (CPU, Memory, Network)
✅ Alert System با threshold ها
✅ Health Report Generator

# فایل: advanced_monitoring.py
```

---

### **فاز 2: ادغام Telegram** ⏳

#### **1. Telegram Bot Integration**
```python
# امکانات:
- جمع‌آوری خودکار از کانال‌ها
- نظارت مداوم (continuous monitoring)
- استخراج هوشمند کانفیگ‌ها
- پشتیبانی از media messages

# فایل: telegram_collector.py
# نیاز به Bot Token از @BotFather
```

#### **2. نحوه راه‌اندازی Telegram Bot**
```bash
# 1. دریافت Bot Token
# به @BotFather در تلگرام پیام دهید:
# /newbot
# نام ربات را وارد کنید و username منحصر به فرد

# 2. تنظیم Token در فایل
# config.env.example را کپی کرده و نام آن را به config.env تغییر دهید
cp config.env.example config.env

# 3. Token را در فایل وارد کنید
TELEGRAM_BOT_TOKEN=your_actual_token_here

# 4. کانال‌های مورد نظر را اضافه کنید
TELEGRAM_CHANNELS=@v2rayngvpn,@freev2ray,@vpnconfigs

# 5. ربات را به کانال‌ها اضافه کنید
# ربات را به عنوان ادمین به کانال‌ها اضافه کنید

# 6. اجرای Telegram Collector
python telegram_collector.py
```

---

### **فاز 3: بهینه‌سازی‌های اضافی** 📊

#### **1. Advanced Analytics**
```python
# Machine Learning Features:
- پیش‌بینی کیفیت کانفیگ‌ها
- تشخیص خودکار کانفیگ‌های تقلبی  
- بهینه‌سازی خودکار منابع
- Anomaly Detection

# نیاز به: scikit-learn, tensorflow
```

#### **2. Geographic Intelligence**
```python
# ویژگی‌های جغرافیایی:
- نقشه تعاملی سرورها
- انتخاب بهترین سرور بر اساس موقعیت
- تست از نقاط مختلف جهان
- CDN Integration

# نیاز به: GeoPy, Folium
```

#### **3. API RESTful**
```python
# Endpoints:
GET /api/v1/configs - لیست همه کانفیگ‌ها
GET /api/v1/configs/{protocol} - کانفیگ‌های یک پروتکل
GET /api/v1/configs/country/{code} - کانفیگ‌های یک کشور
GET /api/v1/health - وضعیت سلامت سیستم
GET /api/v1/stats - آمار کلی
POST /api/v1/test - تست یک کانفیگ

# استفاده از FastAPI
# فایل: api_server.py
```

---

## 🔧 نصب و راه‌اندازی

### **نصب وابستگی‌های پایه**
```bash
pip install -r requirements.txt
```

### **نصب وابستگی‌های پیشرفته**
```bash
pip install -r requirements_enhanced.txt
```

### **راه‌اندازی با Docker**
```bash
# Build
docker build -t v2ray-collector:enhanced .

# Run
docker run -d \\
  --name v2ray-collector \\
  -v $(pwd)/subscriptions:/app/subscriptions \\
  -v $(pwd)/monitoring.db:/app/monitoring.db \\
  -e TELEGRAM_BOT_TOKEN=your_token \\
  v2ray-collector:enhanced
```

---

## 📊 استفاده از ویژگی‌های جدید

### **1. تست پیشرفته**
```python
from config_collector import V2RayCollector

collector = V2RayCollector()

# تست معمولی
configs = await collector.run_collection_cycle()

# تست پیشرفته با جزئیات بیشتر
pool = UltraFastConnectionPool()
is_working, latency, details = pool.test_connection_advanced(
    address='1.1.1.1',
    port=443,
    protocol='tcp'
)

print(f"Working: {is_working}")
print(f"Latency: {latency}ms")
print(f"Details: {details}")
```

### **2. Monitoring**
```python
from advanced_monitoring import AdvancedMonitor

monitor = AdvancedMonitor()

# نظارت بر سلامت کانفیگ‌ها
health_data = await monitor.monitor_config_health(configs)

# نظارت بر معیارهای سیستم
metrics = await monitor.monitor_system_metrics()

# بررسی هشدارها
alerts = monitor.check_alerts(health_data, metrics)

# تولید گزارش
report = monitor.generate_health_report()
```

### **3. Telegram Collection**
```python
from telegram_collector import TelegramCollector, TelegramSource

# ایجاد collector
collector = TelegramCollector(bot_token="YOUR_TOKEN")

# اضافه کردن منابع
source = TelegramSource(
    channel_id="@v2rayngvpn",
    channel_name="V2RayNG VPN"
)
collector.add_source(source)

# جمع‌آوری
configs = await collector.collect_all_sources()

# نظارت مداوم (هر 10 دقیقه)
await collector.monitor_channels(interval=600)
```

### **4. پروتکل‌های جدید**
```python
from new_protocols import NewProtocolParser

parser = NewProtocolParser()

# تجزیه کانفیگ Reality
reality_config = parser.parse_reality_config(
    "reality://eyJ..."
)

# تجزیه کانفیگ Tuic v5
tuic5_config = parser.parse_tuic5_config(
    "tuic5://eyJ..."
)

# لیست پروتکل‌های پشتیبانی شده
protocols = parser.get_supported_protocols()
print(protocols)
```

---

## 📈 معیارهای عملکرد

### **قبل از بهبودها:**
```
⏱️ سرعت تست: 50 کانفیگ/ثانیه
✅ نرخ موفقیت: 68.8%
🔌 پروتکل‌های پشتیبانی شده: 10
🌍 منابع فعال: 68
```

### **بعد از بهبودها (انتظار می‌رود):**
```
⏱️ سرعت تست: 100+ کانفیگ/ثانیه
✅ نرخ موفقیت: 75%+
🔌 پروتکل‌های پشتیبانی شده: 17
🌍 منابع فعال: 100+
📊 Telegram + Discord + Reddit
🤖 AI-powered quality prediction
```

---

## 🎯 نقشه راه آینده

### **Q1 2025:**
- [ ] کامل کردن Telegram Integration
- [ ] اضافه کردن Discord Bot
- [ ] پیاده‌سازی Reddit Scraper
- [ ] راه‌اندازی API RESTful

### **Q2 2025:**
- [ ] Machine Learning برای کیفیت کانفیگ‌ها
- [ ] نقشه جغرافیایی تعاملی
- [ ] اپلیکیشن موبایل
- [ ] Browser Extension

### **Q3 2025:**
- [ ] Desktop App با Electron
- [ ] CLI Tool پیشرفته
- [ ] Dashboard حرفه‌ای با Grafana
- [ ] Kubernetes Deployment

---

## 🤝 مشارکت

برای مشارکت در بهبودها:

1. Fork کنید
2. Branch جدید بسازید (`git checkout -b feature/AmazingFeature`)
3. تغییرات را Commit کنید (`git commit -m 'Add AmazingFeature'`)
4. Push کنید (`git push origin feature/AmazingFeature`)
5. Pull Request باز کنید

---

## 📞 پشتیبانی

- **Issues**: [GitHub Issues](https://github.com/AhmadAkd/Onix-V2Ray-Collector/issues)
- **Discussions**: [GitHub Discussions](https://github.com/AhmadAkd/Onix-V2Ray-Collector/discussions)
- **Email**: your.email@example.com

---

## 📄 مجوز

MIT License - مشاهده فایل [LICENSE](LICENSE) برای جزئیات بیشتر.

---

**🎉 با تشکر از استفاده از V2Ray Collector Enhanced!**
