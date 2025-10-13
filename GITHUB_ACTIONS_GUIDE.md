# 🤖 راهنمای کامل GitHub Actions

## 🎯 خلاصه

پروژه شما حالا **4 workflow خودکار** دارد که همه کارها را به صورت اتوماتیک انجام می‌دهند!

---

## 🔄 Workflow 1: Auto Collect (جمع‌آوری خودکار)

### چه کاری می‌کند؟
- 🕐 **هر 30 دقیقه** کانفیگ‌های جدید را جمع‌آوری می‌کند
- 🧪 تست می‌کند
- 📊 گزارش می‌سازد
- 💾 نتایج را commit و push می‌کند

### زمان‌بندی:
```yaml
schedule:
  - cron: '*/30 * * * *'  # هر 30 دقیقه
```

### نتایج:
- فایل‌های subscription در `subscriptions/`
- گزارش در `subscriptions/report.json`
- Commit خودکار با پیام: `🤖 Auto-update: Collected configs`

---

## 🧪 Workflow 2: Run Tests (تست خودکار)

### چه کاری می‌کند؟
- 🐍 تست روی **3 سیستم‌عامل** (Ubuntu, Windows, macOS)
- 🔢 تست روی **4 نسخه Python** (3.8, 3.9, 3.10, 3.11)
- 🔍 بررسی کیفیت کد
- 🔒 اسکن امنیتی

### زمان اجرا:
- با هر **push** به main/develop
- با هر **Pull Request**
- اجرای دستی

### نتایج:
- گزارش تست برای هر پلتفرم
- گزارش code quality
- Badge های وضعیت

---

## 🐳 Workflow 3: Docker Build (ساخت Docker)

### چه کاری می‌کند؟
- 🏗️ می‌سازد Docker image
- 🔒 اسکن امنیتی
- 📤 Push به GitHub Container Registry
- 🏷️ تگ‌گذاری خودکار

### زمان اجرا:
- با هر **push** به main
- با **tag** جدید (v*)
- با Pull Request (فقط build)

### نتایج:
- Image در: `ghcr.io/ahmadakd/v2ray_collector`
- Tags: `latest`, `v1.0.1`, `sha-...`
- Multi-platform (amd64, arm64)

---

## 🏷️ Workflow 4: Create Release (انتشار خودکار)

### چه کاری می‌کند؟
- 📝 تولید Changelog
- 📊 جمع‌آوری آمار
- 📦 ساخت بسته‌های توزیع
- 🏷️ ایجاد Release
- 📤 آپلود فایل‌ها

### زمان اجرا:
- با push کردن **tag** (v*)
- اجرای دستی با مشخص کردن نسخه

### نتایج:
- Release page در GitHub
- فایل‌های ZIP و tar.gz
- Changelog خودکار

---

## 🚀 نحوه فعال‌سازی

### گام 1: Push به GitHub

```bash
# اضافه کردن همه فایل‌ها
git add .

# Commit
git commit -m "🤖 Add GitHub Actions workflows"

# Push
git push origin main
```

### گام 2: فعال‌سازی Actions

1. رفتن به: `https://github.com/AhmadAkd/V2Ray_Collector`
2. کلیک روی `Actions` tab
3. اگر Actions غیرفعال بود، کلیک روی `Enable workflows`

### گام 3: تنظیم Permissions

1. رفتن به: `Settings` → `Actions` → `General`
2. در بخش `Workflow permissions`:
   - انتخاب: `Read and write permissions`
   - تیک زدن: `Allow GitHub Actions to create and approve pull requests`
3. Save

### گام 4: فعال‌سازی GitHub Pages (اختیاری)

1. رفتن به: `Settings` → `Pages`
2. Source: `GitHub Actions`
3. یا انتخاب branch: `main` و folder: `/subscriptions`

---

## 🎮 استفاده از Workflows

### اجرای دستی Workflow

```bash
# با GitHub CLI (gh)
gh workflow run auto-collect.yml
gh workflow run test.yml
gh workflow run docker-build.yml

# مشاهده وضعیت
gh run list
gh run watch

# دانلود artifacts
gh run download <run-id>
```

### از طریق Web Interface

1. رفتن به `Actions` tab
2. انتخاب workflow
3. کلیک `Run workflow`
4. انتخاب branch
5. کلیک `Run workflow`

---

## 📊 مشاهده نتایج

### Summary Page

هر workflow یک Summary تولید می‌کند:

```markdown
## 📊 Collection Summary

### Statistics:
- 📈 Total configs tested: **1250**
- ✅ Working configs: **892**
- ❌ Failed configs: **358**
- 📊 Success rate: **71.4%**

### Files Generated:
- all_subscription.txt (892 configs)
- vmess_subscription.txt (345 configs)
- vless_subscription.txt (289 configs)
...
```

### Artifacts

