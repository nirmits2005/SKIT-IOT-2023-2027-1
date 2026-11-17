# Network Intrusion Detection System (NIDS) — Team Responsibility Matrix

**Institution:** Swami Keshvanand Institute of Technology, Management & Gramothan, Jaipur (SKIT)  
**Department:** Department of Computer Science & Engineering (IoT Specialization, 2023–2027)  
**Project:** Network Intrusion Detection System (NIDS)  
**Target Repository:** `nirmits2005/SKIT-IOT-2023-2027-1`  

---

## Team Overview & Roster

The project is developed by a four-member engineering team. Each member is assigned specific functional modules and system responsibilities across the machine learning, backend, frontend, dataset processing, DevOps, and reporting lifecycles.

| Member Name | Primary Functional Domain | Verified Git / Repository Identifier |
| :--- | :--- | :--- |
| **Shobhan Bhagwati** | Data Preprocessing, EDA & Statistical Profiling | `Shobhan Bhagwati` |
| **Nitesh Sharma** | Machine Learning Architecture & Model Engineering | `Nitesh Sharma` (`nirmits2005`) |
| **Shaurya Shekhawat** | Backend API, System Architecture & Docker Deployment | `Shaurya Shekhawat` (`Shaurya-pratap`) |
| **Prankur Sharma** | Frontend Interface, UX & Integration Testing | `Prankur Sharma` |

---

## Detailed Responsibility Allocations

### 1. Shobhan Bhagwati — Data Preprocessing & Exploratory Analysis
* **Dataset Ingestion & Auditing:** NSL-KDD dataset ingestion (`Train.txt`, `Test.txt`), schema alignment, and missing value checks.
* **Data Cleaning & Normalization:** Categorical encoding (protocol type, flag, service), outlier clipping, and min-max scaling of continuous attributes.
* **Exploratory Data Analysis (EDA):** Univariate feature distributions, correlation matrix generation (`corrm.csv`), and numerical feature summaries (`num_summary.csv`).
* **Statistical Analysis:** Evaluation of attack frequencies (Normal, DoS, Probe, R2L, U2R) across training and testing partitions.
* **Feature Understanding & Documentation:** Detailed documentation of feature meanings, traffic behavior signatures, and dataset limitations.

### 2. Nitesh Sharma — Machine Learning & Model Engineering
* **Model Research & Prototyping:** Exploring binary and multi-class classifiers (Logistic Regression, Random Forest, SVM, Naive Bayes, XGBoost).
* **Feature Engineering & Selection:** Identifying high-gain features, eliminating multicollinearity based on correlation analysis (`corrm.csv`), reducing input dimensionality to 15 core features.
* **Model Training & Hyperparameter Tuning:** Supervised training for classification into 5 attack classes (Normal, DoS, Probe, R2L, U2R).
* **Model Optimization & Serialization:** Finalizing production model serialization via `joblib` into `model.pkl`.
* **Performance Analysis & Validation:** Confusion matrix generation, precision-recall curve analysis, classification reporting, and accuracy validation.

### 3. Shaurya Shekhawat — Backend Development & DevOps
* **Flask Application Architecture:** Designing and implementing the core Flask service (`app.py`).
* **Prediction APIs:** Implementing web form handling (`/predict`) and JSON REST API (`/results`) for real-time inference.
* **Model Pipeline Integration:** Efficient in-memory deserialization of `model.pkl` and safe vectorized transformation of incoming inference payloads.
* **Backend Unit & Integration Testing:** Validating HTTP response codes, JSON schema compliance, and payload validation.
* **Containerization & Deployment:** Crafting production-grade `Dockerfile` using `python:3.11-slim`, defining multi-worker Gunicorn server configuration (`Procfile`), and specifying environment variables (`PORT`).

### 4. Prankur Sharma — Frontend Interface & Quality Assurance
* **Web User Interface:** Developing interactive web application frontend (`templates/index.html`) for interactive traffic classification.
* **Styling & User Experience:** Custom CSS styling (`static/style.css`), responsive layouts, intuitive form input elements, and color-coded alert badges for predicted attack classes.
* **Prediction Result Presentation:** Dynamic rendering of classification verdicts (`Normal`, `DOS`, `PROBE`, `R2L`, `U2R`) with visual feedback.
* **End-to-End Integration Testing:** Cross-browser testing, edge-case form input validation, and stress-testing frontend-backend communication.
* **Documentation Support:** Contributing to usage instructions, user flow diagrams, and student progress documentation.

---

## Verification & Retrospective Tracking Policy

* **Authentic Git Authorship:** Contribution reports are computed directly from verified Git commit histories without fabricating historical dates.
* **Dual Attribution:** Code commits are verified through Git logs, while non-code engineering (e.g. testing, exploratory analysis, dataset curation) is documented through this responsibility matrix and Form-3 evaluation dossiers.
* **Retrospective Labeling:** Reports covering historical course intervals prior to Git integration are transparently designated as Retrospective Progress Reports in compliance with academic audit guidelines.
