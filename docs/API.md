# 🚀 V2Ray Collector API Documentation

<div align="center">

![API](https://img.shields.io/badge/API-Documentation-blue?style=for-the-badge)
![REST](https://img.shields.io/badge/REST-API-green?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-Powered-red?style=for-the-badge)

**📡 Complete API Reference for V2Ray Config Collector**

*RESTful API • JSON Responses • Real-time Data • Comprehensive Endpoints*

</div>

---

## 🌐 Base URL

```
https://ahmadakd.github.io/V2Ray_Collector/
```

---

## 📋 Available Endpoints

### 📊 **System Statistics**

#### `GET /api/stats`
**دریافت آمار کلی سیستم**

**Response:**
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "total_configs": 1250,
  "working_configs": 1180,
  "failed_configs": 70,
  "success_rate": 94.4,
  "protocols": {
    "vmess": 450,
    "vless": 320,
    "trojan": 280,
    "ss": 130,
    "ssr": 70
  },
  "countries": {
    "US": 280,
    "DE": 220,
    "JP": 180,
    "SG": 150,
    "UK": 120
  },
  "performance": {
    "avg_latency": 245.5,
    "median_latency": 198.2,
    "cache_hit_rate": 67.3
  }
}
```

---

### 📋 **All Configurations**

#### `GET /api/configs`
**دریافت همه کانفیگ‌های سالم**

**Query Parameters:**
- `protocol` (optional): فیلتر بر اساس پروتکل
- `country` (optional): فیلتر بر اساس کشور
- `limit` (optional): محدود کردن تعداد نتایج (default: 100)

**Example:**
```bash
GET /api/configs?protocol=vmess&country=US&limit=50
```

**Response:**
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "total_count": 1180,
  "filtered_count": 45,
  "configs": [
    {
      "protocol": "vmess",
      "address": "server1.example.com",
      "port": 443,
      "uuid": "12345678-1234-1234-1234-123456789abc",
      "alter_id": 0,
      "network": "tcp",
      "tls": true,
      "latency": 198.5,
      "country": "US",
      "speed_test_result": 85.2
    }
  ]
}
```

---

### 🔗 **Subscription Links**

#### `GET /api/subscription/{protocol}`
**دریافت لینک اشتراک پروتکل خاص**

**Parameters:**
- `protocol`: پروتکل مورد نظر (`vmess`, `vless`, `trojan`, `ss`, `ssr`, `all`)

**Example:**
```bash
GET /api/subscription/vmess
```

**Response:**
```json
{
  "protocol": "vmess",
  "subscription_url": "https://github.com/AhmadAkd/V2Ray_Collector/raw/main/subscriptions/vmess_subscription.txt",
  "count": 450,
  "last_updated": "2024-01-15T10:30:00Z",
  "description": "VMess configurations with TLS support"
}
```

---

### 📈 **Analytics Data**

#### `GET /api/analytics`
**دریافت داده‌های تحلیلی پیشرفته**

**Response:**
```json
{
  "generated_at": "2024-01-15T10:30:00Z",
  "current_performance": {
    "total_configs": 1250,
    "working_configs": 1180,
    "failed_configs": 70,
    "success_rate": 94.4,
    "avg_latency": 245.5,
    "median_latency": 198.2,
    "protocol_distribution": {
      "vmess": 450,
      "vless": 320,
      "trojan": 280,
      "ss": 130,
      "ssr": 70
    },
    "country_distribution": {
      "US": 280,
      "DE": 220,
      "JP": 180,
      "SG": 150,
      "UK": 120
    },
    "latency_distribution": {
      "0-100ms": 120,
      "100-300ms": 680,
      "300-500ms": 280,
      "500-1000ms": 80,
      "1000ms+": 20
    },
    "top_performing_protocols": [
      {
        "protocol": "trojan",
        "count": 280,
        "avg_latency": 189.5,
        "success_rate": 96.8
      }
    ],
    "top_performing_countries": [
      {
        "country": "JP",
        "count": 180,
        "avg_latency": 156.2
      }
    ]
  },
  "trends": {
    "period": "7 days",
    "config_count_trend": "increasing",
    "success_rate_trend": "stable",
    "latency_trend": "decreasing",
    "top_growing_protocols": ["trojan", "vless"],
    "top_declining_protocols": ["ssr"]
  },
  "summary": {
    "overall_status": "excellent",
    "key_insights": [
      "عالی! نرخ موفقیت 94.4% است",
      "تأخیر متوسط 245.5ms عالی است",
      "پروتکل محبوب: vmess با 450 کانفیگ",
      "روند مثبت: تعداد کانفیگ‌ها در حال افزایش است"
    ],
    "recommendations": [
      "افزایش منابع کانفیگ با کیفیت بالا",
      "بهینه‌سازی تست‌های اتصال و فیلتر کردن سرورهای کند"
    ]
  }
}
```

---

### 🏥 **Health Status**

#### `GET /api/health`
**بررسی وضعیت سلامت سیستم**

**Response:**
```json
{
  "overall_status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "components": {
    "github_connectivity": {
      "status": "healthy",
      "message": "GitHub API accessible",
      "response_time": 1250.5,
      "details": {
        "status_code": 200
      }
    },
    "config_sources": {
      "status": "healthy",
      "message": "5/5 sources accessible",
      "response_time": 0,
      "details": {
        "total_sources": 8,
        "accessible": 5,
        "accessibility_rate": "100.0%"
      }
    },
    "disk_space": {
      "status": "healthy",
      "message": "Disk space OK (45.2% free)",
      "response_time": 0,
      "details": {
        "free_gb": 12.5,
        "total_gb": 27.8,
        "free_percent": 45.2
      }
    },
    "memory_usage": {
      "status": "healthy",
      "message": "Memory usage OK (68.3%)",
      "response_time": 0,
      "details": {
        "used_gb": 4.2,
        "total_gb": 6.1,
        "percent": 68.3
      }
    },
    "cache_performance": {
      "status": "healthy",
      "message": "Cache performance good (73.2% hit rate)",
      "response_time": 0,
      "details": {
        "hits": 1250,
        "misses": 450,
        "hit_rate": "73.2%",
        "evictions": 12,
        "size": 850,
        "max_size": 2000,
        "memory_usage_mb": 2.5
      }
    }
  },
  "statistics": {
    "total_checks": 5,
    "healthy": 5,
    "warning": 0,
    "critical": 0
  }
}
```

---

## 🔧 Usage Examples

### 📊 **Get System Statistics**
```bash
curl -X GET "https://ahmadakd.github.io/V2Ray_Collector/api/stats" \
  -H "Accept: application/json"
```

### 🔍 **Filter Configurations**
```bash
curl -X GET "https://ahmadakd.github.io/V2Ray_Collector/api/configs?protocol=vmess&country=US&limit=10" \
  -H "Accept: application/json"
```

### 📈 **Get Analytics**
```bash
curl -X GET "https://ahmadakd.github.io/V2Ray_Collector/api/analytics" \
  -H "Accept: application/json"
```

### 🏥 **Check Health**
```bash
curl -X GET "https://ahmadakd.github.io/V2Ray_Collector/api/health" \
  -H "Accept: application/json"
```

---

## 📋 Response Codes

| Code | Description |
|------|-------------|
| `200` | Success |
| `400` | Bad Request |
| `404` | Not Found |
| `429` | Rate Limited |
| `500` | Internal Server Error |

---

## 🔒 Rate Limiting

- **Default Limit**: 100 requests per minute
- **Burst Limit**: 200 requests per minute
- **Headers**:
  - `X-RateLimit-Limit`: Maximum requests per minute
  - `X-RateLimit-Remaining`: Remaining requests in current window
  - `X-RateLimit-Reset`: Time when rate limit resets

---

## 📝 Error Responses

### 400 Bad Request
```json
{
  "error": "Bad Request",
  "message": "Invalid protocol specified",
  "details": {
    "supported_protocols": ["vmess", "vless", "trojan", "ss", "ssr", "all"]
  }
}
```

### 404 Not Found
```json
{
  "error": "Not Found",
  "message": "Endpoint not found",
  "path": "/api/invalid-endpoint"
}
```

### 429 Rate Limited
```json
{
  "error": "Rate Limited",
  "message": "Too many requests",
  "retry_after": 60
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## 🚀 SDK Examples

### 🐍 **Python**
```python
import requests

# Get system statistics
response = requests.get("https://ahmadakd.github.io/V2Ray_Collector/api/stats")
stats = response.json()

# Get VMess configurations
response = requests.get("https://ahmadakd.github.io/V2Ray_Collector/api/configs?protocol=vmess")
configs = response.json()

# Get analytics
response = requests.get("https://ahmadakd.github.io/V2Ray_Collector/api/analytics")
analytics = response.json()
```

### 🟨 **JavaScript**
```javascript
// Get system statistics
fetch('https://ahmadakd.github.io/V2Ray_Collector/api/stats')
  .then(response => response.json())
  .then(data => console.log(data));

// Get configurations with filters
fetch('https://ahmadakd.github.io/V2Ray_Collector/api/configs?protocol=vmess&limit=10')
  .then(response => response.json())
  .then(data => console.log(data));
```

### 🦀 **Rust**
```rust
use reqwest;
use serde_json::Value;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = reqwest::Client::new();
    
    // Get system statistics
    let response = client
        .get("https://ahmadakd.github.io/V2Ray_Collector/api/stats")
        .send()
        .await?;
    
    let stats: Value = response.json().await?;
    println!("Stats: {}", stats);
    
    Ok(())
}
```

---

## 🔧 Development

### 🏃 **Running Locally**
```bash
# Clone repository
git clone https://github.com/AhmadAkd/V2Ray_Collector.git
cd V2Ray_Collector

# Install dependencies
pip install -r requirements.txt

# Run API server
python api_server.py
```

### 🧪 **Testing**
```bash
# Test all endpoints
python -m pytest tests/test_api.py

# Test specific endpoint
curl http://localhost:8000/api/stats
```

---

## 📞 Support

- **GitHub Issues**: [Report API Issues](https://github.com/AhmadAkd/V2Ray_Collector/issues)
- **Documentation**: [Complete Guide](../README.md)
- **Examples**: [SDK Examples](./examples/)

---

<div align="center">

**⭐ If this API was helpful, please give the project a star! ⭐**

![Made with ❤️](https://img.shields.io/badge/Made%20with-❤️-red?style=for-the-badge)

*Made with ❤️ for the V2Ray community*

</div>
