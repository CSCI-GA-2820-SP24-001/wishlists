"""
Test cases for Pet Model
"""

import os
import logging
from unittest import TestCase
from wsgi import app
from unittest.mock import patch
from service.models import Wishlists, Item, db, DataValidationError
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

    def test_add_a_account(self):
        """It should Create a wishlist and add it to the database"""
        wishlists = Wishlists.all()
        self.assertEqual(wishlists, [])
        wishlist = WishlistsFactory()
        wishlist.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(wishlist.id)
        wishlists = Wishlists.all()
        self.assertEqual(len(wishlists), 1)

    @patch("service.models.db.session.commit")
    def test_add_account_failed(self, exception_mock):
        """It should not create an Account on database error"""
        exception_mock.side_effect = Exception()
        wishlist = WishlistsFactory()
        self.assertRaises(DataValidationError, wishlist.create)

    def test_update_wishlist(self):
        """It should Update a wishlist"""
        wishlist = WishlistsFactory(title="Tester Wishlist")
        wishlist.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(wishlist.id)
        self.assertEqual(wishlist.title, "Tester Wishlist")

        # Fetch it back
        wishlist = Wishlists.find(wishlist.id)
        wishlist.title = "Test Update Wishlist"
        wishlist.update()

        # Fetch it back again
        wishlist = Wishlists.find(wishlist.id)
        self.assertEqual(wishlist.title, "Test Update Wishlist")

    @patch("service.models.db.session.commit")
    def test_update_wishlist_failed(self, exception_mock):
        """It should not update a wishlist on database error"""
        exception_mock.side_effect = Exception()
        wishlist = WishlistsFactory()
        self.assertRaises(DataValidationError, wishlist.update)

    def test_read_account(self):
        """It should Read an account"""
        wishlist = WishlistsFactory()
        wishlist.create()

        # Read it back
        found_wishlist = Wishlists.find(wishlist.id)
        self.assertEqual(found_wishlist.id, wishlist.id)
        self.assertEqual(found_wishlist.title, wishlist.title)
        self.assertEqual(found_wishlist.items, [])
        self.assertEqual(found_wishlist.date, wishlist.date)
        self.assertEqual(found_wishlist.count, wishlist.count)
        self.assertEqual(found_wishlist.description, wishlist.description)

    def test_delete_a_wishlist(self):
        """It should Delete a wishlist from the database"""
        wishlists = Wishlists.all()
        self.assertEqual(wishlists, [])
        wishlist = WishlistsFactory()
        wishlist.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(wishlist.id)
        wishlists = Wishlists.all()
        self.assertEqual(len(wishlists), 1)
        wishlist = wishlists[0]
        wishlist.delete()
        wishlists = Wishlists.all()
        self.assertEqual(len(wishlists), 0)

    @patch("service.models.db.session.commit")
    def test_delete_wishlist_failed(self, exception_mock):
        """It should not delete an Account on database error"""
        exception_mock.side_effect = Exception()
        wishlist = WishlistsFactory()
        self.assertRaises(DataValidationError, wishlist.delete)

    def test_list_all_wishlists(self):
        """It should List all wishlists in the database"""
        wishlists = Wishlists.all()
        self.assertEqual(wishlists, [])
        for wish in WishlistsFactory.create_batch(5):
            wish.create()
        # Assert that there are not 5 accounts in the database
        wishlists = Wishlists.all()
        self.assertEqual(len(wishlists), 5)

    def test_find_by_name(self):
        """It should Find an Account by name"""
        wishlist = WishlistsFactory()
        wishlist.create()

        # Fetch it back by name
        same_wishlist = Wishlists.find_by_name(wishlist.title)[0]
        self.assertEqual(same_wishlist.id, wishlist.id)
        self.assertEqual(same_wishlist.title, wishlist.title)

    def test_serialize_a_wishlist(self):
        """It should Serialize an account"""
        wishlist = WishlistsFactory()
        item = ItemsFactory()
        wishlist.items.append(item)
        serial_wishlist = wishlist.serialize()
        self.assertEqual(serial_wishlist["id"], wishlist.id)
        self.assertEqual(serial_wishlist["title"], wishlist.title)
        self.assertEqual(serial_wishlist["description"], wishlist.description)
        self.assertEqual(serial_wishlist["count"], wishlist.count)
        self.assertEqual(serial_wishlist["date"], str(wishlist.date))
        self.assertEqual(len(serial_wishlist["items"]), 1)
        items = serial_wishlist["items"]
        self.assertEqual(items[0]["id"], item.id)
        self.assertEqual(items[0]["item_name"], item.item_name)
        self.assertEqual(items[0]["wishlist_id"], item.wishlist_id)

    def test_deserialize_an_account(self):
        """It should Deserialize a wishlist"""
        account = WishlistsFactory()
        account.items.append(WishlistsFactory())
        account.create()
        serial_account = account.serialize()
        new_account = Wishlists()
        new_account.deserialize(serial_account)
        self.assertEqual(new_account.title, account.title)
        self.assertEqual(new_account.description, account.description)
        self.assertEqual(new_account.count, account.count)
        self.assertEqual(new_account.date, account.date)

    def test_deserialize_with_key_error(self):
        """It should not Deserialize a wishlist with a KeyError"""
        account = Wishlists()
        self.assertRaises(DataValidationError, account.deserialize, {})

    def test_deserialize_with_type_error(self):
        """It should not Deserialize a wishlist with a TypeError"""
        account = Wishlists()
        self.assertRaises(DataValidationError, account.deserialize, [])

    def test_deserialize_item_key_error(self):
        """It should not Deserialize an item with a KeyError"""
        address = Item()
        self.assertRaises(DataValidationError, address.deserialize, {})

    def test_deserialize_item_type_error(self):
        """It should not Deserialize an item with a TypeError"""
        address = Item()
        self.assertRaises(DataValidationError, address.deserialize, [])

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

        new_item = Item()
        new_item.deserialize(item.serialize())
        self.assertEqual(new_item.wishlist_id, item.wishlist_id)
        self.assertEqual(new_item.item_name, item.item_name)
