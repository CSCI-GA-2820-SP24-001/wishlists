"""
Test Factory to make fake objects for testing
"""

from datetime import date
import factory
from factory.fuzzy import FuzzyDate, FuzzyInteger, FuzzyText
from service.models import Wishlists, Item


class WishlistsFactory(factory.Factory):
    """Creates wishlists"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Wishlists

    id = factory.Sequence(lambda n: n)
    user_id = factory.Sequence(lambda n: n)
    title = FuzzyText(length=63)
    description = FuzzyText(length=250)
    count = FuzzyInteger(0, 50, step=1)
    date = FuzzyDate(date(2008, 1, 1))
    # items = FuzzyChoice(choices=[ItemFactory() for _ in range(50)])

    @factory.post_generation
    def items(
        self, create, extracted, **kwargs
    ):  # pylint: disable=method-hidden, unused-argument
        """Creates the items list"""
        if not create:
            return

        if extracted:
            self.items = extracted


class ItemsFactory(factory.Factory):
    """Creates fake Addresses"""

    # pylint: disable=too-few-public-methods
    class Meta:
        """Persistent class"""

        model = Item

    id = factory.Sequence(lambda n: n)
    wishlist_id = None
    item_name = FuzzyText(length=63)
    wishlist = factory.SubFactory(WishlistsFactory)
