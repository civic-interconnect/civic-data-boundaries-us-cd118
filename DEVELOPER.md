# DEVELOPER.md

## Setup for Data Projects

1. Fork the repo.
2. Clone your fork and open it in VS Code.
3. Open a terminal (examples below use PowerShell on Windows).

```
git clone https://github.com/civic-interconnect/civic-data-boundaries-us-cd118.git
cd civic-data-boundaries-us
.\seted.ps1
civic-dev prep-code
civic-dev publish-api
mkdocs serve
```

Visit local API docs at: <http://localhost:8000>

## Before Starting Changes, Verify

```shell
git pull
civic-us-cd118 fetch
civic-us-cd118 export
civic-us-cd118 index
civic-us-cd118 cleanup
```


## Releasing New Version

Before publishing a new version, delete .venv. and recreate and activate.
Run pre-release preparation, installing and upgrading without the -e editable flag.
Verify all tests pass. Run prep-code (twice if needed).
Verify the docs are generated and appear correctly.

```powershell
git pull

deactivate
Remove-Item -Recurse -Force .venv

py -m venv .venv
.\.venv\Scripts\Activate.ps1

py -m pip install --upgrade pip setuptools wheel --prefer-binary
py -m pip install --upgrade .[dev]

pytest tests
civic-dev prep-code
civic-dev publish-api
mkdocs serve
```

After verifying changes, update VERSION, README badge, and pyproject.toml, then git add-commit-tag-push:

```powershell
civic-dev bump-version 0.0.1 0.0.2

git pull

deactivate
Remove-Item -Recurse -Force .venv

py -m venv .venv
.\.venv\Scripts\Activate.ps1

py -m pip install --upgrade pip setuptools wheel --prefer-binary
py -m pip install --upgrade .[dev]

git add .
git commit -m "Release v0.0.1"
git tag "v0.0.1"
git push origin main
git push origin "v0.0.1"
```
