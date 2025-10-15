# 🔒 Security Policy

## 🛡️ نسخه‌های پشتیبانی شده

ما به امنیت V2Ray Collector اهمیت زیادی می‌دهیم. نسخه‌های زیر در حال حاضر پشتیبانی امنیتی دارند:

| Version | Supported          | Status |
| ------- | ------------------ | ------ |
| 2.0.x   | ✅ Yes            | Actively maintained |
| 1.5.x   | ⚠️ Limited        | Security fixes only |
| 1.0.x   | ❌ No             | End of life |
| < 1.0   | ❌ No             | End of life |

---

## 🚨 گزارش آسیب‌پذیری‌ها

### 📧 **گزارش خصوصی**

اگر آسیب‌پذیری امنیتی پیدا کردید، لطفاً **خصوصی** گزارش دهید:

**❌ از ایجاد Public Issue خودداری کنید!**

به جای آن:
1. 📧 ایمیل به: `security@yourproject.com`
2. 🔐 یا از [GitHub Security Advisories](https://github.com/AhmadAkd/Onix-V2Ray-Collector/security/advisories) استفاده کنید

### 📋 **اطلاعات مورد نیاز**

لطفاً موارد زیر را شامل شوید:

```markdown
## 🐛 توضیح آسیب‌پذیری
- نوع آسیب‌پذیری (XSS, Injection, CSRF, etc)
- تأثیر احتمالی
- شدت (Critical/High/Medium/Low)

## 🔄 مراحل بازتولید
1. ...
2. ...
3. ...

## 💻 محیط
- نسخه: [e.g. 2.0.0]
- OS: [e.g. Ubuntu 22.04]
- Python: [e.g. 3.11]

## 📝 Proof of Concept
- کد نمونه یا اسکرین‌شات
- Log ها (در صورت امکان)

## 🛠️ راه‌حل پیشنهادی (اختیاری)
- اگر راه‌حلی در ذهن دارید
```

---

## ⚡ فرآیند پاسخ

### 🕐 **Timeline**

| مرحله | زمان | توضیح |
|-------|------|--------|
| **تأیید دریافت** | 24 ساعت | تأیید دریافت گزارش |
| **بررسی اولیه** | 72 ساعت | تأیید/رد آسیب‌پذیری |
| **رفع مشکل** | 7-30 روز | بسته به شدت |
| **انتشار Patch** | بعد از Fix | بروزرسانی امنیتی |
| **اعلام عمومی** | 30 روز بعد | در CHANGELOG |

### 📊 **اولویت‌بندی**

#### 🔴 **Critical** (24-48 ساعت)
- Remote Code Execution (RCE)
- SQL Injection
- Authentication Bypass
- Data Breach

#### 🟠 **High** (3-7 روز)
- XSS Stored
- CSRF
- Privilege Escalation
- Information Disclosure

#### 🟡 **Medium** (7-14 روز)
- XSS Reflected
- Open Redirect
- Security Misconfiguration

#### 🟢 **Low** (14-30 روز)
- Information Leakage
- Missing Security Headers
- Weak Encryption

---

## 🛡️ اقدامات امنیتی فعلی

### ✅ **Implemented**

#### 1. **Input Validation**
```python
# تمام ورودی‌ها validate می‌شوند
def validate_config(config: str) -> bool:
    if not is_valid_url(config):
        return False
    if len(config) > MAX_LENGTH:
        return False
    return True
```

#### 2. **Rate Limiting**
- محدودیت تعداد request ها
- جلوگیری از abuse

#### 3. **Sanitization**
- Escape کردن HTML
- جلوگیری از Injection

#### 4. **Secrets Management**
- استفاده از Environment Variables
- عدم ذخیره Token ها در کد

#### 5. **HTTPS Only**
- تمام ارتباطات رمزنگاری شده
- Certificate Validation

### 🔄 **In Progress**

- [ ] Dependency Scanning (Dependabot)
- [ ] Code Scanning (CodeQL)
- [ ] Security Headers
- [ ] Content Security Policy (CSP)

---

## 🔐 Best Practices برای کاربران

### ✅ **توصیه‌های امنیتی**

#### 1. **Environment Variables**
```bash
# ❌ هرگز Token ها را در کد ذخیره نکنید
TELEGRAM_BOT_TOKEN=your_token

# ✅ از .env استفاده کنید
cp config.env.example .env
# سپس .env را ویرایش کنید
```

#### 2. **Permissions**
```bash
# محدود کردن دسترسی فایل‌ها
chmod 600 .env
chmod 700 cache/
```

#### 3. **Updates**
```bash
# همیشه از آخرین نسخه استفاده کنید
git pull origin main
pip install -r requirements.txt --upgrade
```

#### 4. **Firewall**
```bash
# محدود کردن دسترسی
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
```

### ⚠️ **خطرات شناخته شده**

#### 1. **Public Deployment**
```
⚠️ اگر این پروژه را Public deploy می‌کنید:
- Rate limiting فعال کنید
- Authentication اضافه کنید
- Monitor کنید
```

#### 2. **Telegram Bot**
```
⚠️ Token Telegram را محافظت کنید:
- در .env ذخیره کنید
- در git commit نکنید
- دسترسی محدود کنید
```

---

## 🏆 Bug Bounty Program

### 💰 **پاداش‌ها**

ما از گزارش‌دهندگان آسیب‌پذیری‌ها قدردانی می‌کنیم:

| شدت | پاداش | شرایط |
|------|--------|--------|
| **Critical** | 🏆 Hall of Fame + $100 | RCE, SQLi, Auth Bypass |
| **High** | 🥈 Hall of Fame + $50 | XSS, CSRF, Privilege Escalation |
| **Medium** | 🥉 Hall of Fame | Open Redirect, Misc |
| **Low** | 👏 Thank You | Info Leakage, Headers |

**توجه**: پاداش‌های مالی در صورت تأمین بودجه

### 🎖️ **Hall of Fame**

| Researcher | Vulnerabilities | Date |
|------------|----------------|------|
| - | - | - |

_هنوز کسی گزارش نداده! شما اولین باشید!_

---

## 📚 منابع امنیتی

### 📖 **مستندات**

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [NIST Guidelines](https://www.nist.gov/cybersecurity)

### 🛠️ **ابزارها**

```bash
# Security scanning
pip install safety bandit

# بررسی dependencies
safety check

# آنالیز کد
bandit -r .

# Secret scanning
git secrets --scan
```

---

## 📞 تماس

### 🚨 **فوری**
- 📧 Email: `security@yourproject.com`
- 🔐 GPG Key: [Download](link-to-gpg-key)

### 💬 **سؤالات عمومی**
- 💬 [GitHub Discussions](https://github.com/AhmadAkd/Onix-V2Ray-Collector/discussions)
- 🐛 [GitHub Issues](https://github.com/AhmadAkd/Onix-V2Ray-Collector/issues) (فقط برای مشکلات غیرامنیتی)

---

## 🙏 تشکر

از تمام کسانی که به بهبود امنیت این پروژه کمک می‌کنند، صمیمانه تشکر می‌کنیم!

### 🌟 **مشارکت‌کنندگان امنیتی**

- شما می‌توانید اولین نفر باشید!

---

<div align="center">

**امنیت یک اولویت است، نه یک ویژگی!** 🔒

**[🏠 بازگشت به README](README.md)**

</div>
