#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V2Ray Collector API Server
سرور API برای V2Ray Collector
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, Query, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel
import uvicorn

from config_collector import V2RayCollector
from notifications import NotificationManager, DEFAULT_NOTIFICATION_CONFIG
from config import API_CONFIG, SECURITY_CONFIG

# تنظیم لاگ‌گیری
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="V2Ray Collector API",
    description="API برای دسترسی به کانفیگ‌های V2Ray",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global collector instance
collector = None
notification_manager = None

# Pydantic models


class ConfigResponse(BaseModel):
    protocol: str
    address: str
    port: int
    country: Optional[str] = None
    latency: Optional[float] = None
    raw_config: str


class StatsResponse(BaseModel):
    total_configs: int
    healthy_configs: int
    failed_configs: int
    success_rate: float
    last_update: str
    sources_checked: int


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    uptime: str
    version: str


# Rate limiting storage
request_counts = {}
rate_limit_window = 3600  # 1 hour


def check_rate_limit(client_ip: str) -> bool:
    """بررسی محدودیت نرخ درخواست"""
    if not SECURITY_CONFIG.get('enable_rate_limiting', True):
        return True

    current_time = datetime.now().timestamp()
    max_requests = SECURITY_CONFIG.get('max_requests_per_hour', 1000)

    # پاک‌سازی درخواست‌های قدیمی
    if client_ip in request_counts:
        request_counts[client_ip] = [
            req_time for req_time in request_counts[client_ip]
            if current_time - req_time < rate_limit_window
        ]
    else:
        request_counts[client_ip] = []

    # بررسی محدودیت
    if len(request_counts[client_ip]) >= max_requests:
        return False

    # ثبت درخواست جدید
    request_counts[client_ip].append(current_time)
    return True


def get_client_ip(request):
    """دریافت IP کلاینت"""
    return request.client.host


@app.on_event("startup")
async def startup_event():
    """شروع سرور"""
    global collector, notification_manager
    logger.info("🚀 شروع V2Ray Collector API Server...")

    # ایجاد collector
    collector = V2RayCollector()

    # ایجاد notification manager
    notification_manager = NotificationManager(DEFAULT_NOTIFICATION_CONFIG)

    logger.info("✅ سرور API آماده است")


@app.on_event("shutdown")
async def shutdown_event():
    """خاموش کردن سرور"""
    logger.info("🛑 خاموش کردن سرور API...")


@app.get("/", response_class=PlainTextResponse)
async def root():
    """صفحه اصلی"""
    return """
V2Ray Collector API Server
=========================

📡 API endpoints:
- GET /health - وضعیت سیستم
- GET /stats - آمار کلی
- GET /configs - همه کانفیگ‌ها
- GET /configs/{protocol} - کانفیگ‌های پروتکل خاص
- GET /subscription/{protocol} - لینک اشتراک
- GET /countries - لیست کشورها
- GET /sources - منابع کانفیگ

📚 Documentation:
- /docs - Swagger UI
- /redoc - ReDoc

🔗 Repository: https://github.com/AhmadAkd/V2Ray_Collector
"""


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """بررسی سلامت سیستم"""
    uptime = "Unknown"  # TODO: محاسبه uptime

    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        uptime=uptime,
        version="1.0.0"
    )


@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    """دریافت آمار کلی"""
    try:
        # بارگذاری آخرین گزارش
        try:
            with open('subscriptions/latest_report.json', 'r', encoding='utf-8') as f:
                report = json.load(f)
        except FileNotFoundError:
            # گزارش اولیه
            report = {
                'working_configs': [],
                'failed_configs': [],
                'sources_checked': 0,
                'success_rate': 0,
                'timestamp': datetime.now().isoformat()
            }

        total_configs = len(report.get('working_configs', [])) + \
            len(report.get('failed_configs', []))
        healthy_configs = len(report.get('working_configs', []))
        failed_configs = len(report.get('failed_configs', []))
        success_rate = report.get('success_rate', 0)
        sources_checked = report.get('sources_checked', 0)
        last_update = report.get('timestamp', datetime.now().isoformat())

        return StatsResponse(
            total_configs=total_configs,
            healthy_configs=healthy_configs,
            failed_configs=failed_configs,
            success_rate=success_rate,
            last_update=last_update,
            sources_checked=sources_checked
        )

    except Exception as e:
        logger.error(f"خطا در دریافت آمار: {e}")
        raise HTTPException(status_code=500, detail="خطا در دریافت آمار")


