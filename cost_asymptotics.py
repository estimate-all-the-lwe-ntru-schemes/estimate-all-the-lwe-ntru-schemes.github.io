# -*- coding: utf-8 -*-
"""
BKZ cost asymptotics proposed to NIST as part of the PQC process.

NOTATION:

    BKZ COST
    beta        block size
    d           lattice dimension
    B           bitsize of entries

    LWE
    n       lwe secret dimension  (d*n for module lwe)
    q       lwe modulo
    sd      lwe secret standard deviation (if normal form)
    m       number of lwe samples

AUTHOR:

    Fernando Virdia - 2017, 2018
    Ben Curtis - 2018
"""


from sage.all import RR, ZZ, log, gamma, pi
from estimator.estimator import BKZ


# List of proposed cost models for BKZ
# Q-Sieving | Sieving | Q-Enum | Enum
# with Sieving = Core  | beta | 8d
BKZ_COST_ASYMPTOTICS = [
    {
        "name": "Q‑Core‑Sieve",
        "reduction_cost_model": lambda beta, d, B: ZZ(2)**RR(0.265*beta),
        "success_probability": 0.99,
        "human_friendly": "2<sup>0.265 β</sup>",
        "group": "Quantum sieving",
    },
    {
        "name": "Q‑Core‑Sieve + O(1)",
        "reduction_cost_model": lambda beta, d, B: ZZ(2)**RR(0.265*beta + 16),
        "success_probability": 0.99,
        "human_friendly": "2<sup>0.265 β + O(1)</sup>",
        "group": "Quantum sieving",
    },
    {
        "name": "Q‑Core‑Sieve (min space)",
        "reduction_cost_model": lambda beta, d, B: ZZ(2)**RR(0.2975*beta),
        "success_probability": 0.99,
        "human_friendly": "2<sup>0.298 β</sup>",
        "group": "Quantum sieving",
    },
    {
        "name": "Q‑β‑Sieve",
        "reduction_cost_model": lambda beta, d, B: ZZ(2)**RR(0.265*beta + log(beta,2)),
        "success_probability": 0.99,
        "human_friendly": "β 2<sup>0.265 β</sup>",
        "group": "Quantum sieving",
    },
    {
        "name": "Q‑8d‑Sieve + O(1)",
        "reduction_cost_model": lambda beta, d, B: ZZ(2)**RR(0.265*beta + 16.4 + log(8*d,2)),
        "success_probability": 0.99,
        "human_friendly": "8d 2<sup>0.265 β + O(1)</sup>",
        "group": "Quantum sieving",
    },
    {
        "name": "Core‑Sieve",
        "reduction_cost_model": lambda beta, d, B: ZZ(2)**RR(0.292*beta),
        "success_probability": 0.99,
        "human_friendly": "2<sup>0.292 β</sup>",
        "group": "Classical sieving",
    },
    {
        "name": "Core‑Sieve + O(1)",
        "reduction_cost_model": lambda beta, d, B: ZZ(2)**RR(0.292*beta + 16),
        "success_probability": 0.99,
        "human_friendly": "2<sup>292 β + O(1)</sup>",
        "group": "Classical sieving",
    },
    {
        "name": "Core‑Sieve (min space)",
        "reduction_cost_model": lambda beta, d, B: ZZ(2)**RR(0.368*beta),
        "success_probability": 0.99,
        "human_friendly": "2<sup>0.368 β</sup>",
        "group": "Classical sieving",
    },
    {
        "name": "β‑Sieve",
        "reduction_cost_model": lambda beta, d, B: ZZ(2)**RR(0.292*beta + log(beta,2)),
        "success_probability": 0.99,
        "human_friendly": "β 2<sup>0.292 β</sup>",
        "group": "Classical sieving",
    },
    {
        "name": "8d‑Sieve + O(1)",
        "reduction_cost_model": lambda beta, d, B: ZZ(2)**RR(0.292*beta + 16.4 + log(8*d,2)),
        "success_probability": 0.99,
        "human_friendly": "8d 2<sup>0.292 β + O(1)</sup>",
        "group": "Classical sieving",
    },
    {
        "name": "Q‑Core‑Enum + O(1)",
        "reduction_cost_model": lambda beta, d, B: ZZ(2)**RR((0.18728*beta*log(beta, 2) - 1.0192*beta + 16.1)/2),
        "success_probability": 0.99,
        "human_friendly": "2<sup>(0.18728 β ㏒ β - 1.0192 β + O(1))/2</sup>",
        "group": "Quantum enumeration",
    },
    {
        "name": "Lotus",
        "reduction_cost_model": lambda beta, d, B: ZZ(2)**(-0.7550818937366788*beta + 0.12472525302110621*beta*log(beta,2) + 2.254440896969337),
        "success_probability": 0.99,
        "human_friendly": "2<sup>-0.755 β + 0.125 β ㏒ β + O(1)</sup>",
        "group": "Quantum enumeration",
    },
    {
        "name": "Core‑Enum + O(1)",
        "reduction_cost_model": lambda beta, d, B: ZZ(2)**RR(0.18728*beta*log(beta, 2) - 1.0192*beta + 16.1),
        "success_probability": 0.99,
        "human_friendly": "2<sup>0.18728 β ㏒ β - 1.0192 β + O(1)</sup>",
        "group": "Classical enumeration",
    },
    # {
    #     "name": "8d‑Enum + O(1)",
    #     "reduction_cost_model": lambda beta, d, B: BKZ.LLL(d, B) +  BKZ.svp_repeat(beta, d) * ZZ(2)**RR(0.270188776350190*beta*log(beta) - 1.0192050451318417*beta + 16.10253135200765),
    #     "success_probability": 0.99,
    #     "human_friendly": "8d 2<sup>0.270 β ㏑ beta - 1.019 β + O(1)</sup>",
    #     "group": "Classical enumeration",
    # },
    {
        "name": "8d‑Enum (quadratic fit) + O(1)",
        "reduction_cost_model": lambda beta, d, B: BKZ.svp_repeat(beta, d) * ZZ(2)**RR(0.000784314*beta**2 + 0.366078*beta - 6.125 + 7),
        "success_probability": 0.99,
        "human_friendly": "8d 2<sup>0.000784 β² + 0.366 β + O(1)</sup>",
        "group": "Classical enumeration",
    },
]
