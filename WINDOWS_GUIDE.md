# 🪟 راهنمای استفاده در Windows

این راهنما برای کاربران Windows PowerShell طراحی شده است.

---

## 📋 دستورات معادل PowerShell

### 🐳 **Docker Desktop**

در Windows، به جای `docker-compose` از Docker Desktop استفاده کنید:

#### نصب Docker Desktop

1. دانلود Docker Desktop از: <https://www.docker.com/products/docker-desktop>
2. نصب و راه‌اندازی
3. باز کردن Docker Desktop

#### دستورات Docker

```powershell
# به جای docker-compose از docker compose استفاده کنید (بدون dash)
docker compose up -d

# مشاهده لاگ‌ها
docker compose logs -f

# توقف
docker compose down

# یا استفاده از Docker Desktop GUI
```

---

## 📝 **مشاهده لاگ‌ها**

### به جای tail -f

```powershell
# روش 1: با Get-Content (توصیه می‌شود)
Get-Content logs\v2ray_collector.log -Wait -Tail 10

# روش 2: مشاهده کل فایل
type logs\v2ray_collector.log

# روش 3: 20 خط آخر
Get-Content logs\v2ray_collector.log -Tail 20

# روش 4: به‌روزرسانی خودکار (مثل tail -f)
Get-Content logs\v2ray_collector.log -Wait
```

### Alias برای راحتی کار

در PowerShell تایپ کنید:

```powershell
# ایجاد alias برای tail
Set-Alias tail Get-Content

# حالا می‌تونید استفاده کنید:
tail -Tail 10 -Wait logs\v2ray_collector.log
```

---

## 🔧 **دستورات معمول Windows**

### لیست فایل‌ها

```powershell
# به جای ls -la
Get-ChildItem
# یا
dir

# نمایش فایل‌های مخفی
Get-ChildItem -Force

# نمایش جزئیات
Get-ChildItem | Format-List
```

### مشاهده محتوای فایل

```powershell
# به جای cat
Get-Content file.txt
# یا
type file.txt
```

### حذف فایل/پوشه

```powershell
# حذف فایل
Remove-Item file.txt

# حذف پوشه
Remove-Item -Recurse -Force folder_name

# به جای rm -rf
Remove-Item -Recurse -Force cache\*
```

### جستجو در فایل

```powershell
# به جای grep
Select-String "pattern" file.txt

# جستجو در چند فایل
Get-ChildItem -Recurse | Select-String "pattern"
```

---

## 🚀 **اجرای پروژه در Windows**

### روش 1: مستقیم با Python

```powershell
# نصب وابستگی‌ها
pip install -r requirements.txt

# اجرای تست‌ها
python run_tests.py

# اجرای جمع‌آوری
python config_collector.py

# اجرای اتوماسیون
python automation.py --mode auto

# اجرای API Server
python api_server.py
```

### روش 2: با Virtual Environment (توصیه می‌شود)

```powershell
# ایجاد virtual environment
python -m venv venv

# فعال‌سازی
.\venv\Scripts\Activate.ps1

# در صورت خطای Execution Policy:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# نصب وابستگی‌ها
pip install -r requirements.txt

# اجرای برنامه
python config_collector.py

# غیرفعال کردن venv
deactivate
```

### روش 3: با Docker Desktop

```powershell
# اجرا
docker compose up -d

# مشاهده لاگ‌ها
docker compose logs -f v2ray-collector

# توقف
docker compose down
```

---

## 📊 **مشاهده و تحلیل نتایج**

### مشاهده گزارش‌ها

```powershell
# مشاهده گزارش JSON
Get-Content subscriptions\report.json

# با فرمت بهتر (نیاز به jq در Windows)
# نصب: choco install jq
Get-Content subscriptions\report.json | jq .

# یا استفاده از ConvertFrom-Json
Get-Content subscriptions\report.json | ConvertFrom-Json | Format-List
```

### بررسی فایل‌های اشتراک

```powershell
# لیست فایل‌های تولید شده
Get-ChildItem subscriptions\*.txt

# تعداد خطوط در فایل (تعداد کانفیگ‌ها)
(Get-Content subscriptions\all_subscription.txt).Count

# نمایش 10 خط اول
Get-Content subscriptions\vmess_subscription.txt -Head 10
```

---

## 🛠️ **ابزارهای مفید برای Windows**

### Windows Terminal (توصیه می‌شود)

```powershell
# نصب از Microsoft Store
# یا با winget:
winget install Microsoft.WindowsTerminal
```

### Git Bash (برای دستورات Unix)

```powershell
# نصب Git for Windows
winget install Git.Git
```

بعد از نصب، می‌تونید Git Bash رو باز کنید و دستورات Linux رو اجرا کنید:

```bash
# حالا می‌تونید استفاده کنید:
tail -f logs/v2ray_collector.log
docker-compose up -d
```

### PowerShell 7 (جدیدترین نسخه)

```powershell
# نصب
winget install Microsoft.PowerShell
```

---

## 🔐 **حل مشکل Execution Policy**

اگر با خطای Execution Policy مواجه شدید:

