# 🤖 GitHub Actions - اتوماسیون کامل

## 🎯 هدف

این پروژه از **GitHub Actions** برای اتوماسیون کامل استفاده می‌کند.

---

## ⚡ قابلیت‌های خودکار

### 🔄 جمع‌آوری خودکار
- **هر 30 دقیقه** کانفیگ‌های جدید جمع‌آوری می‌شود
- **خودکار** تست می‌شود
- **خودکار** commit و push می‌شود

### 🧪 تست خودکار
- تست روی **3 سیستم‌عامل** (Ubuntu, Windows, macOS)
- تست روی **4 نسخه Python** (3.8-3.11)
- **12 ماتریس تست** مختلف

### 🐳 Docker خودکار
- ساخت **image** با هر push
- Push به **GitHub Container Registry**
- اسکن **امنیتی** خودکار

### 🏷️ Release خودکار
- ایجاد **Release** با tag
- تولید **Changelog** خودکار
- آپلود **فایل‌های توزیع**

---

## 📁 ساختار

```
.github/
└── workflows/
    ├── auto-collect.yml   # جمع‌آوری خودکار (هر 30 دقیقه)
    ├── test.yml           # تست چندگانه
    ├── docker-build.yml   # ساخت Docker
    ├── release.yml        # ایجاد Release
    └── README.md          # این فایل
```

---

## 🚀 فعال‌سازی

### گام 1: Push به GitHub

```bash
git add .
git commit -m "🤖 Enable GitHub Actions"
git push origin main
```

### گام 2: تنظیم Permissions

1. `Settings` → `Actions` → `General`
2. Workflow permissions: `Read and write permissions`
3. ✅ `Allow GitHub Actions to create and approve pull requests`

### گام 3: بررسی Actions

1. رفتن به `Actions` tab
2. مشاهده workflows در حال اجرا
3. بررسی نتایج

---

## 📊 زمان‌بندی

| Workflow | زمان اجرا | مدت زمان | هزینه/ماه |
|----------|-----------|----------|-----------|
| Auto Collect | هر 30 دقیقه | ~5 min | 240 min |
| Tests | هر push | ~10 min | 50 min |
| Docker | هر push | ~8 min | 40 min |
| Release | هر tag | ~5 min | 5 min |
| **جمع** | - | - | **~335 min** |

**✅ کاملاً در محدوده رایگان GitHub (2000 min/month)**

---

## 🎮 اجرای دستی

### از GitHub Interface:
1. `Actions` tab
2. انتخاب workflow
3. `Run workflow` button
4. `Run workflow` تایید

### با GitHub CLI:
```bash
gh workflow run auto-collect.yml
gh workflow run test.yml
gh run list
gh run watch
```

---

## 📈 نتایج

### Auto-Collect
- ✅ فایل‌های subscription به‌روز می‌شوند
- ✅ گزارش‌ها تولید می‌شوند
- ✅ Commit خودکار با پیام: `🤖 Auto-update: ...`

### Tests
- ✅ گزارش تست برای هر پلتفرم
- ✅ Badge های وضعیت
- ✅ Artifacts قابل دانلود

### Docker
- ✅ Image در `ghcr.io`
- ✅ Tags خودکار
- ✅ Multi-platform

### Release
- ✅ Release page
- ✅ فایل‌های قابل دانلود
- ✅ Changelog

---

## 🎉 نتیجه

**شما دیگر نیازی به کار دستی ندارید!**

فقط:
1. ✅ یکبار Push کنید
2. ✅ GitHub Actions همه کارها را انجام می‌دهد
3. ✅ پروژه همیشه به‌روز می‌ماند

---

**📚 راهنمای کامل**: `GITHUB_ACTIONS_GUIDE.md`

