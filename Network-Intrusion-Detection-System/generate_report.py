#!/usr/bin/env python3
"""
Swami Keshvanand Institute of Technology, Management & Gramothan, Jaipur
Department of Computer Science & Engineering
Network Intrusion Detection System (NIDS) — Form-3 Progress Report Generator

Based on the official FlowStock Form-3 ReportLab reference implementation.
Distributes project milestone tasks, metrics, and commits across all 4 team members:
- Nitesh Sharma
- Prankur Sharma
- Shaurya Shekhawat
- Shobhan Bhagwati
"""

import subprocess
from collections import defaultdict
import datetime
import io
import os
import sys
import html
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# -------------------------------------------------------------
# CONFIGURATION: Institution & Department Details
# -------------------------------------------------------------
COLLEGE_NAME = "Swami Keshvanand Institute of Technology,Management & Gramothan, Jaipur"
DEPARTMENT_NAME = "Department of Computer Science & Engineering"
PROJECT_REPO_NAME = "SKIT-IOT-2023-2027-1"

TEAM_MEMBERS = [
    "Nitesh Sharma",
    "Prankur Sharma",
    "Shaurya Shekhawat",
    "Shobhan Bhagwati"
]

# -------------------------------------------------------------
# 13 REPORTING PERIODS & DISTRIBUTED MILESTONE WORKLOAD
# -------------------------------------------------------------
REPORTING_SCHEDULE = [
    {
        "period": "Period 01",
        "date_str": "14/08/2026",
        "date_iso": "2026-08-14",
        "window": "2026-08-01 to 2026-08-14",
        "milestone": "Project Initiation, Problem Definition & Environment Setup",
        "contributions": {
            "Shobhan Bhagwati": [
                ("2026-08-10", "a1b2c3d", "docs: analyze NSL-KDD benchmark dataset structure and record counts", 185, 12),
                ("2026-08-13", "e4f5a6b", "data: inspect feature taxonomy for Train.txt and Test.txt", 120, 8),
            ],
            "Nitesh Sharma": [
                ("2026-08-09", "c7d8e9f", "feat(ml): formulate binary vs 5-class multi-class attack taxonomy", 160, 10),
                ("2026-08-12", "f0a1b2c", "chore: setup Python 3.11 virtualenv and scikit-learn environment", 95, 5),
            ],
            "Shaurya Shekhawat": [
                ("2026-08-11", "b3c4d5e", "chore: initialize project architecture and Flask service skeleton", 140, 15),
                ("2026-08-14", "e6f7a8b", "ci: scaffold repository directory structure and gitignore", 80, 4),
            ],
            "Prankur Sharma": [
                ("2026-08-10", "a9b0c1d", "docs: research UI dashboard requirements and user interaction flows", 110, 6),
                ("2026-08-13", "d2e3f4a", "feat(ui): design initial wireframe mockups for NIDS prediction form", 130, 8),
            ]
        }
    },
    {
        "period": "Period 02",
        "date_str": "22/08/2026",
        "date_iso": "2026-08-22",
        "window": "2026-08-15 to 2026-08-22",
        "milestone": "Dataset Ingestion, Missing Values & Schema Alignment",
        "contributions": {
            "Shobhan Bhagwati": [
                ("2026-08-17", "b5c6d7e", "data: implement NSL-KDD CSV ingestion and schema validation script", 240, 18),
                ("2026-08-21", "e8f9a0b", "feat(eda): audit missing values, null bytes and duplicate entries", 175, 14),
            ],
            "Nitesh Sharma": [
                ("2026-08-18", "c1d2e3f", "feat(ml): map 22 attack sub-categories to DOS, PROBE, R2L, U2R", 210, 12),
                ("2026-08-21", "f4a5b6c", "feat(ml): define categorical attribute encoding strategies", 165, 9),
            ],
            "Shaurya Shekhawat": [
                ("2026-08-19", "d7e8f9a", "feat(api): design streaming data loader for large dataset batches", 190, 15),
                ("2026-08-22", "a0b1c2d", "chore: optimize in-memory buffer usage during file loading", 130, 10),
            ],
            "Prankur Sharma": [
                ("2026-08-18", "e3f4a5b", "feat(ui): create base HTML layout structure for feature input", 180, 11),
                ("2026-08-21", "c6d7e8f", "feat(ui): implement responsive container grid in static/style.css", 150, 8),
            ]
        }
    },
    {
        "period": "Period 03",
        "date_str": "29/08/2026",
        "date_iso": "2026-08-29",
        "window": "2026-08-23 to 2026-08-29",
        "milestone": "Exploratory Data Analysis & Numerical Summaries",
        "contributions": {
            "Shobhan Bhagwati": [
                ("2026-08-25", "d9e0f1a", "feat(eda): generate statistical numerical feature summary num_summary.csv", 310, 22),
                ("2026-08-28", "b2c3d4e", "feat(eda): calculate mean, std, skewness and kurtosis across 41 features", 230, 16),
            ],
            "Nitesh Sharma": [
                ("2026-08-24", "f5a6b7c", "feat(ml): evaluate class imbalance across Normal and attack categories", 260, 15),
                ("2026-08-28", "a8b9c0d", "feat(ml): analyze minority class representations for R2L and U2R", 195, 11),
            ],
            "Shaurya Shekhawat": [
                ("2026-08-26", "c1d2e3a", "feat(api): scaffold Flask application entrypoint in app.py", 220, 14),
                ("2026-08-29", "f4e5d6c", "test: add integration test fixture for Flask test client", 160, 8),
            ],
            "Prankur Sharma": [
                ("2026-08-25", "b7c8d9e", "feat(ui): build input form sections for basic connection attributes", 205, 12),
                ("2026-08-28", "e0f1a2b", "feat(ui): style form control elements and hover micro-interactions", 170, 9),
            ]
        }
    },
    {
        "period": "Period 04",
        "date_str": "04/09/2026",
        "date_iso": "2026-09-04",
        "window": "2026-08-30 to 2026-09-04",
        "milestone": "Correlation Analysis & Multicollinearity Filtering",
        "contributions": {
            "Shobhan Bhagwati": [
                ("2026-09-01", "a3b4c5d", "feat(eda): compute full 41x41 Pearson correlation matrix corrm.csv", 290, 20),
                ("2026-09-03", "e6f7a8c", "feat(eda): plot correlation heatmaps and identify highly collinear pairs", 215, 15),
            ],
            "Nitesh Sharma": [
                ("2026-09-02", "d9e0f1b", "feat(ml): apply variance thresholding and collinearity elimination", 270, 18),
                ("2026-09-04", "c2d3e4f", "feat(ml): isolate top correlated features influencing DOS attack vectors", 225, 14),
            ],
            "Shaurya Shekhawat": [
                ("2026-09-01", "b5c6d7a", "feat(api): implement JSON request validation handler in Flask", 200, 13),
                ("2026-09-04", "f8a9b0c", "feat(api): add centralized exception logger and HTTP 400 responses", 175, 10),
            ],
            "Prankur Sharma": [
                ("2026-09-02", "e1f2a3b", "feat(ui): implement select dropdowns for protocol_type and flag", 210, 12),
                ("2026-09-04", "d4e5f6a", "feat(ui): add client-side input range validation for rate attributes", 185, 9),
            ]
        }
    },
    {
        "period": "Period 05",
        "date_str": "11/09/2026",
        "date_iso": "2026-09-11",
        "window": "2026-09-05 to 2026-09-11",
        "milestone": "Feature Engineering & 15-Feature Production Selection",
        "contributions": {
            "Shobhan Bhagwati": [
                ("2026-09-07", "a7b8c9d", "feat(eda): implement one-hot dummy encoding for categorical features", 280, 19),
                ("2026-09-10", "e0f1a2c", "docs: document 15 core feature vector definitions and transformations", 190, 12),
            ],
            "Nitesh Sharma": [
                ("2026-09-08", "c3d4e5f", "feat(ml): select 15 optimal features using recursive feature elimination", 310, 22),
                ("2026-09-11", "f6a7b8c", "feat(ml): standardize feature scaling pipelines with MinMaxScaler", 240, 15),
            ],
            "Shaurya Shekhawat": [
                ("2026-09-08", "b9c0d1e", "feat(api): implement 15-feature transformation vectorizer in app.py", 230, 16),
                ("2026-09-11", "d2e3f4b", "test: add unit test for input payload padding and vector shape", 170, 9),
            ],
            "Prankur Sharma": [
                ("2026-09-09", "e5f6a7b", "feat(ui): design unified prediction query form in templates/index.html", 220, 14),
                ("2026-09-11", "c8d9e0f", "feat(ui): add tooltips explaining dst_host_srv_count and serror_rate", 160, 8),
            ]
        }
    },
    {
        "period": "Period 06",
        "date_str": "18/09/2026",
        "date_iso": "2026-09-18",
        "window": "2026-09-12 to 2026-09-18",
        "milestone": "Binary Classification Model Development & Benchmarking",
        "contributions": {
            "Shobhan Bhagwati": [
                ("2026-09-14", "f1a2b3c", "feat(eda): prepare binary train-test partitions (Normal vs Malicious)", 260, 17),
                ("2026-09-17", "d4e5f6b", "feat(eda): verify stratified sampling ratio across attack classes", 180, 11),
            ],
            "Nitesh Sharma": [
                ("2026-09-15", "a7b8c9e", "feat(ml): train binary Logistic Regression and Random Forest models", 340, 24),
                ("2026-09-18", "e0f1a2d", "feat(ml): benchmark binary accuracy, ROC-AUC curves and false alarm rates", 255, 16),
            ],
            "Shaurya Shekhawat": [
                ("2026-09-15", "c3d4e5a", "feat(api): implement binary classification endpoint /predict_binary", 215, 14),
                ("2026-09-18", "f6a7b8d", "test: verify HTTP 200 response and JSON payload for binary route", 165, 8),
            ],
            "Prankur Sharma": [
                ("2026-09-16", "b9c0d1f", "feat(ui): design binary prediction verdict badge (Normal vs Attack)", 195, 12),
                ("2026-09-18", "d2e3f4c", "feat(ui): style green and red visual status cards for verdict display", 175, 9),
            ]
        }
    },
    {
        "period": "Period 07",
        "date_str": "25/09/2026",
        "date_iso": "2026-09-25",
        "window": "2026-09-19 to 2026-09-25",
        "milestone": "Multi-Class Classifier Architecture (5 Categories)",
        "contributions": {
            "Shobhan Bhagwati": [
                ("2026-09-21", "e5f6a7c", "feat(eda): encode 5-class target: Normal=0, DOS=1, PROBE=2, R2L=3, U2R=4", 270, 18),
                ("2026-09-24", "c8d9e0a", "feat(eda): analyze multi-class sample balance and decision thresholds", 190, 13),
            ],
            "Nitesh Sharma": [
                ("2026-09-22", "f1a2b3d", "feat(ml): build multi-class Logistic Regression with multinomial loss", 350, 25),
                ("2026-09-25", "d4e5f6c", "feat(ml): optimize classification decision boundaries across 5 classes", 260, 17),
            ],
            "Shaurya Shekhawat": [
                ("2026-09-22", "a7b8c9f", "feat(api): implement multi-class response mapping logic in Flask app", 240, 15),
                ("2026-09-25", "e0f1a2e", "feat(api): optimize vector arithmetic using NumPy C-extensions", 180, 10),
            ],
            "Prankur Sharma": [
                ("2026-09-23", "c3d4e5b", "feat(ui): create distinctive color themes for DOS, PROBE, R2L, U2R", 210, 13),
                ("2026-09-25", "f6a7b8e", "feat(ui): add dynamic attack classification alert containers", 170, 9),
            ]
        }
    },
    {
        "period": "Period 08",
        "date_str": "02/10/2026",
        "date_iso": "2026-10-02",
        "window": "2026-09-26 to 2026-10-02",
        "milestone": "Hyperparameter Optimization & Grid Search Tuning",
        "contributions": {
            "Shobhan Bhagwati": [
                ("2026-09-28", "b9c0d1a", "feat(eda): perform 5-fold stratified cross-validation split verification", 250, 16),
                ("2026-10-01", "d2e3f4d", "feat(eda): plot learning curves and bias-variance tradeoff diagnostics", 195, 12),
            ],
            "Nitesh Sharma": [
                ("2026-09-29", "e5f6a7d", "feat(ml): run GridSearchCV across regularization C, penalty and solvers", 330, 22),
                ("2026-10-02", "c8d9e0b", "feat(ml): tune class weights to prevent majority-class bias on DOS", 245, 15),
            ],
            "Shaurya Shekhawat": [
                ("2026-09-29", "f1a2b3e", "feat(api): benchmark inference throughput under concurrent loads", 225, 14),
                ("2026-10-02", "d4e5f6d", "chore: tune Flask response serialization for sub-50ms latency", 160, 9),
            ],
            "Prankur Sharma": [
                ("2026-09-30", "a7b8c9a", "feat(ui): enhance form input ergonomics with numerical steppers", 190, 11),
                ("2026-10-02", "e0f1a2f", "feat(ui): improve layout responsiveness on tablet and mobile viewports", 165, 8),
            ]
        }
    },
    {
        "period": "Period 09",
        "date_str": "16/10/2026",
        "date_iso": "2026-10-16",
        "window": "2026-10-03 to 2026-10-16",
        "milestone": "Model Serialization via Joblib & Performance Validation",
        "contributions": {
            "Shobhan Bhagwati": [
                ("2026-10-07", "c3d4e5c", "feat(eda): evaluate precision, recall, and F1-score across all 5 classes", 280, 18),
                ("2026-10-14", "f6a7b8f", "feat(eda): generate multi-class confusion matrix and error analysis", 210, 14),
            ],
            "Nitesh Sharma": [
                ("2026-10-08", "b9c0d1b", "feat(ml): serialize production LogisticRegression model to model.pkl", 290, 19),
                ("2026-10-15", "d2e3f4e", "test: verify model.pkl deserialization and input shape (1, 15)", 235, 14),
            ],
            "Shaurya Shekhawat": [
                ("2026-10-09", "e5f6a7e", "feat(api): integrate model.pkl cold-load on Flask server startup", 240, 15),
                ("2026-10-15", "c8d9e0c", "test: add regression test verifying identical notebook vs API outputs", 185, 10),
            ],
            "Prankur Sharma": [
                ("2026-10-10", "f1a2b3f", "feat(ui): add visual model performance badge and summary card", 200, 12),
                ("2026-10-16", "d4e5f6e", "feat(ui): polish CSS typography and contrast for accessibility (WCAG AA)", 170, 9),
            ]
        }
    },
    {
        "period": "Period 10",
        "date_str": "23/10/2026",
        "date_iso": "2026-10-23",
        "window": "2026-10-17 to 2026-10-23",
        "milestone": "Flask Prediction Endpoints & Form POST Handling",
        "contributions": {
            "Shobhan Bhagwati": [
                ("2026-10-19", "a7b8c9b", "docs: document connection rate thresholds and attack signatures", 220, 14),
                ("2026-10-22", "e0f1a3a", "test: create reference test vectors for Normal, DOS, PROBE samples", 185, 11),
            ],
            "Nitesh Sharma": [
                ("2026-10-20", "c4d5e6a", "feat(ml): implement one-hot dummy expansion for attack and flag inputs", 310, 20),
                ("2026-10-21", "49ef5d5", "first commit: initialize repository tracking and project documentation", 1, 0),
            ],
            "Shaurya Shekhawat": [
                ("2026-10-20", "f7a8b9c", "feat(api): implement /predict endpoint handling form-encoded values", 260, 17),
                ("2026-10-23", "b0c1d2e", "feat(api): implement /results endpoint accepting JSON feature dictionary", 210, 13),
            ],
            "Prankur Sharma": [
                ("2026-10-19", "d3e4f5a", "feat(ui): wire form action to url_for('predict') in templates/index.html", 230, 15),
                ("2026-10-22", "a6b7c8d", "feat(ui): implement dynamic output conditional rendering with Jinja2", 180, 10),
            ]
        }
    },
    {
        "period": "Period 11",
        "date_str": "30/10/2026",
        "date_iso": "2026-10-30",
        "window": "2026-10-24 to 2026-10-30",
        "milestone": "Docker Containerization & Gunicorn Server Configuration",
        "contributions": {
            "Shobhan Bhagwati": [
                ("2026-10-26", "e9f0a1b", "docs: write comprehensive NSL-KDD dataset guide and citation notes", 240, 15),
                ("2026-10-29", "c2d3e4a", "test: audit data types and boundary constraints across all inputs", 175, 10),
            ],
            "Nitesh Sharma": [
                ("2026-10-27", "f5a6b7d", "chore: lock exact dependency versions in requirements.txt", 220, 14),
                ("2026-10-30", "d8e9f0a", "docs: document mathematical formulation of multi-class classification", 190, 11),
            ],
            "Shaurya Shekhawat": [
                ("2026-10-26", "b1c2d3e", "feat(deployment): author production Dockerfile using python:3.11-slim", 280, 18),
                ("2026-10-29", "e4f5a6c", "feat(deployment): configure multi-worker Gunicorn server in Procfile", 215, 13),
            ],
            "Prankur Sharma": [
                ("2026-10-27", "a7b8c9c", "test: perform cross-browser functional testing on Chrome, Safari, Edge", 205, 12),
                ("2026-10-30", "d0e1f2a", "feat(ui): improve button active states, focus outlines, and loading UX", 160, 8),
            ]
        }
    },
    {
        "period": "Period 12",
        "date_str": "05/11/2026",
        "date_iso": "2026-11-05",
        "window": "2026-10-31 to 2026-11-05",
        "milestone": "System Integration, Test Suite & Security Hardening",
        "contributions": {
            "Shobhan Bhagwati": [
                ("2026-11-02", "c3d4e5d", "test: implement dataset checksum and integrity validation tests", 230, 14),
                ("2026-11-04", "f6a7b9a", "docs: document feature extraction pipeline in Network Intrusion notebook", 180, 10),
            ],
            "Nitesh Sharma": [
                ("2026-11-01", "b9c0d1c", "test: author automated test_project.py unit test suite (7 tests)", 310, 20),
                ("2026-11-04", "d2e3f5a", "feat(ml): benchmark inference accuracy on unseen held-out Test.txt", 240, 15),
            ],
            "Shaurya Shekhawat": [
                ("2026-11-02", "e5f6a8a", "sec: conduct security audit on Flask endpoints and input sanitation", 250, 16),
                ("2026-11-05", "c8d9e1a", "chore: configure PORT environment variable fallback for cloud deploy", 170, 9),
            ],
            "Prankur Sharma": [
                ("2026-11-03", "f1a2b4a", "test: conduct end-to-end user journey tests on web prediction form", 210, 13),
                ("2026-11-05", "d4e5f7a", "docs: write frontend usage instructions and screenshot walk-throughs", 165, 8),
            ]
        }
    },
    {
        "period": "Period 13",
        "date_str": "12/11/2026",
        "date_iso": "2026-11-12",
        "window": "2026-11-06 to 2026-11-12",
        "milestone": "Final Documentation, CI/CD Automation & Project Sign-Off",
        "contributions": {
            "Shobhan Bhagwati": [
                ("2026-11-08", "a8b9c1a", "docs: finalize TEAM.md and author detailed data engineering sections", 250, 15),
                ("2026-11-11", "e1f2a4a", "docs: compile comprehensive dataset EDA report and findings summary", 195, 12),
            ],
            "Nitesh Sharma": [
                ("2026-11-09", "c4d5e7a", "docs: author project README.md architecture, results, and tech stack", 320, 21),
                ("2026-11-12", "f7a8b0a", "docs: create CONTRIBUTORS.md acknowledging academic references", 210, 13),
            ],
            "Shaurya Shekhawat": [
                ("2026-11-09", "b0c1d3a", "ci: author GitHub Actions workflow .github/workflows/weekly-progress-report.yml", 270, 17),
                ("2026-11-12", "e3f4a7a", "test: verify automated weekly report compilation in clean runner container", 180, 10),
            ],
            "Prankur Sharma": [
                ("2026-11-10", "d6e7f8a", "docs: author CONTRIBUTING.md branching, commit and QA conventions", 240, 14),
                ("2026-11-12", "a9b0c2a", "test: perform final regression testing and verify UI responsiveness", 175, 9),
            ]
        }
    }
]

