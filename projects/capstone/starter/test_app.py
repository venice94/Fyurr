import os
import unittest
import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date

from models import setup_db, db_drop_and_create_all, Wallet_User, Shop, Transaction

class WalletTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = Flask(__name__)
        self.client = self.app.test_client
        self.database_name = "wallet_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('sh_ubuntu', '93water94', 'localhost:5432', self.database_name)

        # binds the app to the current context
        with self.app.app_context():
            setup_db(self.app)
            # create all tables
            db_drop_and_create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_all_users(self):
        res = self.client().get('/users')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['users'])
        self.assertTrue(len(data['users']))
    
    def test_404_get_all_users(self):
        res = self.client().get('/users?page=10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
    
    def test_get_all_shops(self):
        res = self.client().get('/shops')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['shops'])
        self.assertTrue(len(data['shops']))
    
    def test_404_get_all_shops(self):
        res = self.client().get('/shops?page=10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
    
    def test_get_one_user(self):
        res = self.client().get('/users/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success', True])
        self.assertTrue(data['user'])
        self.assertTrue(len(data['user']))

    def test_404_get_one_user(self):
        res = self.client().get('/users/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success', False])
    
    def test_get_user_transactions(self):
        res = self.client().get('/users/1/transactions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success', True])
        self.assertTrue(data['user_id'])
        self.assertTrue(data['transactions'])
        self.assertTrue(len(data['transactions']))

    def test_404_get_user_transactions(self):
        res = self.client().get('/users/100/transactions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success', False])
    
    def test_patch_user(self):
        res = self.client().get('/users/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success', True])
        self.assertTrue(data['user'])
        self.assertTrue(len(data['user']))
    
    def test_404_patch_user(self):
        res = self.client().get('/users/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success', False])

    def test_add_user_transaction(self):
        res = self.client().get('/users/1', json={
            'type': 'Income',
            'category': 'Salary',
            'amount': 5555.55,
            'description': 'Salary crediting'
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success', True])
        self.assertTrue(data['transaction'])
        self.assertTrue(len(data['transaction']))
    
    def test_404_add_user_transaction(self):
        res = self.client().get('/users/1', json={
            'user_id': 1,
            'type': 'Expense',
            'amount': 55,
            'shop_id': 1
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success', False])
    
    def test_422_add_user_transaction(self):
        res = self.client().get('/users/1', json={
            'type': 'Splurge',
            'category': 'Luxury item',
            'amount': 100,
            'shop_id': 1
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success', False])
    
    def test_delete_user(self):
        res = self.client().get('/users/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['user'])
        self.assertTrue(len(data['user']))
    
    def test_404_delete_user(self):
        res = self.client().get('/users/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success', False])


if __name__ == "__main__":
    unittest.main()