```powershell
# بررسی policy فعلی
Get-ExecutionPolicy

# تغییر برای کاربر فعلی (امن‌تر)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# یا برای یک بار اجرا
powershell -ExecutionPolicy Bypass -File script.ps1
```

---

## 📦 **نصب ابزارهای مفید**

### Chocolatey (مدیر بسته Windows)

```powershell
# نصب Chocolatey
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

بعد از نصب Chocolatey:

```powershell
# نصب Python
choco install python -y

# نصب Git
choco install git -y

# نصب Docker Desktop
choco install docker-desktop -y

# نصب jq (برای JSON)
choco install jq -y

# نصب VSCode
choco install vscode -y
```

---

## 🎯 **دستورات سریع پروژه**

### اسکریپت PowerShell برای اجرای سریع

ایجاد فایل `run.ps1`:

```powershell
# نمایش منو
Write-Host "🚀 V2Ray Collector - Windows Edition" -ForegroundColor Green
Write-Host "======================================"
Write-Host ""
Write-Host "1. نصب وابستگی‌ها"
Write-Host "2. اجرای تست‌ها"
Write-Host "3. جمع‌آوری کانفیگ‌ها (یکبار)"
Write-Host "4. اتوماسیون (هر 30 دقیقه)"
Write-Host "5. اجرای API Server"
Write-Host "6. مشاهده لاگ‌ها"
Write-Host "7. خروج"
Write-Host ""

$choice = Read-Host "انتخاب کنید (1-7)"

switch ($choice) {
    1 { 
        Write-Host "نصب وابستگی‌ها..." -ForegroundColor Yellow
        pip install -r requirements.txt 
    }
    2 { 
        Write-Host "اجرای تست‌ها..." -ForegroundColor Yellow
        python run_tests.py 
    }
    3 { 
        Write-Host "جمع‌آوری کانفیگ‌ها..." -ForegroundColor Yellow
        python config_collector.py 
    }
    4 { 
        Write-Host "اتوماسیون شروع شد..." -ForegroundColor Yellow
        python automation.py --mode auto 
    }
    5 { 
        Write-Host "API Server در حال اجرا..." -ForegroundColor Yellow
        python api_server.py 
    }
    6 { 
        Write-Host "مشاهده لاگ‌ها..." -ForegroundColor Yellow
        Get-Content logs\v2ray_collector.log -Wait -Tail 20
    }
    7 { 
        Write-Host "خروج..." -ForegroundColor Red
        exit 
    }
    default { 
        Write-Host "انتخاب نامعتبر!" -ForegroundColor Red 
    }
}
```

اجرا:

```powershell
.\run.ps1
```

---

## 📝 **جدول مقایسه دستورات**

| Linux/Mac | Windows PowerShell | توضیح |
|-----------|-------------------|-------|
| `ls -la` | `Get-ChildItem` یا `dir` | لیست فایل‌ها |
| `cat file.txt` | `Get-Content file.txt` | مشاهده فایل |
| `tail -f log.txt` | `Get-Content log.txt -Wait` | مشاهده لاگ زنده |
| `grep "text"` | `Select-String "text"` | جستجو در فایل |
| `rm -rf folder` | `Remove-Item -Recurse -Force folder` | حذف پوشه |
| `cp file1 file2` | `Copy-Item file1 file2` | کپی فایل |
| `mv file1 file2` | `Move-Item file1 file2` | انتقال/تغییر نام |
| `pwd` | `Get-Location` یا `pwd` | مسیر فعلی |
| `cd` | `Set-Location` یا `cd` | تغییر مسیر |
| `docker-compose` | `docker compose` | Docker Compose |

---

## ❓ **حل مشکلات رایج**

### مشکل 1: Python not found

```powershell
# نصب Python
winget install Python.Python.3.11

# یا
choco install python -y

# بررسی نصب
python --version
```

### مشکل 2: pip not working

```powershell
# استفاده از python -m pip
python -m pip install -r requirements.txt

# آپگرید pip
python -m pip install --upgrade pip
```

### مشکل 3: Docker Desktop نصب نیست

1. دانلود از: <https://www.docker.com/products/docker-desktop>
2. نصب و راه‌اندازی
3. Restart سیستم
4. باز کردن Docker Desktop

### مشکل 4: دسترسی رد شد (Access Denied)

```powershell
# اجرای PowerShell به عنوان Administrator
# راست کلیک روی PowerShell → Run as Administrator
```

---

## 💡 **نکات مهم**

1. **از پوشه‌های Farsi خودداری کنید** - ممکن است مشکل ایجاد کند
2. **Path های Windows با `\` هستند** - نه `/`
3. **حساس به بزرگی/کوچکی حروف نیست** - برخلاف Linux
4. **از Windows Terminal استفاده کنید** - تجربه بهتری دارد
5. **Virtual Environment استفاده کنید** - برای جلوگیری از تداخل

---

## 🎓 **منابع آموزشی**

- [PowerShell Documentation](https://docs.microsoft.com/en-us/powershell/)
- [Docker Desktop for Windows](https://docs.docker.com/desktop/windows/)
- [Python on Windows](https://docs.python.org/3/using/windows.html)

---

**✅ حالا آماده‌اید که از پروژه در Windows استفاده کنید!** 🎉
