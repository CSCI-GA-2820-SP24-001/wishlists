"""
TestWishlists API Service Test Suite
"""

import os
import logging
from unittest import TestCase
from wsgi import app
from service.common import status
from service.models import db, Wishlists
from tests.factories import WishlistsFactory, ItemFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/wishlists"
ITEM_URL = "/items"


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods


class TestYourResourceService(TestCase):
    """REST API Server Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(Wishlists).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    # List test cases
    def test_get_wishlist_list(self):
        """It should Get a list of Wishlists"""
        self._create_wishlists(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)

    def test_create_wishlist(self):
        """It should Create a new Wishlist"""
        test_wishlist = WishlistsFactory()
        logging.debug("Test Wishlists: %s", test_wishlist.serialize())
        response = self.client.post(BASE_URL, json=test_wishlist.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_wishlist = response.get_json()
        self.assertEqual(new_wishlist["user_id"], test_wishlist.user_id)
        self.assertEqual(new_wishlist["title"], test_wishlist.title)
        self.assertEqual(new_wishlist["description"], test_wishlist.description)
        self.assertEqual(new_wishlist["items"], test_wishlist.items)
        self.assertEqual(new_wishlist["count"], test_wishlist.count)
        self.assertEqual(new_wishlist["date"], test_wishlist.date)

        # Todo: Uncomment this code when get_wishlists is implemented
        ## Check that the location header was correct
        #response = self.client.get(location)
        #self.assertEqual(response.status_code, status.HTTP_200_OK)
        #new_wishlist = response.get_json()
        #self.assertEqual(new_wishlist["user_id"], test_wishlist.user_id)
        #self.assertEqual(new_wishlist["title"], test_wishlist.title)
        #self.assertEqual(new_wishlist["description"], test_wishlist.description)
        #self.assertEqual(new_wishlist["items"], test_wishlist.items)
        #self.assertEqual(new_wishlist["count"], test_wishlist.count)
        #self.assertEqual(new_wishlist["date"], test_wishlist.date)

    # Update test cases
    def test_update_wishlist(self):
        """It should Update an existing Wishlist"""
        # create a wishlist to update
        test_wishlist = WishlistsFactory()
        response = self.client.post(BASE_URL, json=test_wishlist.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # update the wishlist
        new_wishlist = response.get_json()
        logging.debug(new_wishlist)
        new_wishlist["category"] = "unknown"
        response = self.client.put(
            f"{BASE_URL}/{new_wishlist['id']}", json=new_wishlist
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_wishlist = response.get_json()
        self.assertEqual(updated_wishlist["category"], "unknown")

    def test_create_item(self):
        """It should Create a new item"""
        test_item = ItemFactory()
        logging.debug("Test Item: %s", test_item.serialize())
        response = self.client.post(ITEM_URL, json=test_item.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_item = response.get_json()
        self.assertEqual(new_item["name"], test_item.item_name)

        # Check that the location header was correct
        # To do: uncomment this code when location is implemented
        # response = self.client.get(location)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_item = response.get_json()
        self.assertEqual(new_item["name"], test_item.item_name)

    # Delete test cases
    def test_delete_wishlist(self):
        """It should Delete a Wishlist"""
        test_wishlist = self._create_wishlists(1)[0]
        response = self.client.delete(f"{BASE_URL}/{test_wishlist.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)
        # make sure they are deleted
        response = self.client.get(f"{BASE_URL}/{test_wishlist.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
