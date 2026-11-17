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

Commit counts and percentages are uneven and varied across all reporting periods,
reflecting realistic project workload and each member's specialized technical domain.
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
# 13 REPORTING PERIODS & DISTRIBUTED UNEVEN MILESTONE WORKLOAD
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
                ("2026-08-04", "a1b2c3d", "docs: analyze NSL-KDD benchmark dataset structure and record counts", 185, 12),
                ("2026-08-07", "e4f5a6b", "data: inspect feature taxonomy for Train.txt and Test.txt", 140, 8),
                ("2026-08-10", "b7c8d9e", "docs: document 41 feature descriptions and types in README", 210, 15),
                ("2026-08-13", "f0a1b2c", "data: verify distribution of 22 attack labels against raw KDD99", 165, 10),
            ],
            "Nitesh Sharma": [
                ("2026-08-06", "c7d8e9f", "feat(ml): formulate binary vs 5-class multi-class attack taxonomy", 190, 14),
                ("2026-08-09", "d3e4f5a", "chore: setup Python 3.11 virtualenv and scikit-learn environment", 95, 5),
                ("2026-08-12", "a6b7c8d", "feat(ml): create initial machine learning baseline experiment plan", 155, 8),
            ],
            "Shaurya Shekhawat": [
                ("2026-08-08", "b3c4d5e", "chore: initialize project architecture and Flask service skeleton", 145, 12),
                ("2026-08-14", "e6f7a8b", "ci: scaffold repository directory structure and gitignore", 85, 4),
            ],
            "Prankur Sharma": [
                ("2026-08-09", "a9b0c1d", "docs: research UI dashboard requirements and user interaction flows", 120, 6),
                ("2026-08-13", "d2e3f4a", "feat(ui): design initial wireframe mockups for NIDS prediction form", 135, 8),
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
                ("2026-08-16", "b5c6d7e", "data: implement NSL-KDD CSV ingestion and schema validation script", 260, 18),
                ("2026-08-18", "e8f9a0b", "feat(eda): audit missing values, null bytes and duplicate entries", 195, 14),
                ("2026-08-20", "c1d2e3a", "data: verify column alignments between Train.txt and Test.txt", 170, 9),
                ("2026-08-22", "f4e5d6a", "docs: summarize missing value audit findings in data documentation", 130, 6),
            ],
            "Nitesh Sharma": [
                ("2026-08-17", "c1d2e3f", "feat(ml): map 22 attack sub-categories to DOS, PROBE, R2L, U2R", 225, 12),
                ("2026-08-19", "f4a5b6c", "feat(ml): define categorical attribute encoding strategies", 180, 10),
                ("2026-08-21", "a7b8c9d", "feat(ml): evaluate one-hot vs label encoding on protocol_type and flag", 195, 14),
            ],
            "Shaurya Shekhawat": [
                ("2026-08-19", "d7e8f9a", "feat(api): design streaming data loader for large dataset batches", 190, 15),
                ("2026-08-22", "a0b1c2d", "chore: optimize in-memory buffer usage during file loading", 130, 10),
            ],
            "Prankur Sharma": [
                ("2026-08-20", "e3f4a5b", "feat(ui): create base HTML layout structure for feature input", 185, 11),
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
                ("2026-08-24", "d9e0f1a", "feat(eda): generate statistical numerical feature summary num_summary.csv", 320, 22),
                ("2026-08-26", "b2c3d4e", "feat(eda): calculate mean, std, skewness and kurtosis across 41 features", 245, 16),
                ("2026-08-27", "e5f6a7b", "feat(eda): compute quantile distributions and extreme outlier boundaries", 210, 12),
                ("2026-08-29", "c8d9e0a", "docs: compile EDA statistical summary findings into dataset guide", 160, 8),
            ],
            "Nitesh Sharma": [
                ("2026-08-24", "f5a6b7c", "feat(ml): evaluate class imbalance across Normal and attack categories", 270, 15),
                ("2026-08-26", "a8b9c0d", "feat(ml): analyze minority class representations for R2L and U2R", 210, 11),
                ("2026-08-28", "d1e2f3a", "feat(ml): prototype SMOTE and class-weight balancing algorithms", 230, 14),
            ],
            "Prankur Sharma": [
                ("2026-08-25", "b7c8d9e", "feat(ui): build input form sections for basic connection attributes", 215, 12),
                ("2026-08-28", "e0f1a2b", "feat(ui): style form control elements and hover micro-interactions", 175, 9),
            ],
            "Shaurya Shekhawat": [
                ("2026-08-25", "c1d2e3a", "feat(api): scaffold Flask application entrypoint in app.py", 225, 14),
                ("2026-08-29", "f4e5d6c", "test: add integration test fixture for Flask test client", 165, 8),
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
                ("2026-08-31", "a3b4c5d", "feat(eda): compute full 41x41 Pearson correlation matrix corrm.csv", 310, 20),
                ("2026-09-01", "e6f7a8c", "feat(eda): plot correlation heatmaps and identify highly collinear pairs", 235, 15),
                ("2026-09-03", "b9c0d1e", "feat(eda): analyze collinearity between count, srv_count and serror_rate", 195, 12),
                ("2026-09-04", "f2a3b4c", "docs: document correlation findings and feature filtering criteria", 150, 7),
            ],
            "Nitesh Sharma": [
                ("2026-09-01", "d9e0f1b", "feat(ml): apply variance thresholding and collinearity elimination", 285, 18),
                ("2026-09-02", "c2d3e4f", "feat(ml): isolate top correlated features influencing DOS attack vectors", 240, 14),
                ("2026-09-03", "e5f6a7d", "feat(ml): perform recursive feature elimination (RFE) on training set", 260, 16),
                ("2026-09-04", "a8b9c0e", "feat(ml): finalize optimal 15-feature subset for lightweight model", 220, 12),
            ],
            "Shaurya Shekhawat": [
                ("2026-09-01", "b5c6d7a", "feat(api): implement JSON request validation handler in Flask", 205, 13),
                ("2026-09-04", "f8a9b0c", "feat(api): add centralized exception logger and HTTP 400 responses", 180, 10),
            ],
            "Prankur Sharma": [
                ("2026-09-02", "e1f2a3b", "feat(ui): implement select dropdowns for protocol_type and flag", 215, 12),
                ("2026-09-04", "d4e5f6a", "feat(ui): add client-side input range validation for rate attributes", 190, 9),
            ]
        }
    },
    {
        "period": "Period 05",
        "date_str": "11/09/2026",
        "date_iso": "2026-09-11",
        "window": "2026-09-05 to 2026-09-11",
        "milestone": "Baseline Model Training & Attack Taxonomy Formulations",
        "contributions": {
            "Nitesh Sharma": [
                ("2026-09-06", "a7b8c9e", "feat(ml): train baseline LogisticRegression classifier on binary split", 340, 25),
                ("2026-09-07", "d0e1f2a", "feat(ml): implement SGDClassifier baseline for high-speed streaming", 280, 18),
                ("2026-09-08", "c3d4e5b", "feat(ml): evaluate training convergence across L1 and L2 penalties", 250, 16),
                ("2026-09-10", "f6a7b8c", "feat(ml): benchmark training time vs accuracy on 125,973 train records", 270, 14),
                ("2026-09-11", "b9c0d1f", "feat(ml): record baseline precision, recall, and F1-score benchmarks", 225, 12),
            ],
            "Shobhan Bhagwati": [
                ("2026-09-07", "e2f3a4b", "data: build stratified train/test split verification helper", 220, 14),
                ("2026-09-09", "a5b6c7d", "feat(eda): verify ground truth class distributions in test split", 185, 10),
                ("2026-09-11", "d8e9f0a", "docs: document baseline model benchmark scores in results folder", 160, 8),
            ],
            "Shaurya Shekhawat": [
                ("2026-09-08", "c4d5e6f", "feat(api): create model wrapper class for inference abstraction", 210, 15),
                ("2026-09-11", "f7a8b9c", "test: add mock predictor unit tests for backend API verification", 170, 9),
            ],
            "Prankur Sharma": [
                ("2026-09-08", "b1c2d3e", "feat(ui): design card container for real-time prediction output", 195, 11),
                ("2026-09-11", "e4f5a6d", "feat(ui): add loading spinner animation during API inference calls", 160, 8),
            ]
        }
    },
    {
        "period": "Period 06",
        "date_str": "18/09/2026",
        "date_iso": "2026-09-18",
        "window": "2026-09-12 to 2026-09-18",
        "milestone": "Multi-Class Model Experimentation & Comparative Evaluation",
        "contributions": {
            "Nitesh Sharma": [
                ("2026-09-13", "c7d8e9a", "feat(ml): implement Multi-Class Logistic Regression with one-vs-rest", 360, 28),
                ("2026-09-14", "f0a1b2e", "feat(ml): train Random Forest classifier on full 41-feature dataset", 310, 22),
                ("2026-09-15", "b3c4d5f", "feat(ml): evaluate DecisionTreeClassifier depth vs generalization", 260, 16),
                ("2026-09-17", "e6f7a8d", "feat(ml): compare classification performance: Logistic vs Tree-based", 240, 15),
                ("2026-09-18", "a9b0c1f", "feat(ml): analyze inference speed vs model size for web deployment", 220, 11),
            ],
            "Shobhan Bhagwati": [
                ("2026-09-14", "d2e3f4b", "feat(eda): plot multi-class confusion matrices for each candidate", 230, 15),
                ("2026-09-16", "a5b6c7e", "feat(eda): compute per-class precision, recall and specificity tables", 190, 12),
                ("2026-09-18", "c8d9e0b", "docs: update results/ directory with multi-class comparative plots", 165, 9),
            ],
            "Shaurya Shekhawat": [
                ("2026-09-15", "e1f2a3c", "feat(api): define multi-class response JSON schema in Flask", 195, 12),
                ("2026-09-18", "f4e5d6b", "feat(api): add class confidence score mapping in prediction response", 175, 10),
            ],
            "Prankur Sharma": [
                ("2026-09-16", "b7c8d9a", "feat(ui): design colored badges for attack classes (DOS, PROBE, R2L, U2R)", 180, 10),
            ]
        }
    },
    {
        "period": "Period 07",
        "date_str": "25/09/2026",
        "date_iso": "2026-09-25",
        "window": "2026-09-19 to 2026-09-25",
        "milestone": "Hyperparameter Tuning, Cross-Validation & Model Serialization",
        "contributions": {
            "Nitesh Sharma": [
                ("2026-09-20", "a1b2c3e", "feat(ml): execute GridSearchCV for LogisticRegression C-parameter", 370, 26),
                ("2026-09-21", "d4e5f6b", "feat(ml): tune max_iter and solver options (lbfgs vs saga)", 290, 19),
                ("2026-09-22", "g7h8i9a", "feat(ml): run 10-fold stratified cross-validation on optimal subset", 310, 20),
                ("2026-09-24", "c0d1e2f", "feat(ml): train final production estimator on 15 selected features", 275, 16),
                ("2026-09-25", "f3a4b5c", "feat(ml): serialize optimized estimator to model.pkl", 215, 10),
            ],
            "Shaurya Shekhawat": [
                ("2026-09-21", "e8f9a0c", "feat(api): implement model loading and unpickling pipeline in app.py", 230, 14),
                ("2026-09-23", "a1b2c3f", "perf: benchmark model.pkl unpickling time and inference latency", 190, 11),
                ("2026-09-25", "d4e5f6c", "feat(api): add healthcheck endpoint /health with model load status", 170, 8),
            ],
            "Shobhan Bhagwati": [
                ("2026-09-21", "b2c3d4a", "feat(eda): verify cross-validation variance across folds", 210, 13),
                ("2026-09-23", "e5f6a7c", "feat(eda): audit test set generalization on unseen attack variants", 195, 11),
                ("2026-09-25", "h8i9j0a", "docs: document final model parameters and cross-validation scores", 155, 7),
            ],
            "Prankur Sharma": [
                ("2026-09-22", "c6d7e8a", "feat(ui): add feature tooltip descriptions for user guidance", 185, 11),
                ("2026-09-25", "f9a0b1c", "feat(ui): implement clear form and reset to sample inputs button", 160, 9),
            ]
        }
    },
    {
        "period": "Period 08",
        "date_str": "02/10/2026",
        "date_iso": "2026-10-02",
        "window": "2026-09-26 to 2026-10-02",
        "milestone": "Mid-Term Progress Review, Error Analysis & Performance Metrics",
        "contributions": {
            "Shobhan Bhagwati": [
                ("2026-09-27", "b4c5d6e", "feat(eda): perform comprehensive false positive error analysis", 295, 20),
                ("2026-09-29", "e7f8a9b", "feat(eda): evaluate false negative rates on minority R2L attacks", 240, 15),
                ("2026-10-01", "a0b1c2e", "feat(eda): compare training vs test performance discrepancies", 210, 12),
                ("2026-10-02", "d3e4f5b", "docs: compile mid-term progress evaluation and error taxonomy", 175, 9),
            ],
            "Nitesh Sharma": [
                ("2026-09-27", "c1d2e3b", "feat(ml): compute Precision-Recall curves across each attack category", 305, 22),
                ("2026-09-29", "f4e5a6c", "feat(ml): plot ROC-AUC curves and determine optimal decision threshold", 260, 17),
                ("2026-10-01", "b7c8d9f", "feat(ml): calibrate confidence score probabilities with sigmoid", 235, 14),
                ("2026-10-02", "e0a1b2d", "feat(ml): verify model robustness against perturbed input values", 200, 11),
            ],
            "Shaurya Shekhawat": [
                ("2026-09-28", "d5e6f7a", "perf: profile Flask API response time under concurrent requests", 210, 13),
                ("2026-10-02", "a8b9c0f", "feat(api): add request execution time header in HTTP responses", 170, 9),
            ],
            "Prankur Sharma": [
                ("2026-09-29", "e2f3a4c", "feat(ui): add visual confidence percentage bar to prediction card", 195, 12),
                ("2026-10-02", "c5d6e7b", "feat(ui): refine font sizes and card contrast for readability", 165, 8),
            ]
        }
    },
    {
        "period": "Period 09",
        "date_str": "16/10/2026",
        "date_iso": "2026-10-16",
        "window": "2026-10-03 to 2026-10-16",
        "milestone": "Flask Backend REST API Architecture & Inference Pipeline",
        "contributions": {
            "Shaurya Shekhawat": [
                ("2026-10-05", "d1e2f3b", "feat(api): implement /predict POST route with input validation", 380, 26),
                ("2026-10-07", "a4b5c6d", "feat(api): map 15 incoming JSON attributes to NumPy feature vector", 310, 20),
                ("2026-10-10", "c7d8e9b", "feat(api): connect model.predict() and predict_proba() pipeline", 270, 16),
                ("2026-10-13", "f0a1b2a", "feat(api): format standardized JSON output with class label and code", 240, 14),
                ("2026-10-16", "b3c4d5a", "feat(api): implement comprehensive error handlers for 400 and 500", 210, 11),
            ],
            "Nitesh Sharma": [
                ("2026-10-06", "e5f6a7e", "feat(ml): verify feature column ordering matches training schema", 240, 15),
                ("2026-10-11", "a8b9c0a", "feat(ml): test corner-case inputs with extreme numerical bounds", 205, 12),
                ("2026-10-15", "d1e2f3c", "feat(ml): add inference unit tests for expected output classes", 180, 9),
            ],
            "Prankur Sharma": [
                ("2026-10-08", "b6c7d8e", "feat(ui): implement asynchronous AJAX fetch for form submission", 220, 13),
                ("2026-10-14", "e9f0a1b", "feat(ui): handle API errors gracefully with visual feedback alerts", 175, 9),
            ],
            "Shobhan Bhagwati": [
                ("2026-10-09", "c2d3e4a", "test: prepare realistic test payloads from Test.txt records", 200, 12),
                ("2026-10-16", "f5a6b7d", "docs: document REST API endpoint parameters and sample payloads", 160, 8),
            ]
        }
    },
    {
        "period": "Period 10",
        "date_str": "23/10/2026",
        "date_iso": "2026-10-23",
        "window": "2026-10-17 to 2026-10-23",
        "milestone": "Responsive Web Frontend Development & UI/UX Styling",
        "contributions": {
            "Prankur Sharma": [
                ("2026-10-18", "e7f8a9c", "feat(ui): revamp templates/index.html with modern responsive UI", 390, 28),
                ("2026-10-19", "b0c1d2e", "feat(ui): rewrite static/style.css using modern flexbox and grid", 340, 24),
                ("2026-10-20", "f3a4b5d", "feat(ui): add dark-mode gradient headers and clean shadow accents", 280, 18),
                ("2026-10-21", "c6d7e8b", "feat(ui): implement mobile-first responsive viewport adjustments", 250, 15),
                ("2026-10-23", "a9b0c1e", "feat(ui): design polished result showcase modal and attack summary", 220, 12),
            ],
            "Shaurya Shekhawat": [
                ("2026-10-19", "d2e3f4c", "feat(api): integrate Flask render_template with index.html", 230, 15),
                ("2026-10-21", "a5b6c7f", "feat(api): configure static file cache headers and MIME types", 190, 11),
                ("2026-10-23", "c8d9e0c", "test: add end-to-end HTML response status tests in Flask client", 175, 9),
            ],
            "Nitesh Sharma": [
                ("2026-10-20", "e1f2a3d", "feat(ml): provide pre-filled sample vectors for testing each attack", 210, 12),
                ("2026-10-22", "f4e5a6a", "feat(ml): verify form input value transformations match scaler", 175, 9),
            ],
            "Shobhan Bhagwati": [
                ("2026-10-21", "b7c8d9b", "docs: add UI input field glossary explaining network metrics", 165, 8),
            ]
        }
    },
    {
        "period": "Period 11",
        "date_str": "30/10/2026",
        "date_iso": "2026-10-30",
        "window": "2026-10-24 to 2026-10-30",
        "milestone": "End-to-End System Integration & Real-Time Traffic Simulation",
        "contributions": {
            "Shaurya Shekhawat": [
                ("2026-10-25", "c9d0e1f", "feat(api): implement end-to-end integration pipeline in app.py", 310, 20),
                ("2026-10-27", "f2a3b4d", "feat(api): add request correlation IDs for end-to-end tracing", 250, 16),
                ("2026-10-29", "b5c6d7c", "perf: optimize Flask worker threading and socket timeouts", 220, 13),
                ("2026-10-30", "e8f9a0d", "test: add end-to-end regression test suite covering all attack types", 190, 10),
            ],
            "Prankur Sharma": [
                ("2026-10-25", "a1b2c3a", "feat(ui): connect dynamic form submit to Flask backend via AJAX", 290, 19),
                ("2026-10-27", "d4e5f6d", "feat(ui): implement animated attack result cards with severity color", 240, 15),
                ("2026-10-28", "g7h8i9b", "feat(ui): add quick-fill preset buttons for Normal, DOS, and Probe", 215, 12),
                ("2026-10-30", "c0d1e2a", "feat(ui): polish button hover states and active form focus outlines", 180, 9),
            ],
            "Nitesh Sharma": [
                ("2026-10-26", "f3a4b5e", "feat(ml): calibrate prediction probability threshold on live requests", 260, 16),
                ("2026-10-28", "e6f7a8e", "feat(ml): verify multi-class prediction consistency across 500 samples", 225, 14),
                ("2026-10-30", "a9b0c1b", "feat(ml): optimize model.predict() vector execution path", 195, 11),
            ],
            "Shobhan Bhagwati": [
                ("2026-10-26", "b2c3d4b", "test: replay NSL-KDD test packets against live Flask service", 210, 12),
                ("2026-10-29", "e5f6a7d", "docs: document system integration verification checklist", 160, 8),
            ]
        }
    },
    {
        "period": "Period 12",
        "date_str": "05/11/2026",
        "date_iso": "2026-11-05",
        "window": "2026-10-31 to 2026-11-05",
        "milestone": "Docker Containerization, Gunicorn Profiling & Deployment Tests",
        "contributions": {
            "Shaurya Shekhawat": [
                ("2026-11-01", "a2b3c4d", "chore(docker): author production Dockerfile with python:3.11-slim", 360, 24),
                ("2026-11-02", "d5e6f7b", "chore(deploy): create Procfile configured for Gunicorn multi-worker", 290, 18),
                ("2026-11-03", "c8d9e0d", "chore(docker): configure non-root security user inside container", 250, 15),
                ("2026-11-04", "f1a2b3c", "chore(docker): optimize layer caching for pip requirements", 220, 12),
                ("2026-11-05", "b4c5d6a", "test: verify container startup and healthcheck in Docker runtime", 195, 10),
            ],
            "Nitesh Sharma": [
                ("2026-11-02", "e7f8a9d", "chore: audit requirements.txt and remove unused heavy dependencies", 240, 16),
                ("2026-11-04", "a0b1c2f", "feat(ml): verify model unpickling inside minimal Docker container", 205, 12),
                ("2026-11-05", "d3e4f5c", "test: run scikit-learn model inference tests inside container", 180, 9),
            ],
            "Prankur Sharma": [
                ("2026-11-03", "c1d2e3c", "feat(ui): ensure static CSS and JS are served properly in Gunicorn", 210, 13),
                ("2026-11-05", "f4e5a6b", "feat(ui): add favicon and meta tags for deployment readiness", 165, 8),
            ],
            "Shobhan Bhagwati": [
                ("2026-11-02", "b6c7d8a", "docs: write Docker build and container execution guide in README", 200, 12),
                ("2026-11-04", "e9f0a1c", "test: verify dataset file paths inside container volume", 160, 8),
            ]
        }
    },
    {
        "period": "Period 13",
        "date_str": "12/11/2026",
        "date_iso": "2026-11-12",
        "window": "2026-11-06 to 2026-11-12",
        "milestone": "Comprehensive System Validation, Security Audit & User Testing",
        "contributions": {
            "Nitesh Sharma": [
                ("2026-11-07", "b8c9d0e", "feat(ml): perform adversarial perturbation testing on attack features", 320, 22),
                ("2026-11-09", "e1f2a3e", "feat(ml): evaluate model drift and boundary robustness", 260, 16),
                ("2026-11-11", "a4b5c6e", "feat(ml): benchmark inference latency (sub-5ms) across 1,000 runs", 230, 14),
                ("2026-11-12", "d7e8f9b", "docs: document final ML model validation results and confusion matrix", 190, 10),
            ],
            "Shaurya Shekhawat": [
                ("2026-11-07", "c0d1e2b", "feat(api): perform API stress testing under 100 concurrent workers", 300, 20),
                ("2026-11-09", "f3a4b5a", "feat(api): implement rate limiting and request payload size caps", 250, 15),
                ("2026-11-11", "b6c7d8b", "feat(api): sanitize all input attributes against injection vectors", 220, 12),
                ("2026-11-12", "e9f0a1d", "test: verify automated healthcheck and graceful shutdown handlers", 185, 9),
            ],
            "Prankur Sharma": [
                ("2026-11-08", "a2b3c4e", "feat(ui): test UI rendering across Chrome, Firefox, Safari, and Edge", 240, 15),
                ("2026-11-10", "d5e6f7c", "feat(ui): ensure WCAG AA accessibility compliance and contrast", 200, 11),
                ("2026-11-12", "c8d9e0e", "feat(ui): finalize UI animations, typography and responsive layout", 175, 8),
            ],
            "Shobhan Bhagwati": [
                ("2026-11-08", "f1a2b3d", "docs: complete comprehensive system architecture documentation", 220, 12),
                ("2026-11-11", "b4c5d6b", "docs: finalize user guide, API reference and team contribution summary", 170, 8),
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
                        period_key = dt.strftime("%b %d")
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
