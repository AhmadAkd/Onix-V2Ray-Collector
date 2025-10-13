# استفاده از Python 3.10 slim
FROM python:3.10-slim

# تنظیم متغیرهای محیطی
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# تنظیم working directory
WORKDIR /app

# نصب وابستگی‌های سیستمی
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    git \
    && rm -rf /var/lib/apt/lists/*

# کپی فایل requirements
COPY requirements.txt .

# نصب وابستگی‌های Python
RUN pip install --no-cache-dir -r requirements.txt

# کپی کل پروژه
COPY . .

# ایجاد دایرکتوری‌های مورد نیاز
RUN mkdir -p subscriptions cache analytics logs

# تنظیم دسترسی‌ها
RUN chmod +x *.py

# Expose پورت API (در صورت نیاز)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# دستور پیش‌فرض
CMD ["python", "automation.py", "--mode", "auto"]

