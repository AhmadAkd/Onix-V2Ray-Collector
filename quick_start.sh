#!/bin/bash
# Quick Start Script for V2Ray Collector
# اسکریپت شروع سریع

set -e

echo "=================================="
echo "🚀 V2Ray Collector - Quick Start"
echo "=================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python version
echo -e "\n${YELLOW}📋 Checking Python version...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found. Please install Python 3.8+${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✅ Python $PYTHON_VERSION found${NC}"

# Create virtual environment
echo -e "\n${YELLOW}📦 Creating virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${GREEN}✅ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "\n${YELLOW}🔧 Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "\n${YELLOW}📥 Installing dependencies...${NC}"
pip install -r requirements.txt --quiet
echo -e "${GREEN}✅ Dependencies installed${NC}"

# Create necessary directories
echo -e "\n${YELLOW}📁 Creating directories...${NC}"
mkdir -p subscriptions/by_protocol
mkdir -p subscriptions/by_country
mkdir -p cache
mkdir -p logs
mkdir -p analytics
echo -e "${GREEN}✅ Directories created${NC}"

# Create .env file if not exists
if [ ! -f ".env" ]; then
    echo -e "\n${YELLOW}🔐 Creating .env file...${NC}"
    cp config.env.example .env
    echo -e "${GREEN}✅ .env file created (please edit with your tokens)${NC}"
fi

# Run collection
echo -e "\n${YELLOW}🔄 Starting collection...${NC}"
echo -e "${YELLOW}This may take a few minutes...${NC}\n"

python3 config_collector.py

echo -e "\n${GREEN}✅ Collection completed!${NC}"

# Show results
echo -e "\n${YELLOW}📊 Results:${NC}"
if [ -f "subscriptions/latest_report.json" ]; then
    WORKING=$(cat subscriptions/latest_report.json | grep -o '"working_configs": [0-9]*' | grep -o '[0-9]*')
    TOTAL=$(cat subscriptions/latest_report.json | grep -o '"total_configs_tested": [0-9]*' | grep -o '[0-9]*')
    echo -e "${GREEN}   Working configs: $WORKING${NC}"
    echo -e "${GREEN}   Total tested: $TOTAL${NC}"
fi

# Open browser
echo -e "\n${YELLOW}🌐 Opening web interface...${NC}"
if command -v xdg-open &> /dev/null; then
    xdg-open subscriptions/index.html
elif command -v open &> /dev/null; then
    open subscriptions/index.html
else
    echo -e "${YELLOW}   Please open: subscriptions/index.html${NC}"
fi

echo -e "\n${GREEN}=================================="
echo -e "✅ Setup Complete!"
echo -e "==================================${NC}"
echo -e "\n${YELLOW}Next steps:${NC}"
echo -e "1. Open ${GREEN}subscriptions/index.html${NC} in browser"
echo -e "2. Check ${GREEN}subscriptions/dashboard.html${NC} for analytics"
echo -e "3. Edit ${GREEN}.env${NC} to add Telegram bot token (optional)"
echo -e "4. Run ${GREEN}python api_endpoints.py${NC} to start API server"
echo -e "\n${YELLOW}For help:${NC} See README.md or docs/"
echo ""

