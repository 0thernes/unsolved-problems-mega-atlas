# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Alexander Stephen Donahue
"""V2.8.0 Mega-Atlas Canonical Schema (8 Macro-Pillars × 28 Superdomains, 1,900 Problems, Nov 26, 2026 Edition)."""

from typing import Dict, List, Any

MACRO_PILLARS = [
    "Pure Mathematics",
    "Logic, Statistics & Computing",
    "Fundamental Physics & Cosmos",
    "Matter, Materials & Chemistry",
    "Life, Mind & Medicine",
    "AI, Quantum Tech, Hardware & Systems",
    "Engineering, Design, Earth & Energy",
    "Philosophy, Social & Humanities",
]

SUPERDOMAIN_TO_PILLAR: Dict[str, str] = {
    # 1. Pure Mathematics
    "Number Theory & Arithmetic": "Pure Mathematics",
    "Algebra, Group & Category Theory": "Pure Mathematics",
    "Geometry & Topology": "Pure Mathematics",
    "Analysis, Calculus, PDEs & Dynamics": "Pure Mathematics",
    "Combinatorics & Graph Theory": "Pure Mathematics",
    # 2. Logic, Statistics & Computing
    "Mathematical Logic, Set Theory & Computability": "Logic, Statistics & Computing",
    "Probability, Stochastic Processes & Statistics": "Logic, Statistics & Computing",
    "Computer Science, Complexity, Crypto & Info Theory": "Logic, Statistics & Computing",
    # 3. Fundamental Physics & Cosmos
    "Quantum Mechanics, QFT & Particle Physics": "Fundamental Physics & Cosmos",
    "Spacetime, Gravity, Time, Dimensions & Holography": "Fundamental Physics & Cosmos",
    "Astrophysics, Cosmology & Astrobiology": "Fundamental Physics & Cosmos",
    # 4. Matter, Materials & Chemistry
    "Condensed Matter, Solid-State & Quantum Materials": "Matter, Materials & Chemistry",
    "Fluids, Gases, Plasmas & Non-Equilibrium Matter": "Matter, Materials & Chemistry",
    "Chemistry, Catalysis & Molecular Sciences": "Matter, Materials & Chemistry",
    # 5. Life, Mind & Medicine
    "Biology, Evolution, Origin of Life & Ecology": "Life, Mind & Medicine",
    "Neuroscience, Consciousness & Sentience": "Life, Mind & Medicine",
    "Medicine, Pharmacology, Longevity & Bioengineering": "Life, Mind & Medicine",
    # 6. AI, Quantum Tech, Hardware & Systems
    "Artificial Intelligence, ML & Digital Simulations": "AI, Quantum Tech, Hardware & Systems",
    "Quantum Computing & Quantum Information": "AI, Quantum Tech, Hardware & Systems",
    "Electronics, Photonics & Computing Hardware": "AI, Quantum Tech, Hardware & Systems",
    "Systems, Control, Robotics & Cybernetics": "AI, Quantum Tech, Hardware & Systems",
    # 7. Engineering, Design, Earth & Energy
    "Mechanical, Aerospace, Structural & Civil Engineering": "Engineering, Design, Earth & Energy",
    "Architecture, Urbanism, Design & Ergonomics": "Engineering, Design, Earth & Energy",
    "Geology, Geophysics, Earth, Ocean & Climate": "Engineering, Design, Earth & Energy",
    "Energy, Environment, Food & Sustainability": "Engineering, Design, Earth & Energy",
    # 8. Philosophy, Social & Humanities
    "Philosophy, Metaphysics, Epistemology & Ethics": "Philosophy, Social & Humanities",
    "Economics, Game Theory, Finance & Social Systems": "Philosophy, Social & Humanities",
    "Linguistics, Archaeology, History, Law & Aesthetics": "Philosophy, Social & Humanities",
}

PROBLEM_TYPES = {
    "Conjecture",
    "Existence/Uniqueness Proof",
    "Fundamental Mystery",
    "Hard Engineering Challenge",
    "Theoretical Unification",
    "Paradox / Foundational Apory",
    "Classification / Structural Problem",
    "Computational Complexity Separation",
    "Measurement / Experimental Frontier",
    "Design / Optimization Frontier",
}

EPISTEMIC_CLASSES = {
    "Formal-Deductive",
    "Empirical-Explanatory",
    "Constructive-Technological",
    "Normative-Philosophical",
    "Hybrid Formal-Empirical",
}

STATUSES_2026 = {
    "Completely Open",
    "Partially Solved / Special Cases",
    "Active Breakthroughs / Frontier",
    "AI Proof Claim (Fall/Nov 2026) — Under Verification",
    "Disputed Human Claim / Under Peer Review",
    "Independent / Undecidable Suspected",
    "Experimental Tension / Crisis",
}

