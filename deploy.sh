#!/bin/bash

# V2Ray Config Collector - Deployment Script
# اسکریپت استقرار سیستم جمع‌آوری کانفیگ‌های V2Ray

set -e

echo "🚀 شروع استقرار V2Ray Config Collector"
echo "========================================"

# رنگ‌ها برای خروجی
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# توابع کمکی
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# بررسی Python
check_python() {
    log_info "بررسی نسخه Python..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        log_success "Python $PYTHON_VERSION یافت شد"
        
        if python3 -c 'import sys; exit(0 if sys.version_info >= (3, 8) else 1)'; then
            log_success "نسخه Python مناسب است"
        else
            log_error "نیاز به Python 3.8 یا بالاتر"
            exit 1
        fi
    else
        log_error "Python نصب نشده است"
        exit 1
    fi
}

# بررسی pip
check_pip() {
    log_info "بررسی pip..."
    
    if command -v pip3 &> /dev/null; then
        log_success "pip یافت شد"
    else
        log_error "pip نصب نشده است"
        exit 1
    fi
}

# نصب وابستگی‌ها
install_dependencies() {
    log_info "نصب وابستگی‌ها..."
    
    if [ -f "requirements.txt" ]; then
        pip3 install -r requirements.txt
        log_success "وابستگی‌ها نصب شدند"
    else
        log_error "فایل requirements.txt یافت نشد"
        exit 1
    fi
}

# ایجاد پوشه‌های ضروری
create_directories() {
    log_info "ایجاد پوشه‌های ضروری..."
    
    mkdir -p subscriptions logs backups
    
    log_success "پوشه‌ها ایجاد شدند"
}

# اجرای تست‌ها
run_tests() {
    log_info "اجرای تست‌ها..."
    
    if [ -f "run_tests.py" ]; then
        python3 run_tests.py
        if [ $? -eq 0 ]; then
            log_success "تمام تست‌ها موفق بودند"
        else
            log_warning "برخی تست‌ها ناموفق بودند"
        fi
    else
        log_warning "فایل تست یافت نشد"
    fi
}

# تنظیم مجوزها
set_permissions() {
    log_info "تنظیم مجوزها..."
    
    chmod +x *.py
    chmod +x deploy.sh
    
    log_success "مجوزها تنظیم شدند"
}

# ایجاد سرویس systemd
create_systemd_service() {
    log_info "ایجاد سرویس systemd..."
    
    if [ "$EUID" -eq 0 ]; then
        cat > /etc/systemd/system/v2ray-collector.service << EOF
[Unit]
Description=V2Ray Config Collector
After=network.target

[Service]
Type=simple
User=$SUDO_USER
WorkingDirectory=$(pwd)
ExecStart=/usr/bin/python3 automation.py --mode auto
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
        
        systemctl daemon-reload
        systemctl enable v2ray-collector
        log_success "سرویس systemd ایجاد شد"
    else
        log_warning "برای ایجاد سرویس systemd نیاز به دسترسی root است"
    fi
}

# ایجاد cron job
create_cron_job() {
    log_info "ایجاد cron job..."
    
    CRON_JOB="*/30 * * * * cd $(pwd) && python3 automation.py --mode once"
    
    # بررسی وجود cron job
    if crontab -l 2>/dev/null | grep -q "v2ray-collector"; then
        log_warning "cron job قبلاً موجود است"
    else
        (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
        log_success "cron job ایجاد شد"
    fi
}

# تنظیم فایروال
setup_firewall() {
    log_info "تنظیم فایروال..."
    
    if command -v ufw &> /dev/null; then
        if [ "$EUID" -eq 0 ]; then
            ufw allow 5000/tcp
            log_success "فایروال تنظیم شد"
        else
            log_warning "برای تنظیم فایروال نیاز به دسترسی root است"
        fi
    else
        log_warning "ufw نصب نشده است"
    fi
}

# ایجاد فایل‌های SSL
create_ssl_certificates() {
    log_info "ایجاد گواهی‌های SSL..."
    
    if [ ! -d "ssl" ]; then
        mkdir -p ssl
        
        # ایجاد self-signed certificate
        openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes -subj "/C=IR/ST=Tehran/L=Tehran/O=V2Ray Collector/OU=IT/CN=localhost"
        
        log_success "گواهی‌های SSL ایجاد شدند"
    else
        log_warning "پوشه ssl قبلاً موجود است"
    fi
}

# راه‌اندازی Docker
setup_docker() {
    log_info "راه‌اندازی Docker..."
    
    if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
        if [ -f "docker-compose.yml" ]; then
            docker-compose build
            log_success "Docker image ساخته شد"
        else
            log_warning "فایل docker-compose.yml یافت نشد"
        fi
    else
        log_warning "Docker نصب نشده است"
    fi
}

# نمایش وضعیت
show_status() {
    log_info "وضعیت سرویس‌ها:"
    
    # بررسی systemd service
    if systemctl is-active --quiet v2ray-collector 2>/dev/null; then
        log_success "سرویس systemd فعال است"
    else
        log_warning "سرویس systemd غیرفعال است"
    fi
    
    # بررسی cron jobs
    if crontab -l 2>/dev/null | grep -q "v2ray-collector"; then
        log_success "cron job فعال است"
    else
        log_warning "cron job غیرفعال است"
    fi
    
    # بررسی فایل‌های ضروری
    if [ -d "subscriptions" ] && [ -d "logs" ]; then
        log_success "فایل‌های ضروری موجود هستند"
    else
        log_warning "برخی فایل‌های ضروری مفقود هستند"
    fi
}

# راهنمای استفاده
show_usage() {
    echo "راهنمای استفاده:"
    echo "  ./deploy.sh [option]"
    echo ""
    echo "گزینه‌ها:"
    echo "  --full      استقرار کامل (پیش‌فرض)"
    echo "  --docker    فقط Docker"
    echo "  --service   فقط systemd service"
    echo "  --cron      فقط cron job"
    echo "  --ssl       فقط SSL certificates"
    echo "  --status    نمایش وضعیت"
    echo "  --help      نمایش این راهنما"
}

# تابع اصلی
main() {
    case "${1:-full}" in
        --full)
            log_info "استقرار کامل شروع می‌شود..."
            check_python
            check_pip
            install_dependencies
            create_directories
            set_permissions
            run_tests
            create_systemd_service
            create_cron_job
            setup_firewall
            create_ssl_certificates
            setup_docker
            show_status
            log_success "استقرار کامل انجام شد!"
            ;;
        --docker)
            setup_docker
            ;;
        --service)
            create_systemd_service
            ;;
        --cron)
            create_cron_job
            ;;
        --ssl)
            create_ssl_certificates
            ;;
        --status)
            show_status
            ;;
        --help)
            show_usage
            ;;
        *)
            log_error "گزینه نامعتبر: $1"
            show_usage
            exit 1
            ;;
    esac
}

# اجرای اسکریپت
main "$@"
