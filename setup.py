#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V2Ray Config Collector - Setup Script
نصب و راه‌اندازی سیستم جمع‌آوری کانفیگ‌های V2Ray
"""

from setuptools import setup, find_packages
import os

# خواندن محتوای README
def read_readme():
    with open("README_EN.md", "r", encoding="utf-8") as fh:
        return fh.read()

# خواندن محتوای requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="onix-v2ray-collector",
    version="2.1.0",
    author="AhmadAkd",
    author_email="your-email@example.com",
    description="Automated V2Ray Configuration Collection, Testing & Categorization System",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/AhmadAkd/Onix-V2Ray-Collector",
    project_urls={
        "Bug Reports": "https://github.com/AhmadAkd/Onix-V2Ray-Collector/issues",
        "Source": "https://github.com/AhmadAkd/Onix-V2Ray-Collector",
        "Documentation": "https://github.com/AhmadAkd/Onix-V2Ray-Collector#readme",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: System :: Networking",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Natural Language :: Persian",
        "Natural Language :: English",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "web": [
            "flask>=2.3.0",
            "gunicorn>=20.0",
        ],
        "monitoring": [
            "psutil>=5.8.0",
            "prometheus-client>=0.12.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "onix-collector=config_collector:main",
            "onix-automation=automation:main",
            "onix-api=api_server:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml"],
    },
    keywords=[
        "v2ray", "vmess", "vless", "trojan", "shadowsocks", 
        "vpn", "proxy", "config", "collector", "automation",
        "persian", "iran", "bypass", "gfw", "network"
    ],
    zip_safe=False,
    platforms=["any"],
    license="MIT",
)
