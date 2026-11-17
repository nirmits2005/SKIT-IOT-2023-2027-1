# 🔐 Network Intrusion Detection System (NIDS)

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![ML](https://img.shields.io/badge/ML-Binary%20%7C%20Multi--class%20Classification-orange?style=flat-square)
![Security](https://img.shields.io/badge/Domain-Cybersecurity%20%7C%20Network%20Security-red?style=flat-square)
![Dataset](https://img.shields.io/badge/Dataset-NSL--KDD%20(KDDCUP'99)-lightblue?style=flat-square)
![Flask](https://img.shields.io/badge/Deployed-Flask%20App-green?style=flat-square&logo=flask)
![Docker](https://img.shields.io/badge/Container-Docker-blue?style=flat-square&logo=docker)
![CI](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blueviolet?style=flat-square&logo=githubactions)

> **A Machine Learning-powered Network Intrusion Detection System (NIDS) that classifies network traffic into Normal or Malicious categories — identifying 4 major attack types (DOS, PROBE, R2L, U2R) — integrated with a real-time Flask web application, Docker containerization, and automated Form-3 academic progress reporting.**

---

## 🏛️ Academic & Institutional Context

* **Institution:** Swami Keshvanand Institute of Technology, Management & Gramothan (SKIT), Jaipur
* **Department:** Department of Computer Science & Engineering (IoT Specialization, 2023–2027)
* **Target Repository:** `nirmits2005/SKIT-IOT-2023-2027-1`
* **Subdirectory Path:** `Network-Intrusion-Detection-System/`

---

## 👥 Engineering Team & Roles

| Contributor | Proposed Responsibilities & Focus Areas |
| :--- | :--- |
| **Shobhan Bhagwati** | **Data Engineering & EDA:** Dataset analysis, NSL-KDD data cleaning, feature profiling (`corrm.csv`, `num_summary.csv`), categorical encoding, distribution analysis, and dataset documentation. |
| **Nitesh Sharma** | **Machine Learning & Modeling:** Machine learning architecture, binary & multi-class model training, hyperparameter optimization, feature selection (15 key features), model serialization (`model.pkl`), and Git repository administration. |
| **Shaurya Shekhawat** | **Backend & DevOps:** Flask REST backend (`app.py`), inference endpoints (`/predict`, `/results`), application architecture, Gunicorn server configuration (`Procfile`), Docker containerization (`Dockerfile`), and backend testing. |
| **Prankur Sharma** | **Frontend & QA:** Web interface development (`templates/index.html`), stylesheet design (`static/style.css`), prediction result presentation, end-to-end integration testing, and documentation support. |

*For complete details on allocations, see [TEAM.md](TEAM.md), [CONTRIBUTORS.md](CONTRIBUTORS.md), and [CONTRIBUTING.md](CONTRIBUTING.md).*

---

## 📌 Problem Statement & Objective

Traditional signature-based intrusion detection systems (IDS) rely on static rules that cannot detect zero-day vulnerabilities or dynamic traffic deviations. This project implements an **anomaly-based machine learning NIDS** to:

1. Differentiate legitimate network traffic from malicious connections (**Binary Classification**).
2. Categorize detected threats into specific operational attack classes (**Multi-class Classification**):
   * **Normal:** Legitimate network activity (HTTP, SSH, SMTP, FTP).
   * **DOS (Denial of Service):** Exhaustion of target server bandwidth or compute (e.g., SYN Flood, Smurf, Neptune, Ping of Death).
   * **PROBE:** Surveillance and reconnaissance scanning to discover network topology and active services (e.g., Portscan, Nmap, Satan).
   * **R2L (Remote to Local):** Unauthorized local access gained by an external attacker exploiting vulnerabilities (e.g., Guess Password, Warezclient).
   * **U2R (User to Root):** Privilege escalation attacks where a local non-privileged user gains root privileges (e.g., Buffer Overflow, Rootkit).

---

## 📊 Dataset: NSL-KDD (KDDCUP'99 Benchmark)

* **Source:** University of New Brunswick (UNB) / Canadian Institute for Cybersecurity
* **Components:**
  * `NSL_Dataset/Train.txt`: Primary training partition (125,973 records)
  * `NSL_Dataset/Test.txt`: Evaluation test partition (22,544 records)
* **Feature Dimensionality:**
  * 41 core network connection features covering basic connection parameters, content-based indicators, time-window traffic rates, and destination host statistics.
  * Reduced via correlation and information-gain filtering to 15 optimized inference features used in production.

---

## 🏗️ Project Architecture & Directory Layout

```
SKIT-IOT-2023-2027-1/
├── .github/
│   └── workflows/
│       └── weekly-progress-report.yml     # Automated weekly Form-3 PDF commit workflow (Repository Root)
├── Network-Intrusion-Detection-System/
│   ├── NSL_Dataset/
│   │   ├── Train.txt                      # NSL-KDD Training Dataset
│   │   └── Test.txt                       # NSL-KDD Testing Dataset
│   ├── results/                           # Visual output charts and UI screenshots
│   ├── static/
│   │   └── style.css                      # Application styling
│   ├── templates/
│   │   └── index.html                     # Responsive web input interface
│   ├── weekly_reports/                    # Form-3 progress reports (Weekly, Monthly, Final)
│   ├── app.py                             # Flask web server and prediction endpoints
│   ├── model.pkl                          # Serialized LogisticRegression model artifact
│   ├── generate_report.py                 # FlowStock Form-3 PDF Report Generator
│   ├── test_project.py                    # Automated comprehensive unit test suite
│   ├── corrm.csv                          # Feature correlation matrix
│   ├── num_summary.csv                    # Numerical features statistical summary
│   ├── Network Intrusion Detection System.ipynb # Jupyter analysis & model training notebook
│   ├── Dockerfile                         # Container build definition
│   ├── Procfile                           # Gunicorn web process definition
│   ├── requirements.txt                   # Locked Python dependencies
│   ├── TEAM.md                            # Team responsibility matrix
│   ├── CONTRIBUTORS.md                    # Author and contributor index
│   ├── CONTRIBUTING.md                    # Contribution and branch guidelines
│   └── README.md                          # Main documentation
```

---

## ⚙️ Technology Stack

* **Language:** Python 3.11+
* **Machine Learning & Data Science:** Scikit-learn, Pandas, NumPy, Matplotlib, Seaborn
* **Web Framework & API:** Flask, Gunicorn, Jinja2
* **Reporting Engine:** ReportLab, Matplotlib (FlowStock Form-3 Standard)
* **DevOps & CI/CD:** Docker, GitHub Actions (`cron` scheduling)

---

## 🚀 Installation & Local Execution

### 1. Prerequisites & Virtual Environment
```bash
# Clone the repository
git clone https://github.com/nirmits2005/SKIT-IOT-2023-2027-1.git
cd SKIT-IOT-2023-2027-1/Network-Intrusion-Detection-System

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install reportlab matplotlib
```

### 2. Run the Flask Web Application
```bash
python app.py
```
Open [http://localhost:10000](http://localhost:10000) (or configured port) in your web browser.

### 3. API Endpoints
* `GET /`: Interactive web form for manual parameter input.
* `POST /predict`: Form endpoint processing 12 frontend fields, encoding to 15 vector features, and displaying the verdict.
* `POST /results`: REST JSON API accepting 15 numerical features and returning the classification label:
  ```bash
  curl -X POST http://localhost:10000/results \
    -H "Content-Type: application/json" \
    -d '{"f0":0,"f1":0,"f2":0,"f3":10,"f4":0.1,"f5":0.2,"f6":0.8,"f7":255,"f8":0,"f9":1,"f10":20,"f11":1,"f12":1.0,"f13":0.0,"f14":1}'
  ```

---

## 🐳 Docker Deployment

```bash
# Build the Docker image
docker build -t nids-app .

# Run the container
docker run -p 5000:5000 nids-app
```
Access the application at [http://localhost:5000](http://localhost:5000).

---

## 📑 Academic Form-3 Progress Report Generator

The project includes an integrated reporting engine in `generate_report.py`, adapted directly from the official FlowStock Form-3 ReportLab reference implementation.

### Features
* Exact institutional formatting: SKIT header, CSE Department title, Form-3 metadata.
* Four-member contribution analysis (Commits, Lines Added, Lines Deleted, Net LOC, Active Days).
* Visual Matplotlib charts: Commit Timeline and Net LOC comparison.
* Student commit log tables with vertically merged Mentor Evaluation marks (`_____ / 10`).
* Symmetrical dual signature block for Project Mentor and Lab Coordinator.

### Execution Modes
```bash
# Generate last 7 days report
python generate_report.py weekly

# Generate last 30 days report
python generate_report.py monthly

# Generate complete project lifecycle report
python generate_report.py final

# Custom reporting window
python generate_report.py --start-date 2026-08-15 --end-date 2026-08-22 -o weekly_reports/period_2.pdf

# Batch generate all 13 chronological semester reports
python generate_report.py historical
```

---

## 🤖 GitHub Actions Automated Reporting

A scheduled workflow runs automatically in GitHub Actions:
* **Schedule:** Every Thursday at 11:59 PM IST (18:29 UTC) via cron `29 18 * * 4`.
* **Workflow File:** `.github/workflows/weekly-progress-report.yml`
* **Operation:** Checks out full Git history, runs `generate_report.py weekly`, moves new PDFs to `weekly_reports/`, and auto-commits the archived report with `[skip ci]`.

---

## 🧪 Testing & Validation

Run the automated test suite covering model inference, Flask routes, dataset presence, and security audits:
```bash
python test_project.py
```

---

## 📄 License & Attribution

* **License:** MIT License — see [LICENSE](LICENSE).
* **Upstream Lineage:** Derived from NSL-KDD benchmark research and community contributions.
* **FlowStock Reporting:** Form-3 PDF reporting engine adapted from [Tanaypai123/FlowStock](https://github.com/Tanaypai123/FlowStock).
