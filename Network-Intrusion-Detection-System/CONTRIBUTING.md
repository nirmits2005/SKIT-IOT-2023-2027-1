# Contributing Guidelines — Network Intrusion Detection System (NIDS)

Welcome to the Network Intrusion Detection System (NIDS) repository under `nirmits2005/SKIT-IOT-2023-2027-1`.

To maintain repository integrity, code consistency, and traceable academic attribution, all contributors must adhere to the following workflow standards.

---

## 1. Directory Structure Standards

All NIDS-related source code, artifacts, datasets, and documentation must reside exclusively inside the dedicated subfolder:
```
SKIT-IOT-2023-2027-1/
├── .github/
│   └── workflows/
│       └── weekly-progress-report.yml
└── Network-Intrusion-Detection-System/
    ├── NSL_Dataset/
    │   ├── Train.txt
    │   └── Test.txt
    ├── results/
    ├── static/
    │   └── style.css
    ├── templates/
    │   └── index.html
    ├── weekly_reports/
    ├── app.py
    ├── model.pkl
    ├── generate_report.py
    ├── test_project.py
    ├── requirements.txt
    ├── Dockerfile
    ├── Procfile
    ├── TEAM.md
    ├── CONTRIBUTORS.md
    ├── CONTRIBUTING.md
    └── README.md
```
Do not place loose files outside this project directory.

---

## 2. Git Branching & Commit Conventions

### Branch Strategy
* `main`: Protected production branch. Direct pushes should be coordinated or conducted via pull requests.
* Feature branches: Use namespaced format: `feat/<feature-name>`, `fix/<issue-name>`, or individual contributor branches (e.g., `Nitesh-Sharma`, `Shaurya-pratap`).

### Commit Message Standards
Follow the Conventional Commits specification:
* `feat(scope)`: A new feature or endpoint (e.g., `feat(api): add healthcheck endpoint`)
* `fix(scope)`: A bug fix (e.g., `fix(model): resolve input dimension mismatch`)
* `docs(scope)`: Documentation updates (e.g., `docs(team): update responsibility matrix`)
* `ci(scope)`: CI/CD or workflow adjustments (e.g., `ci(report): update cron schedule`)
* `test(scope)`: Adding or refining test suites (e.g., `test(backend): add pytest for /predict`)
* `chore(scope)`: Maintenance or environment updates (e.g., `chore: bump dependencies`)

---

## 3. Contribution Verification & Form-3 Reporting

1. **Authorship Integrity:** Commit using your verified Git email and name to ensure accurate author resolution in Form-3 PDF generation.
2. **Weekly Automated Reporting:** A GitHub Actions workflow runs every Thursday at 18:29 UTC (11:59 PM IST) to aggregate weekly commits and archive progress PDFs into `weekly_reports/`.
3. **Local Report Generation:**
   ```bash
   python generate_report.py weekly
   python generate_report.py monthly
   python generate_report.py final
   python generate_report.py --start-date YYYY-MM-DD --end-date YYYY-MM-DD -o report.pdf
   ```

---

## 4. Code & Model Quality Standards

* **Dependencies:** Keep `requirements.txt` strictly pinned and auditable.
* **Security:** Never commit API keys, passwords, database credentials, or secret tokens.
* **Model Serialization:** Inspect all pickle/joblib files before committing. Keep artifact sizes within GitHub's standard limits (< 50 MB recommended).
* **Testing:** Run local unit tests and verify Flask endpoints before creating pull requests.
