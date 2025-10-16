# 🤖 راهنمای تنظیم Telegram Bot Token

## 📋 مراحل دریافت Bot Token

### مرحله 1: ایجاد Bot در تلگرام

1. **باز کردن تلگرام** و جستجوی `@BotFather`
2. **شروع گفتگو** با BotFather
3. **ارسال دستور**: `/newbot`
4. **وارد کردن نام Bot** (مثل: `V2Ray Config Collector`)
5. **وارد کردن username** (مثل: `v2ray_collector_bot`)
6. **دریافت Token** (مثل: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### مرحله 2: تنظیم Bot Token

#### روش 1: GitHub Secrets (توصیه شده برای GitHub Actions)

1. برو به **Settings** در repository
2. **Secrets and variables** → **Actions**
3. **New repository secret**
4. **Name**: `TELEGRAM_BOT_TOKEN`
5. **Value**: Token دریافتی از BotFather
6. **Add secret**

#### روش 2: Environment Variable محلی

**Windows:**
```cmd
set TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

**Linux/Mac:**
```bash
export TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

**Python:**
```python
import os
os.environ['TELEGRAM_BOT_TOKEN'] = '1234567890:ABCdefGHIjklMNOpqrsTUVwxyz'
```

### مرحله 3: تست Bot Token

```bash
python test_telegram_bot.py
```

## 🔧 تنظیمات اضافی Bot

### فعال‌سازی دسترسی به کانال‌ها

1. **اضافه کردن Bot به کانال** به عنوان Admin
2. **ارسال دستور** `/setprivacy` به @BotFather
3. **انتخاب Bot** (username شما)
4. **انتخاب Disable** برای دسترسی به پیام‌ها

### تنظیم دسترسی به گروه‌ها

1. **ارسال دستور** `/setjoingroups` به @BotFather
2. **انتخاب Bot** (username شما)
3. **انتخاب Enable** برای دسترسی به گروه‌ها

## 📊 نحوه استفاده

### در GitHub Actions

```yaml
- name: Run collection with Telegram
  env:
    TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
  run: python run_collection.py
```

### در کد Python

```python
import os
from telegram_collector import TelegramCollector

# تنظیم Bot Token
os.environ['TELEGRAM_BOT_TOKEN'] = 'YOUR_TOKEN_HERE'

# ایجاد collector
collector = TelegramCollector()

# جمع‌آوری از تلگرام
configs = await collector.collect_all_sources()
```

## 🔍 عیب‌یابی

### خطاهای رایج

1. **"Unauthorized"**: Bot Token اشتباه است
2. **"Bad Request"**: Bot به کانال دسترسی ندارد
3. **"Forbidden"**: Bot از کانال حذف شده است

### بررسی وضعیت Bot

```bash
# تست API
curl "https://api.telegram.org/bot<YOUR_TOKEN>/getMe"

# تست Updates
curl "https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates"
```

## 📈 مزایای استفاده از Bot Token

- ✅ **جمع‌آوری real-time** از کانال‌های تلگرام
- ✅ **دسترسی به پیام‌های جدید** به صورت خودکار
- ✅ **فیلتر کردن پیام‌ها** بر اساس محتوا
- ✅ **استخراج کانفیگ‌ها** از متن و media
- ✅ **نظارت مداوم** بر کانال‌ها

## ⚠️ نکات امنیتی

- 🔒 **هرگز Bot Token را در کد قرار ندهید**
- 🔒 **از GitHub Secrets استفاده کنید**
- 🔒 **دسترسی‌های Bot را محدود کنید**
- 🔒 **Token را به صورت دوره‌ای تغییر دهید**

## 🎯 نتیجه

با تنظیم صحیح Bot Token، سیستم قادر خواهد بود:
- از 36+ کانال تلگرام جمع‌آوری کند
- کانفیگ‌های جدید را به صورت real-time دریافت کند
- کیفیت و تنوع کانفیگ‌ها را افزایش دهد
- نرخ موفقیت جمع‌آوری را بهبود بخشد
