from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable

from .models import CustomerMatch, ListingCandidate, ProductPlan, StaffRoute


class PlatformAdapter(ABC):
    """Convert one platform's listing source into normalized candidates."""

    @abstractmethod
    def collect(self, plan: ProductPlan) -> Iterable[ListingCandidate]:
        raise NotImplementedError


class RegisterAdapter(ABC):
    """Write candidate records to a human-confirmed business register."""

    @abstractmethod
    def write_candidates(self, candidates: Iterable[ListingCandidate]) -> int:
        raise NotImplementedError


class CustomerMatcher(ABC):
    """Resolve a shop into a customer/company boundary."""

    @abstractmethod
    def match(self, candidate: ListingCandidate) -> CustomerMatch:
        raise NotImplementedError


class StaffRouter(ABC):
    """Resolve customer or region data into notification routes."""

    @abstractmethod
    def route(self, match: CustomerMatch) -> StaffRoute:
        raise NotImplementedError


class Notifier(ABC):
    """Send or preview notification payloads."""

    @abstractmethod
    def dry_run(self, candidates: Iterable[ListingCandidate]) -> list[dict]:
        raise NotImplementedError
