# 🚀 راهنمای Push به GitHub

## 📋 دستورات Git برای Push تغییرات

### روش 1: Push تمام تغییرات (توصیه می‌شود)

```bash
# 1. بررسی وضعیت فعلی
git status

# 2. اضافه کردن همه تغییرات
git add .

# 3. Commit با پیام مناسب
git commit -m "🎉 Release v1.0.1 - Major improvements and bug fixes

✅ Fixed 6 critical bugs
🆕 Added Docker support
🚀 Added CI/CD pipeline
📝 Added comprehensive documentation
🪟 Added Windows PowerShell scripts
🔒 Improved security
📊 100% test coverage

See RELEASE_NOTES_v1.0.1.md for full details"

# 4. Push به GitHub
git push origin main
```

---

### روش 2: Push به Branch جدید (امن‌تر)

```bash
# 1. ایجاد branch جدید
git checkout -b release/v1.0.1

# 2. اضافه کردن تغییرات
git add .

# 3. Commit
git commit -m "🎉 Release v1.0.1 - Major improvements"

# 4. Push branch جدید
git push origin release/v1.0.1

# 5. ایجاد Pull Request در GitHub
# بعد از مرور، merge کنید
```

---

### روش 3: Commit های جداگانه (حرفه‌ای)

```bash
# 1. Bug fixes
git add config_collector.py requirements.txt api_server.py run_tests.py
git commit -m "🐛 Fix: Resolve 6 critical bugs

- Fix syntax error in config_collector.py
- Add missing dependencies (fastapi, uvicorn, pydantic)
- Fix variable name in api_server.py
- Improve SSL/TLS security
- Fix resource leak with cleanup
- Fix connectivity test timeout"

# 2. Docker support
git add Dockerfile docker-compose.yml .dockerignore
git commit -m "🐳 Feature: Add Docker support

- Add optimized Dockerfile
- Add docker-compose.yml with multi-service
- Add .dockerignore for smaller images
- Add health checks"

# 3. CI/CD
git add .github/workflows/ci.yml
git commit -m "🚀 Feature: Add CI/CD pipeline

- Auto test on every push
- Auto update configs every 30 min
- Auto build Docker images
- Deploy to GitHub Pages"

# 4. Logging
git add logging_config.py
git commit -m "📝 Feature: Add log rotation system

- Smart log file management
- Rotation by size and time
- Keep 5 backups
- Separate logs per component"

# 5. Windows support
git add run.ps1 run-fa.ps1 WINDOWS_GUIDE.md POWERSHELL_SCRIPTS.md
git commit -m "🪟 Feature: Add Windows PowerShell support

- Interactive PowerShell script (run.ps1)
- Persian version (run-fa.ps1)
- Complete Windows guide
- Command comparison table"

# 6. Documentation
git add SECURITY.md IMPROVEMENTS.md QUICKSTART.md README_IMPROVEMENTS_FA.md RELEASE_NOTES_v1.0.1.md FIX_TEST_CONNECTIVITY.md
git commit -m "📚 Docs: Add comprehensive documentation

- Security policy (SECURITY.md)
- Improvements details (IMPROVEMENTS.md)
- Quick start guide (QUICKSTART.md)
- Persian summary (README_IMPROVEMENTS_FA.md)
- Release notes (RELEASE_NOTES_v1.0.1.md)"

# 7. Improvements
git add .gitignore
git commit -m "🔧 Chore: Improve .gitignore

- Prevent sensitive files commit
- Manage temporary files
- Protect secrets"

# 8. Push همه
git push origin main
```

---

## 🏷️ ایجاد Release Tag

