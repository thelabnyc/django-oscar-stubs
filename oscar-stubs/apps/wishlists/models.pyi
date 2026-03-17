from oscar.apps.wishlists.abstract_models import (
    AbstractLine,
    AbstractWishList,
    AbstractWishListSharedEmail,
)

class WishList(AbstractWishList):
    id: int

class Line(AbstractLine):
    id: int

class WishListSharedEmail(AbstractWishListSharedEmail):
    id: int
