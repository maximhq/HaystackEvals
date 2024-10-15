import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
import json
from haystack import Document
from haystack.components.evaluators.document_recall import RecallMode
import requests

# Import the functions to test
from app import mape, mrr, recall

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True

    def test_recall_single(self):
        url = "http://127.0.0.1:5000/api/document/evaluator/recall"

        payload = json.dumps({
        "ground_truth_documents": "1,2,3",
        "retrieved_documents": "1,2",
        "mode": "SINGLE_HIT"
        })
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        self.assertEqual(response.status_code, 200)
        self.assertIn("score", response.json())
        self.assertEqual(response.json()["score"], 1.0)
        self.assertIn("recall", response.json())
    
    def test_recall_multi(self):
        url = "http://127.0.0.1:5000/api/document/evaluator/recall"

        payload = json.dumps({
        "ground_truth_documents": "1,2,3",
        "retrieved_documents": "1,2",
        "mode": "MULTI_HIT"
        })
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(round(response.json()["score"],2), round(0.6666666666666666,2))
        self.assertIn("score", response.json())
        self.assertIn("recall", response.json())
    
    def test_mrr(self):
        url = "http://127.0.0.1:5000/api/document/evaluator/mrr"

        payload = json.dumps({
        "ground_truth_documents": "1,2,3",
        "retrieved_documents": "1,2",
        "mode": "MULTI_HIT"
        })
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        self.assertEqual(response.status_code, 200)
        # self.assertEqual(round(response.json()["score"],2), round(0.6666666666666666,2))
        self.assertIn("score", response.json())
        self.assertIn("mrr", response.json())
    
    def test_mape(self):
        url = "http://127.0.0.1:5000/api/document/evaluator/mape"

        payload = json.dumps({
        "ground_truth_documents": "1,2,3",
        "retrieved_documents": "1,2",
        })
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        self.assertEqual(response.status_code, 200)
        # self.assertEqual(round(response.json()["score"],2), round(0.6666666666666666,2))
        self.assertIn("score", response.json())
        self.assertIn("mape", response.json())

if __name__ == '__main__':
    unittest.main()