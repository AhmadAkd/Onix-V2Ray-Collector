#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cleanup Invalid Country Files
حذف فایل‌های کشوری نامعتبر
"""

import os
import re
import glob


def is_valid_country_file(filename):
    """بررسی اعتبار نام فایل کشور"""
    # حذف .txt
    name = filename.replace('.txt', '')

    # لیست کدهای معتبر کشور
    valid_codes = {
        'US', 'DE', 'IR', 'CA', 'NL', 'TR', 'SE', 'IN', 'RU',
        'ES', 'NO', 'LT', 'HK', 'CN', 'GB', 'FR', 'JP', 'SG',
        'AU', 'BR', 'KR', 'IT', 'CH', 'PL', 'UA', 'TW', 'FI',
        'AT', 'BE', 'DK', 'IE', 'PT', 'GR', 'CZ', 'RO', 'BG',
        'HR', 'SK', 'SI', 'EE', 'LV', 'IS', 'LU', 'MT', 'CY',
        'Unknown'
    }

    # اگر شروع با عدد می‌شود، نامعتبر
    if name and name[0].isdigit():
        return False

    # اگر شامل ms یا _ است، نامعتبر
    if 'ms' in name.lower() or '_' in name:
        return False

    # اگر طول بیش از 30 است، نامعتبر
    if len(name) > 30:
        return False

    # اگر کد 2-3 حرفی معتبر است
    if len(name) <= 3 and name.upper() in valid_codes:
        return True

    # اگر نام کامل کشور است
    country_names = {
        'UNITED STATES', 'AMERICA', 'USA', 'GERMANY', 'IRAN',
        'CANADA', 'NETHERLANDS', 'TURKEY', 'SWEDEN', 'INDIA',
        'RUSSIA', 'SPAIN', 'NORWAY', 'LITHUANIA', 'HONG KONG',
        'CHINA', 'UNITED KINGDOM', 'UK', 'FRANCE', 'JAPAN',
        'SINGAPORE', 'AUSTRALIA', 'BRAZIL', 'SOUTH KOREA',
        'ITALY', 'SWITZERLAND', 'POLAND', 'UKRAINE', 'TAIWAN',
        'FINLAND', 'AUSTRIA', 'BELGIUM', 'DENMARK', 'IRELAND'
    }

    if name.upper().replace('_', ' ') in country_names:
        return True

    return False


def cleanup_invalid_files():
    """حذف فایل‌های نامعتبر"""
    country_dir = 'subscriptions/by_country'

    if not os.path.exists(country_dir):
        print(f'❌ پوشه {country_dir} وجود ندارد')
        return

    files = glob.glob(f'{country_dir}/*.txt')

    print(f'🔍 بررسی {len(files)} فایل...\n')

    valid_files = []
    invalid_files = []

    for filepath in files:
        filename = os.path.basename(filepath)

        if is_valid_country_file(filename):
            valid_files.append(filename)
        else:
            invalid_files.append(filepath)

    print(f'✅ فایل‌های معتبر: {len(valid_files)}')
    print(f'❌ فایل‌های نامعتبر: {len(invalid_files)}\n')

    if invalid_files:
        print('🗑️ فایل‌های نامعتبر که حذف می‌شوند:')
        for i, filepath in enumerate(invalid_files[:20], 1):
            filename = os.path.basename(filepath)
            print(f'  {i}. {filename}')

        if len(invalid_files) > 20:
            print(f'  ... و {len(invalid_files) - 20} فایل دیگر')

        response = input(
            f'\n❓ آیا می‌خواهید {len(invalid_files)} فایل نامعتبر را حذف کنید؟ (y/n): ')

        if response.lower() == 'y':
            deleted_count = 0
            for filepath in invalid_files:
                try:
                    os.remove(filepath)
                    deleted_count += 1
                except Exception as e:
                    print(f'❌ خطا در حذف {filepath}: {e}')

            print(f'\n✅ {deleted_count} فایل حذف شد!')
        else:
            print('\n⚠️ عملیات لغو شد')
    else:
        print('✅ هیچ فایل نامعتبری یافت نشد!')

    print(f'\n📊 نتیجه نهایی:')
    print(f'  ✅ فایل‌های معتبر: {len(valid_files)}')
    print(
        f'  ❌ فایل‌های حذف شده: {len(invalid_files) if response.lower() == "y" else 0}')


if __name__ == '__main__':
    cleanup_invalid_files()
