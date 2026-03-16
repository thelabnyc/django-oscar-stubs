"""Tests for the mypy plugin's fork detection logic."""

import textwrap

from mypy_oscar_plugin import (
    _collect_app_config_entries,
    _determine_oscar_label_from_config,
    _parse_config_base_class,
)


class TestCollectAppConfigEntries:
    def test_simple_installed_apps(self, tmp_path):
        settings = tmp_path / "settings.py"
        settings.write_text(
            textwrap.dedent("""\
            INSTALLED_APPS = [
                "django.contrib.admin",
                "django.contrib.auth",
                "myproject.catalogue.apps.CatalogueConfig",
                "oscar.apps.basket.apps.BasketConfig",
                "oscar.apps.order.apps.OrderConfig",
            ]
            """)
        )
        entries = _collect_app_config_entries(str(settings))
        # Should only return non-oscar, non-django entries
        assert entries == ["myproject.catalogue.apps.CatalogueConfig"]

    def test_index_replacement_pattern(self, tmp_path):
        settings = tmp_path / "settings.py"
        settings.write_text(
            textwrap.dedent("""\
            INSTALLED_APPS = [
                "oscar.apps.catalogue.apps.CatalogueConfig",
                "oscar.apps.partner.apps.PartnerConfig",
            ]
            idx = INSTALLED_APPS.index("oscar.apps.partner.apps.PartnerConfig")
            INSTALLED_APPS[idx] = "myproject.partner.apps.PartnerConfig"
            """)
        )
        entries = _collect_app_config_entries(str(settings))
        assert "myproject.partner.apps.PartnerConfig" in entries

    def test_multiple_forks(self, tmp_path):
        settings = tmp_path / "settings.py"
        settings.write_text(
            textwrap.dedent("""\
            INSTALLED_APPS = [
                "myproject.catalogue.apps.CatalogueConfig",
                "myproject.partner.apps.PartnerConfig",
                "oscar.apps.basket.apps.BasketConfig",
            ]
            """)
        )
        entries = _collect_app_config_entries(str(settings))
        assert len(entries) == 2
        assert "myproject.catalogue.apps.CatalogueConfig" in entries
        assert "myproject.partner.apps.PartnerConfig" in entries

    def test_empty_settings(self, tmp_path):
        settings = tmp_path / "settings.py"
        settings.write_text("# empty\n")
        entries = _collect_app_config_entries(str(settings))
        assert entries == []

    def test_nonexistent_file(self):
        entries = _collect_app_config_entries("/nonexistent/settings.py")
        assert entries == []


class TestDetermineOscarLabel:
    def test_known_config_name(self):
        result = _determine_oscar_label_from_config("myproject.catalogue.apps.CatalogueConfig")
        assert result == ("catalogue", "myproject.catalogue")

    def test_known_partner_config(self):
        result = _determine_oscar_label_from_config("myproject.apps.partner.apps.PartnerConfig")
        assert result == ("partner", "myproject.apps.partner")

    def test_known_dashboard_config(self):
        result = _determine_oscar_label_from_config("myproject.dashboard.catalogue.apps.CatalogueDashboardConfig")
        assert result == ("catalogue_dashboard", "myproject.dashboard.catalogue")

    def test_unknown_config_name(self):
        result = _determine_oscar_label_from_config("myproject.foo.apps.SomethingElse")
        assert result is None

    def test_non_app_config_entry(self):
        result = _determine_oscar_label_from_config("myproject.catalogue")
        assert result is None


class TestParseConfigBaseClass:
    def test_inherits_from_oscar_config(self, tmp_path):
        """User renames their config class but inherits from oscar's."""
        pkg = tmp_path / "myproject" / "catalogue"
        pkg.mkdir(parents=True)
        (pkg / "apps.py").write_text(
            textwrap.dedent("""\
            from oscar.apps.catalogue.apps import CatalogueConfig as OscarCatalogueConfig

            class MyCustomConfig(OscarCatalogueConfig):
                name = "myproject.catalogue"
            """)
        )

        import sys

        sys.path.insert(0, str(tmp_path))
        try:
            result = _parse_config_base_class("myproject.catalogue", "MyCustomConfig")
            assert result == "catalogue"
        finally:
            sys.path.remove(str(tmp_path))

    def test_explicit_label(self, tmp_path):
        """User sets label explicitly in config class."""
        pkg = tmp_path / "myproject" / "mycat"
        pkg.mkdir(parents=True)
        (pkg / "apps.py").write_text(
            textwrap.dedent("""\
            from django.apps import AppConfig

            class MyCatConfig(AppConfig):
                label = "catalogue"
                name = "myproject.mycat"
            """)
        )

        import sys

        sys.path.insert(0, str(tmp_path))
        try:
            result = _parse_config_base_class("myproject.mycat", "MyCatConfig")
            assert result == "catalogue"
        finally:
            sys.path.remove(str(tmp_path))

    def test_no_matching_class(self, tmp_path):
        """Config class doesn't exist in the file."""
        pkg = tmp_path / "myproject" / "catalogue"
        pkg.mkdir(parents=True)
        (pkg / "apps.py").write_text("# empty\n")

        import sys

        sys.path.insert(0, str(tmp_path))
        try:
            result = _parse_config_base_class("myproject.catalogue", "NonExistentConfig")
            assert result is None
        finally:
            sys.path.remove(str(tmp_path))
