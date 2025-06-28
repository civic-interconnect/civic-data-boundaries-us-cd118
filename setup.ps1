# setup-dev.ps1
# Civic Interconnect Development Setup Script (PowerShell)

param(
    [switch]$Editable
)

Write-Host "Creating virtual environment in .venv ..." -ForegroundColor Cyan
py -m venv .venv

Write-Host "Virtual environment created."
Write-Host "Activating environment ..."
. .\.venv\Scripts\Activate.ps1

Write-Host "Upgrading pip, setuptools, wheel ..." -ForegroundColor Cyan
py -m pip install --upgrade pip setuptools wheel --prefer-binary

if ($Editable) {
    Write-Host "Installing project in editable mode with dev dependencies ..." -ForegroundColor Cyan
    py -m pip install --upgrade -e .[dev]
}
else {
    Write-Host "Installing project normally with dev dependencies ..." -ForegroundColor Cyan
    py -m pip install --upgrade .[dev]
}

# Write-Host "Running prep-code (format, lint, test) ..." -ForegroundColor Cyan
# civic-dev prep-code

# Write-Host "Publishing API documentation ..." -ForegroundColor Cyan
# civic-dev publish-api

# Write-Host "Starting local docs server ..." -ForegroundColor Cyan
# mkdocs serve
