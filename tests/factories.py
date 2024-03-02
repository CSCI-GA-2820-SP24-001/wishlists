"""
Test Factory to make fake objects for testing
"""

from datetime import date
import factory
from factory.fuzzy import FuzzyChoice, FuzzyDate, FuzzyInteger, FuzzyText
from service.models import Wishlists, Item


class ItemFactory(factory.Factory):
    """Creating Items table for DB"""

    class Meta:
        """Maps Factory to Model"""

        model = Item


class WishlistsFactory(factory.Factory):
    """Creates fake pets that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Wishlists

    id = factory.Sequence(lambda n: n)
    user_id = factory.Sequence(lambda n: n)
    title = FuzzyText(length=63)
    description = FuzzyText(length=250)
    items = FuzzyChoice(choices=[ItemFactory() for _ in range(50)])
    count = FuzzyInteger(0, 50, step=1)
    date = FuzzyDate(date(2008, 1, 1))

    # Todo: Add your other attributes here...
