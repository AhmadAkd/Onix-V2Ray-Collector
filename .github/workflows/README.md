# 🤖 GitHub Actions Workflows

این پوشه شامل workflow های خودکار برای پروژه است.

---

## 📋 Workflows موجود

### 1. 🔄 Auto Collect and Update (`auto-collect.yml`)

**هدف**: جمع‌آوری و به‌روزرسانی خودکار کانفیگ‌ها

**زمان اجرا**:
- 🕐 هر 30 دقیقه یکبار (خودکار)
- 🔀 با هر push به branch main
- 🖱️ اجرای دستی از Actions tab

**کارهایی که انجام می‌دهد**:
1. ✅ نصب Python و وابستگی‌ها
2. 🧪 اجرای تست‌ها
3. 🔄 جمع‌آوری کانفیگ‌ها از منابع
4. 📊 تولید گزارش analytics
5. 🏥 بررسی سلامت سیستم
6. 💾 Commit و Push نتایج
7. 📢 ایجاد Issue در صورت خطا
8. 📤 آپلود artifacts

**خروجی**:
- فایل‌های subscription در `subscriptions/`
- گزارش‌ها در `subscriptions/report.json`
- Artifacts قابل دانلود

---

### 2. 🧪 Run Tests (`test.yml`)

**هدف**: اجرای تست‌ها روی پلتفرم‌ها و نسخه‌های مختلف

**زمان اجرا**:
- 🔀 با هر push به main/develop
- 🔀 با هر Pull Request
- 🖱️ اجرای دستی

**ماتریس تست**:
- OS: Ubuntu, Windows, macOS
- Python: 3.8, 3.9, 3.10, 3.11

**کارهایی که انجام می‌دهد**:
1. ✅ تست روی سیستم‌عامل‌های مختلف
2. ✅ تست روی نسخه‌های مختلف Python
3. 🔍 بررسی کیفیت کد (flake8, black)
4. 🔒 اسکن امنیتی (bandit, safety)
5. 📤 آپلود گزارش‌های تست

**خروجی**:
- گزارش تست برای هر پلتفرم
- گزارش‌های code quality
- گزارش‌های امنیتی

---

### 3. 🏷️ Create Release (`release.yml`)

**هدف**: ایجاد خودکار Release

**زمان اجرا**:
- 🏷️ با push کردن tag (مثلاً v1.0.1)
- 🖱️ اجرای دستی با مشخص کردن نسخه

**کارهایی که انجام می‌دهد**:
1. 🧪 اجرای تست‌ها
2. 📝 تولید Changelog خودکار
3. 📊 جمع‌آوری آمار پروژه
4. 📦 ساخت بسته‌های توزیع (ZIP, tar.gz)
5. 🏷️ ایجاد Release در GitHub
6. 📤 آپلود فایل‌های subscription

**خروجی**:
- Release صفحه در GitHub
- فایل‌های قابل دانلود برای کاربران
- Changelog کامل

---

### 4. 🐳 Docker Build and Push (`docker-build.yml`)

**هدف**: ساخت و انتشار Docker image

**زمان اجرا**:
- 🔀 با هر push به main
- 🏷️ با push کردن tag
- 🔀 با Pull Request (فقط build، بدون push)
- 🖱️ اجرای دستی

**کارهایی که انجام می‌دهد**:
1. 🧪 اجرای تست‌ها
2. 🐳 ساخت Docker image
3. 🔒 اسکن امنیتی image (Trivy)
4. 📤 Push به GitHub Container Registry
5. 🏷️ تگ‌گذاری خودکار (latest, version, sha)

**خروجی**:
- Docker image در `ghcr.io/ahmadakd/v2ray_collector`
- گزارش امنیتی
- Multi-platform support (amd64, arm64)

---

## 🚀 نحوه استفاده

### فعال‌سازی Workflows

1. **Push به GitHub**:
   ```bash
   git add .
   git commit -m "Enable workflows"
   git push origin main
   ```

2. **فعال‌سازی GitHub Actions**:
   - رفتن به repository در GitHub
   - Settings → Actions → General
   - Allow all actions

3. **تنظیم GitHub Pages** (اختیاری):
   - Settings → Pages
   - Source: GitHub Actions
   - یا Branch: main, Folder: /subscriptions

### اجرای دستی Workflow

1. رفتن به: `Actions` tab
2. انتخاب workflow مورد نظر
3. کلیک روی `Run workflow`
4. انتخاب branch و پارامترها
5. کلیک `Run workflow`

