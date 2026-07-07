from ecommerce_monitor_public.config import PublicConfig
from ecommerce_monitor_public.pipeline import STAGE_NAMES, build_demo_manifest


def test_public_demo_has_expected_stages():
    manifest = build_demo_manifest(PublicConfig())
    assert [stage["name"] for stage in manifest["stages"]] == list(STAGE_NAMES)


def test_public_demo_contains_no_recipients_or_real_send():
    manifest = build_demo_manifest(PublicConfig())
    assert manifest["summary"]["sent"] == 0
    assert manifest["stages"][6]["status"] == "dry_run"
    assert manifest["stages"][7]["status"] == "dry_run"


def test_config_defaults_are_safe():
    config = PublicConfig()
    assert config.dry_run is True
    assert config.notification_enabled is False
    assert config.external_table_enabled is False
