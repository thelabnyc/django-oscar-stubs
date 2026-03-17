from oscar.apps.voucher.abstract_models import (
    AbstractVoucher,
    AbstractVoucherApplication,
    AbstractVoucherSet,
)

class VoucherSet(AbstractVoucherSet):
    id: int

class Voucher(AbstractVoucher):
    id: int

class VoucherApplication(AbstractVoucherApplication):
    id: int