```bash
# 1. ایجاد tag
git tag -a v1.0.1 -m "Release v1.0.1

Major improvements and bug fixes:
- 6 critical bugs fixed
- Docker support added
- CI/CD pipeline implemented
- Comprehensive documentation
- Windows PowerShell scripts
- Security improvements
- 100% test coverage"

# 2. Push tag
git push origin v1.0.1

# 3. ایجاد Release در GitHub
# رفتن به: https://github.com/AhmadAkd/V2Ray_Collector/releases/new
# انتخاب tag: v1.0.1
# عنوان: Release v1.0.1 - Major Improvements
# توضیحات: کپی از RELEASE_NOTES_v1.0.1.md
```

---

## 🔍 بررسی قبل از Push

### چک‌لیست

```bash
# 1. بررسی تغییرات
git status
git diff

# 2. اجرای تست‌ها
python run_tests.py

# 3. بررسی لاگ commit ها
git log --oneline -5

# 4. بررسی branch فعلی
git branch

# 5. بررسی remote
git remote -v
```

---

## ⚠️ مشکلات احتمالی و راه‌حل

### مشکل 1: Authentication Failed

```bash
# راه‌حل: استفاده از Personal Access Token
git remote set-url origin https://YOUR_TOKEN@github.com/AhmadAkd/V2Ray_Collector.git
```

### مشکل 2: Merge Conflict

```bash
# راه‌حل: Pull قبل از Push
git pull origin main
# حل conflict ها
git add .
git commit -m "Resolve conflicts"
git push origin main
```

### مشکل 3: Large Files

```bash
# راه‌حل: بررسی فایل‌های بزرگ
find . -type f -size +50M

# حذف از git
git rm --cached large_file.txt
echo "large_file.txt" >> .gitignore
git commit -m "Remove large file"
```

### مشکل 4: Permission Denied

```bash
# راه‌حل: تنظیم SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"
# اضافه کردن به GitHub: Settings → SSH Keys
```

---

## 📊 بعد از Push

### 1. بررسی GitHub Actions

```
رفتن به: https://github.com/AhmadAkd/V2Ray_Collector/actions
بررسی اینکه workflow ها اجرا شدند
```

### 2. بررسی GitHub Pages

```
رفتن به: https://ahmadakd.github.io/V2Ray_Collector/
بررسی اینکه صفحه به‌روز شده
```

### 3. تست Docker Image

```bash
docker pull ghcr.io/ahmadakd/v2ray-collector:latest
docker run -d ghcr.io/ahmadakd/v2ray-collector:latest
```

### 4. اطلاع‌رسانی

- [ ] Update README.md badge ها
- [ ] اعلام در Discussions
- [ ] اطلاع‌رسانی کاربران
- [ ] Update Wiki

---

## 🎯 دستورات سریع

### دستور یکخطی (تمام کار)

```bash
# ⚠️ فقط اگر مطمئن هستید!
git add . && git commit -m "🎉 Release v1.0.1" && git push origin main && git tag v1.0.1 && git push origin v1.0.1
```

### دستور با بررسی

```bash
# با تست و بررسی
python run_tests.py && git add . && git commit -m "🎉 Release v1.0.1" && git push origin main
```

---

## 📝 Template پیام Commit

```
🎉 Release v1.0.1 - [عنوان کوتاه]

[توضیحات کامل]

Changes:
- ✅ Fixed: [باگ‌ها]
- 🆕 Added: [ویژگی‌های جدید]
- 🔧 Improved: [بهبودها]
- 📚 Docs: [مستندات]

Breaking Changes: None

See RELEASE_NOTES_v1.0.1.md for details
```

---

## 🔐 امنیت

### قبل از Push

```bash
# 1. بررسی secrets
git grep -i "password\|token\|key\|secret"

# 2. بررسی .gitignore
cat .gitignore

# 3. حذف فایل‌های حساس از تاریخچه
git filter-branch --force --index-filter \
'git rm --cached --ignore-unmatch sensitive_file.txt' \
--prune-empty --tag-name-filter cat -- --all
```

---

**✅ آماده Push!**

دستورات بالا را به ترتیب اجرا کنید.

موفق باشید! 🎉
