# Quick Start Script for V2Ray Collector (Windows PowerShell)
# اسکریپت شروع سریع برای ویندوز

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "🚀 V2Ray Collector - Quick Start" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan

# Check Python
Write-Host "`n📋 Checking Python version..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ $pythonVersion found" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "`n📦 Creating virtual environment..." -ForegroundColor Yellow
if (-Not (Test-Path "venv")) {
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✅ Virtual environment already exists" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "`n🔧 Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "`n📥 Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "✅ Dependencies installed" -ForegroundColor Green

# Create directories
Write-Host "`n📁 Creating directories..." -ForegroundColor Yellow
$dirs = @("subscriptions\by_protocol", "subscriptions\by_country", "cache", "logs", "analytics")
foreach ($dir in $dirs) {
    if (-Not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}
Write-Host "✅ Directories created" -ForegroundColor Green

# Create .env file
if (-Not (Test-Path ".env")) {
    Write-Host "`n🔐 Creating .env file..." -ForegroundColor Yellow
    Copy-Item config.env.example .env
    Write-Host "✅ .env file created (please edit with your tokens)" -ForegroundColor Green
}

# Run collection
Write-Host "`n🔄 Starting collection..." -ForegroundColor Yellow
Write-Host "This may take a few minutes...`n" -ForegroundColor Yellow

python config_collector.py

Write-Host "`n✅ Collection completed!" -ForegroundColor Green

# Show results
Write-Host "`n📊 Results:" -ForegroundColor Yellow
if (Test-Path "subscriptions\latest_report.json") {
    $report = Get-Content "subscriptions\latest_report.json" | ConvertFrom-Json
    Write-Host "   Working configs: $($report.working_configs)" -ForegroundColor Green
    Write-Host "   Total tested: $($report.total_configs_tested)" -ForegroundColor Green
    Write-Host "   Success rate: $($report.success_rate)" -ForegroundColor Green
}

# Open browser
Write-Host "`n🌐 Opening web interface..." -ForegroundColor Yellow
Start-Process "subscriptions\index.html"

Write-Host "`n==================================" -ForegroundColor Green
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green

Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Open subscriptions\index.html in browser" -ForegroundColor White
Write-Host "2. Check subscriptions\dashboard.html for analytics" -ForegroundColor White
Write-Host "3. Edit .env to add Telegram bot token (optional)" -ForegroundColor White
Write-Host "4. Run 'python api_endpoints.py' to start API server" -ForegroundColor White
Write-Host "`nFor help: See README.md or docs/`n" -ForegroundColor Yellow

