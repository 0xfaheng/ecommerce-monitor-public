from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from .config import PublicConfig
from .models import ListingCandidate, PipelineStage, ProductPlan, now_iso


STAGE_NAMES = (
    "load_product_plans",
    "collect_candidates",
    "normalize_fields",
    "apply_rules",
    "match_customers",
    "route_staff",
    "write_register",
    "dry_run_notify",
    "write_audit_manifest",
)


def build_demo_manifest(config: PublicConfig) -> dict:
    plans = [
        ProductPlan(
            plan_id="plan_demo_001",
            product_name="示例产品A",
            specification="10ml*10支",
            brand="示例品牌",
            platforms=("platform_a", "platform_b"),
            required_keywords=("示例产品A", "10ml"),
            priority=10,
        )
    ]
    candidates = [
        ListingCandidate(
            platform="platform_a",
            product_id="demo-item-001",
            title="示例产品A 10ml*10支 示例标题",
            specification="10ml*10支",
            price="0.00",
            shop_name="示例药房A",
            url="https://example.invalid/items/demo-item-001",
            matched_plan_id="plan_demo_001",
        )
    ]
    stages = [
        PipelineStage(
            name="load_product_plans",
            status="completed",
            output_count=len(plans),
            note=f"source={config.product_library_source}",
        ),
        PipelineStage(
            name="collect_candidates",
            status="completed",
            input_count=len(plans),
            output_count=len(candidates),
            note="public demo uses synthetic candidates only",
        ),
        PipelineStage(
            name="normalize_fields",
            status="completed",
            input_count=len(candidates),
            output_count=len(candidates),
        ),
        PipelineStage(
            name="apply_rules",
            status="completed",
            input_count=len(candidates),
            output_count=len(candidates),
            note="no private exclusion rules in public demo",
        ),
        PipelineStage(
            name="match_customers",
            status="completed",
            input_count=len(candidates),
            output_count=len(candidates),
            note=f"source={config.customer_library_source}",
        ),
        PipelineStage(
            name="route_staff",
            status="completed",
            input_count=len(candidates),
            output_count=0,
            note="recipient ids are intentionally blank in public demo",
        ),
        PipelineStage(
            name="write_register",
            status="dry_run",
            input_count=len(candidates),
            output_count=0,
            note="external table writes disabled",
        ),
        PipelineStage(
            name="dry_run_notify",
            status="dry_run",
            input_count=len(candidates),
            output_count=0,
            note="notification send disabled",
        ),
        PipelineStage(
            name="write_audit_manifest",
            status="completed",
            output_count=1,
        ),
    ]
    return {
        "run_id": "public-demo",
        "mode": "dry_run" if config.dry_run else "send_disabled_in_public_demo",
        "generated_at": now_iso(),
        "summary": {
            "plans": len(plans),
            "candidates": len(candidates),
            "filtered": 0,
            "ready_for_confirmation": len(candidates),
            "ready_to_notify": 0,
            "sent": 0,
        },
        "stages": [asdict(stage) for stage in stages],
        "candidates": [asdict(candidate) for candidate in candidates],
        "private_data_policy": "no real accounts, customers, recipients, tokens, logs, cookies, or server data",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the sanitized public dry-run demo.")
    parser.add_argument("--demo", action="store_true", help="print a synthetic dry-run manifest")
    args = parser.parse_args()

    config = PublicConfig.from_env()
    manifest = build_demo_manifest(config)
    if args.demo:
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
    else:
        print("Use --demo to print the public dry-run manifest.")


if __name__ == "__main__":
    main()
