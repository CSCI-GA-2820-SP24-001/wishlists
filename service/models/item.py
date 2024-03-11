"""
Models for Wishlists

All of the models are stored in this module
"""

import logging
from .persistent_base import db, PersistentBase, DataValidationError

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
# db = SQLAlchemy()


# class DataValidationError(Exception):
# #     """Used for an data validation errors when deserializing"""


class Item(db.Model, PersistentBase):
    """Class that represents items"""

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(63), nullable=False)
    wishlist_id = db.Column(
        db.Integer, db.ForeignKey("wishlist.id", ondelete="CASCADE"), nullable=False
    )

    def __repr__(self):
        return f"<Item {self.item_name} id=[{self.id}]>"

    def __str__(self):
        return f"{self.id}: {self.item_name}"

    def serialize(self):
        """Serializes a item into a dictionary"""
        return {
            "id": self.id,
            "wishlist_id": self.wishlist_id,
            "name": self.item_name,
        }

    def deserialize(self, data):
        """
        Deserializes a item from a dictionary
        Args:
            data (dict): A dictionary containing the item data
        """
        try:
            self.wishlist_id = data["wishlist_id"]
            self.item_name = data["item_name"]
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0]) from error
        except KeyError as error:
            raise DataValidationError(
                "Invalid item: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid item: body of request contained bad or no data " + str(error)
            ) from error
        return self
