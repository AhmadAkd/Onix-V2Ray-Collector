# 🔧 V2Ray Collector Troubleshooting Guide

<div align="center">

![Troubleshooting](https://img.shields.io/badge/Troubleshooting-Guide-red?style=for-the-badge)
![Issues](https://img.shields.io/badge/Issues-Solved-green?style=for-the-badge)
![Support](https://img.shields.io/badge/Support-24/7-blue?style=for-the-badge)

**🛠️ Complete Troubleshooting and Problem Solving Guide**

*Common Issues • Solutions • Debug Methods • Performance Optimization*

</div>

---

## 🚨 Quick Diagnostics

### ⚡ **Emergency Checklist**
```bash
# Quick system check
python run_tests.py

# Check system health
python health_monitor.py

# Verify installation
python -c "import sys; print(f'Python: {sys.version}')"
python -c "import requests, aiohttp, flask; print('Dependencies OK')"

# Check network connectivity
ping github.com
curl -I https://github.com
```

---

## 🔍 Common Issues & Solutions

### 1️⃣ **Installation Issues**

#### ❌ **Python Version Error**
```bash
# Error: Python 3.8+ required
python --version
# Output: Python 3.7.x
```

**✅ Solution:**
```bash
# Update Python
# Windows: Download from python.org
# macOS: brew install python@3.11
# Ubuntu: sudo apt update && sudo apt install python3.11

# Verify installation
python3.11 --version
```

#### ❌ **Package Installation Failed**
```bash
# Error: pip install failed
ERROR: Could not find a version that satisfies the requirement aiohttp
```

**✅ Solution:**
```bash
# Update pip
python -m pip install --upgrade pip

# Install with specific version
pip install aiohttp==3.8.0

# Use alternative index
pip install -i https://pypi.org/simple/ -r requirements.txt

# Install with --no-cache
pip install --no-cache-dir -r requirements.txt
```

#### ❌ **Permission Denied**
```bash
# Error: Permission denied
ERROR: Could not install packages due to an EnvironmentError: [Errno 13] Permission denied
```

**✅ Solution:**
```bash
# Use --user flag
pip install --user -r requirements.txt

# Or use virtual environment
python -m venv v2ray-env
source v2ray-env/bin/activate  # Linux/macOS
v2ray-env\Scripts\activate     # Windows
pip install -r requirements.txt
```

---

### 2️⃣ **Network Issues**

#### ❌ **Connection Timeout**
```bash
# Error: Connection timeout
aiohttp.ClientTimeout: Timeout connecting to 'github.com'
```

**✅ Solution:**
```bash
# Check network connectivity
ping github.com
nslookup github.com

# Use proxy if needed
export https_proxy=http://proxy:port
export http_proxy=http://proxy:port

# Increase timeout in config
# Edit config.py
COLLECTION_CONFIG = {
    'timeout': 60,  # Increase from 30 to 60
    'max_retries': 5
}
```

#### ❌ **SSL Certificate Error**
```bash
# Error: SSL certificate verification failed
SSL: CERTIFICATE_VERIFY_FAILED
```

**✅ Solution:**
```bash
# Update certificates
# macOS
/Applications/Python\ 3.11/Install\ Certificates.command

# Linux
sudo apt-get install ca-certificates

# Temporary workaround (not recommended for production)
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```

#### ❌ **DNS Resolution Error**
```bash
# Error: Name resolution failed
aiohttp.ClientConnectorError: Cannot connect to host github.com
```

**✅ Solution:**
```bash
# Check DNS settings
nslookup github.com

# Use alternative DNS
# Windows: Change DNS to 8.8.8.8, 8.8.4.4
# Linux: Edit /etc/resolv.conf
nameserver 8.8.8.8
nameserver 8.8.4.4

# Flush DNS cache
# Windows
ipconfig /flushdns

# Linux
sudo systemctl restart systemd-resolved
```

---

### 3️⃣ **Runtime Issues**

#### ❌ **Import Error**
```bash
# Error: Module not found
ModuleNotFoundError: No module named 'cache_manager'
```

**✅ Solution:**
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Add current directory to path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or run from project directory
cd /path/to/Onix-V2Ray-Collector
python config_collector.py
```

#### ❌ **Memory Error**
```bash
# Error: Out of memory
MemoryError: Unable to allocate array
```

**✅ Solution:**
```bash
# Check memory usage
python -c "import psutil; print(f'Memory: {psutil.virtual_memory().percent}%')"

# Reduce cache size
# Edit config.py
CACHE_CONFIG = {
    'max_size': 500,  # Reduce from 2000
    'ttl': 900        # Reduce from 1800
}

# Clear cache
python -c "from cache_manager import CacheManager; CacheManager().clear()"
```

#### ❌ **Disk Space Error**
```bash
# Error: No space left on device
OSError: [Errno 28] No space left on device
```

**✅ Solution:**
```bash
# Check disk space
df -h

# Clean up old files
rm -rf cache/*
rm -rf logs/*.log.old
rm -rf analytics/historical_data.json.bak

# Reduce log retention
# Edit logging configuration
```

---

### 4️⃣ **Performance Issues**

#### ❌ **Slow Collection**
```bash
# Issue: Collection takes too long
# Normal: 2-5 minutes
# Slow: 10+ minutes
```

**✅ Solution:**
```bash
# Check network speed
speedtest-cli

# Reduce concurrent requests
# Edit config.py
COLLECTION_CONFIG = {
    'concurrent_requests': 5,  # Reduce from 10
    'timeout': 15              # Reduce from 30
}

# Use cache
python -c "from cache_manager import CacheManager; print(CacheManager().get_stats())"
```

#### ❌ **High CPU Usage**
```bash
# Issue: High CPU usage during testing
# Normal: 10-30%
# High: 80%+
```

**✅ Solution:**
```bash
# Check CPU usage
top -p $(pgrep -f config_collector)

# Reduce test concurrency
# Edit config.py
TEST_CONFIG = {
    'concurrent_tests': 5,  # Reduce from 10
    'test_timeout': 5       # Reduce from 10
}

# Use less aggressive testing
```

#### ❌ **Cache Performance**
```bash
# Issue: Low cache hit rate
# Good: 70%+
# Poor: <30%
```

**✅ Solution:**
```bash
# Check cache stats
python -c "from cache_manager import CacheManager; print(CacheManager().get_stats())"

# Increase cache TTL
CACHE_CONFIG = {
    'ttl': 3600,  # Increase from 1800
    'max_size': 5000
}

# Clear and rebuild cache
python -c "from cache_manager import CacheManager; CacheManager().clear()"
```

---

### 5️⃣ **API Issues**

#### ❌ **API Server Won't Start**
```bash
# Error: Port already in use
OSError: [Errno 98] Address already in use
```

**✅ Solution:**
```bash
# Find process using port
lsof -i :8000  # Linux/macOS
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>

# Or use different port
python api_server.py --port 8080
```

#### ❌ **API Response Error**
```bash
# Error: API returns 500
{"error": "Internal Server Error", "message": "Database connection failed"}
```

**✅ Solution:**
```bash
# Check API logs
tail -f api_server.log

# Test API endpoints
curl -v http://localhost:8000/api/stats
curl -v http://localhost:8000/api/health

# Restart API server
pkill -f api_server
python api_server.py
```

---

## 🔧 Debug Methods

### 1️⃣ **Enable Debug Logging**
```python
# Edit config.py
DEBUG = True
LOG_LEVEL = 'DEBUG'

# Or set environment variable
export DEBUG=true
export LOG_LEVEL=DEBUG
```

### 2️⃣ **Verbose Output**
```bash
# Run with verbose output
python -v config_collector.py

# Enable debug mode
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from config_collector import V2RayCollector
collector = V2RayCollector()
"
```

### 3️⃣ **Step-by-Step Debugging**
```bash
# Test individual components
python -c "from config_collector import V2RayCollector; print('Collector OK')"
python -c "from cache_manager import CacheManager; print('Cache OK')"
python -c "from health_monitor import HealthMonitor; print('Health OK')"
python -c "from analytics import AdvancedAnalytics; print('Analytics OK')"
```

### 4️⃣ **Network Debugging**
```bash
# Test network connectivity
curl -v https://github.com
curl -v https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt

# Check DNS
nslookup github.com
dig github.com

# Test with different user agent
curl -H "User-Agent: Mozilla/5.0" https://github.com
```

---

## 📊 Performance Optimization

### 1️⃣ **System Optimization**
```bash
# Increase file limits
ulimit -n 65536

# Optimize Python
export PYTHONOPTIMIZE=1
export PYTHONUNBUFFERED=1

# Use faster DNS
echo "nameserver 8.8.8.8" > /etc/resolv.conf
```

### 2️⃣ **Cache Optimization**
```python
# Optimize cache settings
CACHE_CONFIG = {
    'max_size': 10000,      # Increase cache size
    'ttl': 7200,            # Increase TTL to 2 hours
    'persistence': True,    # Enable disk persistence
    'compression': True     # Enable compression
}
```

### 3️⃣ **Network Optimization**
```python
# Optimize network settings
COLLECTION_CONFIG = {
    'timeout': 20,           # Reduce timeout
    'max_retries': 2,        # Reduce retries
    'concurrent_requests': 15, # Increase concurrency
    'keepalive': True,       # Enable keep-alive
    'connection_pool': 100   # Increase pool size
}
```

---

## 🧪 Testing & Validation

### 1️⃣ **Run Test Suite**
```bash
# Run all tests
python run_tests.py

# Run specific tests
python -m pytest tests/test_config_collector.py
python -m pytest tests/test_api.py -v
```

### 2️⃣ **Performance Testing**
```bash
# Test collection performance
time python config_collector.py

# Test API performance
ab -n 1000 -c 10 http://localhost:8000/api/stats

# Test memory usage
python -m memory_profiler config_collector.py
```

### 3️⃣ **Health Check**
```bash
# Run health checks
python health_monitor.py

# Check specific components
python -c "
from health_monitor import HealthMonitor
import asyncio
asyncio.run(HealthMonitor().run_health_checks())
"
```

---

## 📋 Error Codes Reference

| Code | Error | Solution |
|------|-------|----------|
| `101` | Connection timeout | Check network, increase timeout |
| `102` | SSL certificate error | Update certificates |
| `103` | DNS resolution failed | Check DNS settings |
| `201` | Import error | Check Python path, install dependencies |
| `202` | Memory error | Reduce cache size, check memory |
| `203` | Disk space error | Free up disk space |
| `301` | API server error | Check port, restart server |
| `302` | Database error | Check database connection |
| `401` | Permission denied | Check file permissions |
| `402` | Authentication failed | Check credentials |

---

## 📞 Getting Help

### 💬 **Support Channels**
- **GitHub Issues**: [Create Issue](https://github.com/AhmadAkd/Onix-V2Ray-Collector/issues)
- **Discussions**: [Community Help](https://github.com/AhmadAkd/Onix-V2Ray-Collector/discussions)
- **Documentation**: [Complete Guide](../README.md)

### 📝 **Reporting Issues**
When reporting issues, include:
1. **Error message** (full traceback)
2. **System information** (OS, Python version)
3. **Steps to reproduce**
4. **Log files** (if available)
5. **Configuration** (anonymized)

### 🔧 **Quick Commands**
```bash
# System information
python -c "import sys, platform; print(f'Python: {sys.version}, OS: {platform.system()}')"

# Dependency check
pip list | grep -E "(requests|aiohttp|flask)"

# Network test
curl -I https://github.com

# Quick health check
python health_monitor.py
```

---

## 🎯 Prevention Tips

### ✅ **Best Practices**
1. **Keep Python updated** (3.8+)
2. **Use virtual environments**
3. **Regular system maintenance**
4. **Monitor disk space**
5. **Backup configurations**
6. **Update dependencies regularly**

### ⚠️ **Common Pitfalls**
1. **Running as root** (security risk)
2. **Ignoring error logs**
3. **Not backing up data**
4. **Using outdated dependencies**
5. **Not monitoring system resources**

---

<div align="center">

**⭐ If this guide helped you, please give the project a star! ⭐**

![Made with ❤️](https://img.shields.io/badge/Made%20with-❤️-red?style=for-the-badge)

*Made with ❤️ for the V2Ray community*

</div>
