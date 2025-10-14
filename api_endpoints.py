#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
REST API Endpoints for V2Ray Collector
API های RESTful برای دسترسی به کانفیگ‌ها و آمار
"""

from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from typing import List, Dict, Optional
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="V2Ray Collector API",
    description="REST API for V2Ray Config Collection System",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper functions
def load_latest_report() -> Dict:
    """بارگذاری آخرین گزارش"""
    try:
        with open('subscriptions/latest_report.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading report: {e}")
        return {}

def load_subscription_file(filename: str) -> List[str]:
    """بارگذاری فایل subscription"""
    try:
        with open(f'subscriptions/{filename}', 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        logger.error(f"Error loading {filename}: {e}")
        return []

# API Endpoints

@app.get("/")
async def root():
    """صفحه اصلی API"""
    return {
        "name": "V2Ray Collector API",
        "version": "2.0.0",
        "status": "operational",
        "endpoints": {
            "stats": "/api/v1/stats",
            "protocols": "/api/v1/protocols",
            "countries": "/api/v1/countries",
            "configs": "/api/v1/configs",
            "health": "/api/v1/health"
        },
        "documentation": "/api/docs"
    }

@app.get("/api/v1/stats")
async def get_stats():
    """
    دریافت آمار کلی
    
    Returns:
        آمار کلی سیستم
    """
    report = load_latest_report()
    
    if not report:
        raise HTTPException(status_code=404, detail="No data available")
    
    return {
        "timestamp": report.get('timestamp'),
        "total_configs": report.get('total_configs_tested', 0),
        "working_configs": report.get('working_configs', 0),
        "failed_configs": report.get('failed_configs', 0),
        "success_rate": report.get('success_rate', '0%'),
        "total_protocols": len(report.get('protocols', {})),
        "total_countries": len(report.get('countries', {}))
    }

@app.get("/api/v1/protocols")
async def get_protocols():
    """
    دریافت لیست پروتکل‌ها
    
    Returns:
        لیست پروتکل‌ها با آمار
    """
    report = load_latest_report()
    return report.get('protocols', {})

@app.get("/api/v1/protocols/{protocol}")
async def get_protocol_stats(
    protocol: str = Path(..., description="Protocol name (vmess, vless, trojan, etc)")
):
    """
    دریافت آمار یک پروتکل خاص
    
    Args:
        protocol: نام پروتکل
        
    Returns:
        آمار پروتکل
    """
    report = load_latest_report()
    protocols = report.get('protocols', {})
    
    if protocol not in protocols:
        raise HTTPException(status_code=404, detail=f"Protocol '{protocol}' not found")
    
    return {
        "protocol": protocol,
        "stats": protocols[protocol],
        "subscription_url": f"/subscriptions/by_protocol/{protocol}.txt"
    }

@app.get("/api/v1/countries")
async def get_countries():
    """
    دریافت لیست کشورها
    
    Returns:
        لیست کشورها با آمار
    """
    report = load_latest_report()
    return report.get('countries', {})

@app.get("/api/v1/countries/{country}")
async def get_country_stats(
    country: str = Path(..., description="Country code (US, DE, IR, etc)")
):
    """
    دریافت آمار یک کشور خاص
    
    Args:
        country: کد کشور
        
    Returns:
        آمار کشور
    """
    report = load_latest_report()
    countries = report.get('countries', {})
    
    if country not in countries:
        raise HTTPException(status_code=404, detail=f"Country '{country}' not found")
    
    return {
        "country": country,
        "stats": countries[country],
        "subscription_url": f"/subscriptions/by_country/{country}.txt"
    }

@app.get("/api/v1/configs/protocol/{protocol}", response_class=PlainTextResponse)
async def get_configs_by_protocol(
    protocol: str = Path(..., description="Protocol name"),
    limit: Optional[int] = Query(None, description="Limit number of configs")
):
    """
    دریافت کانفیگ‌های یک پروتکل
    
    Args:
        protocol: نام پروتکل
        limit: محدودیت تعداد
        
    Returns:
        لیست کانفیگ‌ها (plain text)
    """
    configs = load_subscription_file(f'by_protocol/{protocol}.txt')
    
    if not configs:
        raise HTTPException(status_code=404, detail=f"No configs found for '{protocol}'")
    
    if limit:
        configs = configs[:limit]
    
    return '\n'.join(configs)

@app.get("/api/v1/configs/country/{country}", response_class=PlainTextResponse)
async def get_configs_by_country(
    country: str = Path(..., description="Country code"),
    limit: Optional[int] = Query(None, description="Limit number of configs")
):
    """
    دریافت کانفیگ‌های یک کشور
    
    Args:
        country: کد کشور
        limit: محدودیت تعداد
        
    Returns:
        لیست کانفیگ‌ها (plain text)
    """
    configs = load_subscription_file(f'by_country/{country}.txt')
    
    if not configs:
        raise HTTPException(status_code=404, detail=f"No configs found for '{country}'")
    
    if limit:
        configs = configs[:limit]
    
    return '\n'.join(configs)

@app.get("/api/v1/configs/all", response_class=PlainTextResponse)
async def get_all_configs(
    limit: Optional[int] = Query(None, description="Limit number of configs")
):
    """
    دریافت تمام کانفیگ‌ها
    
    Args:
        limit: محدودیت تعداد
        
    Returns:
        لیست تمام کانفیگ‌ها
    """
    configs = load_subscription_file('all_subscription.txt')
    
    if not configs:
        raise HTTPException(status_code=404, detail="No configs available")
    
    if limit:
        configs = configs[:limit]
    
    return '\n'.join(configs)

@app.get("/api/v1/health")
async def get_health():
    """
    دریافت وضعیت سلامت سیستم
    
    Returns:
        وضعیت سلامت
    """
    try:
        with open('health_report.json', 'r', encoding='utf-8') as f:
            health = json.load(f)
        return health
    except:
        return {
            "status": "unknown",
            "message": "Health report not available"
        }

@app.get("/api/v1/history")
async def get_history(hours: int = Query(24, description="Hours of history")):
    """
    دریافت تاریخچه
    
    Args:
        hours: تعداد ساعات گذشته
        
    Returns:
        تاریخچه جمع‌آوری
    """
    try:
        from database_manager import DatabaseManager
        db = DatabaseManager()
        history = db.get_history(hours=hours)
        return {"history": history, "count": len(history)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching history: {str(e)}")

# Run server
if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting API Server...")
    print("📡 API Docs: http://localhost:8000/api/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)