BOTTLENECKS = {
    "Mathematical Tools Missing",
    "Energy / Experimental Scale Limit",
    "Computational Complexity Barrier",
    "Conceptual / Paradigmatic Gap",
    "Measurement / Instrumentation Limit",
    "Materials / Physical Limit",
    "Multiscale Coupling Complexity",
    "Ethical / Normative Ambiguity",
    "Data / Observational Horizon Limit",
}

SCALE_REGIMES = {
    "Planck / Sub-Atomic",
    "Atomic / Molecular",
    "Mesoscale / Cellular",
    "Macroscopic / Human",
    "Planetary / Ecological",
    "Astrophysical / Cosmic",
    "Scale-Invariant / Abstract Formal",
}

VERIFICATION_TYPES = {
    "Formal Mathematical Proof",
    "Reproducible Laboratory Experiment",
    "Astronomical / Observational Evidence",
    "Working Engineering Prototype / Benchmark",
    "Philosophical / Reflective Consensus",
    "Computational / Algorithmic Demonstration",
}

# Canonical Cross-Domain Hub Anchors (resolved by v2_loader.py to real problem IDs)
CANONICAL_HUBS = {
    "HUB:RIEMANN": "NT-001",
    "HUB:GRH": "NT-002",
    "HUB:GOLDBACH": "NT-003",
    "HUB:TWIN_PRIME": "NT-004",
    "HUB:COLLATZ": "NT-005",
    "HUB:BSD": "NT-006",
    "HUB:ABC": "NT-007",
    "HUB:LANGLANDS": "NT-008",
    "HUB:HODGE": "GEOM-001",
    "HUB:SPC4": "GEOM-002",
    "HUB:SPHERE_PACK": "GEOM-003",
    "HUB:NAVIER_STOKES": "ANL-001",
    "HUB:EULER_BLOWUP": "ANL-002",
    "HUB:KAKEYA": "ANL-003",
    "HUB:HADWIGER": "COMB-001",
    "HUB:RAMSEY": "COMB-002",
    "HUB:CONTINUUM_HYP": "LOG-001",
    "HUB:BUSY_BEAVER": "LOG-002",
    "HUB:PERCOLATION": "STAT-001",
    "HUB:CAUSAL_INFERENCE": "STAT-002",
    "HUB:P_VS_NP": "CS-001",
    "HUB:CRYPTO_OWF": "CS-002",
    "HUB:BQP_NP": "CS-003",
    "HUB:MATRIX_MULT": "CS-004",
    "HUB:QM_MEASUREMENT": "QM-001",
    "HUB:YANG_MILLS": "QM-002",
    "HUB:STRONG_CP": "QM-003",
    "HUB:HIERARCHY": "QM-004",
    "HUB:BARYOGENESIS": "QM-005",
    "HUB:ARROW_OF_TIME": "QM-006",
    "HUB:QUANTUM_GRAVITY": "GR-001",
    "HUB:BH_INFO": "GR-002",
    "HUB:HOLOGRAPHY": "GR-003",
    "HUB:DIMENSIONS": "GR-004",
    "HUB:DARK_MATTER": "ASTRO-001",
    "HUB:DARK_ENERGY": "ASTRO-002",
    "HUB:HUBBLE_TENSION": "ASTRO-003",
    "HUB:FERMI_PARADOX": "ASTRO-004",
    "HUB:SUPERCONDUCTIVITY": "CM-001",
    "HUB:GLASS_TRANSITION": "CM-002",
    "HUB:TURBULENCE": "FLD-001",
    "HUB:FUSION_PLASMA": "FLD-002",
    "HUB:FRACTURE": "FLD-003",
    "HUB:QUANTUM_CHEM": "CHEM-001",
    "HUB:HOMOCHIRALITY": "CHEM-002",
    "HUB:CATALYSIS_N2": "CHEM-003",
    "HUB:ABIOGENESIS": "BIO-001",
    "HUB:AGING": "BIO-002",
    "HUB:PROTEIN_DYNAMICS": "BIO-003",
    "HUB:GENOTYPE_PHENO": "BIO-004",
    "HUB:WHOLE_CELL": "BIO-005",
    "HUB:CONSCIOUSNESS": "NEURO-001",
    "HUB:NEURAL_CODE": "NEURO-002",
    "HUB:SENTIENCE": "NEURO-003",
    "HUB:ALZHEIMERS": "MED-001",
    "HUB:DRUG_DESIGN": "MED-002",
    "HUB:AI_ALIGNMENT": "AI-001",
    "HUB:OOD_AGI": "AI-002",
    "HUB:SIMULATION_HYP": "AI-003",
    "HUB:WHOLE_BRAIN_EMU": "AI-004",
    "HUB:FAULT_TOL_QC": "QC-001",
    "HUB:QUANTUM_PCP": "QC-002",
    "HUB:POST_MOORE": "HW-001",
    "HUB:LANDAUER": "HW-002",
    "HUB:OPTIMAL_CONTROL": "SYS-001",
    "HUB:SAFE_AUTONOMY": "SYS-002",
    "HUB:CASCADING_NETS": "SYS-003",
    "HUB:FATIGUE_STRUCT": "ENG-001",
    "HUB:SPACE_PROPULSION": "ENG-002",
    "HUB:GREEN_CONCRETE": "ENG-003",
    "HUB:ERGONOMICS": "ARC-001",
    "HUB:REGEN_CITIES": "ARC-002",
    "HUB:EARTHQUAKES": "GEO-001",
    "HUB:CLIMATE_ECS": "GEO-002",
    "HUB:TIPPING_POINTS": "GEO-003",
    "HUB:COMMERCIAL_FUSION": "ENR-001",
    "HUB:GRID_STORAGE": "ENR-002",
    "HUB:CARBON_CAPTURE": "ENR-003",
    "HUB:MIND_BODY": "PHIL-001",
    "HUB:INDUCTION": "PHIL-002",
    "HUB:FREE_WILL": "PHIL-003",
    "HUB:ETHICS_IS_OUGHT": "PHIL-004",
    "HUB:DIGITAL_MINDS": "PHIL-005",
    "HUB:MACRO_ECON": "ECON-001",
    "HUB:SOCIAL_CHOICE": "ECON-002",
    "HUB:COLLECTIVE_ACTION": "ECON-003",
    "HUB:ORIGIN_LANGUAGE": "HUM-001",
    "HUB:SYMBOL_GROUNDING": "HUM-002",
}


