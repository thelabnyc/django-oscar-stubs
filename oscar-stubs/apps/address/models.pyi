from oscar.apps.address.abstract_models import AbstractCountry, AbstractUserAddress

class UserAddress(AbstractUserAddress):
    id: int

class Country(AbstractCountry):
    id: int