### مشاهده نتایج

**در GitHub**:
- رفتن به Actions tab
- کلیک روی workflow run
- مشاهده logs و artifacts

**Summary**:
هر workflow یک خلاصه تولید می‌کند که شامل:
- آمار کانفیگ‌ها
- نتایج تست‌ها
- فایل‌های تولید شده

---

## 🔐 Permissions مورد نیاز

Workflows نیاز به permissions زیر دارند:

```yaml
permissions:
  contents: write      # برای commit و push
  packages: write      # برای Docker images
  issues: write        # برای ایجاد issue
  pull-requests: write # برای PR comments
```

این permissions به صورت خودکار از طریق `GITHUB_TOKEN` داده می‌شوند.

---

## 🔧 سفارشی‌سازی

### تغییر زمان اجرا

در `auto-collect.yml`:

```yaml
schedule:
  # هر ساعت
  - cron: '0 * * * *'
  
  # هر 2 ساعت
  - cron: '0 */2 * * *'
  
  # هر روز ساعت 12
  - cron: '0 12 * * *'
```

### غیرفعال کردن Workflow

**روش 1**: تغییر نام فایل:
```bash
mv auto-collect.yml auto-collect.yml.disabled
```

**روش 2**: اضافه کردن شرط:
```yaml
on:
  workflow_dispatch:  # فقط دستی
```

### اضافه کردن Notification

در `auto-collect.yml`:

```yaml
- name: 📧 Send notification
  if: success()
  run: |
    # ارسال به Telegram
    curl -X POST "https://api.telegram.org/bot${{ secrets.TELEGRAM_BOT_TOKEN }}/sendMessage" \
      -d "chat_id=${{ secrets.TELEGRAM_CHAT_ID }}" \
      -d "text=✅ Configs updated successfully!"
```

---

## 📊 Monitoring

### GitHub Actions Dashboard

مشاهده وضعیت تمام workflows:
```
https://github.com/AhmadAkd/V2Ray_Collector/actions
```

### Workflow Badges

اضافه کردن به README.md:

```markdown
![Auto Collect](https://github.com/AhmadAkd/V2Ray_Collector/workflows/Auto%20Collect%20and%20Update%20Configs/badge.svg)
![Tests](https://github.com/AhmadAkd/V2Ray_Collector/workflows/Run%20Tests/badge.svg)
![Docker](https://github.com/AhmadAkd/V2Ray_Collector/workflows/Build%20and%20Push%20Docker%20Image/badge.svg)
```

---

## ⚠️ نکات مهم

### محدودیت‌های GitHub Actions

- ⏱️ حداکثر 6 ساعت برای هر job
- 💾 حداکثر 500MB برای artifacts
- 🔄 حداکثر 20 workflow همزمان
- 📅 2000 دقیقه رایگان در ماه (برای private repos)

### بهینه‌سازی

1. **استفاده از Cache**:
   ```yaml
   - uses: actions/cache@v3
     with:
       path: ~/.cache/pip
       key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
   ```

2. **Timeout مناسب**:
   ```yaml
   - name: Collect configs
     run: python config_collector.py
     timeout-minutes: 30
   ```

3. **Conditional execution**:
   ```yaml
   - name: Step
     if: github.event_name == 'push'
     run: command
   ```

---

## 🐛 Debug Workflows

### فعال‌سازی Debug Logging

در repository secrets اضافه کنید:
- `ACTIONS_STEP_DEBUG`: `true`
- `ACTIONS_RUNNER_DEBUG`: `true`

### مشاهده Logs دقیق

```bash
# دانلود logs
gh run download <run-id>

# مشاهده live logs
gh run watch
```

---

## 📚 منابع بیشتر

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [GitHub CLI](https://cli.github.com/)

---

## 🎯 مثال‌های کاربردی

### اجرای دستی Auto-Collect

```bash
# با GitHub CLI
gh workflow run auto-collect.yml

# مشاهده وضعیت
gh run list --workflow=auto-collect.yml
```

### دانلود Artifacts

```bash
# لیست artifacts
gh run list

# دانلود
gh run download <run-id>
```

### مشاهده Logs

```bash
# آخرین run
gh run view

# Run خاص
gh run view <run-id> --log
```

---

**✅ Workflows آماده هستند!**

بعد از push، GitHub Actions به صورت خودکار شروع به کار می‌کند.

