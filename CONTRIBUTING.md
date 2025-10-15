# 🤝 راهنمای مشارکت در V2Ray Collector

<div align="center">

**از اینکه می‌خواهید در بهبود این پروژه مشارکت کنید متشکریم! 🙏**

این راهنما به شما کمک می‌کند تا به بهترین شکل ممکن مشارکت کنید.

</div>

---

## 📑 فهرست

- [🎯 انواع مشارکت](#-انواع-مشارکت)
- [🚀 شروع کار](#-شروع-کار)
- [💻 توسعه](#-توسعه)
- [✅ Code Style](#-code-style)
- [🧪 تست](#-تست)
- [📝 Commit Messages](#-commit-messages)
- [🔄 Pull Request](#-pull-request)
- [🐛 گزارش باگ](#-گزارش-باگ)
- [💡 پیشنهاد ویژگی](#-پیشنهاد-ویژگی)

---

## 🎯 انواع مشارکت

### 1. **🐛 گزارش باگ**
اگر باگی پیدا کردید، لطفاً:
- از قسمت [Issues](https://github.com/AhmadAkd/Onix-V2Ray-Collector/issues) گزارش دهید
- توضیح دقیق از مشکل
- مراحل بازتولید باگ
- اسکرین‌شات (در صورت امکان)

### 2. **💡 پیشنهاد ویژگی**
ایده جدیدی دارید؟
- Issue جدید با label `enhancement` باز کنید
- توضیح دقیق از ویژگی
- مثال‌های کاربردی
- دلایل نیاز به این ویژگی

### 3. **📝 بهبود مستندات**
- اصلاح typo ها
- اضافه کردن مثال‌ها
- ترجمه به زبان‌های دیگر
- بهبود توضیحات

### 4. **🔧 کد نویسی**
- رفع باگ‌ها
- اضافه کردن ویژگی‌های جدید
- بهینه‌سازی عملکرد
- رفع مشکلات امنیتی

### 5. **🎨 طراحی UI/UX**
- بهبود رابط کاربری
- طراحی صفحات جدید
- بهبود تجربه کاربری
- ایجاد mockup ها

---

## 🚀 شروع کار

### 1. **Fork کردن Repository**

```bash
# 1. از GitHub روی دکمه Fork کلیک کنید
# 2. Clone کنید
git clone https://github.com/YOUR_USERNAME/Onix-V2Ray-Collector.git
cd Onix-V2Ray-Collector

# 3. Remote اضافه کنید
git remote add upstream https://github.com/AhmadAkd/Onix-V2Ray-Collector.git
```

### 2. **نصب Dependencies**

```bash
# ایجاد virtual environment
python -m venv venv

# فعال‌سازی
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# نصب dependencies
pip install -r requirements.txt
pip install -r requirements_enhanced.txt  # برای توسعه

# نصب pre-commit hooks (اختیاری)
pip install pre-commit
pre-commit install
```

### 3. **ایجاد Branch جدید**

```bash
# بروزرسانی از upstream
git fetch upstream
git checkout main
git merge upstream/main

# ایجاد branch جدید
git checkout -b feature/your-feature-name
# یا
git checkout -b fix/bug-description
```

---

## 💻 توسعه

### 🏗️ **ساختار پروژه**

```
Onix-V2Ray-Collector/
├── config_collector.py      # ⚡ Core: موتور اصلی
├── singbox_parser.py        # 📦 Parser: SingBox JSON
├── geoip_lookup.py          # 🌍 GeoIP: شناسایی کشور
├── cache_manager.py         # 🗄️ Cache: مدیریت کش
├── config.py                # ⚙️ Config: تنظیمات
├── subscriptions/           # 📁 Output: فایل‌های خروجی
│   ├── index.html          # 🏠 صفحه اصلی
│   ├── dashboard.html      # 📊 داشبورد
│   └── ...
└── .github/workflows/       # 🤖 CI/CD: اتوماسیون
```

### 🔧 **اضافه کردن Parser جدید**

```python
# مثال: اضافه کردن parser برای پروتکل جدید
class NewProtocolParser:
    def parse(self, config_string: str) -> Optional[V2RayConfig]:
        """
        Parse کردن فرمت جدید
        
        Args:
            config_string: رشته کانفیگ
            
        Returns:
            V2RayConfig یا None
        """
        try:
            # Logic پارس
            if not config_string.startswith('newprotocol://'):
                return None
                
            # استخراج اطلاعات
            # ...
            
            return V2RayConfig(
                protocol='newprotocol',
                address=address,
                port=port,
                # ...
            )
        except Exception as e:
            logger.error(f"Error parsing: {e}")
            return None
```

### 🌐 **اضافه کردن منبع جدید**

در فایل `config.py`:

```python
CONFIG_SOURCES = [
    # ... منابع موجود
    
    # منبع جدید
    "https://your-source.com/configs.txt",
]
```

**چک لیست برای منابع جدید:**
- [ ] URL معتبر و دائمی است
- [ ] حداقل 10+ کانفیگ دارد
- [ ] منبع به‌روز می‌شود (حداقل هفتگی)
- [ ] فرمت استاندارد است (vmess://, vless://, ...)
- [ ] تست شده و کار می‌کند

---

## ✅ Code Style

### 🐍 **Python**

ما از **PEP 8** پیروی می‌کنیم:

```python
# ✅ خوب
def fetch_configs_from_source(source_url: str, timeout: int = 30) -> List[str]:
    """
    جمع‌آوری کانفیگ‌ها از یک منبع
    
    Args:
        source_url: آدرس منبع
        timeout: زمان انتظار (ثانیه)
        
    Returns:
        لیست کانفیگ‌ها
    """
    try:
        response = await fetch(source_url, timeout=timeout)
        return parse_response(response)
    except Exception as e:
        logger.error(f"Error fetching from {source_url}: {e}")
        return []

# ❌ بد
def get_configs(url,t=30):
    r=fetch(url,t)
    return parse(r)
```

**قوانین مهم:**
- ✅ Type hints برای تمام توابع
- ✅ Docstrings برای توابع public
- ✅ نام‌گذاری واضح و معنادار
- ✅ Error handling مناسب
- ✅ Logging برای debug
- ✅ کامنت برای کدهای پیچیده

### 🌐 **JavaScript/HTML/CSS**

```javascript
// ✅ خوب
async function loadStatistics() {
    try {
        const response = await fetch('latest_report.json');
        const data = await response.json();
        updateUI(data);
    } catch (error) {
        console.error('Error loading stats:', error);
        showErrorMessage();
    }
}

// ❌ بد
function load(){fetch('latest_report.json').then(r=>r.json()).then(d=>update(d))}
```

---

## 🧪 تست

### ✅ **قبل از Commit**

```bash
# 1. اجرای تست‌های موجود
python -m pytest tests/

# 2. تست دستی
python config_collector.py

# 3. بررسی output
open subscriptions/index.html
```

### 📝 **نوشتن تست**

```python
# tests/test_parser.py
import pytest
from config_collector import V2RayCollector

def test_vmess_parser():
    """تست parser برای VMess"""
    collector = V2RayCollector()
    config = "vmess://eyJ2IjoiMiIsInBzIjoi..."
    
    result = collector.parse_config(config)
    
    assert result is not None
    assert result.protocol == 'vmess'
    assert result.port == 443

def test_invalid_config():
    """تست با کانفیگ نامعتبر"""
    collector = V2RayCollector()
    config = "invalid://config"
    
    result = collector.parse_config(config)
    
    assert result is None
```

---

## 📝 Commit Messages

### 📋 **فرمت**

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 🏷️ **Types**

- `feat`: ویژگی جدید
- `fix`: رفع باگ
- `docs`: تغییرات مستندات
- `style`: فرمت کد (بدون تغییر logic)
- `refactor`: بازنویسی کد
- `perf`: بهبود عملکرد
- `test`: اضافه/تغییر تست‌ها
- `chore`: تغییرات build/tools

### ✅ **مثال‌های خوب**

```bash
# ویژگی جدید
feat(parser): add WireGuard protocol support

- Implement WireGuard parser
- Add tests for WireGuard configs
- Update documentation

# رفع باگ
fix(dashboard): prevent infinite chart height

- Wrap canvas in fixed-height container
- Add max-height CSS constraints
- Fix chart aspectRatio

# مستندات
docs: update README with new features

- Add SingBox parser section
- Update statistics
- Add badges
```

### ❌ **مثال‌های بد**

```bash
# بیش از حد کلی
update files

# بدون توضیح
fix bug

# فینگلیش!
fix: moshkel chart ha hal shod
```

---

## 🔄 Pull Request

### 📋 **چک لیست قبل از PR**

- [ ] کد تست شده است
- [ ] تست‌های موجود Pass می‌شوند
- [ ] Documentation بروز شده (در صورت نیاز)
- [ ] Commit messages استاندارد هستند
- [ ] Code style رعایت شده
- [ ] تغییرات breaking مستند شده‌اند

### 📝 **Template**

```markdown
## 📋 توضیحات

<!-- توضیح کامل از تغییرات -->

## 🔗 Related Issues

Closes #123
Fixes #456

## 🧪 چطور تست کردم؟

1. ...
2. ...
3. ...

## 📸 اسکرین‌شات (در صورت نیاز)

<!-- اگر تغییرات UI دارید -->

## ✅ چک لیست

- [x] تست شده
- [x] Documentation بروز شده
- [x] Code style رعایت شده
- [ ] Breaking changes مستند شده
```

### 🔍 **Code Review**

پس از ارسال PR:
1. ✅ GitHub Actions چک می‌شود
2. 👀 یکی از maintainer ها review می‌کند
3. 💬 Feedback داده می‌شود (در صورت نیاز)
4. ✅ پس از تأیید، merge می‌شود

---

## 🐛 گزارش باگ

### 📋 **Template**

```markdown
## 🐛 توضیح باگ

<!-- توضیح واضح و کامل -->

## 🔄 مراحل بازتولید

1. برو به '...'
2. کلیک کن روی '...'
3. Scroll کن به '...'
4. مشاهده خطا

## ✅ رفتار مورد انتظار

<!-- چه اتفاقی باید می‌افتاد؟ -->

## ❌ رفتار فعلی

<!-- چه اتفاقی افتاده؟ -->

## 📸 اسکرین‌شات

<!-- در صورت امکان -->

## 💻 محیط

- OS: [e.g. Windows 11]
- Python: [e.g. 3.11]
- Browser: [e.g. Chrome 120]

## 📝 اطلاعات اضافی

<!-- Context، logs، etc -->
```

---

## 💡 پیشنهاد ویژگی

### 📋 **Template**

```markdown
## 🎯 مشکل

<!-- چه مشکلی را حل می‌کند؟ -->

## 💡 راه‌حل پیشنهادی

<!-- توضیح دقیق از ویژگی -->

## 🔄 جایگزین‌های در نظر گرفته شده

<!-- راه‌حل‌های دیگر -->

## 📝 Context اضافی

<!-- مثال‌ها، mockup ها، etc -->
```

---

## 🏆 تشکر

### 🌟 **مشارکت‌کنندگان برتر**

<a href="https://github.com/AhmadAkd/Onix-V2Ray-Collector/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=AhmadAkd/Onix-V2Ray-Collector" />
</a>

### 💝 **تشکر ویژه از:**

- تمام کسانی که باگ گزارش می‌کنند
- تمام کسانی که ویژگی پیشنهاد می‌کنند
- تمام کسانی که مستندات را بهبود می‌دهند
- تمام کسانی که این پروژه را ستاره می‌دهند!

---

## 📞 ارتباط

### 💬 **راه‌های ارتباطی**

- 🐛 **باگ و مشکلات**: [GitHub Issues](https://github.com/AhmadAkd/Onix-V2Ray-Collector/issues)
- 💡 **ایده‌ها**: [GitHub Discussions](https://github.com/AhmadAkd/Onix-V2Ray-Collector/discussions)
- 📧 **ایمیل**: your.email@example.com
- 💬 **Telegram**: [@your_channel](https://t.me/your_channel)

---

## 📄 Code of Conduct

### 🤝 **قوانین رفتاری**

1. **احترام**: به همه با احترام رفتار کنید
2. **سازنده**: نقد سازنده ارائه دهید
3. **صبور**: همه سطح تجربه را بپذیرید
4. **حمایتگر**: به یکدیگر کمک کنید
5. **منصف**: بدون تبعیض

### ⚠️ **رفتارهای غیرقابل قبول**

- ❌ زبان توهین‌آمیز
- ❌ حمله شخصی
- ❌ Trolling
- ❌ Harassment
- ❌ تبلیغات غیرمجاز

---

<div align="center">

**با تشکر از مشارکت شما! 🙏**

**این پروژه را با ⭐ ستاره کنید!**

[🏠 بازگشت به README](README.md)

</div>
