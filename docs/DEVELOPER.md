# 👨‍💻 V2Ray Collector Developer Guide

<div align="center">

![Developer](https://img.shields.io/badge/Developer-Guide-purple?style=for-the-badge)
![Code](https://img.shields.io/badge/Code-Architecture-blue?style=for-the-badge)
![API](https://img.shields.io/badge/API-Development-green?style=for-the-badge)
![Testing](https://img.shields.io/badge/Testing-Unit%20Tests-orange?style=for-the-badge)

**🔧 Complete Developer Documentation and Contribution Guide**

*Architecture • API Development • Testing • Code Standards • Contributing*

</div>

---

## 🏗️ System Architecture

### 📊 **High-Level Architecture**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │───▶│  V2Ray Collector │───▶│  Output Files   │
│                 │    │                 │    │                 │
│ • GitHub APIs   │    │ • Collection    │    │ • Subscriptions │
│ • Config URLs   │    │ • Testing       │    │ • Reports       │
│ • JSON Sources  │    │ • Analytics     │    │ • Dashboard     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 🔧 **Component Architecture**
```
Onix-V2Ray-Collector/
├── 🔄 Core Engine
│   ├── config_collector.py    # Main collection logic
│   ├── config.py             # Configuration management
│   └── run_tests.py          # Testing framework
│
├── 💾 Data Management
│   ├── cache_manager.py      # Intelligent caching
│   ├── analytics.py          # Advanced analytics
│   └── health_monitor.py     # System monitoring
│
├── 🌐 Interface Layer
│   ├── api_server.py         # REST API
│   ├── web_server.py         # Web interface
│   └── notifications.py      # Notification system
│
├── ⚙️ Automation
│   └── automation.py         # Scheduling and automation
│
└── 📊 Output
    └── subscriptions/        # Generated files
        ├── *.txt            # Subscription files
        ├── *.html           # Web pages
        └── *.json           # Reports and analytics
```

---

## 🧩 Core Components

### 1️⃣ **V2RayCollector Class**
```python
class V2RayCollector:
    """Main collection and testing engine"""
    
    def __init__(self):
        self.configs: List[V2RayConfig] = []
        self.working_configs: List[V2RayConfig] = []
        self.failed_configs: List[V2RayConfig] = []
        self.cache = CacheManager()
        self.analytics = AdvancedAnalytics()
    
    async def collect_all_configs(self) -> List[str]:
        """Collect configurations from all sources"""
        
    async def test_all_configs(self, configs: List[str]):
        """Test all collected configurations"""
        
    def categorize_configs(self) -> Dict[str, List[V2RayConfig]]:
        """Categorize configs by protocol"""
        
    def generate_subscription_links(self, categories: Dict) -> Dict:
        """Generate subscription files"""
```

### 2️⃣ **V2RayConfig Data Class**
```python
@dataclass
class V2RayConfig:
    """Configuration data structure"""
    protocol: str
    address: str
    port: int
    uuid: str
    alter_id: Optional[int] = None
    network: str = "tcp"
    tls: bool = False
    raw_config: str = ""
    latency: float = 0.0
    is_working: bool = False
    country: str = "unknown"
    speed_test_result: float = 0.0
```

### 3️⃣ **CacheManager Class**
```python
class CacheManager:
    """Intelligent caching system"""
    
    def __init__(self, cache_dir: str = "cache", max_size: int = 1000):
        self.memory_cache: Dict[str, CacheEntry] = {}
        self.max_size = max_size
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached data"""
        
    def set(self, key: str, data: Any, ttl: int = 3600):
        """Cache data with TTL"""
        
    def get_or_set(self, key: str, factory_func, ttl: int = 3600):
        """Get from cache or generate and cache"""
```

---

## 🔌 API Development

### 1️⃣ **FastAPI Server Structure**
```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="V2Ray Collector API",
    description="Advanced V2Ray configuration collection and testing API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/stats")
async def get_stats():
    """Get system statistics"""
    
@app.get("/api/configs")
async def get_configs(protocol: str = None, country: str = None, limit: int = 100):
    """Get configurations with optional filters"""
    
@app.get("/api/subscription/{protocol}")
async def get_subscription(protocol: str):
    """Get subscription link for specific protocol"""
```

### 2️⃣ **API Response Models**
```python
from pydantic import BaseModel
from typing import List, Dict, Optional

class ConfigResponse(BaseModel):
    protocol: str
    address: str
    port: int
    uuid: str
    latency: float
    country: str

class StatsResponse(BaseModel):
    total_configs: int
    working_configs: int
    success_rate: float
    protocols: Dict[str, int]
    countries: Dict[str, int]
    performance: Dict[str, float]

class SubscriptionResponse(BaseModel):
    protocol: str
    subscription_url: str
    count: int
    last_updated: str
```

### 3️⃣ **Error Handling**
```python
from fastapi import HTTPException, status

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "Bad Request", "message": str(exc)}
    )

@app.exception_handler(ConnectionError)
async def connection_error_handler(request: Request, exc: ConnectionError):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"error": "Service Unavailable", "message": "Unable to connect to sources"}
    )
```

---

## 🧪 Testing Framework

### 1️⃣ **Unit Tests Structure**
```python
import pytest
import asyncio
from unittest.mock import Mock, patch
from config_collector import V2RayCollector, V2RayConfig

class TestV2RayCollector:
    """Test suite for V2RayCollector"""
    
    @pytest.fixture
    def collector(self):
        """Create collector instance for testing"""
        return V2RayCollector()
    
    @pytest.fixture
    def sample_config(self):
        """Sample configuration for testing"""
        return V2RayConfig(
            protocol="vmess",
            address="test.example.com",
            port=443,
            uuid="12345678-1234-1234-1234-123456789abc"
        )
    
    def test_config_parsing(self, collector):
        """Test configuration parsing"""
        vmess_config = "vmess://eyJ2IjoiMiIsInBzIjoiVGVzdCJ9"
        config = collector.parse_vmess_config(vmess_config)
        assert config is not None
        assert config.protocol == "vmess"
    
    @pytest.mark.asyncio
    async def test_connectivity_testing(self, collector, sample_config):
        """Test connectivity testing"""
        with patch('socket.socket') as mock_socket:
            mock_socket.return_value.connect_ex.return_value = 0
            is_working, latency = await collector.test_config_connectivity(sample_config)
            assert is_working is True
            assert latency > 0
    
    def test_categorization(self, collector):
        """Test configuration categorization"""
        configs = [
            V2RayConfig("vmess", "test1.com", 443, "uuid1"),
            V2RayConfig("vless", "test2.com", 443, "uuid2"),
            V2RayConfig("trojan", "test3.com", 443, "uuid3")
        ]
        categories = collector.categorize_configs()
        assert "vmess" in categories
        assert "vless" in categories
        assert "trojan" in categories
```

### 2️⃣ **Integration Tests**
```python
import pytest
import asyncio
from config_collector import V2RayCollector

class TestIntegration:
    """Integration tests"""
    
    @pytest.mark.asyncio
    async def test_full_collection_cycle(self):
        """Test complete collection cycle"""
        collector = V2RayCollector()
        
        # Collect configurations
        configs = await collector.collect_all_configs()
        assert len(configs) > 0
        
        # Test configurations
        await collector.test_all_configs(configs)
        assert len(collector.working_configs) > 0
        
        # Categorize
        categories = collector.categorize_configs()
        assert len(categories) > 0
        
        # Generate subscription files
        subscription_files = collector.generate_subscription_links(categories)
        assert len(subscription_files) > 0
    
    @pytest.mark.asyncio
    async def test_api_endpoints(self):
        """Test API endpoints"""
        from api_server import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        
        # Test stats endpoint
        response = client.get("/api/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total_configs" in data
        
        # Test configs endpoint
        response = client.get("/api/configs")
        assert response.status_code == 200
        data = response.json()
        assert "configs" in data
```

### 3️⃣ **Performance Tests**
```python
import pytest
import time
import asyncio
from config_collector import V2RayCollector

class TestPerformance:
    """Performance tests"""
    
    @pytest.mark.asyncio
    async def test_collection_performance(self):
        """Test collection performance"""
        collector = V2RayCollector()
        
        start_time = time.time()
        configs = await collector.collect_all_configs()
        collection_time = time.time() - start_time
        
        assert collection_time < 60  # Should complete within 60 seconds
        assert len(configs) > 0
    
    @pytest.mark.asyncio
    async def test_cache_performance(self):
        """Test cache performance"""
        from cache_manager import CacheManager
        
        cache = CacheManager()
        
        # Test cache hit performance
        start_time = time.time()
        for i in range(1000):
            cache.set(f"key_{i}", f"value_{i}")
            cache.get(f"key_{i}")
        cache_time = time.time() - start_time
        
        assert cache_time < 1  # Should complete within 1 second
        
        stats = cache.get_stats()
        assert stats['hit_rate'] == '100.00%'
```

---

## 📋 Code Standards

### 1️⃣ **Python Style Guide**
```python
# Follow PEP 8
# Use type hints
# Document functions and classes
# Use meaningful variable names

def parse_vmess_config(config_str: str) -> Optional[V2RayConfig]:
    """
    Parse VMess configuration string.
    
    Args:
        config_str: Base64 encoded VMess configuration
        
    Returns:
        V2RayConfig object or None if parsing fails
    """
    try:
        # Implementation here
        pass
    except Exception as e:
        logger.error(f"Error parsing VMess config: {e}")
        return None
```

### 2️⃣ **Error Handling**
```python
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def safe_function(param: str) -> Optional[str]:
    """Safe function with proper error handling"""
    try:
        # Main logic
        result = process_data(param)
        return result
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        return None
    except ConnectionError as e:
        logger.error(f"Connection failed: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None
```

### 3️⃣ **Async/Await Patterns**
```python
import asyncio
import aiohttp
from typing import List, Dict

async def fetch_configs_concurrently(urls: List[str]) -> List[str]:
    """Fetch configurations concurrently"""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_single_config(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions
        configs = [result for result in results if not isinstance(result, Exception)]
        return configs

async def fetch_single_config(session: aiohttp.ClientSession, url: str) -> List[str]:
    """Fetch configuration from single URL"""
    try:
        async with session.get(url, timeout=30) as response:
            if response.status == 200:
                content = await response.text()
                return content.strip().split('\n')
    except Exception as e:
        logger.error(f"Error fetching {url}: {e}")
        return []
```

---

## 🔧 Development Setup

### 1️⃣ **Development Environment**
```bash
# Clone repository
git clone https://github.com/AhmadAkd/Onix-V2Ray-Collector.git
cd Onix-V2Ray-Collector

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests
python run_tests.py
```

### 2️⃣ **Development Dependencies**
```txt
# requirements-dev.txt
pytest>=7.0.0
pytest-asyncio>=0.21.0
pytest-cov>=4.0.0
black>=22.0.0
flake8>=5.0.0
mypy>=1.0.0
pre-commit>=2.20.0
```

### 3️⃣ **Pre-commit Configuration**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.12.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.0.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests, types-aiofiles]
```

---

## 🚀 Contributing

### 1️⃣ **Contribution Workflow**
```bash
# Fork repository
git clone https://github.com/YOUR_USERNAME/Onix-V2Ray-Collector.git
cd Onix-V2Ray-Collector

# Create feature branch
git checkout -b feature/new-feature

# Make changes
# Add tests
# Update documentation

# Run tests
python run_tests.py

# Format code
black .
flake8 .

# Commit changes
git add .
git commit -m "feat: add new feature"

# Push to fork
git push origin feature/new-feature

# Create pull request
```

### 2️⃣ **Pull Request Guidelines**
- **Clear title** describing the change
- **Detailed description** of what was changed and why
- **Tests included** for new functionality
- **Documentation updated** if needed
- **Backward compatibility** maintained

### 3️⃣ **Commit Message Format**
```
type(scope): description

feat(api): add new endpoint for analytics
fix(collector): resolve connection timeout issue
docs(readme): update installation instructions
test(cache): add performance tests for cache manager
```

---

## 📊 Performance Optimization

### 1️⃣ **Profiling**
```python
import cProfile
import pstats
from io import StringIO

def profile_function(func, *args, **kwargs):
    """Profile function performance"""
    pr = cProfile.Profile()
    pr.enable()
    
    result = func(*args, **kwargs)
    
    pr.disable()
    s = StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats()
    
    print(s.getvalue())
    return result
```

### 2️⃣ **Memory Profiling**
```python
from memory_profiler import profile

@profile
def memory_intensive_function():
    """Function with memory profiling"""
    # Implementation here
    pass
```

### 3️⃣ **Async Optimization**
```python
import asyncio
from asyncio import Semaphore

async def rate_limited_requests(urls: List[str], max_concurrent: int = 10):
    """Rate-limited concurrent requests"""
    semaphore = Semaphore(max_concurrent)
    
    async def fetch_with_semaphore(session, url):
        async with semaphore:
            return await fetch_single_config(session, url)
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_with_semaphore(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results
```

---

## 🔒 Security Considerations

### 1️⃣ **Input Validation**
```python
import re
from typing import Optional

def validate_config_string(config_str: str) -> bool:
    """Validate configuration string"""
    if not config_str or len(config_str) > 10000:
        return False
    
    # Check for malicious patterns
    malicious_patterns = [
        r'<script',
        r'javascript:',
        r'eval\(',
        r'exec\('
    ]
    
    for pattern in malicious_patterns:
        if re.search(pattern, config_str, re.IGNORECASE):
            return False
    
    return True
```

### 2️⃣ **Rate Limiting**
```python
from collections import defaultdict
import time

class RateLimiter:
    """Simple rate limiter"""
    
    def __init__(self, max_requests: int = 100, window: int = 60):
        self.max_requests = max_requests
        self.window = window
        self.requests = defaultdict(list)
    
    def is_allowed(self, client_id: str) -> bool:
        """Check if request is allowed"""
        now = time.time()
        client_requests = self.requests[client_id]
        
        # Remove old requests
        client_requests[:] = [req_time for req_time in client_requests if now - req_time < self.window]
        
        if len(client_requests) >= self.max_requests:
            return False
        
        client_requests.append(now)
        return True
```

---

## 📞 Support & Resources

### 💬 **Developer Support**
- **GitHub Issues**: [Technical Issues](https://github.com/AhmadAkd/Onix-V2Ray-Collector/issues)
- **Discussions**: [Developer Discussions](https://github.com/AhmadAkd/Onix-V2Ray-Collector/discussions)
- **Documentation**: [Complete Guide](../README.md)

### 📚 **Additional Resources**
- [Python Async/Await Guide](https://docs.python.org/3/library/asyncio.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pytest Documentation](https://docs.pytest.org/)
- [aiohttp Documentation](https://docs.aiohttp.org/)

---

<div align="center">

**⭐ If this guide was helpful, please give the project a star! ⭐**

![Made with ❤️](https://img.shields.io/badge/Made%20with-❤️-red?style=for-the-badge)

*Made with ❤️ for the V2Ray community*

</div>
