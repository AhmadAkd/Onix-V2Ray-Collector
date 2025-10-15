# 👤 V2Ray Collector User Guide

<div align="center">

![User Guide](https://img.shields.io/badge/User-Guide-green?style=for-the-badge)
![Easy](https://img.shields.io/badge/Easy-to-Use-blue?style=for-the-badge)
![Complete](https://img.shields.io/badge/Complete-Guide-purple?style=for-the-badge)

**📖 Complete User Guide for V2Ray Config Collector**

*Step-by-Step Instructions • Usage Examples • Best Practices • Tips & Tricks*

</div>

---

## 🎯 Getting Started

### 📋 **What is V2Ray Collector?**
V2Ray Collector is an advanced system that automatically collects, tests, and categorizes free V2Ray configurations from multiple sources. It provides you with high-quality, tested configurations ready for use.

### ✨ **Key Benefits**
- **🔄 Automatic Updates**: Configurations are updated every 30 minutes
- **✅ Quality Testing**: Only working configurations are provided
- **📊 Smart Categorization**: Organized by protocol type
- **🌐 Multiple Formats**: Support for all major V2Ray clients
- **📈 Performance Analytics**: Real-time statistics and insights

---

## 🚀 Quick Start

### 1️⃣ **Access Subscription Links**
Visit the main page: [https://ahmadakd.github.io/Onix-V2Ray-Collector/subscriptions/](https://ahmadakd.github.io/Onix-V2Ray-Collector/subscriptions/)

### 2️⃣ **Choose Your Protocol**
Select the subscription link for your preferred protocol:
- **VMess**: Most common, good compatibility
- **VLESS**: Newer protocol, better performance
- **Trojan**: High security, good for China
- **Shadowsocks**: Simple and reliable
- **ShadowsocksR**: Enhanced Shadowsocks

### 3️⃣ **Add to Your Client**
Copy the subscription URL and add it to your V2Ray client:
- **v2rayN** (Windows)
- **v2rayNG** (Android)
- **V2RayU** (macOS)
- **Qv2ray** (Cross-platform)

---

## 📱 Using with Different Clients

### 🖥️ **Windows - v2rayN**

#### Step 1: Download and Install
1. Download v2rayN from [GitHub](https://github.com/2dust/v2rayN)
2. Extract and run `v2rayN.exe`
3. Right-click the system tray icon

#### Step 2: Add Subscription
1. Click **"订阅"** → **"订阅设置"**
2. Click **"添加"**
3. Enter subscription URL:
   ```
   https://github.com/AhmadAkd/Onix-V2Ray-Collector/raw/main/subscriptions/all_subscription.txt
   ```
4. Click **"确定"**

#### Step 3: Update Configurations
1. Click **"订阅"** → **"更新订阅"**
2. Wait for update to complete
3. Select a server and click **"设为活动服务器"**

### 📱 **Android - v2rayNG**

#### Step 1: Install v2rayNG
1. Download from [Google Play](https://play.google.com/store/apps/details?id=com.v2ray.ang) or [GitHub](https://github.com/2dust/v2rayNG)
2. Open the app and grant necessary permissions

#### Step 2: Add Subscription
1. Tap the **"+"** button
2. Select **"订阅设置"**
3. Tap **"+"** to add new subscription
4. Enter subscription URL and a name
5. Tap **"确定"**

#### Step 3: Update and Connect
1. Tap **"订阅"** → **"更新订阅"**
2. Select a server from the list
3. Tap the **"V"** button to connect

### 🍎 **macOS - V2RayU**

#### Step 1: Install V2RayU
1. Download from [GitHub](https://github.com/yanue/V2rayU)
2. Install using Homebrew: `brew install v2rayu`

#### Step 2: Add Subscription
1. Open V2RayU
2. Go to **"服务器"** → **"订阅设置"**
3. Click **"+"** to add subscription
4. Enter URL and name
5. Click **"确定"**

#### Step 3: Connect
1. Click **"更新订阅"**
2. Select a server
3. Click **"设为活动"**

---

## 🌐 Using Web Interface

### 📊 **Dashboard Access**
Visit: [https://ahmadakd.github.io/Onix-V2Ray-Collector/subscriptions/dashboard.html](https://ahmadakd.github.io/Onix-V2Ray-Collector/subscriptions/dashboard.html)

### 📈 **Viewing Statistics**
The dashboard shows:
- **Total Configurations**: Number of available configs
- **Success Rate**: Percentage of working configurations
- **Protocol Distribution**: Breakdown by protocol type
- **Country Distribution**: Geographic distribution
- **Performance Metrics**: Average latency and speed

### 🔍 **Filtering Options**
Use the dashboard to:
- Filter by protocol type
- Filter by country
- Sort by latency
- View detailed server information

---

## 📡 API Usage

### 🔍 **Get System Statistics**
```bash
curl https://ahmadakd.github.io/Onix-V2Ray-Collector/api/stats
```

**Response:**
```json
{
  "total_configs": 1250,
  "working_configs": 1180,
  "success_rate": 94.4,
  "protocols": {
    "vmess": 450,
    "vless": 320,
    "trojan": 280
  }
}
```

### 📋 **Get Configurations**
```bash
# Get all configurations
curl https://ahmadakd.github.io/Onix-V2Ray-Collector/api/configs

# Filter by protocol
curl "https://ahmadakd.github.io/Onix-V2Ray-Collector/api/configs?protocol=vmess"

# Filter by country
curl "https://ahmadakd.github.io/Onix-V2Ray-Collector/api/configs?country=US"

# Limit results
curl "https://ahmadakd.github.io/Onix-V2Ray-Collector/api/configs?limit=50"
```

### 🔗 **Get Subscription Links**
```bash
# VMess subscription
curl https://ahmadakd.github.io/Onix-V2Ray-Collector/api/subscription/vmess

# VLESS subscription
curl https://ahmadakd.github.io/Onix-V2Ray-Collector/api/subscription/vless

# All protocols
curl https://ahmadakd.github.io/Onix-V2Ray-Collector/api/subscription/all
```

---

## 🎯 Best Practices

### ✅ **Recommended Settings**

#### **Protocol Selection**
- **VMess**: Best for general use, good compatibility
- **VLESS**: Better performance, newer protocol
- **Trojan**: Best for bypassing deep packet inspection
- **Shadowsocks**: Simple and reliable
- **ShadowsocksR**: Enhanced security

#### **Server Selection**
- **Low Latency**: Choose servers with <200ms latency
- **High Success Rate**: Prefer servers with >95% success rate
- **Geographic Proximity**: Choose servers closer to your location
- **Stable Performance**: Look for consistent speed test results

### 🔧 **Client Configuration**

#### **v2rayN Settings**
```
路由设置:
- 绕过大陆: 勾选
- 绕过局域网: 勾选

DNS设置:
- DNS服务器: 8.8.8.8, 1.1.1.1

代理设置:
- HTTP代理: 127.0.0.1:10809
- SOCKS代理: 127.0.0.1:10808
```

#### **v2rayNG Settings**
```
路由设置:
- 绕过中国大陆: 开启
- 绕过局域网: 开启

DNS设置:
- DNS: 8.8.8.8

分应用代理:
- 根据需要选择应用
```

### 📊 **Performance Optimization**

#### **Connection Settings**
- **Timeout**: 10-15 seconds
- **Retry**: 2-3 attempts
- **Concurrent**: 5-10 connections
- **Buffer**: 1-2 MB

#### **Network Settings**
- **MTU**: 1500 (default)
- **TCP Fast Open**: Enable if supported
- **UDP**: Enable for better performance

---

## 🔍 Troubleshooting

### ❌ **Common Issues**

#### **Cannot Connect**
1. **Check Internet**: Ensure stable internet connection
2. **Update Configurations**: Refresh subscription
3. **Try Different Server**: Switch to another server
4. **Check Firewall**: Disable firewall temporarily

#### **Slow Speed**
1. **Choose Closer Server**: Select geographically closer server
2. **Check Server Load**: Avoid overloaded servers
3. **Optimize Settings**: Adjust connection parameters
4. **Try Different Protocol**: Switch between VMess/VLESS

#### **Connection Drops**
1. **Check Server Status**: Verify server is working
2. **Update Configurations**: Refresh subscription
3. **Restart Client**: Close and reopen client
4. **Check Network**: Ensure stable connection

### 🔧 **Diagnostic Commands**

#### **Test Connectivity**
```bash
# Test basic connectivity
ping 8.8.8.8

# Test DNS resolution
nslookup google.com

# Test specific server
telnet server.example.com 443
```

#### **Check Client Logs**
- **v2rayN**: Check log window in the application
- **v2rayNG**: Go to Settings → Log → View Log
- **V2RayU**: Check Console window

---

## 📊 Understanding Statistics

### 📈 **Dashboard Metrics**

#### **Success Rate**
- **95%+**: Excellent quality
- **90-95%**: Good quality
- **80-90%**: Average quality
- **<80%**: Poor quality

#### **Latency**
- **<100ms**: Excellent speed
- **100-200ms**: Good speed
- **200-500ms**: Average speed
- **>500ms**: Slow speed

#### **Protocol Distribution**
Shows the number of configurations available for each protocol type.

#### **Country Distribution**
Shows geographic distribution of servers.

### 📊 **Performance Indicators**

#### **Green Indicators** ✅
- High success rate (>95%)
- Low latency (<200ms)
- Recent update time
- Good speed test results

#### **Yellow Indicators** ⚠️
- Medium success rate (80-95%)
- Medium latency (200-500ms)
- Older update time
- Average speed test results

#### **Red Indicators** ❌
- Low success rate (<80%)
- High latency (>500ms)
- Very old update time
- Poor speed test results

---

## 🔄 Keeping Configurations Updated

### ⏰ **Automatic Updates**
- Configurations are automatically updated every 30 minutes
- No manual intervention required
- Always use the latest subscription links

### 🔄 **Manual Updates**
- **v2rayN**: Right-click → 订阅 → 更新订阅
- **v2rayNG**: Tap 订阅 → 更新订阅
- **V2RayU**: Click 更新订阅

### 📅 **Update Schedule**
- **Every 30 minutes**: New configurations collected
- **Every 5 minutes**: Server health checked
- **Every hour**: Performance analytics updated
- **Daily**: Historical data archived

---

## 🎛️ Advanced Usage

### 🔧 **Custom Filters**
Use API parameters to customize your experience:

```bash
# Get only US servers
curl "https://ahmadakd.github.io/Onix-V2Ray-Collector/api/configs?country=US"

# Get only fast servers (low latency)
curl "https://ahmadakd.github.io/Onix-V2Ray-Collector/api/configs?max_latency=200"

# Get only VMess with TLS
curl "https://ahmadakd.github.io/Onix-V2Ray-Collector/api/configs?protocol=vmess&tls=true"
```

### 📊 **Monitoring**
Set up monitoring for your configurations:

```bash
# Check system health
curl https://ahmadakd.github.io/Onix-V2Ray-Collector/api/health

# Get analytics
curl https://ahmadakd.github.io/Onix-V2Ray-Collector/api/analytics

# Monitor performance
watch -n 60 'curl -s https://ahmadakd.github.io/Onix-V2Ray-Collector/api/stats | jq .success_rate'
```

### 🔗 **Integration**
Integrate with other tools:

```python
import requests

# Get configurations programmatically
response = requests.get('https://ahmadakd.github.io/Onix-V2Ray-Collector/api/configs')
configs = response.json()

# Filter and use configurations
fast_configs = [c for c in configs['configs'] if c['latency'] < 200]
```

---

## 📞 Support & Help

### 💬 **Getting Help**
- **GitHub Issues**: [Report Problems](https://github.com/AhmadAkd/Onix-V2Ray-Collector/issues)
- **Documentation**: [Complete Guide](../README.md)
- **API Reference**: [API Documentation](./API.md)

### 🔧 **Useful Resources**
- **V2Ray Documentation**: [V2Ray User Guide](https://www.v2ray.com/en/)
- **Client Downloads**: [Official Clients](https://github.com/v2ray/v2ray-core)
- **Configuration Examples**: [V2Ray Examples](https://github.com/v2ray/v2ray-examples)

### 📋 **Quick Commands**
```bash
# Check system status
curl -s https://ahmadakd.github.io/Onix-V2Ray-Collector/api/stats | jq .

# Get subscription URL
curl -s https://ahmadakd.github.io/Onix-V2Ray-Collector/api/subscription/vmess | jq .subscription_url

# Check health
curl -s https://ahmadakd.github.io/Onix-V2Ray-Collector/api/health | jq .overall_status
```

---

## 🎯 Tips & Tricks

### 💡 **Pro Tips**
1. **Use Multiple Protocols**: Combine VMess and VLESS for better reliability
2. **Geographic Selection**: Choose servers in countries with good internet freedom
3. **Regular Updates**: Always keep your configurations updated
4. **Monitor Performance**: Use analytics to find the best servers
5. **Backup Configurations**: Save working configurations locally

### 🚀 **Performance Tips**
1. **Choose Closer Servers**: Lower latency = better performance
2. **Use Fast Protocols**: VLESS generally performs better than VMess
3. **Optimize Settings**: Adjust timeout and retry settings
4. **Monitor Usage**: Track which servers work best for you
5. **Update Regularly**: New configurations are often better

### 🔒 **Security Tips**
1. **Use TLS**: Always prefer TLS-enabled configurations
2. **Verify Sources**: Only use trusted subscription sources
3. **Regular Updates**: Keep configurations updated for security
4. **Monitor Logs**: Check for any unusual activity
5. **Use Strong Authentication**: Prefer configurations with strong encryption

---

<div align="center">

**⭐ If this guide was helpful, please give the project a star! ⭐**

![Made with ❤️](https://img.shields.io/badge/Made%20with-❤️-red?style=for-the-badge)

*Made with ❤️ for the V2Ray community*

</div>
