# 🚀 راهنمای تنظیمات GitHub - گام به گام

این راهنما به شما کمک می‌کند تا تنظیمات حرفه‌ای GitHub را برای پروژه V2Ray Collector انجام دهید.

---

## 📋 فهرست

1. [تنظیم Description و About](#1-تنظیم-description-و-about)
2. [اضافه کردن Topics](#2-اضافه-کردن-topics)
3. [تنظیم Website](#3-تنظیم-website)
4. [آپلود Social Preview Image](#4-آپلود-social-preview-image)
5. [فعال‌سازی GitHub Pages](#5-فعالسازی-github-pages)
6. [فعال‌سازی Discussions](#6-فعالسازی-discussions)
7. [ایجاد Release اول](#7-ایجاد-release-اول)
8. [تنظیمات امنیتی](#8-تنظیمات-امنیتی)

---

## 1️⃣ تنظیم Description و About

### مرحله 1: باز کردن صفحه Repository

```
https://github.com/AhmadAkd/Onix-V2Ray-Collector
```

### مرحله 2: کلیک روی Settings

- در صفحه اصلی repository، **بالای صفحه** سمت راست، آیکون **⚙️ Settings** رو پیدا کن
- روش کلیک کن

### مرحله 3: ویرایش About

- در سمت راست صفحه، بخش **"About"** رو پیدا کن
- روی آیکون **⚙️** (کنار کلمه About) کلیک کن
- یا مستقیم روی **"Edit repository details"** کلیک کن

### مرحله 4: وارد کردن Description

در کادر **"Description"** این متن رو کپی کن:

```
🚀 Advanced V2Ray Config Collector & Tester | جمع‌آوری و تست هوشمند کانفیگ V2Ray | ML scoring + REST API + Health monitoring | Auto-update 6h | بروزرسانی خودکار هر 6 ساعت | 1000+ configs from 40+ sources
```

**⚠️ نکته:** اگر خیلی طولانی شد، می‌تونی از نسخه کوتاه‌تر استفاده کنی:

```
🚀 Smart V2Ray Config Collector | جمع‌آوری هوشمند کانفیگ V2Ray | ML + API + Monitor | Auto 6h | 1000+ configs from 40+ sources
```

---

## 2️⃣ اضافه کردن Topics

### مرحله 1: در همون پنجره About

- پایین‌تر، بخش **"Topics"** رو پیدا کن
- این Topics رو **یکی یکی** اضافه کن:

```
v2ray
vmess
vless
trojan
shadowsocks
proxy
vpn
subscription
collector
tester
fastapi
machine-learning
rest-api
github-actions
auto-update
persian
iran
free-vpn
config-tester
health-monitoring
```

### مرحله 2: نحوه اضافه کردن

1. کادر "Add topics" رو پیدا کن
2. هر کلمه رو تایپ کن (مثل `v2ray`)
3. Enter بزن یا از dropdown انتخاب کن
4. کلمه بعدی رو تایپ کن
5. تا آخر ادامه بده

**💡 نکته:** حداکثر 20 topic می‌تونی اضافه کنی

---

## 3️⃣ تنظیم Website

### در همون پنجره About

- کادر **"Website"** رو پیدا کن
- این لینک رو وارد کن:

```
https://ahmadakd.github.io/Onix-V2Ray-Collector/
```

### بعد از تمام تنظیمات About

- روی دکمه **"Save changes"** کلیک کن

---

## 4️⃣ آپلود Social Preview Image

این تصویر وقتی لینک GitHub رو در Twitter, Telegram, Discord و... share می‌کنی نمایش داده میشه.

### مرحله 1: ساخت تصویر

**گزینه A: استفاده از Canva (آسان‌تر)**

1. برو به: <https://www.canva.com>
2. سایز: **1280 × 640 پیکسل**
3. المان‌ها:
   - پس‌زمینه: گرادیانت آبی/بنفش (#4158D0 → #C850C0)
   - لوگو: V2Ray
   - متن اصلی: **"V2Ray Collector"**
   - متن فرعی: **"1000+ Configs | 40+ Sources | Auto-Update 6h"**
   - آیکون‌ها: 🚀 ⚡ 🔒 📊

**گزینه B: استفاده از Figma (حرفه‌ای‌تر)**

1. برو به: <https://www.figma.com>
2. ایجاد Frame با سایز 1280×640
3. طراحی مشابه UI پروژه

**گزینه C: استفاده از PhotoShop/GIMP**

- سایز: 1280×640
- فرمت: PNG یا JPG
- حجم: کمتر از 1MB

### مرحله 2: آپلود تصویر

1. برو به: **Settings** > **Options**
2. پایین صفحه scroll کن
3. بخش **"Social preview"** رو پیدا کن
4. روی **"Upload an image..."** کلیک کن
5. تصویر رو انتخاب کن
6. منتظر آپلود بمون
7. روی **"Save"** کلیک کن

**✅ تست:** لینک repository رو در Telegram بفرست، باید تصویر نمایش داده بشه

---

## 5️⃣ فعال‌سازی GitHub Pages

### مرحله 1: رفتن به تنظیمات Pages

```
Repository > Settings > Pages (از منوی سمت چپ)
```

### مرحله 2: تنظیم Source

- **Source**: Deploy from a branch
- **Branch**: `main`
- **Folder**: `/ (root)` یا `docs` (اگر موجوده)
- روی **"Save"** کلیک کن

### مرحله 3: منتظر بمون

- ممکنه 2-3 دقیقه طول بکشه
- بعد از آماده شدن، یه لینک سبز رنگ نشون داده میشه:

```
✅ Your site is live at https://ahmadakd.github.io/Onix-V2Ray-Collector/
```

### مرحله 4: تست

- روی لینک کلیک کن
- صفحه اصلی پروژه باید لود بشه

**⚠️ مشکل؟**
اگر صفحه 404 داد:

1. مطمئن شو که فایل `index.html` در `subscriptions/` موجوده
2. یا تنظیمات رو به `docs` تغییر بده (اگر فایل‌ها توی docs هستن)

---

## 6️⃣ فعال‌سازی Discussions

### مرحله 1: رفتن به Settings

```
Repository > Settings > General
```

### مرحله 2: پیدا کردن بخش Features

- Scroll کن تا بخش **"Features"** رو ببینی
- گزینه **"Discussions"** رو پیدا کن

### مرحله 3: فعال‌سازی

- چک‌باکس **"Discussions"** رو تیک بزن
- منتظر بمون تا فعال بشه (چند ثانیه)

### مرحله 4: تنظیم Categories (اختیاری)

بعد از فعال شدن، می‌تونی Categories بسازی:

- 💬 General
- 💡 Ideas
- 🐛 Troubleshooting
- 📚 Documentation
- 🎉 Show and Tell

---

## 7️⃣ ایجاد Release اول

### مرحله 1: رفتن به Releases

```
Repository > Releases (در سمت راست صفحه اصلی)
```

یا مستقیم:

```
https://github.com/AhmadAkd/Onix-V2Ray-Collector/releases/new
```

### مرحله 2: ایجاد Tag

- **Choose a tag**: `v2.0.0`
- **Target**: `main`

### مرحله 3: عنوان Release

```
🚀 V2Ray Collector v2.0.0 - Enterprise Edition
```

### مرحله 4: توضیحات Release

کپی کن و Paste کن:

```markdown
# 🎉 V2Ray Collector v2.0.0 - Enterprise Edition

## 🌟 ویژگی‌های اصلی

### 🤖 هوشمند و پیشرفته
- ✅ **ML-based Config Scoring** - امتیازدهی هوشمند با Machine Learning
- ✅ **Health Monitoring** - نظارت Real-time بر سلامت سیستم
- ✅ **Error Recovery** - بازیابی خودکار خطاها
- ✅ **Smart Caching** - کش هوشمند برای بهینه‌سازی

### 📡 API و یکپارچه‌سازی
- ✅ **REST API** - FastAPI با Swagger documentation
- ✅ **10+ Endpoints** - دسترسی کامل به داده‌ها
- ✅ **Rate Limiting** - محدودسازی درخواست‌ها
- ✅ **Security Validation** - اعتبارسنجی امنیتی

### 🎨 رابط کاربری مدرن
- ✅ **Dark/Light Theme** - تم تاریک و روشن
- ✅ **Interactive Dashboard** - داشبورد تحلیلی با Chart.js
- ✅ **Real-time Stats** - آمار لحظه‌ای
- ✅ **Responsive Design** - طراحی ریسپانسیو

### 📊 جمع‌آوری و تست
- ✅ **40+ Sources** - بیش از 40 منبع معتبر
- ✅ **1000+ Configs** - بیش از 1000 کانفیگ روزانه
- ✅ **17+ Protocols** - پشتیبانی از 17 پروتکل
- ✅ **50+ Countries** - 50+ کشور دسته‌بندی شده
- ✅ **Auto-Update** - بروزرسانی خودکار هر 6 ساعت

### 🔒 امنیت و پایداری
- ✅ **Input Validation** - اعتبارسنجی ورودی‌ها
- ✅ **SQL Injection Prevention** - جلوگیری از SQL Injection
- ✅ **XSS Protection** - محافظت در برابر XSS
- ✅ **Security Scanning** - اسکن امنیتی خودکار

## 📦 نصب

### روش 1: استفاده از Subscription Links (آسان‌ترین)
```
<https://ahmadakd.github.io/Onix-V2Ray-Collector/>

```

### روش 2: نصب Local
```bash
git clone https://github.com/AhmadAkd/Onix-V2Ray-Collector.git
cd Onix-V2Ray-Collector
pip install -r requirements.txt
python run_collection.py
```

### روش 3: Docker

```bash
docker-compose up -d
```

## 📚 مستندات

- 📖 [راهنمای کاربر](https://github.com/AhmadAkd/Onix-V2Ray-Collector/blob/main/docs/USER_GUIDE.md)
- 🔧 [راهنمای توسعه‌دهنده](https://github.com/AhmadAkd/Onix-V2Ray-Collector/blob/main/docs/DEVELOPER.md)
- 📡 [API Documentation](https://github.com/AhmadAkd/Onix-V2Ray-Collector/blob/main/docs/API.md)
- 🐛 [عیب‌یابی](https://github.com/AhmadAkd/Onix-V2Ray-Collector/blob/main/docs/TROUBLESHOOTING.md)

## 🔄 تغییرات نسبت به v1.x

- 🆕 اضافه شدن ML Scoring System
- 🆕 اضافه شدن REST API
- 🆕 اضافه شدن Health Monitoring
- 🆕 اضافه شدن Dark Mode
- 🆕 اضافه شدن Database Manager
- 🆕 اضافه شدن Security Validator
- 🆕 بهبود عملکرد تا 300%
- 🆕 بهبود UI/UX
- 🆕 مستندات کامل

## 🐛 مشکلات شناخته شده

هیچ مشکل جدی شناخته شده‌ای وجود ندارد.

## 🙏 تشکر

از تمامی کاربران و مشارکت‌کنندگانی که در توسعه این نسخه کمک کردند، تشکر می‌کنیم!

## 📧 پشتیبانی

- 🐛 [گزارش باگ](https://github.com/AhmadAkd/Onix-V2Ray-Collector/issues)
- 💬 [بحث و گفتگو](https://github.com/AhmadAkd/Onix-V2Ray-Collector/discussions)
- 📧 Email: [Your Email]

---

**⭐ اگر این پروژه رو دوست دارید، لطفا ستاره بدهید!**

```

### مرحله 5: انتشار
- روی **"Publish release"** کلیک کن

---

## 8️⃣ تنظیمات امنیتی

### مرحله 1: فعال‌سازی Security Advisories
```

Settings > Security > Security advisories

```
- **"Enable"** رو بزن

### مرحله 2: فعال‌سازی Dependabot
```

Settings > Security > Dependabot

```
- **Dependabot alerts**: Enable
- **Dependabot security updates**: Enable
- **Dependabot version updates**: Enable

### مرحله 3: Code Scanning (پیشنهادی)
```

Security > Code scanning > Set up code scanning

```
- **CodeQL Analysis** رو انتخاب کن
- روی **"Set up this workflow"** کلیک کن

---

## ✅ چک‌لیست نهایی

بعد از انجام همه کارها، این موارد رو چک کن:

```

✅ Description تنظیم شده
✅ Topics اضافه شده (حداقل 10 تا)
✅ Website لینک شده
✅ Social Preview Image آپلود شده
✅ GitHub Pages فعال شده
✅ Discussions فعال شده
✅ Release v2.0.0 منتشر شده
✅ Security features فعال شده

```

---

## 🎯 نتیجه

بعد از انجام این کارها:

1. ✅ Repository حرفه‌ای به نظر میاد
2. ✅ SEO بهتر میشه (Topics)
3. ✅ Social sharing بهتر کار می‌کنه (Social Preview)
4. ✅ کاربران راحت‌تر می‌تونن از پروژه استفاده کنن (Pages)
5. ✅ بحث و گفتگو راحت‌تره (Discussions)
6. ✅ Version management حرفه‌ای (Releases)

---

## ❓ سوالات متداول

### Q: Description خیلی طولانی شد، چیکار کنم؟
**A:** از نسخه کوتاه‌تر استفاده کن (نوشتم در مرحله 1)

### Q: تصویر Social Preview رو از کجا بگیرم؟
**A:** می‌تونی با Canva بسازی یا از من بخوای برات بسازم

### Q: GitHub Pages 404 میده، چرا؟
**A:** مطمئن شو branch و folder درست تنظیم شده

### Q: نمی‌تونم Release بسازم، چرا؟
**A:** باید حداقل یک commit در repository داشته باشی

---

## 📞 کمک بیشتر

اگر در هر مرحله‌ای مشکل داشتی، بهم بگو تا کمک کنم! 😊


