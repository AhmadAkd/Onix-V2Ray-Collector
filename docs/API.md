# 📡 V2Ray Collector API Documentation

<div align="center">

**REST API Documentation for V2Ray Collector**

Version 2.0.0

</div>

---

## 📑 Table of Contents

- [🚀 Quick Start](#-quick-start)
- [🔐 Authentication](#-authentication)
- [📊 Endpoints](#-endpoints)
- [📝 Examples](#-examples)
- [⚠️ Rate Limits](#️-rate-limits)
- [🐛 Error Handling](#-error-handling)

---

## 🚀 Quick Start

### Start API Server

```bash
# Method 1: Direct
python api_endpoints.py

# Method 2: Uvicorn
uvicorn api_endpoints:app --host 0.0.0.0 --port 8000

# Method 3: Docker
docker-compose up v2ray-api
```

### Base URL

```
http://localhost:8000
```

### Interactive Documentation

```
Swagger UI: http://localhost:8000/api/docs
ReDoc: http://localhost:8000/api/redoc
```

---

## 🔐 Authentication

Currently, the API is **open** and doesn't require authentication.

**Coming Soon**: API Key authentication

```bash
# Future usage
curl -H "X-API-Key: your_api_key_here" \
  http://localhost:8000/api/v1/stats
```

---

## 📊 Endpoints

### 📈 Statistics

#### Get Overall Stats

```http
GET /api/v1/stats
```

**Response:**
```json
{
  "timestamp": "2025-10-14 18:08:56",
  "total_configs": 10583,
  "working_configs": 7449,
  "failed_configs": 3134,
  "success_rate": "70.4%",
  "total_protocols": 5,
  "total_countries": 27
}
```

#### Get Protocol List

```http
GET /api/v1/protocols
```

**Response:**
```json
{
  "vmess": {
    "count": 1617,
    "avg_latency": "64.7ms"
  },
  "vless": {
    "count": 5119,
    "avg_latency": "77.0ms"
  }
}
```

#### Get Protocol Stats

```http
GET /api/v1/protocols/{protocol}
```

**Parameters:**
- `protocol` (path): Protocol name (vmess, vless, trojan, ss, ssr, hysteria)

**Response:**
```json
{
  "protocol": "vless",
  "stats": {
    "count": 5119,
    "avg_latency": "77.0ms"
  },
  "subscription_url": "/subscriptions/by_protocol/vless.txt"
}
```

#### Get Country List

```http
GET /api/v1/countries
```

**Response:**
```json
{
  "US": {
    "count": 2829,
    "avg_latency": "36.9ms"
  },
  "IR": {
    "count": 1179,
    "avg_latency": "85.3ms"
  }
}
```

#### Get Country Stats

```http
GET /api/v1/countries/{country}
```

**Parameters:**
- `country` (path): Country code (US, DE, IR, etc)

**Response:**
```json
{
  "country": "US",
  "stats": {
    "count": 2829,
    "avg_latency": "36.9ms"
  },
  "subscription_url": "/subscriptions/by_country/US.txt"
}
```

---

### 🔧 Config Retrieval

#### Get Configs by Protocol

```http
GET /api/v1/configs/protocol/{protocol}?limit={limit}
```

**Parameters:**
- `protocol` (path): Protocol name
- `limit` (query, optional): Number of configs to return

**Response:** Plain text, one config per line

```
vless://12345@example.com:443?...
vless://67890@example2.com:443?...
```

#### Get Configs by Country

```http
GET /api/v1/configs/country/{country}?limit={limit}
```

**Parameters:**
- `country` (path): Country code
- `limit` (query, optional): Number of configs to return

**Response:** Plain text, one config per line

#### Get All Configs

```http
GET /api/v1/configs/all?limit={limit}
```

**Parameters:**
- `limit` (query, optional): Number of configs to return

**Response:** Plain text, all configs

---

### 🏥 Health & Monitoring

#### Get Health Status

```http
GET /api/v1/health
```

**Response:**
```json
{
  "timestamp": "2025-10-14T18:30:00",
  "is_healthy": true,
  "system": {
    "cpu_usage": "25.5%",
    "memory_usage": "45.2%",
    "disk_usage": "60.1%"
  },
  "sources": {
    "active": 35,
    "failed": 4
  },
  "errors": [],
  "warnings": []
}
```

#### Get Collection History

```http
GET /api/v1/history?hours={hours}
```

**Parameters:**
- `hours` (query, default: 24): Hours of history to retrieve

**Response:**
```json
{
  "history": [
    {
      "timestamp": "2025-10-14 18:00:00",
      "total_configs": 10583,
      "working_configs": 7449,
      "success_rate": 70.4
    }
  ],
  "count": 48
}
```

---

## 📝 Examples

### cURL

```bash
# Get stats
curl http://localhost:8000/api/v1/stats

# Get VLESS configs
curl http://localhost:8000/api/v1/configs/protocol/vless?limit=10

# Get US configs
curl http://localhost:8000/api/v1/configs/country/US?limit=5

# Get health status
curl http://localhost:8000/api/v1/health
```

### Python

```python
import requests

# Get stats
response = requests.get('http://localhost:8000/api/v1/stats')
stats = response.json()
print(f"Working configs: {stats['working_configs']}")

# Get configs
response = requests.get('http://localhost:8000/api/v1/configs/protocol/vless?limit=10')
configs = response.text.split('\n')
print(f"Retrieved {len(configs)} configs")
```

### JavaScript

```javascript
// Get stats
fetch('http://localhost:8000/api/v1/stats')
  .then(response => response.json())
  .then(data => {
    console.log(`Working configs: ${data.working_configs}`);
  });

// Get configs
fetch('http://localhost:8000/api/v1/configs/protocol/vless?limit=10')
  .then(response => response.text())
  .then(configs => {
    const configList = configs.split('\n');
    console.log(`Retrieved ${configList.length} configs`);
  });
```

---

## ⚠️ Rate Limits

Currently: **No rate limiting**

**Coming Soon:**
- 100 requests per hour per IP
- 1000 requests per day per IP
- Configurable limits

---

## 🐛 Error Handling

### HTTP Status Codes

| Code | Description |
|------|-------------|
| `200` | Success |
| `404` | Not Found |
| `429` | Too Many Requests (future) |
| `500` | Internal Server Error |

### Error Response Format

```json
{
  "detail": "Protocol 'invalid' not found"
}
```

---

## 🎯 Response Format

### JSON Responses

All JSON responses include:
- Proper content-type header
- UTF-8 encoding
- Pretty-printed (in development)

### Text Responses

Config endpoints return:
- Plain text
- UTF-8 encoding
- One config per line
- No HTML/JSON wrapper

---

<div align="center">

**[🏠 Back to README](../README.md)** • **[📚 Documentation](README.md)**

</div>
