"""
Models for Wishlists

All of the models are stored in this module
"""

import logging
from datetime import date
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


class Item(db.Model):
    """Class that represents items"""

    __tablename__ = "items"

    item_id = db.Column(
        db.Integer, autoincrement=True, nullable=False, primary_key=True
    )
    item_name = db.Column(db.String(63), nullable=False)

    def __repr__(self):
        return f"<Items {self.item_name} id=[{self.item_id}]>"


class Wishlists(db.Model):
    """
    Class that represents a Wishlists
    """

    __tablename__ = "wishlists"
    ##################################################
    # Table Schema
    ##################################################
    id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    user_id = db.Column(db.String(63), nullable=False)
    title = db.Column(db.String(63), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    items = db.Column(db.PickleType, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date(), nullable=False, default=date.today())

    def __repr__(self):
        return f"<Wishlists {self.title} id=[{self.id}]>"

    def create(self):
        """
        Creates a Wishlists to the database
        """
        logger.info("Creating %s", self.title)
        self.id = None  # pylint: disable=invalid-name
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error creating record: %s", self)
            raise DataValidationError(e) from e

    def update(self):
        """
        Updates a Wishlists to the database
        """
        logger.info("Saving %s", self.title)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error updating record: %s", self)
            raise DataValidationError(e) from e

    def delete(self):
        """Removes a Wishlists from the data store"""
        logger.info("Deleting %s", self.title)
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error deleting record: %s", self)
            raise DataValidationError(e) from e

    def serialize(self):
        """Serializes a Wishlists into a dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "items": self.items,
            "count": self.count,
            "date": self.date.isoformat(),
        }

    def deserialize(self, data):
        """
        Deserializes a Wishlists from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.id = data["id"]
            self.user_id = data["user_id"]
            self.title = data["title"]
            self.items = data["items"]
            self.description = data["description"]
            self.count = getattr("count", data["count"])
            self.date = date.fromisoformat(data["date"])

        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0]) from error
        except KeyError as error:
            raise DataValidationError(
                "Invalid Wishlists: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Wishlists: body of request contained bad or no data "
                + str(error)
            ) from error
        return self

    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def all(cls):
        """Returns all of the Wishlists in the database"""
        logger.info("Processing all Wishlists")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a Wishlists by it's ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.session.get(cls, by_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all Wishlists with the given name

        Args:
            name (string): the name of the Wishlists you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)
