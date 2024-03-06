"""
Test cases for Pet Model
"""

import os
import logging
from unittest import TestCase
from wsgi import app
from service.models import Wishlists, Item, db
from .factories import ItemFactory, WishlistsFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  Wishlists   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestWishlists(TestCase):
    """Test Cases for Wishlists Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Wishlists).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_wishlist(self):
        """It should create a Wishlists"""
        wishlist = WishlistsFactory()
        wishlist.create()
        self.assertIsNotNone(wishlist.id)
        found = Wishlists.all()
        self.assertEqual(len(found), 1)
        data = Wishlists.find(wishlist.id)
        self.assertEqual(data.id, wishlist.id)
        self.assertEqual(data.user_id, wishlist.user_id)
        self.assertEqual(data.title, wishlist.title)
        self.assertEqual(data.description, wishlist.description)
        self.assertEqual(data.count, wishlist.count)
        self.assertEqual(data.date, wishlist.date)

        return self


class TestItems(TestCase):
    """Test Cases for Items Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Item).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_item(self):
        """It should create an item"""
        items = ItemFactory()
        items.create()
        # self.assertIsNotNone(items.id)
        found = Item.all()
        self.assertEqual(len(found), 1)
        # data = Item.find(items.id)
        # self.assertEqual(data.id, items.id)
        # self.assertEqual(data.item_name, items.item_name)

    def test_create_new_item(self):
        """this should create an item and assert that it exists"""
        item = Item(item_name="sponge")
        item.create()
        self.assertTrue(item is not None)


#        '''It should Create an item and assert that it exists'''
#         item = Item(item_name="sponge")
#         item.create()
# self.assertEqual(str(item), "<New Item id=[None]>")
# self.assertTrue(item is not None)
# self.assertEqual(item.id, None)
# self.assertEqual(item.item_name, "sponge")
