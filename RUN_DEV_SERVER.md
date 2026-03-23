# Run the Django Dev Server (Mac + Windows)

This guide shows the exact steps to start the local development server for this project.

## Prerequisites

- Python installed (`python --version` or `python3 --version`)
- Git installed
- Repo cloned locally

---

## 1) Open terminal and go to the project

### macOS
```bash
cd /ChesapeakeCommunityConnect/cccSite
```

### Windows (PowerShell)
```powershell
cd C:\path\to\ChesapeakeCommunityConnect\cccSite
```

---

## 2) Create a virtual environment (first time only)

### macOS
```bash
python3 -m venv venv
```

### Windows (PowerShell)
```powershell
python -m venv venv
```

---

## 3) Activate the virtual environment

### macOS
```bash
source venv/bin/activate
```

### Windows (PowerShell)
```powershell
.\venv\Scripts\Activate.ps1
```

> If PowerShell blocks script execution, run this once in an Admin PowerShell and try again:
```powershell
Set-ExecutionPolicy RemoteSigned
```

---

## 4) Install dependencies

### macOS
```bash
pip install -r requirements.txt
pip install python-magic
brew install libmagic
```

### Windows (PowerShell)
```powershell
pip install -r requirements.txt
pip install python-magic-bin
```

---

## 5) Run migrations

```bash
python manage.py migrate
```

If Django says model changes are not reflected in migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 6) Start the dev server

```bash
python manage.py runserver 8080
```

---

## 7) Open the app in your browser

- Main site: <http://localhost:8080>

---

## 8) Stop the server

In the terminal where it is running, press:

- `Ctrl + C`

---

## Quick daily start (after initial setup)

### macOS
```bash
cd ChesapeakeCommunityConnect-1/cccSite
source venv/bin/activate
python manage.py runserver 8080
```

### Windows (PowerShell)
```powershell
cd C:\path\to\ChesapeakeCommunityConnect-1\cccSite
.\venv\Scripts\Activate.ps1
python manage.py runserver 8080
```

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'django'`
Your venv is not active or dependencies are not installed.

```bash
python -m pip install -r requirements.txt
```

### Verify you are using venv Python

### macOS
```bash
which python
```

### Windows (PowerShell)
```powershell
Get-Command python
```

It should point to your project `venv` path.
