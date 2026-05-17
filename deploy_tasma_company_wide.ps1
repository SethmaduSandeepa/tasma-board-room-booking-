# TASMA Booking System - Automated Deployment Script
# PowerShell script for automated deployment across multiple machines
# Usage: .\deploy_tasma_company_wide.ps1 -ServerName "SERVER_NAME" -ComputerNames @("COMPUTER1", "COMPUTER2")

param(
    [Parameter(Mandatory=$true)]
    [string]$ServerName,
    
    [Parameter(Mandatory=$false)]
    [string[]]$ComputerNames,
    
    [Parameter(Mandatory=$false)]
    [string]$ShareName = "TASMA_App",
    
    [Parameter(Mandatory=$false)]
    [switch]$SetupServerShares,
    
    [Parameter(Mandatory=$false)]
    [switch]$DeployToAllUsers = $false
)

# Configuration
$ErrorActionPreference = "Stop"
$VerbosePreference = "Continue"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "TASMA Deployment Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verify server connectivity
Write-Host "Testing server connection..." -ForegroundColor Yellow
try {
    $path = "\\$ServerName\$ShareName"
    if (-not (Test-Path $path)) {
        throw "Cannot access $path"
    }
    Write-Host "✓ Server connection verified: $path" -ForegroundColor Green
}
catch {
    Write-Host "✗ Cannot connect to server: $_" -ForegroundColor Red
    Write-Host "Verify:"
    Write-Host "  - Server is running and reachable (ping $ServerName)"
    Write-Host "  - Share name is correct: $ShareName"
    Write-Host "  - You have network access permissions"
    exit 1
}

# Function to create shortcut on a local machine
function Create-TASMA-Shortcut {
    param(
        [string]$ServerName,
        [string]$ShareName,
        [string]$DesktopPath = $null
    )
    
    if (-not $DesktopPath) {
        $DesktopPath = [System.Environment]::GetFolderPath("Desktop")
    }
    
    $shortcutPath = Join-Path $DesktopPath "TASMA Booking System.lnk"
    $appPath = "\\$ServerName\$ShareName"
    $exePath = Join-Path $appPath "TASMA Board Room Booking System.exe"
    $iconPath = Join-Path $appPath "booking_icon.ico"
    
    try {
        $WshShell = New-Object -ComObject WScript.Shell
        $shortcut = $WshShell.CreateShortcut($shortcutPath)
        $shortcut.TargetPath = $exePath
        $shortcut.WorkingDirectory = $appPath
        
        if (Test-Path $iconPath) {
            $shortcut.IconLocation = $iconPath
        }
        
        $shortcut.Description = "TASMA Board Room Booking System"
        $shortcut.Save()
        
        return $shortcutPath
    }
    catch {
        throw "Failed to create shortcut: $_"
    }
}

