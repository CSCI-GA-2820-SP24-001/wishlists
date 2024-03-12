"""
Persistent Base class for database CRUD functions
"""

import logging
from datetime import date
from .persistent_base import db, PersistentBase, DataValidationError
from .item import Item

logger = logging.getLogger("flask.app")


######################################################################
#  W I S H L I S T  M O D E L
######################################################################


class Wishlist(db.Model, PersistentBase):
    """
    Class that represents a Wishlist
    """

    ##################################################
    # Table Schema
    ##################################################
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(63), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    items = db.relationship("Item", backref="wishlist", passive_deletes=True)
    count = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date(), nullable=False, default=date.today())

    def serialize(self):
        """Serializes a Wishlist into a dictionary"""
        wishlist = {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            # "items": self.items,
            "count": self.count,
            "date": self.date.isoformat(),
            "items": [],
        }
        for item in self.items:
            wishlist["items"].append(item.serialize())
        return wishlist

    def deserialize(self, data):
        """
        Deserializes a Wishlist from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            # self.id = data["id"]
            self.user_id = data["user_id"]
            self.title = data["title"]
            # self.items = data["items"]
            self.description = data["description"]
            self.count = data["count"]
            self.date = date.fromisoformat(data["date"])
            item_list = data.get("items")
            for json_item in item_list:
                item = Item()
                item.deserialize(json_item)
                self.items.append(item)
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0]) from error
        except KeyError as error:
            raise DataValidationError(
                "Invalid Wishlist: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Wishlist: body of request contained bad or no data "
                + str(error)
            ) from error
        return self

    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def find_by_name(cls, title):
        """Returns all Wishlist with the given name

        Args:
            name (string): the name of the Wishlist you want to match
        """
        logger.info("Processing name query for %s ...", title)
        return cls.query.filter(cls.title == title)
