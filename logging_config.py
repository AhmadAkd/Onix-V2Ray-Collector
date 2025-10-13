#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Logging Configuration with Rotation
تنظیمات لاگ‌گیری با قابلیت چرخش فایل‌ها
"""

import logging
import logging.handlers
import os
from typing import Optional


def setup_logger(
    name: str,
    log_file: Optional[str] = None,
    level: int = logging.INFO,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
    console: bool = True
) -> logging.Logger:
    """
    تنظیم logger با قابلیت rotation

    Args:
        name: نام logger
        log_file: مسیر فایل لاگ
        level: سطح لاگ
        max_bytes: حداکثر حجم فایل لاگ (بایت)
        backup_count: تعداد فایل‌های backup
        console: نمایش لاگ در کنسول

    Returns:
        Logger تنظیم شده
    """
    # ایجاد logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # پاک کردن handler های قبلی
    logger.handlers.clear()

    # فرمت لاگ
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # اضافه کردن handler برای فایل با rotation
    if log_file:
        # ایجاد دایرکتوری لاگ
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        # Rotating file handler
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # اضافه کردن handler برای کنسول
    if console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


def setup_time_rotating_logger(
    name: str,
    log_file: str,
    level: int = logging.INFO,
    when: str = 'midnight',
    interval: int = 1,
    backup_count: int = 7,
    console: bool = True
) -> logging.Logger:
    """
    تنظیم logger با قابلیت rotation بر اساس زمان

    Args:
        name: نام logger
        log_file: مسیر فایل لاگ
        level: سطح لاگ
        when: زمان rotation ('midnight', 'H', 'D', 'W0'-'W6')
        interval: فاصله زمانی
        backup_count: تعداد فایل‌های backup
        console: نمایش لاگ در کنسول

    Returns:
        Logger تنظیم شده
    """
    # ایجاد logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # پاک کردن handler های قبلی
    logger.handlers.clear()

    # فرمت لاگ
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # ایجاد دایرکتوری لاگ
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    # Time rotating file handler
    file_handler = logging.handlers.TimedRotatingFileHandler(
        log_file,
        when=when,
        interval=interval,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # اضافه کردن handler برای کنسول
    if console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


# تنظیمات پیش‌فرض لاگ‌گیری برای پروژه
def setup_project_logging():
    """تنظیم لاگ‌گیری برای کل پروژه"""

    # ایجاد دایرکتوری logs
    os.makedirs('logs', exist_ok=True)

    # Logger اصلی
    main_logger = setup_logger(
        name='v2ray_collector',
        log_file='logs/v2ray_collector.log',
        level=logging.INFO,
        max_bytes=10 * 1024 * 1024,  # 10MB
        backup_count=5
    )

    # Logger برای اتوماسیون
    automation_logger = setup_logger(
        name='automation',
        log_file='logs/automation.log',
        level=logging.INFO,
        max_bytes=5 * 1024 * 1024,  # 5MB
        backup_count=3
    )

    # Logger برای API
    api_logger = setup_logger(
        name='api',
        log_file='logs/api.log',
        level=logging.INFO,
        max_bytes=5 * 1024 * 1024,  # 5MB
        backup_count=3
    )

    # Logger برای خطاها
    error_logger = setup_logger(
        name='errors',
        log_file='logs/errors.log',
        level=logging.ERROR,
        max_bytes=10 * 1024 * 1024,  # 10MB
        backup_count=10
    )

    return {
        'main': main_logger,
        'automation': automation_logger,
        'api': api_logger,
        'errors': error_logger
    }


# نمونه استفاده
if __name__ == "__main__":
    # تنظیم لاگ‌گیری
    loggers = setup_project_logging()

    # تست
    loggers['main'].info("این یک پیام تست است")
    loggers['automation'].info("اتوماسیون شروع شد")
    loggers['api'].info("API شروع شد")
    loggers['errors'].error("این یک خطای تست است")

    print("✅ لاگ‌گیری با موفقیت تنظیم شد")
    print("📁 فایل‌های لاگ در پوشه logs/ ذخیره شدند")
