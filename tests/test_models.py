"""
Test cases for Pet Model
"""

import os
import logging
from unittest import TestCase
from wsgi import app
from service.models import Wishlists, Item, db
from .factories import ItemsFactory, WishlistsFactory

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
        """It should Create an Account and assert that it exists"""
        fake_wishlist = WishlistsFactory()
        # pylint: disable=unexpected-keyword-arg
        wishlist = Wishlists(
            title=fake_wishlist.title,
            description=fake_wishlist.description,
            items=fake_wishlist.items,
            date=fake_wishlist.date,
            count=fake_wishlist.count,
        )
        self.assertIsNotNone(wishlist)
        self.assertEqual(wishlist.id, None)
        self.assertEqual(wishlist.title, fake_wishlist.title)
        self.assertEqual(wishlist.description, fake_wishlist.description)
        self.assertEqual(wishlist.count, fake_wishlist.count)
        self.assertEqual(wishlist.date, fake_wishlist.date)

    ##to do: test_update_wishlist

    ## to do: test_delete_wishlist

    ##to do: test_list_wishlist

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_add_wishlist_item(self):
        """It should Create a wishlist with an item and add it to the database"""
        # wishlists = Item()
        # self.assertIsNotNone(wishlists)
        wishlists = Wishlists.all()
        self.assertEqual(wishlists, [])
        wishlist = WishlistsFactory()
        item = ItemsFactory(wishlist=wishlist)
        wishlist.items.append(item)
        wishlist.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(wishlist.id)
        wishlists = Wishlists.all()
        self.assertNotEqual(len(wishlists), 0)

        new_wishlist = Wishlists.find(wishlist.id)
        self.assertEqual(new_wishlist.items[0].item_name, item.item_name)

        item2 = ItemsFactory(wishlist=wishlist)
        wishlist.items.append(item2)
        wishlist.update()

        new_wishlist = Wishlists.find(wishlist.id)
        self.assertEqual(len(new_wishlist.items), 2)
        self.assertEqual(new_wishlist.items[1].item_name, item2.item_name)

    def test_update_wishlist_item(self):
        """It should Update a wishlists item"""
        wishlists = Wishlists.all()

        wishlist = WishlistsFactory()
        item = ItemsFactory(wishlist=wishlist)
        wishlist.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(wishlist.id)
        wishlists = Wishlists.all()
        self.assertGreaterEqual(len(wishlists), 0)

        # Fetch it back
        wishlist = Wishlists.find(wishlist.id)
        old_item = wishlist.items[0]
        print("%r", old_item)
        self.assertEqual(old_item.item_name, item.item_name)
        # Change the city
        old_item.item_name = "XX"
        wishlist.update()

        # Fetch it back again
        wishlist = Wishlists.find(wishlist.id)
        item = wishlist.items[0]
        self.assertEqual(item.item_name, "XX")

    def test_serialize_an_item(self):
        """It should serialize an item"""
        item = ItemsFactory()
        serial_item = item.serialize()
        self.assertEqual(serial_item["id"], item.id)
        # self.assertEqual(serial_item["wishlist_id"], item.wishlist_id)
        self.assertEqual(serial_item["name"], item.item_name)

    def test_deserialize_an_item(self):
        """It should deserialize an item"""
        item = ItemsFactory()
        item.create()
        new_item = Item()
        new_item.deserialize(item.serialize())
        # self.assertEqual(new_item.id, item.id)
        self.assertEqual(new_item.item_name, item.item_name)