@app.get("/configs", response_model=List[ConfigResponse])
async def get_all_configs(
    limit: int = Query(100, ge=1, le=1000, description="حداکثر تعداد کانفیگ"),
    protocol: Optional[str] = Query(None, description="فیلتر پروتکل"),
    country: Optional[str] = Query(None, description="فیلتر کشور"),
    min_latency: Optional[float] = Query(
        None, ge=0, description="حداقل تأخیر (ms)")
):
    """دریافت همه کانفیگ‌ها"""
    try:
        # بارگذاری کانفیگ‌های سالم
        try:
            with open('subscriptions/latest_report.json', 'r', encoding='utf-8') as f:
                report = json.load(f)
            configs = report.get('working_configs', [])
        except FileNotFoundError:
            configs = []

        # اعمال فیلترها
        filtered_configs = []
        for config_data in configs:
            if protocol and config_data.get('protocol') != protocol:
                continue
            if country and config_data.get('country') != country:
                continue
            if min_latency and config_data.get('latency', 0) < min_latency:
                continue

            filtered_configs.append(ConfigResponse(**config_data))

        # محدودیت تعداد
        return filtered_configs[:limit]

    except Exception as e:
        logger.error(f"خطا در دریافت کانفیگ‌ها: {e}")
        raise HTTPException(status_code=500, detail="خطا در دریافت کانفیگ‌ها")


@app.get("/configs/{protocol}", response_model=List[ConfigResponse])
async def get_configs_by_protocol(
    protocol: str,
    limit: int = Query(100, ge=1, le=500),
    country: Optional[str] = Query(None)
):
    """دریافت کانفیگ‌های پروتکل خاص"""
    if protocol not in ['vmess', 'vless', 'trojan', 'ss', 'ssr']:
        raise HTTPException(status_code=400, detail="پروتکل نامعتبر")

    return await get_all_configs(limit=limit, protocol=protocol, country=country)


@app.get("/subscription/{protocol}")
async def get_subscription(
    protocol: str,
    request: Request
):
    """دریافت لینک اشتراک"""
    # بررسی rate limit
    client_ip = get_client_ip(request)
    if not check_rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="محدودیت نرخ درخواست")

    if protocol not in ['vmess', 'vless', 'trojan', 'ss', 'ssr', 'all']:
        raise HTTPException(status_code=400, detail="پروتکل نامعتبر")

    try:
        # بارگذاری فایل اشتراک
        filename = f"subscriptions/{protocol}_subscription.txt"
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()

            return PlainTextResponse(
                content=content,
                media_type="text/plain",
                headers={
                    "Content-Disposition": f"attachment; filename={protocol}_subscription.txt"
                }
            )
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="فایل اشتراک یافت نشد")

    except Exception as e:
        logger.error(f"خطا در دریافت اشتراک: {e}")
        raise HTTPException(status_code=500, detail="خطا در دریافت اشتراک")


@app.get("/countries")
async def get_countries():
    """دریافت لیست کشورها"""
    try:
        with open('subscriptions/latest_report.json', 'r', encoding='utf-8') as f:
            report = json.load(f)

        countries = set()
        for config in report.get('working_configs', []):
            country = config.get('country', 'unknown')
            countries.add(country)

        return {"countries": sorted(list(countries))}

    except Exception as e:
        logger.error(f"خطا در دریافت لیست کشورها: {e}")
        raise HTTPException(
            status_code=500, detail="خطا در دریافت لیست کشورها")


@app.get("/sources")
async def get_sources():
    """دریافت منابع کانفیگ"""
    from config import CONFIG_SOURCES

    return {
        "sources": CONFIG_SOURCES,
        "total_sources": len(CONFIG_SOURCES)
    }


@app.post("/webhook/test")
async def test_webhook(request: Request):
    """تست webhook"""
    try:
        body = await request.json()
        logger.info(f"Webhook test received: {body}")

        return {"status": "success", "message": "Webhook test successful"}

    except Exception as e:
        logger.error(f"Webhook test error: {e}")
        raise HTTPException(status_code=500, detail="خطا در تست webhook")


@app.get("/dashboard")
async def get_dashboard_data():
    """دریافت داده‌های dashboard"""
    try:
        with open('subscriptions/latest_report.json', 'r', encoding='utf-8') as f:
            report = json.load(f)

        # آمار پروتکل‌ها
        protocol_stats = {}
        for config in report.get('working_configs', []):
            protocol = config.get('protocol', 'unknown')
            protocol_stats[protocol] = protocol_stats.get(protocol, 0) + 1

        # آمار کشورها
        country_stats = {}
        for config in report.get('working_configs', []):
            country = config.get('country', 'unknown')
            country_stats[country] = country_stats.get(country, 0) + 1

        return {
            "report": report,
            "protocol_stats": protocol_stats,
            "country_stats": country_stats
        }

    except Exception as e:
        logger.error(f"خطا در دریافت داده‌های dashboard: {e}")
        raise HTTPException(
            status_code=500, detail="خطا در دریافت داده‌های dashboard")

# Error handlers


@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "منبع یافت نشد"}
    )


@app.exception_handler(429)
async def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "محدودیت نرخ درخواست - لطفاً بعداً تلاش کنید"}
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "خطای داخلی سرور"}
    )

if __name__ == "__main__":
    # تنظیمات سرور
    host = API_CONFIG.get('host', '0.0.0.0')
    port = API_CONFIG.get('port', 8000)
    debug = API_CONFIG.get('debug', False)

    logger.info(f"🚀 شروع سرور API روی {host}:{port}")

    uvicorn.run(
        "api_server:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )
