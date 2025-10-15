# 🚀 V2Ray Collector Installation Guide

<div align="center">

![Installation](https://img.shields.io/badge/Installation-Guide-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-Supported-blue?style=for-the-badge)
![GitHub](https://img.shields.io/badge/GitHub-Actions-orange?style=for-the-badge)

**📋 Complete Installation and Setup Guide**

*Multiple Installation Methods • Step-by-Step Instructions • Troubleshooting*

</div>

---

## 📋 Prerequisites

### 🖥️ **System Requirements**
- **OS**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **Python**: 3.8 or higher
- **Memory**: Minimum 2GB RAM
- **Disk Space**: At least 1GB free space
- **Network**: Stable internet connection

### 🔧 **Required Software**
- **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
- **Git**: [Download Git](https://git-scm.com/downloads)
- **pip**: Usually comes with Python

---

## 🚀 Installation Methods

### 1️⃣ **Quick Installation (Recommended)**

#### **Step 1: Clone Repository**
```bash
git clone https://github.com/AhmadAkd/Onix-V2Ray-Collector.git
cd Onix-V2Ray-Collector
```

#### **Step 2: Install Dependencies**
```bash
# Install Python dependencies
pip install -r requirements.txt

# Or using pip3
pip3 install -r requirements.txt
```

#### **Step 3: Run System**
```bash
# Quick start
python config_collector.py

# Or with automation
python automation.py --mode auto
```

---

### 2️⃣ **Manual Installation**

#### **Step 1: Create Project Directory**
```bash
mkdir v2ray-collector
cd v2ray-collector
```

#### **Step 2: Clone Repository**
```bash
git clone https://github.com/AhmadAkd/Onix-V2Ray-Collector.git .
```

#### **Step 3: Install Python Dependencies**
```bash
# Install core dependencies
pip install requests aiohttp pyyaml schedule psutil flask

# Install optional dependencies
pip install fastapi uvicorn

# Install development dependencies
pip install pytest black flake8
```

#### **Step 4: Verify Installation**
```bash
python run_tests.py
```

---

### 3️⃣ **Docker Installation**

#### **Step 1: Create Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p subscriptions logs cache analytics

# Run tests
RUN python run_tests.py

# Expose port
EXPOSE 8000

# Start application
CMD ["python", "api_server.py"]
```

#### **Step 2: Build and Run**
```bash
# Build Docker image
docker build -t v2ray-collector .

# Run container
docker run -d -p 8000:8000 --name v2ray-collector v2ray-collector

# Check logs
docker logs v2ray-collector
```

---

### 4️⃣ **Virtual Environment Installation**

#### **Step 1: Create Virtual Environment**
```bash
# Create virtual environment
python -m venv v2ray-env

# Activate virtual environment
# Windows
v2ray-env\Scripts\activate

# macOS/Linux
source v2ray-env/bin/activate
```

#### **Step 2: Install Dependencies**
```bash
pip install -r requirements.txt
```

#### **Step 3: Run System**
```bash
python config_collector.py
```

---

## ⚙️ Configuration

### 📝 **Environment Variables**
Create `.env` file:
```bash
# Cache settings
CACHE_MAX_SIZE=2000
CACHE_TTL=1800

# Health check settings
HEALTH_CHECK_TIMEOUT=10
DISK_THRESHOLD=20

# Analytics settings
ANALYTICS_HISTORY_DAYS=30
ANALYTICS_TREND_PERIOD=7

# API settings
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=false
```

### 🔧 **Config File**
Edit `config.py`:
```python
# Collection settings
COLLECTION_CONFIG = {
    'timeout': 30,
    'max_retries': 3,
    'concurrent_requests': 10,
    'test_timeout': 10
}

# Cache settings
CACHE_CONFIG = {
    'max_size': 2000,
    'ttl': 1800,  # 30 minutes
    'persistence': True,
    'cache_dir': 'cache'
}

# Health monitoring
HEALTH_CONFIG = {
    'github_timeout': 10,
    'source_timeout': 5,
    'disk_threshold': 20,
    'memory_threshold': 90
}
```

---

## 🚀 Running the System

### 1️⃣ **One-time Execution**
```bash
python config_collector.py
```

### 2️⃣ **Automated System**
```bash
# Run every 30 minutes
python automation.py --mode auto

# Run with custom interval
python automation.py --mode auto --interval 15

# Run once
python automation.py --mode once
```

### 3️⃣ **API Server**
```bash
# Run on default port (8000)
python api_server.py

# Run with custom settings
python api_server.py --host 0.0.0.0 --port 8080

# Run with debug mode
python api_server.py --debug
```

### 4️⃣ **Web Interface**
```bash
# Start web server
python web_server.py

# Access at http://localhost:5000
```

---

## 🔧 Advanced Setup

### 📊 **Analytics Setup**
```bash
# Enable analytics
export ENABLE_ANALYTICS=true

# Set analytics directory
export ANALYTICS_DIR=analytics

# Run with analytics
python config_collector.py
```

### 💾 **Cache Configuration**
```bash
# Configure cache
export CACHE_MAX_SIZE=5000
export CACHE_TTL=3600

# Clear cache
python -c "from cache_manager import CacheManager; CacheManager().clear()"
```

### 🏥 **Health Monitoring**
```bash
# Run health checks
python health_monitor.py

# Check specific component
python -c "from health_monitor import HealthMonitor; import asyncio; asyncio.run(HealthMonitor().run_health_checks())"
```

---

## 🧪 Testing Installation

### 1️⃣ **Run Test Suite**
```bash
python run_tests.py
```

### 2️⃣ **Test Individual Components**
```bash
# Test config collector
python -c "from config_collector import V2RayCollector; print('Config collector OK')"

# Test cache manager
python -c "from cache_manager import CacheManager; print('Cache manager OK')"

# Test health monitor
python -c "from health_monitor import HealthMonitor; print('Health monitor OK')"

# Test analytics
python -c "from analytics import AdvancedAnalytics; print('Analytics OK')"
```

### 3️⃣ **Test API Endpoints**
```bash
# Start API server
python api_server.py &

# Test endpoints
curl http://localhost:8000/api/stats
curl http://localhost:8000/api/health
curl http://localhost:8000/api/configs
```

---

## 🔍 Verification

### ✅ **Check Installation**
```bash
# Check Python version
python --version

# Check installed packages
pip list | grep -E "(requests|aiohttp|flask)"

# Check project structure
ls -la

# Verify configuration
python -c "from config import *; print('Config OK')"
```

### 📊 **Expected Output**
```
✅ Python version: 3.11.x
✅ Required packages installed
✅ Project files present
✅ Configuration loaded
✅ All tests passing
```

---

## 🛠️ Troubleshooting

### ❌ **Common Issues**

#### **Python Version Error**
```bash
# Error: Python 3.8+ required
# Solution: Update Python
python --version  # Check version
# Download latest Python from python.org
```

#### **Package Installation Failed**
```bash
# Error: pip install failed
# Solution: Update pip and try again
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### **Permission Denied**
```bash
# Error: Permission denied
# Solution: Use --user flag or sudo
pip install --user -r requirements.txt
# Or on Linux/macOS
sudo pip install -r requirements.txt
```

#### **Network Connection Issues**
```bash
# Error: Connection timeout
# Solution: Check internet connection
ping github.com
# Use proxy if needed
pip install --proxy http://proxy:port -r requirements.txt
```

### 🔧 **Debug Mode**
```bash
# Enable debug logging
export DEBUG=true
python config_collector.py

# Verbose output
python -v config_collector.py
```

---

## 📋 Post-Installation

### 1️⃣ **Create Startup Script**
```bash
# Windows (start.bat)
@echo off
cd /d "C:\path\to\Onix-V2Ray-Collector"
python automation.py --mode auto

# macOS/Linux (start.sh)
#!/bin/bash
cd /path/to/Onix-V2Ray-Collector
python automation.py --mode auto
```

### 2️⃣ **Setup System Service**
```bash
# Create systemd service (Linux)
sudo nano /etc/systemd/system/v2ray-collector.service

[Unit]
Description=V2Ray Config Collector
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/Onix-V2Ray-Collector
ExecStart=/usr/bin/python3 automation.py --mode auto
Restart=always

[Install]
WantedBy=multi-user.target

# Enable and start service
sudo systemctl enable v2ray-collector
sudo systemctl start v2ray-collector
```

### 3️⃣ **Setup Cron Job**
```bash
# Add to crontab
crontab -e

# Run every 30 minutes
*/30 * * * * cd /path/to/Onix-V2Ray-Collector && python config_collector.py
```

---

## 🚀 Next Steps

### 📚 **Read Documentation**
- [API Documentation](./API.md)
- [User Guide](./USER_GUIDE.md)
- [Troubleshooting](./TROUBLESHOOTING.md)
- [Developer Guide](./DEVELOPER.md)

### 🔗 **Access Services**
- **Web Interface**: http://localhost:5000
- **API Server**: http://localhost:8000
- **Dashboard**: http://localhost:5000/dashboard

### 📊 **Monitor System**
```bash
# Check logs
tail -f v2ray_collector.log

# Monitor health
python health_monitor.py

# View analytics
python -c "from analytics import AdvancedAnalytics; print(AdvancedAnalytics().get_stats())"
```

---

## 📞 Support

### 💬 **Get Help**
- **GitHub Issues**: [Report Installation Issues](https://github.com/AhmadAkd/Onix-V2Ray-Collector/issues)
- **Documentation**: [Complete Guide](../README.md)
- **Community**: [Discussions](https://github.com/AhmadAkd/Onix-V2Ray-Collector/discussions)

### 🔧 **Common Commands**
```bash
# Quick start
python start.py

# Run tests
python run_tests.py

# Check status
python -c "from health_monitor import HealthMonitor; import asyncio; asyncio.run(HealthMonitor().run_health_checks())"

# Clear cache
python -c "from cache_manager import CacheManager; CacheManager().clear()"
```

---

<div align="center">

**⭐ If this guide was helpful, please give the project a star! ⭐**

![Made with ❤️](https://img.shields.io/badge/Made%20with-❤️-red?style=for-the-badge)

*Made with ❤️ for the V2Ray community*

</div>
