from __future__ import annotations

import os
from dataclasses import dataclass


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class PublicConfig:
    environment: str = "development"
    dry_run: bool = True
    product_library_source: str = "examples/product_library.sample.csv"
    customer_library_source: str = "examples/customer_library.sample.csv"
    staff_route_source: str = "examples/staff_routes.sample.csv"
    notification_enabled: bool = False
    external_table_enabled: bool = False

    @classmethod
    def from_env(cls) -> "PublicConfig":
        return cls(
            environment=os.getenv("ENVIRONMENT", "development"),
            dry_run=_env_bool("DRY_RUN", True),
            product_library_source=os.getenv(
                "PRODUCT_LIBRARY_SOURCE", "examples/product_library.sample.csv"
            ),
            customer_library_source=os.getenv(
                "CUSTOMER_LIBRARY_SOURCE", "examples/customer_library.sample.csv"
            ),
            staff_route_source=os.getenv(
                "STAFF_ROUTE_SOURCE", "examples/staff_routes.sample.csv"
            ),
            notification_enabled=_env_bool("NOTIFICATION_ENABLED", False),
            external_table_enabled=_env_bool("EXTERNAL_TABLE_ENABLED", False),
        )
