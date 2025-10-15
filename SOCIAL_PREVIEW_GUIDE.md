# 🎨 راهنمای ساخت Social Preview Image

## 🚀 روش 1: با Canva (پیشنهادی - خیلی آسون)

### مرحله 1: ورود به Canva

1. برو به: <https://www.canva.com>
2. ثبت‌نام کن (رایگان)
3. از Dashboard، **"Create a design"** رو انتخاب کن
4. **"Custom size"** رو بزن
5. سایز: **1280 × 640 پیکسل**

### مرحله 2: طراحی پس‌زمینه

1. از منوی چپ **"Elements"** رو انتخاب کن
2. **"Gradients"** رو سرچ کن
3. یه گرادیانت آبی/بنفش انتخاب کن
4. یا خودت بساز:
   - کلیک روی پس‌زمینه
   - رنگ 1: `#4158D0`
   - رنگ 2: `#C850C0`
   - نوع: Linear Gradient

### مرحله 3: اضافه کردن لوگو V2Ray

1. از منوی چپ **"Elements"** > **"Graphics"**
2. سرچ کن: `shield` یا `network` یا `vpn`
3. یه آیکون مناسب انتخاب کن
4. رنگش رو سفید کن
5. سایزش رو بزرگ کن و بالای صفحه بذار

### مرحله 4: اضافه کردن متن اصلی

1. از منوی چپ **"Text"** رو انتخاب کن
2. **"Add a heading"** رو بزن
3. تایپ کن:

```
V2Ray Collector
جمع‌آوری‌کننده پیشرفته V2Ray
```

