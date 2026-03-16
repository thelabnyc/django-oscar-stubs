import subprocess
import sys

from django.conf import settings
import django

if not settings.configured:
    settings.configure(
        INSTALLED_APPS=[
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.sites",
            "django.contrib.flatpages",
            "oscar.config.Shop",
            "oscar.apps.analytics.apps.AnalyticsConfig",
            "oscar.apps.checkout.apps.CheckoutConfig",
            "oscar.apps.address.apps.AddressConfig",
            "oscar.apps.shipping.apps.ShippingConfig",
            "oscar.apps.catalogue.apps.CatalogueConfig",
            "oscar.apps.catalogue.reviews.apps.CatalogueReviewsConfig",
            "oscar.apps.communication.apps.CommunicationConfig",
            "oscar.apps.partner.apps.PartnerConfig",
            "oscar.apps.basket.apps.BasketConfig",
            "oscar.apps.payment.apps.PaymentConfig",
            "oscar.apps.offer.apps.OfferConfig",
            "oscar.apps.order.apps.OrderConfig",
            "oscar.apps.customer.apps.CustomerConfig",
            "oscar.apps.search.apps.SearchConfig",
            "oscar.apps.voucher.apps.VoucherConfig",
            "oscar.apps.wishlists.apps.WishlistsConfig",
            "oscar.apps.dashboard.apps.DashboardConfig",
            "oscar.apps.dashboard.reports.apps.ReportsDashboardConfig",
            "oscar.apps.dashboard.users.apps.UsersDashboardConfig",
            "oscar.apps.dashboard.orders.apps.OrdersDashboardConfig",
            "oscar.apps.dashboard.catalogue.apps.CatalogueDashboardConfig",
            "oscar.apps.dashboard.offers.apps.OffersDashboardConfig",
            "oscar.apps.dashboard.partners.apps.PartnersDashboardConfig",
            "oscar.apps.dashboard.pages.apps.PagesDashboardConfig",
            "oscar.apps.dashboard.ranges.apps.RangesDashboardConfig",
            "oscar.apps.dashboard.reviews.apps.ReviewsDashboardConfig",
            "oscar.apps.dashboard.vouchers.apps.VouchersDashboardConfig",
            "oscar.apps.dashboard.communications.apps.CommunicationsDashboardConfig",
            "oscar.apps.dashboard.shipping.apps.ShippingDashboardConfig",
            "widget_tweaks",
            "haystack",
            "treebeard",
            "django_tables2",
        ],
        DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
        STATIC_URL="/static/",
        ROOT_URLCONF="django.contrib.admin.sites",
        OSCAR_SHOP_NAME="Test",
        SITE_ID=1,
        HAYSTACK_CONNECTIONS={
            "default": {
                "ENGINE": "haystack.backends.simple_backend.SimpleEngine",
            },
        },
    )

django.setup()

sys.exit(
    subprocess.call(
        [
            sys.executable,
            "-m",
            "mypy.stubtest",
            "oscar",
            "--allowlist",
            "stubtest-allowlist.txt",
            "--mypy-config-file",
            "stubtest_mypy.ini",
        ]
    )
)
