# setup-dev.ps1
# Civic Interconnect Development Setup Script (PowerShell)

Write-Host "Deactivate any existing virtual environment if active ..." -ForegroundColor Cyan
if ($env:VIRTUAL_ENV) {
    Write-Host "Deactivating existing virtual environment ..." -ForegroundColor Yellow
    deactivate
} else {
    Write-Host "No active virtual environment found." -ForegroundColor Green
}

Write-Host "Deleting existing .venv if it exists ..." -ForegroundColor Cyan
if (Test-Path ".venv") {
    $confirm = Read-Host "Delete existing .venv virtual environment? (y/n)"
    if ($confirm -eq "y") {
        Remove-Item ".venv" -Recurse -Force
        Write-Host "Removed .venv"
    } else {
        Write-Host "Skipped .venv deletion"
    }
} else {
    Write-Host ".venv does not exist, proceeding to create a new one." -ForegroundColor Green
}


Write-Host "Creating virtual environment in .venv ..." -ForegroundColor Cyan
py -m venv .venv

Write-Host "Virtual environment created."
Write-Host "Activating environment ..."
. .\.venv\Scripts\Activate.ps1

Write-Host "Upgrading pip, setuptools, wheel ..." -ForegroundColor Cyan
py -m pip install --upgrade pip setuptools wheel --prefer-binary


Write-Host "Installing project in editable mode with dev dependencies ..." -ForegroundColor Cyan
py -m pip install --upgrade -e .[dev]


# Write-Host "Running prep-code (format, lint, test) ..." -ForegroundColor Cyan
# civic-dev prep-code

# Write-Host "Publishing API documentation ..." -ForegroundColor Cyan
# civic-dev publish-api

# Write-Host "Starting local docs server ..." -ForegroundColor Cyan
# mkdocs serve
