# 🤖 راهنمای کامل Telegram Bot برای V2Ray Collector

## 📋 فهرست مطالب

- [🎯 مقدمه](#-مقدمه)
- [🔧 نصب و راه‌اندازی](#-نصب-و-راه‌اندازی)
- [⚙️ پیکربندی](#️-پیکربندی)
- [🚀 استفاده](#-استفاده)
- [📱 دستورات](#-دستورات)
- [🛠️ توسعه](#️-توسعه)
- [❓ عیب‌یابی](#-عیب‌یابی)

---

## 🎯 مقدمه

Telegram Bot برای V2Ray Collector یک ربات پیشرفته و کامل است که امکان دسترسی آسان به کانفیگ‌های V2Ray را از طریق تلگرام فراهم می‌کند.

### ✨ ویژگی‌های کلیدی

- 🤖 **ربات کامل**: تمام دستورات مورد نیاز
- 📡 **دسترسی به کانفیگ‌ها**: دریافت کانفیگ‌های مختلف
- 🌍 **دسته‌بندی جغرافیایی**: فیلتر بر اساس کشور
- 🔌 **پروتکل‌های متنوع**: پشتیبانی از تمام پروتکل‌ها
- 📊 **آمار Real-time**: نمایش آمار زنده سیستم
- 👑 **سیستم ادمین**: مدیریت کامل برای ادمین‌ها
- 🔍 **جستجوی پیشرفته**: جستجو در کانفیگ‌ها
- 📢 **اشتراک**: دریافت آپدیت‌های خودکار

---

## 🔧 نصب و راه‌اندازی

### 1️⃣ **پیش‌نیازها**

```bash
# Python 3.8+
python --version

# نصب وابستگی‌ها
pip install aiohttp python-telegram-bot
```

### 2️⃣ **دریافت Bot Token**

1. به [@BotFather](https://t.me/BotFather) در تلگرام پیام دهید
2. دستور `/newbot` را ارسال کنید
3. نام ربات را وارد کنید: `V2Ray Collector Bot`
4. نام کاربری را وارد کنید: `v2ray_collector_bot`
5. Bot Token را کپی کنید

### 3️⃣ **تنظیم Token**

```python
# در فایل config.py یا .env
TELEGRAM_BOT_TOKEN = "6942899950:AAEDV4iX8jh2zD8be2dPqcADnB7V4xWy7aE"
```

### 4️⃣ **راه‌اندازی ربات**

```bash
# اجرای ربات
python telegram_bot_enhanced.py

# یا اجرای در پس‌زمینه
nohup python telegram_bot_enhanced.py &
```

---

## ⚙️ پیکربندی

### 📝 **متغیرهای محیطی**

```bash
# فایل .env
TELEGRAM_BOT_TOKEN=6942899950:AAEDV4iX8jh2zD8be2dPqcADnB7V4xWy7aE
TELEGRAM_ADMIN_USERS=123456789,987654321
TELEGRAM_WEBHOOK_URL=https://yourdomain.com/webhook
TELEGRAM_POLLING_INTERVAL=1
```

### 🔧 **تنظیمات پیشرفته**

```python
# در فایل telegram_bot_enhanced.py
class EnhancedTelegramBot:
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.admin_users = set([123456789])  # ID ادمین‌ها
        self.commands = self._setup_commands()
```

---

## 🚀 استفاده

### 🎯 **شروع کار**

1. ربات را در تلگرام پیدا کنید: `@v2ray_collector_bot`
2. دستور `/start` را ارسال کنید
3. از دستور `/help` برای مشاهده راهنما استفاده کنید

### 📱 **نحوه کار**

```
کاربر: /start
ربات: 🎉 خوش آمدید! ربات V2Ray Collector آماده خدمت‌رسانی است.

کاربر: /configs vmess
ربات: 📡 کانفیگ‌های VMess:
vmess://eyJ2IjoiMiIsInBzIjoiVGVzdCIsImFkZCI6InRlc3QuY29tIiwicG9ydCI6IjQ0MyIsImlkIjoiYWFhYSIsInR5cGUiOiJub25lIiwiaG9zdCI6IiIsInRscyI6InRscyJ9

کاربر: /countries
ربات: 🌍 کشورهای پشتیبانی شده:
🇺🇸 آمریکا (US)
🇩🇪 آلمان (DE)
🇨🇦 کانادا (CA)
...
```

---

## 📱 دستورات

### 🔧 **دستورات اصلی**

| دستور | توضیح | مثال |
|-------|-------|------|
| `/start` | شروع کار با ربات | `/start` |
| `/help` | راهنمای کامل | `/help` |
| `/stats` | آمار کلی سیستم | `/stats` |
| `/ping` | تست اتصال | `/ping` |
| `/about` | درباره ربات | `/about` |

### 📡 **دستورات کانفیگ**

| دستور | توضیح | مثال |
|-------|-------|------|
| `/configs` | تمام کانفیگ‌ها | `/configs` |
| `/configs vmess` | کانفیگ‌های VMess | `/configs vmess` |
| `/configs vless` | کانفیگ‌های VLESS | `/configs vless` |
| `/configs trojan` | کانفیگ‌های Trojan | `/configs trojan` |
| `/configs ss` | کانفیگ‌های Shadowsocks | `/configs ss` |

### 🌍 **دستورات جغرافیایی**

| دستور | توضیح | مثال |
|-------|-------|------|
| `/countries` | لیست کشورها | `/countries` |
| `/configs US` | کانفیگ‌های آمریکا | `/configs US` |
| `/configs DE` | کانفیگ‌های آلمان | `/configs DE` |
| `/configs IR` | کانفیگ‌های ایران | `/configs IR` |

### 🔍 **دستورات جستجو**

| دستور | توضیح | مثال |
|-------|-------|------|
| `/search vmess` | جستجوی VMess | `/search vmess` |
| `/search vless US` | جستجوی VLESS آمریکا | `/search vless US` |
| `/latest` | آخرین کانفیگ‌ها | `/latest` |
| `/latest 10` | آخرین 10 کانفیگ | `/latest 10` |

### ⚙️ **دستورات تنظیمات**

| دستور | توضیح | مثال |
|-------|-------|------|
| `/subscribe` | اشتراک در آپدیت‌ها | `/subscribe` |
| `/unsubscribe` | لغو اشتراک | `/unsubscribe` |

### 👑 **دستورات ادمین**

| دستور | توضیح | مثال |
|-------|-------|------|
| `/admin` | منوی ادمین | `/admin` |
| `/admin stats` | آمار تفصیلی | `/admin stats` |
| `/admin users` | لیست کاربران | `/admin users` |
| `/admin broadcast` | ارسال پیام به همه | `/admin broadcast سلام` |

---

## 🛠️ توسعه

### 📁 **ساختار فایل‌ها**

```
telegram_bot_enhanced.py     # ربات اصلی
test_enhanced_telegram_bot.py # تست‌ها
TELEGRAM_BOT_GUIDE.md        # این راهنما
```

### 🔧 **اضافه کردن دستور جدید**

```python
async def _handle_new_command(self, chat_id: int, user_session: UserSession, args: List[str]):
    """دستور جدید"""
    response_text = "پاسخ دستور جدید"
    await self.send_message(chat_id, response_text)

# در تابع handle_command اضافه کنید:
elif command == 'newcommand':
    await self._handle_new_command(chat_id, user_session, parts[1:])
```

### 🔧 **اضافه کردن منبع جدید**

```python
# در فایل telegram_collector.py
TELEGRAM_SOURCES.append(
    TelegramSource(
        channel_id="@new_channel",
        channel_name="New Channel",
    )
)
```

---

## ❓ عیب‌یابی

### 🔴 **مشکلات رایج**

#### 1. **خطای SSL Certificate**

```
SSLCertVerificationError: certificate verify failed
```

**راه‌حل:**

```python
# در فایل telegram_bot_enhanced.py
connector = aiohttp.TCPConnector(ssl=False)
```

#### 2. **خطای Bot Token**

```
Unauthorized: Invalid token
```

**راه‌حل:**

- Bot Token را بررسی کنید
- از BotFather دوباره دریافت کنید
- در فایل `.env` قرار دهید

#### 3. **خطای Connection**

```
Cannot connect to host api.telegram.org
```

**راه‌حل:**

- اتصال اینترنت را بررسی کنید
- فایروال را بررسی کنید
- VPN استفاده کنید

#### 4. **خطای Permission**

```
Forbidden: bot was blocked by the user
```

**راه‌حل:**

- کاربر باید ربات را unblock کند
- یا از chat_id دیگری استفاده کنید

### 🔍 **لاگ‌گیری**

```python
# فعال‌سازی لاگ‌گیری تفصیلی
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

### 📊 **نظارت بر عملکرد**

```python
# اضافه کردن آمار عملکرد
async def get_performance_stats(self):
    return {
        'total_users': len(self.user_sessions),
        'total_requests': self.stats.total_requests,
        'active_users_today': len([u for u in self.user_sessions.values() 
                                 if (datetime.now() - u.last_activity).days < 1])
    }
```

---

## 🎯 **نتیجه‌گیری**

Telegram Bot برای V2Ray Collector یک ابزار قدرتمند و کامل است که:

- ✅ **آسان**: استفاده ساده برای کاربران
- ✅ **قدرتمند**: تمام قابلیت‌های مورد نیاز
- ✅ **قابل توسعه**: امکان اضافه کردن ویژگی‌های جدید
- ✅ **مستند**: راهنمای کامل و واضح
- ✅ **پایدار**: تست شده و قابل اعتماد

### 🚀 **مراحل بعدی**

1. **Deploy**: راه‌اندازی روی سرور
2. **Webhook**: تنظیم webhook برای production
3. **Monitoring**: نظارت بر عملکرد
4. **Updates**: بروزرسانی‌های مداوم
5. **Features**: اضافه کردن ویژگی‌های جدید

---

**🤖 ربات شما آماده استفاده است!**

برای شروع:

```bash
python telegram_bot_enhanced.py
```

و سپس در تلگرام به `@v2ray_collector_bot` پیام دهید و `/start` را ارسال کنید.
