#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V2Ray Config Collector - Starter Script
اسکریپت شروع سریع سیستم جمع‌آوری کانفیگ‌های V2Ray
"""

import sys
import os
import subprocess
import time
import threading
from automation import AutomationManager
from web_server import run_server


def check_dependencies():
    """بررسی وابستگی‌ها"""
    print("🔍 بررسی وابستگی‌ها...")

    try:
        import requests
        import aiohttp
        import flask
        import schedule
        print("✅ تمام وابستگی‌ها نصب شده")
        return True
    except ImportError as e:
        print(f"❌ وابستگی مفقود: {e}")
        print("📦 در حال نصب وابستگی‌ها...")

        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ وابستگی‌ها با موفقیت نصب شد")
            return True
        except subprocess.CalledProcessError:
            print("❌ خطا در نصب وابستگی‌ها")
            return False


def create_directories():
    """ایجاد پوشه‌های ضروری"""
    print("📁 ایجاد پوشه‌های ضروری...")

    directories = ['subscriptions', 'logs']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ پوشه {directory} ایجاد شد")


def run_initial_collection():
    """اجرای جمع‌آوری اولیه"""
    print("🚀 اجرای جمع‌آوری اولیه...")

    automation = AutomationManager()
    automation.run_once()

    print("✅ جمع‌آوری اولیه کامل شد")


def start_web_server():
    """شروع سرور وب"""
    print("🌐 شروع سرور وب...")
    run_server(host='0.0.0.0', port=5000, debug=False)


def start_automation():
    """شروع سیستم اتوماسیون"""
    print("⏰ شروع سیستم اتوماسیون...")
    automation = AutomationManager()
    automation.start_automation()


def main():
    """تابع اصلی"""
    print("=" * 60)
    print("🔒 V2Ray Config Collector & Tester")
    print("سیستم جمع‌آوری، تست و دسته‌بندی کانفیگ‌های رایگان V2Ray")
    print("=" * 60)

    # بررسی وابستگی‌ها
    if not check_dependencies():
        print("❌ لطفاً وابستگی‌ها را به صورت دستی نصب کنید:")
        print("pip install -r requirements.txt")
        return

    # ایجاد پوشه‌ها
    create_directories()

    # جمع‌آوری اولیه
    run_initial_collection()

    print("\n" + "=" * 60)
    print("🎯 انتخاب حالت اجرا:")
    print("1. فقط سرور وب (برای مشاهده نتایج)")
    print("2. فقط اتوماسیون (جمع‌آوری خودکار)")
    print("3. هر دو (پیشنهادی)")
    print("4. خروج")
    print("=" * 60)

    while True:
        try:
            choice = input(
                "\nلطفاً گزینه مورد نظر را انتخاب کنید (1-4): ").strip()

            if choice == '1':
                print("🌐 شروع سرور وب...")
                print("📱 دسترسی از طریق: http://localhost:5000")
                start_web_server()
                break

            elif choice == '2':
                print("⏰ شروع اتوماسیون...")
                start_automation()
                break

            elif choice == '3':
                print("🚀 شروع هر دو سرویس...")

                # شروع اتوماسیون در thread جداگانه
                automation_thread = threading.Thread(
                    target=start_automation, daemon=True)
                automation_thread.start()

                time.sleep(2)  # کمی صبر برای شروع اتوماسیون

                # شروع سرور وب
                start_web_server()
                break

            elif choice == '4':
                print("👋 خداحافظ!")
                break

            else:
                print("❌ گزینه نامعتبر. لطفاً 1، 2، 3 یا 4 وارد کنید.")

        except KeyboardInterrupt:
            print("\n👋 خداحافظ!")
            break
        except Exception as e:
            print(f"❌ خطا: {e}")


if __name__ == "__main__":
    main()
