# 🤖 V2Ray Collector Telegram Bot

ربات تلگرام پیشرفته برای دسترسی آسان به کانفیگ‌های V2Ray

## 🚀 شروع سریع

### 1. نصب وابستگی‌ها

```bash
pip install aiohttp python-telegram-bot
```

### 2. اجرای ربات

```bash
python start_telegram_bot.py
```

### 3. استفاده در تلگرام

- ربات را در تلگرام پیدا کنید: `@v2ray_collector_bot`
- دستور `/start` را ارسال کنید
- از دستور `/help` برای مشاهده راهنما استفاده کنید

## 📱 دستورات اصلی

| دستور | توضیح |
|-------|-------|
| `/start` | شروع کار |
| `/help` | راهنما |
| `/stats` | آمار سیستم |
| `/configs` | دریافت کانفیگ‌ها |
| `/configs vmess` | کانفیگ‌های VMess |
| `/configs vless` | کانفیگ‌های VLESS |
| `/countries` | لیست کشورها |
| `/search vmess US` | جستجوی VMess آمریکا |
| `/ping` | تست اتصال |

## 🔧 پیکربندی

### متغیرهای محیطی

```bash
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
```

### فایل .env

```bash
# ایجاد فایل .env
echo "TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE" > .env
```

## 📁 فایل‌ها

- `telegram_bot_enhanced.py` - ربات اصلی
- `start_telegram_bot.py` - راه‌انداز ساده
- `test_enhanced_telegram_bot_simple.py` - تست‌ها
- `TELEGRAM_BOT_GUIDE.md` - راهنمای کامل

## 🛠️ تست

```bash
# تست ساده
python test_enhanced_telegram_bot_simple.py

# تست کامل
python test_enhanced_telegram_bot.py
```

## 📊 آمار

ربات با موفقیت:

- ✅ Bot Token فعال و کارآمد
- ✅ 5,109+ کانفیگ در دسترس
- ✅ 9,240+ کانفیگ سالم
- ✅ 17+ پروتکل پشتیبانی شده
- ✅ 25+ کشور

## 🎯 ویژگی‌ها

- 🤖 ربات کامل با تمام دستورات
- 📡 دسترسی به کانفیگ‌های V2Ray
- 🌍 دسته‌بندی بر اساس کشور
- 🔌 پشتیبانی از تمام پروتکل‌ها
- 📊 آمار Real-time
- 👑 سیستم ادمین
- 🔍 جستجوی پیشرفته
- 📢 اشتراک در آپدیت‌ها

## 🚨 عیب‌یابی

### مشکل SSL

```python
# در فایل telegram_bot_enhanced.py
connector = aiohttp.TCPConnector(ssl=False)
```

### مشکل Bot Token

- Bot Token را از [@BotFather](https://t.me/BotFather) دریافت کنید
- در فایل `.env` قرار دهید

## 📞 پشتیبانی

- 📚 راهنمای کامل: `TELEGRAM_BOT_GUIDE.md`
- 🐛 گزارش باگ: GitHub Issues
- 💬 تلگرام: @AhmadAkd

---

**🤖 ربات شما آماده استفاده است!**