4. تنظیمات:
   - فونت: **Poppins Bold** یا **Montserrat Bold**
   - سایز: **72-80**
   - رنگ: **سفید (#FFFFFF)**
   - Alignment: **وسط**

### مرحله 5: اضافه کردن اطلاعات

1. یه Text Box جدید اضافه کن
2. تایپ کن:

```
🚀 1000+ Configs  |  ⚡ 40+ Sources  |  🔄 Auto-Update 6h
```

3. تنظیمات:
   - فونت: **Poppins Medium** یا **Roboto**
   - سایز: **32-36**
   - رنگ: **سفید کمرنگ (#E0E0E0)**

### مرحله 6: اضافه کردن ویژگی‌ها

1. یه Text Box دیگه اضافه کن
2. تایپ کن:

```
✅ ML Scoring  ✅ REST API  ✅ Dark Mode  ✅ Health Monitor
```

3. تنظیمات:
   - فونت: **Poppins Regular**
   - سایز: **24-28**
   - رنگ: **سفید (#FFFFFF)**

### مرحله 7: اضافه کردن GitHub Link (اختیاری)

در پایین صفحه:

```
github.com/AhmadAkd/Onix-V2Ray-Collector
```

- سایز: **20-24**
- رنگ: **سفید کمرنگ**

### مرحله 8: دانلود

1. بالای صفحه، **"Share"** > **"Download"**
2. نوع فایل: **PNG**
3. کیفیت: **Standard** یا **High**
4. **Download** رو بزن

---

## 🎨 روش 2: با Figma (حرفه‌ای‌تر)

### مرحله 1: ورود به Figma

1. برو به: <https://www.figma.com>
2. ثبت‌نام کن (رایگان)
3. **"New design file"** رو بزن

### مرحله 2: ایجاد Frame

1. از منوی بالا **Frame** رو انتخاب کن (کلید F)
2. سایز: **Width: 1280, Height: 640**

### مرحله 3: اضافه کردن گرادیانت

1. Frame رو انتخاب کن
2. از پنل راست **Fill** > **Linear Gradient**
3. رنگ اول: `#4158D0`
4. رنگ دوم: `#C850C0`
5. زاویه: **45 درجه**

### مرحله 4: اضافه کردن محتوا

مشابه Canva، متن‌ها و آیکون‌ها رو اضافه کن

### مرحله 5: Export

1. Frame رو انتخاب کن
2. پنل راست > **Export**
3. فرمت: **PNG**
4. Scale: **1x**
5. **Export Frame** رو بزن

---

## 🎨 روش 3: استفاده از Template آماده

من یه **Code برای HTML/CSS** بهت می‌دم که می‌تونی با screenshot بگیری:

### فایل: `social-preview-template.html`

```html
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>V2Ray Collector - Social Preview</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700;900&family=Poppins:wght@600;700&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            width: 1280px;
            height: 640px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Vazirmatn', 'Poppins', sans-serif;
            overflow: hidden;
        }
        
        .container {
            text-align: center;
            color: white;
            padding: 60px;
            position: relative;
        }
        
        .icon {
            font-size: 120px;
            margin-bottom: 20px;
            filter: drop-shadow(0 10px 30px rgba(0,0,0,0.3));
        }
        
        h1 {
            font-size: 72px;
            font-weight: 900;
            margin-bottom: 10px;
            text-shadow: 0 5px 20px rgba(0,0,0,0.3);
            font-family: 'Poppins', sans-serif;
        }
        
        .subtitle {
            font-size: 38px;
            margin-bottom: 40px;
            opacity: 0.95;
            font-weight: 700;
        }
        
        .stats {
            display: flex;
            justify-content: center;
            gap: 50px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }
        
        .stat-item {
            background: rgba(255,255,255,0.15);
            backdrop-filter: blur(10px);
            padding: 15px 30px;
            border-radius: 15px;
            font-size: 28px;
            font-weight: 600;
            border: 2px solid rgba(255,255,255,0.2);
        }
        
        .features {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 30px;
            flex-wrap: wrap;
        }
        
        .feature {
            font-size: 24px;
            background: rgba(255,255,255,0.1);
            padding: 10px 20px;
            border-radius: 25px;
        }
        
        .github-link {
            position: absolute;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 22px;
            opacity: 0.8;
            font-family: 'Poppins', monospace;
        }
        
        .badge {
            position: absolute;
            top: 30px;
            right: 30px;
            background: rgba(255,255,255,0.2);
            backdrop-filter: blur(10px);
            padding: 10px 20px;
            border-radius: 25px;
            font-size: 20px;
            font-weight: 600;
            border: 2px solid rgba(255,255,255,0.3);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="badge">🚀 v2.0 Enterprise</div>
        
        <div class="icon">🛡️</div>
        
        <h1>V2Ray Collector</h1>
        <div class="subtitle">جمع‌آوری‌کننده پیشرفته V2Ray</div>
        
        <div class="stats">
            <div class="stat-item">🚀 1000+ Configs</div>
            <div class="stat-item">⚡ 40+ Sources</div>
            <div class="stat-item">🔄 Auto 6h</div>
        </div>
        
        <div class="features">
            <div class="feature">✅ ML Scoring</div>
            <div class="feature">✅ REST API</div>
            <div class="feature">✅ Dark Mode</div>
            <div class="feature">✅ Health Monitor</div>
        </div>
        
        <div class="github-link">github.com/AhmadAkd/Onix-V2Ray-Collector</div>
    </div>
</body>
</html>
```

### نحوه استفاده

1. این کد رو توی یه فایل `social-preview.html` ذخیره کن
2. باز کن با مرورگر (Chrome/Firefox)
3. F12 بزن > Device Toolbar رو فعال کن > سایز رو بذار `1280x640`
4. F12 رو ببند تا فقط صفحه نمایش داده بشه
5. با یه ابزار screenshot بگیر:
   - **Windows**: Windows Key + Shift + S
   - **Mac**: Cmd + Shift + 4
   - **یا استفاده از Extension**: [GoFullPage](https://chrome.google.com/webstore/detail/gofullpage-full-page-scre/fdpohaocaechififmbbbbbknoalclacl)

---

## 📸 روش 4: استفاده از OG Image Generator آنلاین

### سایت‌های پیشنهادی

1. **<https://www.kapwing.com/tools/og-image-generator>**
2. **<https://www.bannerbear.com/demos/social-media-preview/>**
3. **<https://ogimage.gallery/>**

این سایت‌ها یه interface ساده دارن که می‌تونی متن و رنگ رو تنظیم کنی و تصویر رو دانلود کنی.

---

## ✅ چک‌لیست طراحی

- ✅ سایز دقیقاً **1280 × 640 پیکسل**
- ✅ فرمت **PNG** یا **JPG**
- ✅ حجم کمتر از **1MB**
- ✅ متن واضح و خوانا
- ✅ رنگ‌های جذاب (گرادیانت)
- ✅ آیکون/لوگو مشخص
- ✅ اطلاعات کلیدی (1000+ configs, 40+ sources)
- ✅ لینک GitHub (اختیاری)

---

## 🎨 ایده‌های طراحی

### طرح 1: مینیمال

- پس‌زمینه: گرادیانت آبی/بنفش
- وسط: لوگو + عنوان
- پایین: آمار (1000+ configs, 40+ sources)

### طرح 2: پر جزئیات

- پس‌زمینه: گرادیانت با pattern
- بالا: Badge "v2.0"
- وسط: عنوان + توضیح
- پایین: ویژگی‌ها به صورت badge

### طرح 3: تکنولوژی

- پس‌زمینه: Matrix effect یا خطوط
- کنار: اسکرین‌شات Dashboard
- راست: اطلاعات و آمار

---

## 💡 نکات مهم

1. **رنگ‌ها:** از رنگ‌های مشابه با UI پروژه استفاده کن (آبی، بنفش، سبز)
2. **متن:** خیلی شلوغ نکن، فقط اطلاعات مهم
3. **Contrast:** مطمئن شو متن واضح خونده میشه
4. **Brand Identity:** اگر لوگوی خاصی داری، حتماً استفاده کن
5. **Test:** بعد از آپلود، حتماً تست کن (لینک رو در Telegram بفرست)

---

## 🚀 بعد از ساخت

1. تصویر رو ذخیره کن با نام `social-preview.png`
2. برو به: GitHub > Settings > Options
3. پایین صفحه: Social preview
4. آپلود کن
5. تست کن!

---

**اگر کمک بیشتری لازم داشتی، بگو!** 😊
