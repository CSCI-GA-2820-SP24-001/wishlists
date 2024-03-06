"""
Test Factory to make fake objects for testing
"""

from datetime import date
import factory
from factory.fuzzy import FuzzyChoice, FuzzyDate, FuzzyInteger, FuzzyText
from service.models import Wishlists, Item


class ItemFactory(factory.Factory):
    """Creating Items table for DB"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps Factory to Model"""

        model = Item

    id = factory.Sequence(lambda n: n)
    item_name = factory.Faker("first_name")


class WishlistsFactory(factory.Factory):
    """Creates wishlists"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Wishlists

    id = factory.Sequence(lambda n: n)
    user_id = factory.Sequence(lambda n: n)
    title = FuzzyText(length=63)
    description = FuzzyText(length=250)
    # items = FuzzyChoice(choices=[ItemFactory() for _ in range(50)])
    
    # method suggested by the professor
    @factory.post_generation
    def items(self, create, extracted, **kwargs):  # pylint: disable=method-hidden, unused-argument
        """Creates the Items list"""
        if not create:
            return
        if extracted:
            self.items = extracted
    count = FuzzyInteger(0, 50, step=1)
    date = FuzzyDate(date(2008, 1, 1))
