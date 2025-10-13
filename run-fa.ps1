# V2Ray Collector - Windows PowerShell Runner (Persian)
# اسکریپت اجرای سریع برای ویندوز

# تنظیم encoding به UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

param(
    [string]$Action = "menu"
)

function Show-Menu {
    Clear-Host
    Write-Host "======================================================" -ForegroundColor Cyan
    Write-Host "   V2Ray Collector - نسخه ویندوز" -ForegroundColor Cyan  
    Write-Host "======================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  [1] نصب وابستگی‌ها" -ForegroundColor Yellow
    Write-Host "  [2] اجرای تست‌ها" -ForegroundColor Yellow
    Write-Host "  [3] جمع‌آوری کانفیگ‌ها (یکبار)" -ForegroundColor Yellow
    Write-Host "  [4] اتوماسیون (هر 30 دقیقه)" -ForegroundColor Yellow
    Write-Host "  [5] اجرای API Server" -ForegroundColor Yellow
    Write-Host "  [6] مشاهده لاگ‌ها" -ForegroundColor Yellow
    Write-Host "  [7] پاکسازی Cache" -ForegroundColor Yellow
    Write-Host "  [8] نمایش اطلاعات سیستم" -ForegroundColor Yellow
    Write-Host "  [9] دستورات Docker" -ForegroundColor Yellow
    Write-Host "  [0] خروج" -ForegroundColor Red
    Write-Host ""
}

function Install-Dependencies {
    Write-Host "در حال نصب وابستگی‌ها..." -ForegroundColor Green
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    Write-Host "نصب با موفقیت انجام شد!" -ForegroundColor Green
    pause
}

function Run-Tests {
    Write-Host "در حال اجرای تست‌ها..." -ForegroundColor Green
    python run_tests.py
    pause
}

function Collect-Configs {
    Write-Host "در حال جمع‌آوری کانفیگ‌ها..." -ForegroundColor Green
    python config_collector.py
    pause
}

function Start-Automation {
    Write-Host "اتوماسیون شروع شد..." -ForegroundColor Green
    Write-Host "برای توقف Ctrl+C را فشار دهید" -ForegroundColor Yellow
    python automation.py --mode auto
}

function Start-APIServer {
    Write-Host "API Server در حال اجرا..." -ForegroundColor Green
    Write-Host "آدرس: http://localhost:8000" -ForegroundColor Cyan
    Write-Host "مستندات: http://localhost:8000/docs" -ForegroundColor Cyan
    Write-Host "برای توقف Ctrl+C را فشار دهید" -ForegroundColor Yellow
    python api_server.py
}

function Show-Logs {
    Write-Host "انتخاب فایل لاگ:" -ForegroundColor Green
    Write-Host "  [1] v2ray_collector.log"
    Write-Host "  [2] automation.log"
    Write-Host "  [3] همه لاگ‌ها"
    $choice = Read-Host "انتخاب کنید"
    
    switch ($choice) {
        1 { 
            if (Test-Path "logs\v2ray_collector.log") {
                Get-Content "logs\v2ray_collector.log" -Wait -Tail 20
            } else {
                Write-Host "فایل لاگ یافت نشد!" -ForegroundColor Red
            }
        }
        2 { 
            if (Test-Path "logs\automation.log") {
                Get-Content "logs\automation.log" -Wait -Tail 20
            } else {
                Write-Host "فایل لاگ یافت نشد!" -ForegroundColor Red
            }
        }
        3 {
            if (Test-Path "logs") {
                Get-ChildItem logs\*.log | ForEach-Object {
                    Write-Host "`n=== $($_.Name) ===" -ForegroundColor Cyan
                    Get-Content $_.FullName -Tail 10
                }
            } else {
                Write-Host "پوشه لاگ یافت نشد!" -ForegroundColor Red
            }
        }
    }
    pause
}

function Clear-Cache {
    Write-Host "در حال پاکسازی..." -ForegroundColor Green
    
    if (Test-Path "cache") {
        Remove-Item -Path "cache\*" -Recurse -Force
        Write-Host "Cache پاک شد" -ForegroundColor Green
    }
    
    if (Test-Path "logs") {
        Get-ChildItem -Path "logs\*.log.*" | Remove-Item -Force
        Write-Host "لاگ‌های قدیمی پاک شدند" -ForegroundColor Green
    }
    
    Get-ChildItem -Path . -Directory -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force
    Write-Host "__pycache__ پاک شد" -ForegroundColor Green
    
    pause
}

function Show-Info {
    Write-Host "اطلاعات سیستم:" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "نسخه Python: " -NoNewline
    python --version
    
    Write-Host "نسخه pip: " -NoNewline
    pip --version
    
    Write-Host "Docker: " -NoNewline
    try {
        docker --version
    } catch {
        Write-Host "نصب نشده" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "فضای دیسک:" -ForegroundColor Cyan
    Get-PSDrive C | Select-Object Name, @{Name="Used(GB)";Expression={[math]::Round($_.Used/1GB,2)}}, @{Name="Free(GB)";Expression={[math]::Round($_.Free/1GB,2)}}
    
    Write-Host ""
    Write-Host "فایل‌های اشتراک:" -ForegroundColor Cyan
    if (Test-Path "subscriptions") {
        Get-ChildItem subscriptions\*.txt | ForEach-Object {
            $lines = (Get-Content $_.FullName | Measure-Object -Line).Lines
            Write-Host "  - $($_.Name): $lines کانفیگ"
        }
    } else {
        Write-Host "  هنوز فایلی تولید نشده" -ForegroundColor Yellow
    }
    
    pause
}

function Show-DockerMenu {
    Write-Host "دستورات Docker:" -ForegroundColor Green
    Write-Host "  [1] اجرا (docker compose up -d)"
    Write-Host "  [2] توقف (docker compose down)"
    Write-Host "  [3] مشاهده لاگ‌ها"
    Write-Host "  [4] وضعیت"
    Write-Host "  [5] بازگشت"
    
    $choice = Read-Host "انتخاب کنید"
    
    switch ($choice) {
        1 { 
            docker compose up -d 
            pause
        }
        2 { 
            docker compose down 
            pause
        }
        3 { 
            docker compose logs -f 
        }
        4 { 
            docker compose ps 
            pause
        }
        5 { return }
    }
}

# اجرای برنامه اصلی
if ($Action -eq "menu") {
    do {
        Show-Menu
        $choice = Read-Host "انتخاب کنید (0-9)"
        
        switch ($choice) {
            1 { Install-Dependencies }
            2 { Run-Tests }
            3 { Collect-Configs }
            4 { Start-Automation }
            5 { Start-APIServer }
            6 { Show-Logs }
            7 { Clear-Cache }
            8 { Show-Info }
            9 { Show-DockerMenu }
            0 { 
                Write-Host "خداحافظ!" -ForegroundColor Green
                exit 
            }
            default { 
                Write-Host "انتخاب نامعتبر!" -ForegroundColor Red
                pause
            }
        }
    } while ($true)
} else {
    switch ($Action) {
        "install" { Install-Dependencies }
        "test" { Run-Tests }
        "collect" { Collect-Configs }
        "auto" { Start-Automation }
        "api" { Start-APIServer }
        "logs" { Show-Logs }
        "clean" { Clear-Cache }
        "info" { Show-Info }
        default { 
            Write-Host "Action نامعتبر!" -ForegroundColor Red
            Write-Host "استفاده: .\run-fa.ps1 [install|test|collect|auto|api|logs|clean|info]"
        }
    }
}

