#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""
    __storage = None

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        # Initialize a new database
        models.storage.reload()

    @classmethod
    def delete_test_data_all(cls, objs):
        """Delete all rows from all tables"""
        storage = models.storage
        for obj in objs:
            storage.delete(obj)
        storage.save()

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        storage = models.storage
        result = storage.all()
        self.assertIs(type(result), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        objs = []
        storage = models.storage
        # Create some rows
        state = State(name="California")
        objs.append(state)
        state.save()
        city = City(name="San Francisco", state_id=state.id)
        objs.append(city)
        city.save()
        # Get all rows
        result = storage.all()
        # Check that all rows are returned
        self.assertEqual(len(result), 2)
        self.assertIn(f"State.{state.id}", result)
        self.assertIn(f"City.{city.id}", result)
        # Delete all rows
        self.delete_test_data_all(objs)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        objs = []
        storage = models.storage
        # Create some rows
        state = State(name="California")
        objs.append(state)
        storage.new(state)
        storage.save()
        # Get all rows
        result = storage.all()
        # Check that all rows are returned
        self.assertEqual(len(result), 1)
        self.assertIn(f"State.{state.id}", result)
        # Delete all rows
        self.delete_test_data_all(objs)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """test that new adds an object to the database"""
        objs = []
        storage = models.storage
        # Create some rows
        state = State(name="California")
        objs.append(state)
        storage.new(state)
        storage.save()
        # Get row by id
        result = storage.get(State, state.id)
        # Check that the correct row is returned
        self.assertEqual(result.id, state.id)
        # Asser not found
        result = storage.get(State, "not_found")
        self.assertIsNone(result)
        # Delete all rows
        self.delete_test_data_all(objs)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """test that count returns the number of rows in the table"""
        objs = []
        storage = models.storage
        # Empty table
        result = storage.count()
        self.assertEqual(result, 0)
        # Count all inserted types
        state = State(name="California")
        objs.append(state)
        storage.new(state)
        storage.save()
        city = City(name="San Francisco", state_id=state.id)
        objs.append(city)
        storage.new(city)
        storage.save()
        # Count rows
        result = storage.count()
        # Check that the correct row is returned
        self.assertEqual(result, len(objs))
        # Count specific type
        result = storage.count(State)
        # Check that the correct row is returned
        self.assertEqual(result, 1)
        # Delete all rows
        self.delete_test_data_all(objs)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        """test that new adds an object to the database"""
        objs = []
        storage = models.storage
        # Create some rows
        state = State(name="California")
        objs.append(state)
        storage.new(state)
        storage.save()
        # Get all rows
        result = storage.all()
        # Check that all rows are returned
        self.assertEqual(len(result), 1)
        self.assertIn(f"State.{state.id}", result)
        # Delete all rows
        self.delete_test_data_all(objs)
