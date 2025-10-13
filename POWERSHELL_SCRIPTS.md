# 🪟 راهنمای اسکریپت‌های PowerShell

## 📁 فایل‌های موجود

### 1. `run.ps1` (English Version)

اسکریپت انگلیسی - بدون مشکل encoding

### 2. `run-fa.ps1` (Persian Version)  

اسکریپت فارسی - با پشتیبانی کامل UTF-8

---

## 🚀 نحوه استفاده

### روش 1: اجرای مستقیم (ساده‌ترین)

```powershell
# نسخه انگلیسی (توصیه می‌شود)
.\run.ps1

# یا نسخه فارسی
.\run-fa.ps1
```

### روش 2: اجرای دستور خاص

```powershell
# نصب وابستگی‌ها
.\run.ps1 install

# اجرای تست‌ها
.\run.ps1 test

# جمع‌آوری کانفیگ‌ها
.\run.ps1 collect

# اتوماسیون
.\run.ps1 auto

# API Server
.\run.ps1 api

# مشاهده لاگ‌ها
.\run.ps1 logs

# پاکسازی
.\run.ps1 clean

# اطلاعات سیستم
.\run.ps1 info
```

---

## ⚠️ حل مشکل Execution Policy

اگر با این خطا مواجه شدید:

```
File cannot be loaded because running scripts is disabled on this system.
```

**راه‌حل:**

```powershell
# روش 1: تغییر Policy برای کاربر فعلی (امن)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# روش 2: اجرای با Bypass (یکبار)
powershell -ExecutionPolicy Bypass -File .\run.ps1

# روش 3: راست کلیک روی فایل → Properties → Unblock
```

---

## 🎯 منوی اسکریپت

بعد از اجرا، منوی زیر نمایش داده می‌شود:

```
======================================================
   V2Ray Collector - Windows Edition
======================================================

  [1] Install Dependencies
  [2] Run Tests
  [3] Collect Configs (Once)
  [4] Automation (Every 30 min)
  [5] Start API Server
  [6] View Logs
  [7] Clean Cache
  [8] Show System Info
  [9] Docker Commands
  [0] Exit
```

---

## 📝 مثال‌های کاربردی

### شروع سریع

```powershell
# 1. باز کردن PowerShell در پوشه پروژه
cd C:\Users\Ahmad\Desktop\Github\V2Ray-Checker\new1

# 2. اجرای اسکریپت
.\run.ps1

# 3. انتخاب گزینه 1 برای نصب
# 4. انتخاب گزینه 2 برای تست
# 5. انتخاب گزینه 3 برای جمع‌آوری
```

### تست سریع

```powershell
# تست مستقیم
.\run.ps1 test

# یا
python run_tests.py
```

### مشاهده لاگ‌ها

```powershell
# با اسکریپت
.\run.ps1 logs

# یا دستی
Get-Content logs\v2ray_collector.log -Wait -Tail 20
```

### پاکسازی

```powershell
# با اسکریپت
.\run.ps1 clean

# یا دستی
Remove-Item -Recurse -Force cache\*
```

---

## 🔧 تفاوت‌های دو نسخه

| ویژگی | `run.ps1` | `run-fa.ps1` |
|-------|-----------|-------------|
| زبان رابط | English | فارسی |
| مشکل Encoding | ندارد | ممکن است در PowerShell قدیمی |
| سازگاری | بالا | متوسط |
| توصیه | ✅ بله | برای کاربران فارسی‌زبان |

---

## 💡 نکات مهم

1. **از `run.ps1` استفاده کنید** - مشکل encoding ندارد
2. **فقط در صورت نیاز به فارسی** از `run-fa.ps1` استفاده کنید
3. **PowerShell 7** را نصب کنید برای پشتیبانی بهتر UTF-8
4. **Windows Terminal** را برای تجربه بهتر استفاده کنید

---

## 🐛 حل مشکلات رایج

### خطای "cannot be loaded"

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### خطای "is not recognized"

```powershell
# اضافه کردن .\ قبل از نام فایل
.\run.ps1
```

### متن فارسی خراب می‌شود

```powershell
# استفاده از نسخه انگلیسی
.\run.ps1

# یا تنظیم encoding
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
.\run-fa.ps1
```

### Python not found

```powershell
# نصب Python
winget install Python.Python.3.11

# بررسی نصب
python --version
```

---

## 🎓 دستورات مفید PowerShell

```powershell
# مسیر فعلی
Get-Location

# لیست فایل‌ها
Get-ChildItem

# مشاهده فایل
Get-Content file.txt

# جستجو
Select-String "pattern" file.txt

# تعداد خطوط فایل
(Get-Content file.txt | Measure-Object -Line).Lines

# حذف پوشه
Remove-Item -Recurse -Force folder
```

---

## 📚 منابع بیشتر

- [WINDOWS_GUIDE.md](WINDOWS_GUIDE.md) - راهنمای کامل Windows
- [QUICKSTART.md](QUICKSTART.md) - راهنمای شروع سریع
- [README.md](README.md) - مستندات اصلی

---

## ✅ چک‌لیست

- [ ] Python نصب شده؟ (`python --version`)
- [ ] pip کار می‌کند؟ (`pip --version`)
- [ ] ExecutionPolicy تنظیم شده؟
- [ ] در پوشه صحیح هستید؟
- [ ] اسکریپت Unblock شده؟

---

**موفق باشید! 🎉**

برای کمک بیشتر:

- GitHub Issues: [گزارش مشکل](https://github.com/AhmadAkd/V2Ray_Collector/issues)
- Documentation: [مستندات کامل](docs/)