def compute_era(year: int) -> str:
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


def P(
    id: str,
    name: str,
    superdomain: str,
    subdomain: str,
    problem_type: str,
    epistemic_class: str,
    year_formulated: int,
    originator: str,
    status_2026: str,
    ai_verification_nov2026: str,
    registry_source: str,
    core_question: str,
    formal_expression: str,
    diff: int,
    tract: int,
    impact: int,
    interdisc: int,
    bottleneck: str,
    approaches: str,
    progress_2026: str,
    links: List[str],
    industries: str,
    scale: str,
    prize: str,
    verif: str,
    axis: str,
) -> Dict[str, Any]:
    assert superdomain in SUPERDOMAIN_TO_PILLAR, f"Bad superdomain '{superdomain}' in {id}"
    assert problem_type in PROBLEM_TYPES, f"Bad problem_type '{problem_type}' in {id}"
    assert epistemic_class in EPISTEMIC_CLASSES, f"Bad epistemic_class '{epistemic_class}' in {id}"
    assert status_2026 in STATUSES_2026, f"Bad status_2026 '{status_2026}' in {id}"
    assert bottleneck in BOTTLENECKS, f"Bad bottleneck '{bottleneck}' in {id}"
    assert scale in SCALE_REGIMES, f"Bad scale '{scale}' in {id}"
    assert verif in VERIFICATION_TYPES, f"Bad verif '{verif}' in {id}"
    for k, v in [("diff", diff), ("tract", tract), ("impact", impact), ("interdisc", interdisc)]:
        assert isinstance(v, int) and 1 <= v <= 10, f"Bad {k}={v} in {id}"
    return {
        "id": id,
        "name": name,
        "macro_pillar": SUPERDOMAIN_TO_PILLAR[superdomain],
        "superdomain": superdomain,
        "subdomain": subdomain,
        "problem_type": problem_type,
        "epistemic_class": epistemic_class,
        "year_formulated": int(year_formulated),
        "era": compute_era(int(year_formulated)),
        "age_years_2026": 2026 - int(year_formulated),
        "originator": originator,
        "status_2026": status_2026,
        "ai_verification_nov2026": ai_verification_nov2026,
        "registry_source": registry_source,
        "core_question": core_question,
        "formal_expression": formal_expression,
        "difficulty_score": diff,
        "tractability_2050": tract,
        "civilizational_impact": impact,
        "interdisciplinarity_index": interdisc,
        "primary_bottleneck": bottleneck,
        "competing_approaches": approaches,
        "closest_progress_2026": progress_2026,
        "raw_links": list(links),
        "affected_industries": industries,
        "scale_regime": scale,
        "prize_or_initiative": prize,
        "verification_type": verif,
        "contrast_axis": axis,
    }