فایل‌های زیر قابل دانلود هستند:
- `subscriptions-<run-number>` - همه فایل‌های subscription
- `test-results-<os>-py<version>` - نتایج تست
- `code-quality-reports` - گزارش‌های کیفیت

---

## 🔔 Notifications

### تنظیم Telegram Notification

1. ایجاد bot در Telegram
2. دریافت token
3. افزودن به Secrets:
   - `Settings` → `Secrets and variables` → `Actions`
   - New secret: `TELEGRAM_BOT_TOKEN`
   - New secret: `TELEGRAM_CHAT_ID`

4. اضافه کردن به workflow:
```yaml
- name: 📢 Telegram notification
  if: success()
  run: |
    curl -X POST "https://api.telegram.org/bot${{ secrets.TELEGRAM_BOT_TOKEN }}/sendMessage" \
      -d "chat_id=${{ secrets.TELEGRAM_CHAT_ID }}" \
      -d "text=✅ Configs updated! Total: $TOTAL_CONFIGS"
```

### ایمیل Notification

GitHub به صورت خودکار برای failed workflows ایمیل می‌فرستد.

تنظیم: `Settings` → `Notifications` → `Actions`

---

## 📈 Monitoring

### Badge ها

اضافه کردن به `README.md`:

```markdown
[![Auto Collect](https://github.com/AhmadAkd/V2Ray_Collector/actions/workflows/auto-collect.yml/badge.svg)](https://github.com/AhmadAkd/V2Ray_Collector/actions/workflows/auto-collect.yml)

[![Tests](https://github.com/AhmadAkd/V2Ray_Collector/actions/workflows/test.yml/badge.svg)](https://github.com/AhmadAkd/V2Ray_Collector/actions/workflows/test.yml)

[![Docker](https://github.com/AhmadAkd/V2Ray_Collector/actions/workflows/docker-build.yml/badge.svg)](https://github.com/AhmadAkd/V2Ray_Collector/actions/workflows/docker-build.yml)
```

### Dashboard

استفاده از GitHub CLI:

```bash
# نصب gh
# Windows: winget install GitHub.cli
# Mac: brew install gh
# Linux: apt install gh

# لیست runs
gh run list

# مشاهده جزئیات
gh run view <run-id>

# مشاهده logs
gh run view <run-id> --log
```

---

## 🔧 Troubleshooting

### مشکل 1: Workflow اجرا نمی‌شود

**راه‌حل**:
1. بررسی Actions در Settings (باید enabled باشد)
2. بررسی Permissions
3. بررسی syntax فایل yml

### مشکل 2: Push permission denied

**راه‌حل**:
```yaml
permissions:
  contents: write
```

### مشکل 3: Rate limit exceeded

**راه‌حل**:
- کاهش frequency از 30 دقیقه به 1 ساعت
- استفاده از cache بیشتر

### مشکل 4: Timeout

**راه‌حل**:
```yaml
timeout-minutes: 60  # افزایش timeout
```

---

## 💡 نکات و ترفندها

### 1. Cache Dependencies

```yaml
- uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```

### 2. Matrix Strategy

```yaml
strategy:
  matrix:
    python: [3.8, 3.9, 3.10]
    os: [ubuntu, windows, macos]
```

### 3. Conditional Steps

```yaml
- name: Deploy
  if: github.ref == 'refs/heads/main'
  run: deploy.sh
```

### 4. Secrets

```yaml
- name: Use secret
  run: echo ${{ secrets.MY_SECRET }}
```

---

## 📊 آمار Workflows

| Workflow | Frequency | Duration | Cost (mins/month) |
|----------|-----------|----------|-------------------|
| Auto Collect | 30 min | ~5 min | ~240 mins |
| Tests | On push | ~10 min | ~50 mins |
| Docker | On push | ~8 min | ~40 mins |
| Release | On tag | ~5 min | ~5 mins |
| **Total** | - | - | **~335 mins** |

**✅ در محدوده رایگان (2000 mins/month)**

---

## 🎯 Best Practices

1. ✅ استفاده از `cache` برای سرعت بیشتر
2. ✅ تنظیم `timeout` مناسب
3. ✅ استفاده از `continue-on-error` برای steps اختیاری
4. ✅ تولید `summary` برای نمایش بهتر
5. ✅ آپلود `artifacts` برای دانلود
6. ✅ استفاده از `matrix` برای تست چندگانه
7. ✅ استفاده از `secrets` برای اطلاعات حساس
8. ✅ اضافه کردن `badge` ها به README

---

## 🎉 نتیجه

با این workflows:
- ✅ پروژه **هر 30 دقیقه** به‌روز می‌شود
- ✅ تست‌ها **خودکار** اجرا می‌شوند
- ✅ Docker image **خودکار** ساخته می‌شود
- ✅ Release **خودکار** ایجاد می‌شود
- ✅ همه چیز **بدون دخالت شما**!

---

**🚀 فقط یکبار Push کنید، بقیه کارها خودکار انجام می‌شود!**

