"""
TestWishlists API Service Test Suite
"""

import os
import logging
from unittest import TestCase
from wsgi import app
from service.common import status
from service.models import db, Wishlists
from tests.factories import WishlistsFactory, ItemsFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/wishlists"


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods


class TestWishlists(TestCase):
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

    def _create_wishlists(self, count):
        """Factory method to create wishlists in bulk"""
        wishlists = []
        for _ in range(count):
            wishlist = WishlistsFactory()
            response = self.client.post(BASE_URL, json=wishlist.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test wishlists",
            )
            new_wishlist = response.get_json()
            wishlist.id = new_wishlist["id"]
            wishlists.append(wishlist)
        return wishlists

    def _create_items(self, count):
        """Factory method to create items in bulk"""
        items = []
        for _ in range(count):
            item = ItemsFactory()
            response = self.client.post(BASE_URL, json=item.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test items",
            )
            new_item = response.get_json()
            item.id = new_item["id"]
            items.append(item)
        return items

    ######################################################################
    #  TEST CASES FOR WISHLIST
    ######################################################################

    # List wishlist
    def test_get_wishlist_list(self):
        """It should Get a list of Wishlists"""
        self._create_wishlists(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)

    # Create wishlist
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
        self.assertEqual(new_wishlist["date"], str(test_wishlist.date))

        # Todo: Uncomment this code when get_wishlists is implemented
        ## Check that the location header was correct
        # response = self.client.get(location)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # new_wishlist = response.get_json()
        # self.assertEqual(new_wishlist["user_id"], test_wishlist.user_id)
        # self.assertEqual(new_wishlist["title"], test_wishlist.title)
        # self.assertEqual(new_wishlist["description"], test_wishlist.description)
        # self.assertEqual(new_wishlist["items"], test_wishlist.items)
        # self.assertEqual(new_wishlist["count"], test_wishlist.count)
        # self.assertEqual(new_wishlist["date"], test_wishlist.date)

    # Update wishlist
    def test_update_wishlist(self):
        """It should Update an existing Wishlist"""
        # create a wishlist to update
        test_wishlist = WishlistsFactory()
        response = self.client.post(BASE_URL, json=test_wishlist.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # update the wishlist
        new_wishlist = response.get_json()
        logging.debug(new_wishlist)
        new_wishlist["title"] = "New Wishlist"
        response = self.client.put(
            f"{BASE_URL}/{new_wishlist['id']}", json=new_wishlist
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_wishlist = response.get_json()
        self.assertEqual(updated_wishlist["title"], "New Wishlist")

    # Delete wishlist
    def test_delete_wishlist(self):
        """It should Delete a Wishlist"""
        # get the id of an account
        wishlist = self._create_wishlists(1)[0]
        resp = self.client.delete(f"{BASE_URL}/{wishlist.id}")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    # Read wishlist
    def test_get_wishlist(self):
        """It should Get a single Wishlist"""
        # get the id of a wishlist
        test_wishlist = self._create_wishlists(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_wishlist.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["title"], test_wishlist.title)

    ######################################################################
    #  I T E M S  T E S T   C A S E S
    ######################################################################

    # Create item
    def test_add_item(self):
        """It should Add an item to a wishlist"""
        wishlist = self._create_wishlists(1)[0]
        item = ItemsFactory()
        resp = self.client.post(
            f"{BASE_URL}/{wishlist.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["wishlist_id"], wishlist.id)
        self.assertEqual(data["name"], item.item_name)

    # Update item
    def test_update_item(self):
        """It should Update an item on a wishlist"""
        # create a known item
        wishlist = self._create_wishlists(1)[0]
        item = ItemsFactory()
        resp = self.client.post(
            f"{BASE_URL}/{wishlist.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        data = resp.get_json()
        logging.debug(data)
        item_id = data["id"]
        # data["name"] = item.item_name

        # send the update back
        resp = self.client.put(
            f"{BASE_URL}/{wishlist.id}/items/{item_id}",
            json=data,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # retrieve it back
        resp = self.client.get(
            f"{BASE_URL}/{wishlist.id}/items/{item_id}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["id"], item_id)
        self.assertEqual(data["wishlist_id"], wishlist.id)
        # self.assertEqual(data["name"], item.item_name)

    # List item
    def test_get_item_list(self):
        """It should Get a list of Items"""
        # add two items to wishlist
        wishlist = self._create_wishlists(1)[0]
        item_list = ItemsFactory.create_batch(2)

        # Create item 1
        resp = self.client.post(
            f"{BASE_URL}/{wishlist.id}/items", json=item_list[0].serialize()
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Create item 2
        resp = self.client.post(
            f"{BASE_URL}/{wishlist.id}/items", json=item_list[1].serialize()
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # get the list back and make sure there are 2
        resp = self.client.get(f"{BASE_URL}/{wishlist.id}/items")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        self.assertEqual(len(data), 2)

    # Delete item
    def test_delete_item(self):
        """It should Delete an Item"""
        wishlist = self._create_wishlists(1)[0]
        item = ItemsFactory()
        resp = self.client.post(
            f"{BASE_URL}/{wishlist.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.get_json()
        logging.debug(data)
        item_id = data["id"]

        # send delete request
        resp = self.client.delete(
            f"{BASE_URL}/{wishlist.id}/items/{item_id}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        # retrieve it back and make sure item is not there
        resp = self.client.get(
            f"{BASE_URL}/{wishlist.id}/items/{item_id}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # Read item
    def test_get_item(self):
        """It should Get an item from a wishlist"""
        # create a known item
        wishlist = self._create_wishlists(1)[0]
        item = ItemsFactory()
        resp = self.client.post(
            f"{BASE_URL}/{wishlist.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        data = resp.get_json()
        logging.debug(data)
        item_id = data["id"]

        # retrieve it back
        resp = self.client.get(
            f"{BASE_URL}/{wishlist.id}/items/{item_id}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["id"], item_id)
        self.assertEqual(data["wishlist_id"], wishlist.id)
        # self.assertEqual(data["name"], item.item_name)
