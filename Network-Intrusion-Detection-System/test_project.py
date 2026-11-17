"""
Automated Comprehensive Test Suite for Network Intrusion Detection System (NIDS)
Verifies:
- Dependency availability
- Model loading and serialization integrity
- Prediction logic & endpoint responses
- Dataset availability and structure
- Form-3 PDF Report generation
- Security assertions
"""

import os
import unittest
import numpy as np
import joblib
from app import app
import generate_report

class TestNIDSProject(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        app.testing = True
        cls.client = app.test_client()
        cls.model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
        cls.model = joblib.load(cls.model_path)
    
    def test_01_model_loading_and_properties(self):
        """Verify model deserialization, feature dimensions, and class outputs."""
        self.assertIsNotNone(self.model, "Model should not be None")
        self.assertTrue(hasattr(self.model, "predict"), "Model must have predict method")
        self.assertEqual(self.model.n_features_in_, 15, "Model must expect exactly 15 features")
        self.assertTrue(len(self.model.classes_) >= 3, "Model classes must be initialized")

    def test_02_flask_home_route(self):
        """Verify GET / returns 200 and renders HTML index template."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Network Intrusion Detection System", response.data)
        self.assertIn(b"form", response.data)

    def test_03_flask_form_prediction_endpoint(self):
        """Verify POST /predict handles form payload and returns expected attack classification."""
        form_payload = {
            'attack': '2',                      # normal
            'count': '5',
            'dst_host_diff_srv_rate': '0.0',
            'dst_host_same_src_port_rate': '1.0',
            'dst_host_same_srv_rate': '1.0',
            'dst_host_srv_count': '255',
            'flag': '2',                        # SF
            'last_flag': '21',
            'logged_in': '1',
            'same_srv_rate': '1.0',
            'serror_rate': '0.0',
            'service_http': '1'
        }
        response = self.client.post("/predict", data=form_payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Attack Class should be", response.data)

    def test_04_flask_json_results_endpoint(self):
        """Verify POST /results accepts 15 numerical features and returns JSON attack string."""
        json_payload = {f"f{i}": 0.0 for i in range(15)}
        response = self.client.post("/results", json=json_payload)
        self.assertEqual(response.status_code, 200)
        output = response.get_json()
        self.assertIn(output, ["Normal", "DOS", "PROBE", "R2L", "U2R"])

    def test_05_dataset_files_exist(self):
        """Verify NSL-KDD dataset files exist and are not empty."""
        train_path = os.path.join(os.path.dirname(__file__), "NSL_Dataset", "Train.txt")
        test_path = os.path.join(os.path.dirname(__file__), "NSL_Dataset", "Test.txt")
        self.assertTrue(os.path.isfile(train_path), "Train.txt must exist")
        self.assertTrue(os.path.isfile(test_path), "Test.txt must exist")
        self.assertGreater(os.path.getsize(train_path), 10_000_000, "Train.txt should be > 10MB")
        self.assertGreater(os.path.getsize(test_path), 1_000_000, "Test.txt should be > 1MB")

    def test_06_report_generator_pdf_creation(self):
        """Verify generate_report.py generates valid PDF without runtime errors."""
        generate_report.generate_pdf("weekly")
        repo_name, _ = generate_report.get_repo_info()
        import datetime
        date_stamp = datetime.date.today().strftime("%Y-%m-%d")
        expected_pdf = f"{repo_name}_Weekly_Progress_Report_Form-3_{date_stamp}.pdf"
        self.assertTrue(os.path.isfile(expected_pdf), f"Expected PDF {expected_pdf} to exist")
        self.assertGreater(os.path.getsize(expected_pdf), 1000)

    def test_07_no_hardcoded_secrets(self):
        """Verify repository files contain no hardcoded API keys or private tokens."""
        prohibited = ["BEGIN " + "RSA PRIVATE KEY", "ghp" + "_", "github" + "_pat_"]
        for root, _, files in os.walk(os.path.dirname(__file__)):
            if ".git" in root or ".venv" in root or "__pycache__" in root:
                continue
            for file in files:
                if file == "test_project.py":
                    continue
                if file.endswith((".py", ".yml", ".md", ".txt", ".html", ".css")):
                    path = os.path.join(root, file)
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        for p in prohibited:
                            self.assertNotIn(p, content, f"Secret pattern '{p}' found in {path}")

if __name__ == "__main__":
    unittest.main()