# Function to deploy shortcut to remote computer
function Deploy-To-RemoteComputer {
    param(
        [string]$ComputerName,
        [string]$ServerName,
        [string]$ShareName
    )
    
    Write-Host "Deploying to $ComputerName..." -ForegroundColor Yellow
    
    try {
        # Create session
        $session = New-PSSession -ComputerName $ComputerName -ErrorAction Stop
        
        # Deploy shortcut
        $result = Invoke-Command -Session $session -ScriptBlock ${function:Create-TASMA-Shortcut} `
            -ArgumentList $ServerName, $ShareName -ErrorAction Stop
        
        Remove-PSSession -Session $session
        
        Write-Host "✓ Deployed to $ComputerName: $result" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "✗ Failed to deploy to $ComputerName : $_" -ForegroundColor Red
        return $false
    }
}

# Function to setup server shares (must run on server)
function Setup-ServerShares {
    param(
        [string]$AppDrive = "C:",
        [string]$DataDrive = "C:"
    )
    
    Write-Host "Setting up server shares..." -ForegroundColor Yellow
    
    # Check if running on server
    $appPath = "$AppDrive\SharedApps\TASMA"
    $dataPath = "$DataDrive\SharedData\TASMA"
    
    # Create directories
    if (-not (Test-Path $appPath)) {
        New-Item -ItemType Directory -Path $appPath -Force | Out-Null
        Write-Host "Created directory: $appPath"
    }
    
    if (-not (Test-Path $dataPath)) {
        New-Item -ItemType Directory -Path $dataPath -Force | Out-Null
        Write-Host "Created directory: $dataPath"
    }
    
    # Create SMB shares
    try {
        # Remove existing shares
        Get-SmbShare -Name "TASMA_App" -ErrorAction SilentlyContinue | Remove-SmbShare -Force
        Get-SmbShare -Name "TASMA_Data" -ErrorAction SilentlyContinue | Remove-SmbShare -Force
        
        # Create new shares
        New-SmbShare -Name "TASMA_App" -Path $appPath -FullAccess "Everyone" -ErrorAction Stop | Out-Null
        Write-Host "✓ Created share: TASMA_App"
        
        New-SmbShare -Name "TASMA_Data" -Path $dataPath -FullAccess "Everyone" -ErrorAction Stop | Out-Null
        Write-Host "✓ Created share: TASMA_Data"
    }
    catch {
        Write-Host "✗ Error creating shares: $_" -ForegroundColor Red
        Write-Host "Ensure you're running this on the server with Administrator privileges"
    }
}

# Function to generate deployment report
function Generate-DeploymentReport {
    param(
        [hashtable]$Results
    )
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Deployment Report" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    
    $successful = @($Results.Values | Where-Object { $_ -eq $true })
    $failed = @($Results.Values | Where-Object { $_ -eq $false })
    
    Write-Host "Server: $ServerName" -ForegroundColor White
    Write-Host "Share: $ShareName" -ForegroundColor White
    Write-Host ""
    Write-Host "Results:" -ForegroundColor Cyan
    Write-Host "  Successful: $($successful.Count)" -ForegroundColor Green
    Write-Host "  Failed: $($failed.Count)" -ForegroundColor Red
    Write-Host ""
    
    if ($failed.Count -gt 0) {
        Write-Host "Failed computers:" -ForegroundColor Yellow
        $Results.GetEnumerator() | Where-Object { $_.Value -eq $false } | ForEach-Object {
            Write-Host "  - $($_.Key)"
        }
    }
}

# Main execution
Write-Host "Configuration:" -ForegroundColor Cyan
Write-Host "  Server: $ServerName" -ForegroundColor White
Write-Host "  Share: $ShareName" -ForegroundColor White
if ($ComputerNames) {
    Write-Host "  Computers: $($ComputerNames -join ', ')" -ForegroundColor White
}
Write-Host ""

# Setup server shares if requested
if ($SetupServerShares) {
    Write-Host "Setting up server shares..." -ForegroundColor Yellow
    Setup-ServerShares
    Write-Host ""
}

# Deploy to local machine
Write-Host "Creating shortcut on local machine..." -ForegroundColor Yellow
try {
    $localPath = Create-TASMA-Shortcut -ServerName $ServerName -ShareName $ShareName
    Write-Host "✓ Created local shortcut: $localPath" -ForegroundColor Green
}
catch {
    Write-Host "✗ Failed to create local shortcut: $_" -ForegroundColor Red
}

Write-Host ""

# Deploy to remote computers
if ($ComputerNames) {
    Write-Host "Deploying to remote computers..." -ForegroundColor Yellow
    Write-Host ""
    
    $deployResults = @{}
    foreach ($computer in $ComputerNames) {
        $success = Deploy-To-RemoteComputer -ComputerName $computer -ServerName $ServerName -ShareName $ShareName
        $deployResults[$computer] = $success
    }
    
    Generate-DeploymentReport -Results $deployResults
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Deployment Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Users can now double-click 'TASMA Booking System' on desktop" -ForegroundColor White
Write-Host "  2. First launch takes 3-5 seconds" -ForegroundColor White
Write-Host "  3. Subsequent launches will be faster (1-2 seconds)" -ForegroundColor White
Write-Host ""
Write-Host "Troubleshooting:" -ForegroundColor Cyan
Write-Host "  - Verify network connectivity: ping $ServerName" -ForegroundColor White
Write-Host "  - Check share access: dir \\$ServerName\$ShareName" -ForegroundColor White
Write-Host "  - Review logs: Check tasma_app.log in app directory" -ForegroundColor White
Write-Host ""
