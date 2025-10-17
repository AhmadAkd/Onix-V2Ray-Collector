# 🔐 راهنمای تنظیم GitHub Secrets

## 🎯 **مشکل فعلی**

ربات Telegram شما روی GitHub اجرا نمی‌شود چون **GitHub Secrets** تنظیم نشده است.

## 🔧 **راه حل**

### 1️⃣ **تنظیم GitHub Secrets**

#### **مرحله 1: رفتن به تنظیمات Repository**

```
1. برو به: https://github.com/AhmadAkd/Onix-V2Ray-Collector
2. کلیک روی Settings
3. در منوی سمت چپ، Secrets and variables را انتخاب کن
4. روی Actions کلیک کن
```

#### **مرحله 2: اضافه کردن Secret جدید**

```
1. روی "New repository secret" کلیک کن
2. Name: TELEGRAM_BOT_TOKEN
3. Secret: 8474552244:AAERRNE4n7_aFIeqxRlwEmutYn9jUvd9yUQ
4. روی "Add secret" کلیک کن
```

#### **مرحله 3: اضافه کردن Admin Chat ID**

```
1. دوباره روی "New repository secret" کلیک کن
2. Name: TELEGRAM_CHAT_ID
3. Secret: 6563143907
4. روی "Add secret" کلیک کن
```

### 2️⃣ **فعال‌سازی Workflow**

#### **مرحله 1: رفتن به Actions**

```
1. برو به: https://github.com/AhmadAkd/Onix-V2Ray-Collector/actions
2. روی "Deploy Telegram Bot" کلیک کن
3. روی "Run workflow" کلیک کن
4. روی "Run workflow" سبز کلیک کن
```

#### **مرحله 2: بررسی نتایج**

```
1. منتظر بمان تا workflow تمام شود
2. روی run کلیک کن
3. لاگ‌ها را بررسی کن
4. اگر موفق بود، ربات آنلاین است
```

---

## 📱 **نحوه استفاده**

### ✅ **بعد از تنظیم Secrets:**

#### **1. در تلگرام:**

```
1. ربات را پیدا کن: @onixdev_bot
2. دستور /start را ارسال کن
3. دستورات مختلف را تست کن
```

#### **2. دستورات اصلی:**

```
/start - شروع کار
/help - راهنما
/stats - آمار سیستم
/configs - دریافت کانفیگ‌ها
/admin - دستورات ادمین (فقط برای شما)
```

#### **3. دستورات ادمین (فقط برای شما):**

```
/admin - منوی ادمین
/admin stats - آمار تفصیلی
/admin users - لیست کاربران
/admin broadcast - ارسال پیام به همه
```

---

## 🔍 **تشخیص مشکلات**

### ❌ **اگر ربات کار نمی‌کند:**

#### **1. بررسی Secrets:**

```
- برو به Settings > Secrets and variables > Actions
- مطمئن شو که TELEGRAM_BOT_TOKEN موجود است
- مطمئن شو که TELEGRAM_CHAT_ID موجود است
```

#### **2. بررسی Workflow:**

```
- برو به Actions tab
- بررسی کن که workflow اجرا شده باشد
- لاگ‌ها را بررسی کن
```

#### **3. بررسی Bot Token:**

```
- مطمئن شو که Bot Token درست است
- با @BotFather چک کن که ربات فعال است
```

---

## 🎯 **مراحل کامل**

### ✅ **چک‌لیست:**

- [ ] GitHub Secrets تنظیم شده
- [ ] TELEGRAM_BOT_TOKEN اضافه شده
- [ ] TELEGRAM_CHAT_ID اضافه شده
- [ ] Workflow اجرا شده
- [ ] ربات در تلگرام پاسخ می‌دهد
- [ ] دستورات ادمین کار می‌کند

### 🚀 **بعد از تکمیل:**

```
✅ ربات آنلاین خواهد بود
✅ دستورات کار خواهند کرد
✅ شما ادمین خواهید بود
✅ می‌توانید ربات را مدیریت کنید
```

---

## 📊 **وضعیت فعلی**

```
🤖 ربات:
├── نام: onix
├── Username: @onixdev_bot
├── Bot ID: 8474552244
├── وضعیت: ⏳ منتظر تنظیم Secrets
└── ادمین: 6563143907 (@Deltamax)

🔧 تنظیمات:
├── GitHub Secrets: ❌ تنظیم نشده
├── Workflow: ✅ آماده
├── Bot Token: ✅ موجود
└── Admin ID: ✅ موجود
```

---

## 🎉 **نتیجه**

بعد از تنظیم GitHub Secrets:

✅ **ربات آنلاین خواهد بود**
✅ **دستورات کار خواهند کرد**  
✅ **شما ادمین خواهید بود**
✅ **می‌توانید ربات را مدیریت کنید**

**🎯 اولین قدم: تنظیم GitHub Secrets!**
