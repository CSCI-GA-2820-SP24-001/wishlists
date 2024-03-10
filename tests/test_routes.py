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
ITEM_URL = "/items"


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
            test_wishlist = WishlistsFactory()
            response = self.client.post(BASE_URL, json=test_wishlist.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test wishlists",
            )
            new_wishlist = response.get_json()
            test_wishlist.id = new_wishlist["id"]
            wishlists.append(test_wishlist)
        return wishlists

    ##to do: create item test
    # def _create_pets(self, count):
    #     """Factory method to create pets in bulk"""
    #     pets = []
    #     for _ in range(count):
    #         test_pet = PetFactory()
    #         response = self.client.post(BASE_URL, json=test_pet.serialize())
    #         self.assertEqual(
    #             response.status_code,
    #             status.HTTP_201_CREATED,
    #             "Could not create test pet",
    #         )
    #         new_pet = response.get_json()
    #         test_pet.id = new_pet["id"]
    #         pets.append(test_pet)
    #     return pets

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
        new_wishlist["title"] = "New Wishlist"
        response = self.client.put(
            f"{BASE_URL}/{new_wishlist['id']}", json=new_wishlist
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_wishlist = response.get_json()
        self.assertEqual(updated_wishlist["title"], "New Wishlist")

    def test_delete_wishlist(self):
        """It should Delete an Account"""
        # get the id of an account
        wishlist = self._create_wishlists(1)[0]
        resp = self.client.delete(f"{BASE_URL}/{wishlist.id}")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    ####items test cases
    def test_add_wishlist_item(self):
        """It should Create a wishlist with an item and add it to the database"""
        wishlists = Wishlists.all()
        self.assertEqual(wishlists, [])
        wishlist = WishlistsFactory()
        item = ItemsFactory(wishlist=wishlist)
        wishlist.items.append(item)
        wishlist.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(wishlist.id)
        wishlists = Wishlists.all()
        self.assertEqual(len(wishlists), 1)
        new_wishlist = Wishlists.find(wishlist.id)
        self.assertEqual(new_wishlist.items[0].item_name, item.item_name)

        wl2 = ItemsFactory(wishlist=wishlist)
        wishlist.items.append(wl2)
        wishlist.update()

        new_wishlist = Wishlists.find(wishlist.id)
        self.assertEqual(len(new_wishlist.items), 2)
        self.assertEqual(new_wishlist.items[1].item_name, wl2.item_name)

        # new_account = Account.find(account.id)
        # self.assertEqual(new_account.addresses[0].name, address.name)

        # address2 = AddressFactory(account=account)
        # account.addresses.append(address2)
        # account.update()

        # new_account = Account.find(account.id)
        # self.assertEqual(len(new_account.addresses), 2)
        # self.assertEqual(new_account.addresses[1].name, address2.name)
