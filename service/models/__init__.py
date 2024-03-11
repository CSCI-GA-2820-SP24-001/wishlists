"""
Models for Wishlist

All of the models are stored in this package
"""

from .persistent_base import db, DataValidationError
from .wishlist import Wishlists
from .item import Item