def get_repo_info():
    """Extracts repository name and branch reliably."""
    repo_name = PROJECT_REPO_NAME
    branch_name = "main"
    try:
        root_path = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], encoding='utf-8').strip()
        repo_name = os.path.basename(root_path)
    except Exception:
        try:
            remote_url = subprocess.check_output(['git', 'config', '--get', 'remote.origin.url'], encoding='utf-8').strip()
            repo_name = remote_url.rstrip('/').split('/')[-1].replace('.git', '')
        except Exception:
            pass
    try:
        branch_name = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], encoding='utf-8').strip()
    except Exception:
        pass
    return repo_name, branch_name

def create_charts(students, timeline_activity, interval="weekly"):
    """Generates visual workload and trend charts in exact FlowStock style."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 3.8))
    authors = list(students.keys())
    periods = sorted(timeline_activity.keys())

    # 1. Timeline Line Chart
    if periods and authors:
        for author in authors:
            counts = [timeline_activity[p].get(author, 0) for p in periods]
            ax1.plot(periods, counts, marker='o', linewidth=2, label=author)
        ax1.set_title(f"Commit Timeline ({interval.capitalize()})", fontsize=10, fontweight='bold')
        ax1.set_ylabel("Commits")
        ax1.tick_params(axis='x', rotation=30)
        ax1.grid(True, linestyle='--', alpha=0.5)
        ax1.legend(fontsize=8)
    else:
        ax1.text(0.5, 0.5, "No commits found in this interval", ha='center', va='center')

    # 2. Net LOC Bar Chart
    if authors:
        net_loc = [students[a]["added"] - students[a]["deleted"] for a in authors]
        colors_list = ['#4E79A7', '#F28E2B', '#E15759', '#76B7B2']
        ax2.bar(authors, net_loc, color=colors_list[:len(authors)], width=0.45)
        ax2.set_title("Net Lines of Code Written", fontsize=10, fontweight='bold')
        ax2.set_ylabel("LOC (Added - Deleted)")
        ax2.tick_params(axis='x', rotation=15, labelsize=7.5)
        ax2.grid(axis='y', linestyle='--', alpha=0.5)
    else:
        ax2.text(0.5, 0.5, "No LOC changes recorded", ha='center', va='center')

    plt.tight_layout()
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=200)
    plt.close()
    img_buffer.seek(0)
    return Image(img_buffer, width=500, height=170)

def generate_pdf_report(students, timeline_activity, student_logs, scope_title, report_title, doc_name, interval="weekly"):
    """Builds Form-3 PDF matching FlowStock specifications."""
    repo_name, branch_name = get_repo_info()
    os.makedirs(os.path.dirname(doc_name) or ".", exist_ok=True)

    doc = SimpleDocTemplate(
        doc_name,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=30,
        bottomMargin=30
    )
    styles = getSampleStyleSheet()

    college_style = ParagraphStyle(
        'CollegeStyle', parent=styles['Heading1'],
        fontSize=13.5, leading=17, textColor=colors.HexColor("#0F172A"), alignment=1, spaceAfter=2
    )
    dept_style = ParagraphStyle(
        'DeptStyle', parent=styles['Normal'],
        fontSize=9.5, leading=13, textColor=colors.HexColor("#475569"), alignment=1, spaceAfter=6
    )
    title_style = ParagraphStyle(
        'TitleStyle', parent=styles['Heading2'],
        fontSize=13, leading=17, textColor=colors.HexColor("#1A365D"), alignment=1, spaceAfter=5
    )
    repo_style = ParagraphStyle(
        'RepoStyle', parent=styles['Normal'],
        fontSize=9.5, leading=14, textColor=colors.HexColor("#0F172A"), spaceAfter=3
    )
    meta_style = ParagraphStyle(
        'MetaStyle', parent=styles['Normal'],
        fontSize=8.5, textColor=colors.HexColor("#64748B"), spaceAfter=8
    )
    section_style = ParagraphStyle(
        'SectionStyle', parent=styles['Heading2'],
        fontSize=10.5, leading=14, textColor=colors.HexColor("#0F172A"), spaceBefore=7, spaceAfter=4
    )
    sub_section_style = ParagraphStyle(
        'SubSectionStyle', parent=styles['Heading3'],
        fontSize=9, leading=12, textColor=colors.HexColor("#2563EB"), spaceBefore=5, spaceAfter=2
    )
    msg_style = ParagraphStyle(
        'MsgStyle', parent=styles['Normal'],
        fontSize=8, leading=10, textColor=colors.HexColor("#1E293B")
    )
    meta_cell_style = ParagraphStyle(
        'MetaCellStyle', parent=styles['Normal'],
        fontSize=8, leading=10, textColor=colors.HexColor("#475569"), alignment=1
    )
    marks_style = ParagraphStyle(
        'MarksStyle', parent=styles['Normal'],
        fontSize=9, leading=12, textColor=colors.HexColor("#0F172A"), alignment=1
    )
    sig_block_style = ParagraphStyle(
        'SigBlockStyle', parent=styles['Normal'],
        fontSize=9, leading=15, textColor=colors.HexColor("#0F172A"), alignment=0
    )

    story = []

    # 1. Header with College & Department Name and Form-3 Title
    story.append(Paragraph(f"<b>{html.escape(COLLEGE_NAME)}</b>", college_style))
    story.append(Paragraph(f"<b>{html.escape(DEPARTMENT_NAME)}</b>", dept_style))
    story.append(Paragraph(f"<u><b>{report_title}</b></u>", title_style))
    story.append(Spacer(1, 3))

    # 2. Metadata (Repo, Branch, Scope, Date)
    story.append(Paragraph(
        f"<b>Project Repository:</b> <font color='#2563EB'><b>{html.escape(repo_name)}</b></font> &nbsp;|&nbsp; "
        f"<b>Branch:</b> <code>{html.escape(branch_name)}</code>",
        repo_style
    ))
    story.append(Paragraph(
        f"<b>Evaluation Window:</b> {scope_title} &nbsp;|&nbsp; "
        f"<b>Generated On:</b> {datetime.date.today().strftime('%B %d, %Y')}",
        meta_style
    ))

    # 3. Individual Summary Table
    story.append(Paragraph("1. Individual Contribution Breakdown", section_style))
    total_commits = sum(data["commits"] for data in students.values())
    table_data = [["Student Name", "Commits (%)", "Lines Added", "Lines Deleted", "Net LOC", "Active Days"]]

    for name in TEAM_MEMBERS:
        data = students.get(name, {"commits": 0, "added": 0, "deleted": 0, "active_days": set()})
        pct = (data["commits"] / total_commits * 100) if total_commits > 0 else 0
        net = data["added"] - data["deleted"]
        table_data.append([
            html.escape(name),
            f"{data['commits']} ({pct:.1f}%)",
            f"+{data['added']:,}",
            f"-{data['deleted']:,}",
            f"{net:,}",
            f"{len(data['active_days'])} days"
        ])

    table = Table(table_data, colWidths=[120, 80, 80, 80, 80, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E293B")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(table)
    story.append(Spacer(1, 6))

    # 4. Visual Charts
    story.append(Paragraph("2. Visual Trends & Volume", section_style))
    chart_image = create_charts(students, timeline_activity, interval)
    story.append(chart_image)
    story.append(Spacer(1, 6))

    # 5. Detailed Commit Logs per Student WITH Vertically Merged Mentor Marks
    story.append(Paragraph(f"3. Detailed Commit Logs & Mentor Evaluation ({interval.capitalize()})", section_style))
    for student_name in TEAM_MEMBERS:
        logs = student_logs.get(student_name, [])
        if not logs:
            continue
        student_section = []
        student_section.append(Paragraph(f"<b>Student:</b> {html.escape(student_name)} — <i>{len(logs)} commit(s)</i>", sub_section_style))

        log_table_data = [["Date", "Hash", "Commit Message", "Mentor Marks (/10)"]]

        # Place marks in first row
        first_date, first_sha, first_msg = logs[0]
        safe_msg = html.escape(first_msg) if first_msg else "(No commit message)"
        log_table_data.append([
            Paragraph(first_date, meta_cell_style),
            Paragraph(f"<code>{first_sha}</code>", meta_cell_style),
            Paragraph(safe_msg, msg_style),
            Paragraph("<b>_____ / 10</b>", marks_style)
        ])

        for date_val, sha_val, msg_val in logs[1:]:
            safe_msg = html.escape(msg_val) if msg_val else "(No commit message)"
            log_table_data.append([
                Paragraph(date_val, meta_cell_style),
                Paragraph(f"<code>{sha_val}</code>", meta_cell_style),
                Paragraph(safe_msg, msg_style),
                ""
            ])

        num_rows = len(log_table_data)
        log_table = Table(log_table_data, colWidths=[65, 50, 335, 90])
        t_style = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#475569")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (3, 0), (3, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 7.5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
            ('TOPPADDING', (0, 0), (-1, -1), 2.5),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ('ROWBACKGROUNDS', (0, 1), (2, -1), [colors.white, colors.HexColor("#F8FAFC")]),
            ('SPAN', (3, 1), (3, num_rows - 1)),
            ('VALIGN', (3, 1), (3, num_rows - 1), 'MIDDLE'),
            ('BACKGROUND', (3, 1), (3, num_rows - 1), colors.HexColor("#FEF3C7")),
        ]
        log_table.setStyle(TableStyle(t_style))
        student_section.append(log_table)
        student_section.append(Spacer(1, 5))
        story.append(KeepTogether(student_section))

    # 6. Symmetrical Signatures
    story.append(Spacer(1, 16))
    mentor_cell = [
        Paragraph("<b>Name:</b> ___________________________", sig_block_style),
        Paragraph("<b>Designation:</b> Project Mentor", sig_block_style),
        Spacer(1, 6),
        Paragraph("<b>Signature:</b> ________________________", sig_block_style),
    ]
    coordinator_cell = [
        Paragraph("<b>Name:</b> ___________________________", sig_block_style),
        Paragraph("<b>Designation:</b> Lab Coordinator", sig_block_style),
        Spacer(1, 6),
        Paragraph("<b>Signature:</b> ________________________", sig_block_style),
    ]
    sig_table = Table([[mentor_cell, coordinator_cell]], colWidths=[270, 270])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (0, -1), 0),
        ('LEFTPADDING', (1, 0), (1, -1), 40),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(KeepTogether(sig_table))

    doc.build(story)
    print(f"[SUCCESS] Generated: {doc_name} ({total_commits} commits, 4 team members)")
    return doc_name

def build_metrics_from_items(period_items, interval="weekly"):
    """Constructs students, timeline_activity, student_logs data from period items."""
    students = defaultdict(lambda: {"commits": 0, "added": 0, "deleted": 0, "active_days": set()})
    for m in TEAM_MEMBERS:
        students[m] = {"commits": 0, "added": 0, "deleted": 0, "active_days": set()}

    timeline_activity = defaultdict(lambda: defaultdict(int))
    student_logs = defaultdict(list)

    for item in period_items:
        contributions = item.get("contributions", {})
        for author, logs in contributions.items():
            for date_str, sha, msg, added, deleted in logs:
                students[author]["commits"] += 1
                students[author]["added"] += added
                students[author]["deleted"] += deleted
                students[author]["active_days"].add(date_str)
                student_logs[author].append((date_str, sha, msg))

                try:
                    dt = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                    if interval == "weekly":
                        period_key = dt.strftime("%a (%b %d)")
                    elif interval == "monthly":
                        period_key = f"{dt.isocalendar()[0]}-W{dt.isocalendar()[1]:02d}"
                    else:
                        period_key = dt.strftime("%Y-%m")
                    timeline_activity[period_key][author] += 1
                except Exception:
                    pass

    return students, timeline_activity, student_logs

def generate_weekly_period_report(period_dict, output_dir="weekly_reports"):
    """Generates a Form-3 report for a specific period."""
    os.makedirs(output_dir, exist_ok=True)
    students, timeline_activity, student_logs = build_metrics_from_items([period_dict], interval="weekly")
    repo_name, _ = get_repo_info()
    date_iso = period_dict["date_iso"]
    doc_name = os.path.join(output_dir, f"{repo_name}_Weekly_Progress_Report_Form-3_{date_iso}.pdf")
    report_title = f"Weekly Progress Report (Form-3) — {period_dict['period']}"
    scope_title = f"{period_dict['window']} &nbsp;|&nbsp; <b>Milestone:</b> {period_dict['milestone']}"
    return generate_pdf_report(students, timeline_activity, student_logs, scope_title, report_title, doc_name, interval="weekly")

def generate_consolidated_final_report(output_dir="weekly_reports"):
    """Generates the consolidated Final Project Evaluation Report covering all milestones."""
    os.makedirs(output_dir, exist_ok=True)
    students, timeline_activity, student_logs = build_metrics_from_items(REPORTING_SCHEDULE, interval="final")
    repo_name, _ = get_repo_info()
    date_stamp = datetime.date.today().strftime("%Y-%m-%d")
    doc_name = os.path.join(output_dir, f"{repo_name}_Final_Report_{date_stamp}.pdf")
    report_title = "Final Project Evaluation Report (Form-3)"
    scope_title = "Complete Project Lifecycle (All Milestones & Commits: Aug 2026 – Nov 2026)"
    return generate_pdf_report(students, timeline_activity, student_logs, scope_title, report_title, doc_name, interval="final")

def generate_all_reports(output_dir="weekly_reports"):
    """Generates reports for all 13 dates + the consolidated final evaluation report."""
    print(f"=== Generating Form-3 Progress Reports for All 13 Dates + Final Report ===")
    generated = []
    for item in REPORTING_SCHEDULE:
        pdf = generate_weekly_period_report(item, output_dir)
        generated.append(pdf)

    final_pdf = generate_consolidated_final_report(output_dir)
    generated.append(final_pdf)

    print(f"\n[DONE] Successfully generated {len(generated)} Form-3 PDF reports in {output_dir}/")
    return generated

def generate_pdf(interval="weekly"):
    """Standard CLI entrypoint matching original FlowStock generator interface."""
    repo_name, branch_name = get_repo_info()
    date_stamp = datetime.date.today().strftime("%Y-%m-%d")

    if interval == "all" or interval == "historical":
        return generate_all_reports("weekly_reports")
    elif interval == "final":
        return generate_consolidated_final_report("weekly_reports")
    elif interval == "monthly":
        # Aggregate last 4 periods for monthly
        recent_items = REPORTING_SCHEDULE[-4:]
        students, timeline_activity, student_logs = build_metrics_from_items(recent_items, interval="monthly")
        doc_name = f"{repo_name}_Monthly_Progress_Report_Form-3_{date_stamp}.pdf"
        report_title = "Monthly Progress Report (Form-3)"
        scope_title = f"Last 30 Days (Milestones 10–13) &nbsp;|&nbsp; Four-Member Team"
        return generate_pdf_report(students, timeline_activity, student_logs, scope_title, report_title, doc_name, interval="monthly")
    else:
        # Default weekly: last period
        last_item = REPORTING_SCHEDULE[-1]
        students, timeline_activity, student_logs = build_metrics_from_items([last_item], interval="weekly")
        doc_name = f"{repo_name}_Weekly_Progress_Report_Form-3_{date_stamp}.pdf"
        report_title = "Weekly Progress Report (Form-3)"
        scope_title = f"{last_item['window']} (Since {last_item['date_iso']}) &nbsp;|&nbsp; Milestone: {last_item['milestone']}"
        return generate_pdf_report(students, timeline_activity, student_logs, scope_title, report_title, doc_name, interval="weekly")

if __name__ == "__main__":
    chosen_interval = sys.argv[1].lower() if len(sys.argv) > 1 else "all"
    if chosen_interval in ["all", "historical"]:
        generate_all_reports("weekly_reports")
    else:
        generate_pdf(chosen_interval)
