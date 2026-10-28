# QA Automation README

## Purpose

This folder contains the QA automation system for ChesapeakeCommunityConnect.

The goal is to allow R&D to run one command and quickly determine whether critical website functionality still works.

Run the full QA suite with:

```bash
./qa/run_all.sh
```

---

## Folder Structure

- `qa/run_all.sh` — press-play runner script  
- `qa/ui/` — smoke tests  
- `qa/ui/conftest.py` — shared test configuration (base URL)  
- `qa/README.md` — contributor instructions and testing standards  

---

## General Workflow

All QA work should follow this process:

1. Pull latest code:
   ```bash
   git checkout development
   git pull origin development
   ```

2. Create a new branch:
   ```bash
   git checkout -b qa/<issue-number>-short-description>
   ```

3. Make changes (only inside `qa/` unless instructed otherwise)

4. Run tests:
   ```bash
   ./qa/run_all.sh
   ```

5. Commit and push:
   ```bash
   git add qa
   git commit -m "Describe your change"
   git push -u origin <branch-name>
   ```

6. Open a Pull Request into:
   - Base: `development`

7. After merge:
   - Delete your branch (GitHub button or `git branch -d <branch>`)

---

## Smoke Test Standards

A smoke test verifies that a core part of the application still works.

### Every smoke test must:

- Test **one route or one small behavior**
- Use the shared `base_url` (from `conftest.py`)
- Include `timeout=5` in requests
- Check response status
- Check at least one stable piece of text (if applicable)
- Be simple and easy to understand

### Smoke tests should NOT:

- Test styling or layout
- Use `time.sleep()`
- Include unnecessary setup or complexity
- Combine multiple unrelated checks into one test
- Modify application code outside QA scope

---

## Example Smoke Test

```python
import requests

def test_about_page_loads(base_url):
    response = requests.get(base_url + "/about/", timeout=5)
    assert response.status_code == 200
    assert "About" in response.text
```

---

## pytest Basics

- Test functions must start with `test_`  
- Tests are stored in `qa/ui/`  
- Assertions use `assert`  
- Run tests with:
  ```bash
  ./qa/run_all.sh
  ```

Optional manual run:
```bash
QA_BASE_URL=http://127.0.0.1:8080 pytest qa/ui
```

---

## QA Virtual Environment

Enter the QA virtual environment manually:

```bash
source qa/.venv/bin/activate
```

You should see:
```bash
(.venv) yourname@...
```

To exit:
```bash
deactivate
```

---

## Django Admin Access (DJadmin)

Some tests may require access to the Django admin panel.

To create a superuser:

1. Navigate to project:
   ```bash
   cd /home/<your-username>/shared_workspace/ChesapeakeCommunityConnect/cccSite
   ```

2. Create account:
   ```bash
   python3.10 manage.py createsuperuser
   ```

3. Follow prompts

Admin URL:
```
http://127.0.0.1:8080/DJadmin/
```

---

## What You May Want to Learn

Helpful topics for QA contributors:

- Python basics  
- Virtual environments  
- pytest fundamentals  
- HTTP requests using `requests`  
- Basic Git workflow (branching + PRs)