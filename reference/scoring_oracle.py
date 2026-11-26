#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Alexander Stephen Donahue
"""Exact rational / arbitrary-precision Reference Oracle (Build Standard B12)
for differential verification against `src/v2_loader.py` and Lean 4.35.0
`MegaAtlasProofs.Scoring`, `Quadrants`, and `LayerGradients`.

Uses Python's exact `fractions.Fraction` and `decimal.Decimal` (50-digit precision)
with zero shared implementation code from `src/v2_loader.py`.
"""

from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 50


def exact_age_score_100(age_years: int) -> Fraction:
    """Exact antiquity score in [0, 100]: min(100, max(0, age_years / 3))."""
    if age_years <= 0:
        return Fraction(0, 1)
    if age_years >= 300:
        return Fraction(100, 1)
    return Fraction(age_years, 3)


def exact_deg_term_100(degree: int) -> Decimal:
    """50-digit Decimal evaluation of min(100, 25 * ln(1 + degree))."""
    if degree <= 0:
        return Decimal(0)
    val = Decimal(25) * (Decimal(1 + degree).ln())
    return min(Decimal(100), val)


def oracle_css_score(diff: int, impact: int, degree: int, age_years: int, tract: int) -> float:
    """Independent high-precision reference oracle for 0thernes CSS (0..100)."""
    diff_100 = Decimal(diff * 10)
    deg_100 = exact_deg_term_100(degree)
    cent_100 = (Decimal(impact * 10) + deg_100) / Decimal(2)
    age_frac = exact_age_score_100(age_years)
    age_100 = Decimal(age_frac.numerator) / Decimal(age_frac.denominator)
    tract_100 = Decimal(tract * 10)
    css = (
        Decimal("0.40") * diff_100
        + Decimal("0.30") * cent_100
        + Decimal("0.20") * age_100
        + Decimal("0.10") * (Decimal(100) - tract_100)
    )
    return round(float(css), 2)


def oracle_titan_index(diff: int, impact: int, interdisc: int, degree: int) -> float:
    """Independent high-precision reference oracle for Composite Titan Index (0.90..10.00)."""
    deg_term = exact_deg_term_100(degree) / Decimal(10)
    titan = (
        Decimal("0.35") * Decimal(diff)
        + Decimal("0.35") * Decimal(impact)
        + Decimal("0.20") * Decimal(interdisc)
        + Decimal("0.10") * deg_term
    )
    return round(float(titan), 2)


def oracle_leverage(impact: int, tract: int) -> float:
    """Exact rational Near-Term Leverage Score `(impact * tract) / 10`."""
    return float(Fraction(impact * tract, 10))


def oracle_quadrant(impact: int, tract: int) -> str:
    """Exact strategic 4-quadrant classifier matching Lean `classifyQuadrant`."""
    if impact >= 8:
        if tract >= 7:
            return "Q1: Near-Term Civilizational Levers (High Impact, High Tractability)"
        return "Q2: Grand Centuries-Scale Titans (High Impact, Low Tractability)"
    if tract >= 7:
        return "Q3: Targeted Technical Frontiers (Focused Impact, High Tractability)"
    return "Q4: Deep Foundational & Formal Enigmas (Focused Impact, Low Tractability)"


def oracle_era(year: int) -> str:
    """Exact 6-era classifier matching Lean `computeEra`."""
    if year < 500:
        return "Antiquity (<500 CE)"
    if year < 1800:
        return "Early Modern (500-1799)"
    if year < 1900:
        return "19th Century (1800-1899)"
    if year < 1970:
        return "Early-Mid 20th C. (1900-1969)"
    if year < 2000:
        return "Late 20th C. (1970-1999)"
    return "21st Century (2000-2026)"


def oracle_margin_role(adj_pillars: int, cross_sd: int, bridge_ratio: float) -> str:
    """Exact 4-class margin role matching Lean `classifyMarginRole`."""
    if adj_pillars >= 3:
        return "Apex Multi-Pillar Keystone (3+ Adjacent Pillars)"
    if adj_pillars >= 1 and bridge_ratio >= 0.30:
        return "Trans-Pillar Boundary Interface"
    if cross_sd >= 1 or adj_pillars >= 1:
        return "Intra-Pillar Bridge (Cross-Superdomain)"
    return "Core Intra-Pillar Specialist"
