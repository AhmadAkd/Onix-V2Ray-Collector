# V2Ray Collector - Windows PowerShell Runner
# Script for quick execution on Windows

param(
    [string]$Action = "menu"
)

# Show Menu
function Show-Menu {
    Clear-Host
    Write-Host "======================================================" -ForegroundColor Cyan
    Write-Host "   V2Ray Collector - Windows Edition" -ForegroundColor Cyan
    Write-Host "======================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  [1] Install Dependencies" -ForegroundColor Yellow
    Write-Host "  [2] Run Tests" -ForegroundColor Yellow
    Write-Host "  [3] Collect Configs (Once)" -ForegroundColor Yellow
    Write-Host "  [4] Automation (Every 30 min)" -ForegroundColor Yellow
    Write-Host "  [5] Start API Server" -ForegroundColor Yellow
    Write-Host "  [6] View Logs" -ForegroundColor Yellow
    Write-Host "  [7] Clean Cache" -ForegroundColor Yellow
    Write-Host "  [8] Show System Info" -ForegroundColor Yellow
    Write-Host "  [9] Docker Commands" -ForegroundColor Yellow
    Write-Host "  [0] Exit" -ForegroundColor Red
    Write-Host ""
}

# Install Dependencies
function Install-Dependencies {
    Write-Host "Installing dependencies..." -ForegroundColor Green
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    Write-Host "Installation completed successfully!" -ForegroundColor Green
    pause
}

# Run Tests
function Run-Tests {
    Write-Host "Running tests..." -ForegroundColor Green
    python run_tests.py
    pause
}

# Collect Configs
function Collect-Configs {
    Write-Host "Collecting configs..." -ForegroundColor Green
    python config_collector.py
    pause
}

# Start Automation
function Start-Automation {
    Write-Host "Automation started..." -ForegroundColor Green
    Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
    python automation.py --mode auto
}

# Start API Server
function Start-APIServer {
    Write-Host "API Server is starting..." -ForegroundColor Green
    Write-Host "Address: http://localhost:8000" -ForegroundColor Cyan
    Write-Host "Docs: http://localhost:8000/docs" -ForegroundColor Cyan
    Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
    python api_server.py
}

# Show Logs
function Show-Logs {
    Write-Host "Select log file:" -ForegroundColor Green
    Write-Host "  [1] v2ray_collector.log"
    Write-Host "  [2] automation.log"
    Write-Host "  [3] All logs"
    $choice = Read-Host "Choose"
    
    switch ($choice) {
        1 { 
            if (Test-Path "logs\v2ray_collector.log") {
                Get-Content "logs\v2ray_collector.log" -Wait -Tail 20
            }
            else {
                Write-Host "Log file not found!" -ForegroundColor Red
            }
        }
        2 { 
            if (Test-Path "logs\automation.log") {
                Get-Content "logs\automation.log" -Wait -Tail 20
            }
            else {
                Write-Host "Log file not found!" -ForegroundColor Red
            }
        }
        3 {
            if (Test-Path "logs") {
                Get-ChildItem logs\*.log | ForEach-Object {
                    Write-Host "`n=== $($_.Name) ===" -ForegroundColor Cyan
                    Get-Content $_.FullName -Tail 10
                }
            }
            else {
                Write-Host "Logs directory not found!" -ForegroundColor Red
            }
        }
    }
    pause
}

# Clean Cache
function Clear-Cache {
    Write-Host "Cleaning..." -ForegroundColor Green
    
    if (Test-Path "cache") {
        Remove-Item -Path "cache\*" -Recurse -Force
        Write-Host "Cache cleared" -ForegroundColor Green
    }
    
    if (Test-Path "logs") {
        Get-ChildItem -Path "logs\*.log.*" | Remove-Item -Force
        Write-Host "Old logs cleared" -ForegroundColor Green
    }
    
    Get-ChildItem -Path . -Directory -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force
    Write-Host "__pycache__ cleared" -ForegroundColor Green
    
    pause
}

# Show System Info
function Show-Info {
    Write-Host "System Information:" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "Python: " -NoNewline
    python --version
    
    Write-Host "pip: " -NoNewline
    pip --version
    
    Write-Host "Docker: " -NoNewline
    try {
        docker --version
    }
    catch {
        Write-Host "Not installed" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "Disk Space:" -ForegroundColor Cyan
    Get-PSDrive C | Select-Object Name, @{Name = "Used(GB)"; Expression = { [math]::Round($_.Used / 1GB, 2) } }, @{Name = "Free(GB)"; Expression = { [math]::Round($_.Free / 1GB, 2) } }
    
    Write-Host ""
    Write-Host "Subscription Files:" -ForegroundColor Cyan
    if (Test-Path "subscriptions") {
        Get-ChildItem subscriptions\*.txt | ForEach-Object {
            $lines = (Get-Content $_.FullName | Measure-Object -Line).Lines
            Write-Host "  - $($_.Name): $lines configs"
        }
    }
    else {
        Write-Host "  No files generated yet" -ForegroundColor Yellow
    }
    
    pause
}

# Docker Commands
function Show-DockerMenu {
    Write-Host "Docker Commands:" -ForegroundColor Green
    Write-Host "  [1] Start (docker compose up -d)"
    Write-Host "  [2] Stop (docker compose down)"
    Write-Host "  [3] View Logs"
    Write-Host "  [4] Status"
    Write-Host "  [5] Back"
    
    $choice = Read-Host "Choose"
    
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

# Main Program
if ($Action -eq "menu") {
    do {
        Show-Menu
        $choice = Read-Host "Choose (0-9)"
        
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
                Write-Host "Goodbye!" -ForegroundColor Green
                exit 
            }
            default { 
                Write-Host "Invalid choice!" -ForegroundColor Red
                pause
            }
        }
    } while ($true)
}
else {
    # Direct execution
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
            Write-Host "Invalid action!" -ForegroundColor Red
            Write-Host "Usage: .\run.ps1 [install|test|collect|auto|api|logs|clean|info]"
        }
    }
}
