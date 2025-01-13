"""Composite charges built from the policy tables."""
from . import rules


def combined_charge(x):
    """Total of the two base schedules for x."""
    return rules.shipping_fee_cents(x) + rules.handling_fee_cents(x)
