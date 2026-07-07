from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class ProductPlan:
    plan_id: str
    product_name: str
    specification: str = ""
    brand: str = ""
    platforms: tuple[str, ...] = field(default_factory=tuple)
    required_keywords: tuple[str, ...] = field(default_factory=tuple)
    priority: int = 100
    enabled: bool = True


@dataclass(frozen=True)
class ListingCandidate:
    platform: str
    product_id: str
    title: str
    specification: str
    price: str
    shop_name: str
    url: str
    matched_plan_id: str
    collected_at: str = field(default_factory=now_iso)


@dataclass(frozen=True)
class CustomerMatch:
    shop_name: str
    company_name: str
    region: str
    matched_from: str
    needs_manual_review: bool = False


@dataclass(frozen=True)
class StaffRoute:
    region: str
    owner_role: str
    support_role: str
    recipient_ids: tuple[str, ...] = field(default_factory=tuple)
    missing_reason: str = ""


@dataclass(frozen=True)
class PipelineStage:
    name: str
    status: str
    input_count: int = 0
    output_count: int = 0
    note: str = ""
