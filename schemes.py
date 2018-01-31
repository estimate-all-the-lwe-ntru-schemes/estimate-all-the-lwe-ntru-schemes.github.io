# -*- coding: utf-8 -*-
"""
Parameter selection for lattice based schemes submitted to NIST.

NOTATION:

    LWE
    n       lwe secret dimension (d*n for module lwe)
    q       lwe modulo
    sd      lwe error standard deviation (if normal form)
            the lwe error distribution which secret = error is normal form
    m       number of lwe samples

    NTRU-like
    n       dimension of f,g,h
    q       modulus
    norm_f  expected norm of f  -- we can swap norm_f and norm_g such that norm_g <= norm_f for a potentially better attack
    norm_g  expected norm of g  -- we can swap norm_f and norm_g such that norm_g <= norm_f for a potentially better attack
    m       number of lwe samples

AUTHOR:

    Ben Curtis - 2017, 2018
    Alex Davidson - 2017, 2018
    Amit Deo - 2018
    Rachel Player - 2017, 2018
    Eamonn Postlethwaite - 2018
    Fernando Virdia - 2017, 2018
    Thomas Wunderer - 2018

"""

from sage.all import sqrt, ln, floor, RR, ZZ

# List of proposed schemes
LWE_SCHEMES = [
    {
        "name": "AKCN‑RLWE",
        "params": [
            {
                "n": 1024,
                "sd": sqrt(8),
                "q": 12289,
                "secret_distribution": "normal",
                "m": 2*1024,
                "claimed": 255,
                "category": [
                    5,
                ],
                "ring": "x^n+1",
            },
        ],
        "assumption": [
            "RLWE",
        ],
        "primitive": [
            "KEM",
        ],
    },
    {
        "name": "AKCN‑MLWE",
        "params": [
            {
                "n": 256*3,
                "sd": 1,
                "q": 7681,
                "k": 3,
                "secret_distribution": "normal",
                "m": 6*768,
                "claimed": 147,
                "category": [
                    4,
                ],
                "ring": "x^{n/k}+1",
            },
            {
                "n": 256*3,
                "sd": sqrt(5),
                "q": 7681,
                "k": 3,
                "secret_distribution": "normal",
                "m": 6*768,
                "claimed": 183,
                "category": [
                    4,
                ],
                "ring": "x^{n/k}+1",
            },
        ],
        "assumption": [
            "MLWE",
        ],
        "primitive": [
            "KEM",
        ],
    },
    {
        "name": "BabyBear",
        "params": [
            {
                "n": 2*312,
                "sd": 1.,
                "q": 2**10,
                "k": 2,
                "secret_distribution": "normal",
                "claimed": 152,
                "category": [
                    2,
                ],
                "ring": "q^{n/k} - q^{n/(2k)} - 1",
            },
            {
                "n": 2*312,
                "sd": sqrt(5/ZZ(8)),
                "q": 2**10,
                "k": 2,
                "secret_distribution": "normal",
                "claimed": 141,
                "category": [
                    2,
                ],
                "ring": "q^{n/k} - q^{n/(2k)} - 1",
            },
        ],
        "assumption": [
            "ILWE",
        ],
        "primitive": [
            "KEM",
        ],
    },
    {
        "name": "MamaBear",
        "params": [
            {
                "n": 3*312,
                "sd": sqrt(7/ZZ(8)),
                "q": 2**10,
                "k": 3,
                "secret_distribution": "normal",
                "claimed": 237,
                "category": [
                    5,
                ],
                "ring": "q^{n/k} - q^{n/(2k)} - 1",
            },
            {

                "n": 3*312,
                "sd": sqrt(1/ZZ(2)),
                "q": 2**10,
                "k": 3,
                "secret_distribution": "normal",
                "claimed": 219,
                "category": [
                    4,
                ],
                "ring": "q^{n/k} - q^{n/(2k)} - 1",
            },
        ],
        "assumption": [
            "ILWE",
        ],
        "primitive": [
            "KEM",
        ],
    },
    {
        "name": "PapaBear",
        "params": [
            { # CPA
                "n": 3*312, # 1
                "sd": sqrt(3/ZZ(4)),
                "q": 2**10, # 2**(10*312) - 2**(5*312) - 1,
                "k": 3,
                "secret_distribution": "normal",
                "claimed": 320,
                "category": [
                    5,
                ],
                "ring": "q^{n/k} - q^{n/(2k)} - 1",
            },
            { # CCA
                "n": 3*312, # 1
                "sd": sqrt(3/ZZ(8)),
                "q": 2**10, # 2**(10*312) - 2**(5*312) - 1,
                "k": 3,
                "secret_distribution": "normal",
                "claimed": 292,
                "category": [
                    5,
                ],
                "ring": "q^{n/k} - q^{n/(2k)} - 1",
            },
        ],
        "assumption": [
            "ILWE",
        ],
        "primitive": [
            "KEM",
        ],
    },
    {
        "name": "CRYSTALS‑Dilithium",
        "params": [
            {
                "n": 256*3,
                "sd": sqrt((13**2-1)/ZZ(12)).n(),
                "q": 8380417,
                "k": 3,
                "secret_distribution": (-6, 6),
                "m": 256*4,
                "claimed": 91,
                "category": [
                    1,
                ],
                "ring": "x^{n/k}+1",
            },
            {
                "n": 256*4,
                "sd": sqrt((11**2-1)/ZZ(12)).n(),
                "q": 8380417,
                "k": 4,
                "secret_distribution": (-5, 5),
                "m": 256*5,
                "claimed": 125,
                "category": [
                    2,
                ],
                "ring": "x^{n/k}+1",
            },
            {
                "n": 256*5,
                "sd": sqrt((7**2-1)/ZZ(12)).n(),
                "q": 8380417,
                "k": 5,
                "secret_distribution": (-3, 3),
                "m": 256*6,
                "claimed": 158,
                "category": [
                    3,
                ],
                "ring": "x^{n/k}+1",
            },
        ],
        "assumption": [
            "MLWE",
        ],
        "primitive": [
            "DSA",
        ],
    },
    {
        "name": "CRYSTALS‑Kyber",
        "params": [
            {
                "n": 256*2,
                "sd": sqrt(5/ZZ(2)),
                "q": 7681,
                "k": 2,
                "secret_distribution": "normal",
                "m": 256*3,
                "claimed": 102,
                "category": [
                    1,
                ],
                "ring": "x^{n/k}+1",
            },
            {
                "n": 256*3,
                "sd": sqrt(4/ZZ(2)),
                "q": 7681,
                "k": 3,
                "secret_distribution": "normal",
                "m": 256*4,
                "claimed": 161,
                "category": [
                    3,
                ],
                "ring": "x^{n/k}+1",
            },
            {
                "n": 256*4,
                "sd": sqrt(3/ZZ(2)),
                "q": 7681,
                "k": 4,
                "secret_distribution": "normal",
                "m": 256*5,
                "claimed": 218,
                "category": [
                    5,
                ],
                "ring": "x^{n/k}+1",
            },
        ],
        "assumption": [
            "MLWE",
        ],
        "primitive": [
            "KEM",
            "PKE",
        ],
    },
    {
        "name": "Ding Key Exchange",
        "params": [
            {
                "n": 512,
                "sd": 4.19,
                "q": 120883,
                "secret_distribution": "normal",
                "claimed": None,
                "category": [
                    1,
                ],
                "ring": "x^n+1",
            },
            {
                "n": 1024,
                "sd": 2.6,
                "q": 120883,
                "secret_distribution": "normal",
                "claimed": None,
                "category": [
                    3,
                    5,
                ],
                "ring": "x^n+1",
            },
        ],
        "assumption": [
            "RLWE",
        ],
        "primitive": [
            "KEM",
        ],
    },
    {
        "name": "EMBLEM",
        "params": [
            {
                "n": 770,
                "sd": 25,
                "q": 2**24,
                "secret_distribution": (-1, 1),
                "m": 1003,
                "claimed": 128.3,
                "category": [
                    1,
                ],
            },
            {
                "n": 611,
                "sd": 25,
                "q": 2**24,
                "secret_distribution": (-2,2),
                "m": 832,
                "claimed": 128.3,
                "category": [
                    1,
                ],
            },
        ],
        "assumption": [
            "LWE",
        ],
        "primitive": [
            "PKE",
            "KEM",
        ],
    },
    {
        "name": "R EMBLEM",
        "params": [
            {
                "n": 512,
                "sd": 25,
                "q": 2**16,
                "secret_distribution": (-1,1),
                "claimed": 128,
                "category": [
                    1,
                ],
                "ring": "x^n+1",
            },
            {
                "n": 512,
                "sd": 3,
                "q": 2**14,
                "secret_distribution": (-1,1),
                "claimed": 128,
                "category": [
                    1,
                ],
                "ring": "x^n+1",
            },
        ],
        "assumption": [
            "RLWE"
        ],
        "primitive": [
            "PKE",
            "KEM",
        ],
    },
    {
        "name": "Frodo",
        "params": [
            {
                "n": 640,
                "sd": 2.75,
                "q": 2**15,
                "secret_distribution": "normal",
                "claimed": 103,
                "category": [
                    1,
                ],
            },
            {
                "n": 976,
                "sd": 2.3,
                "q":2**16,
                "secret_distribution": "normal",
                "claimed": 150,
                "category": [
                    3,
                ],
            },
        ],
        "assumption": [
            "LWE",
        ],
        "primitive": [
            "KEM",
            "PKE",
        ],
    },
    {
        "name": "NewHope",
        "params": [
            {
                "n": 512,
                "sd": 2,
                "q": 12289,
                "secret_distribution": "normal",
                "claimed": 101,
                "category": [
                    1,
                ],
                "ring": "x^n+1",
            },
            {
                "n": 1024,
                "sd": 2,
                "q": 12289,
                "secret_distribution": "normal",
                "claimed": 233,
                "category": [
                    5,
                ],
                "ring": "x^n+1",
            },
        ],
        "assumption": [
            "RLWE",
        ],
        "primitive": [
            "KEM",
            "PKE",
        ],
    },
    {
        "name": "HILA5",
        "params": [
            {
                "n": 1024,
                "sd": sqrt(8),
                "q": 12289,
                "secret_distribution": "normal",
                "claimed": 128,
                "category": [
                    5,
                ],
                "ring": "x^n+1",
            },
        ],
        "assumption": [
            "RLWE",
        ],
        "primitive": [
            "KE",
        ],
    },
    {
        "name": "KINDI",
        "params": [
            {
                "n": 256*3,
                "sd": sqrt((8**2-1)/ZZ(12) + (-0.5)**2),
                "q": 2**14,
                "k": 3,
                "secret_distribution": (-4, 4), # (-4,3),
                "claimed": 164,
                "category": [
                    2,
                ],
                "ring": "x^{n/k}+1",
            },
            {
                "n": 512*2,
                "sd": sqrt((4**2-1)/ZZ(12)),
                "q": 2**13,
                "k": 2,
                "secret_distribution": (-2, 2), # (-2,1),
                "claimed": 207,
                "category": [
                    4,
                ],
                "ring": "x^{n/k}+1",
            },
            {
                "n": 512*2,
                "sd": sqrt((8**2-1)/ZZ(12)),
                "q": 2**14,
                "k": 2,
                "secret_distribution": (-4, 4), # (-4,3),
                "claimed": 232,
                "category": [
                    4,
                ],
                "ring": "x^{n/k}+1",
            },
            {
                "n": 256*5,
                "sd": sqrt((4**2-1)/ZZ(12)),
                "q": 2**14,
                "k": 5,
                "secret_distribution": (-2, 2), # (-2,1),
                "claimed": 251,
                "category": [
                    5,
                ],
                "ring": "x^{n/k}+1",
            },
            {
                "n": 512*3,
                "sd": sqrt((4**2-1)/ZZ(12)),
                "q": 2**13,
                "k": 3,
                "secret_distribution": (-2, 2), # (-2,1),
                "claimed": 330,
                "category": [
                    5,
                ],
                "ring": "x^{n/k}+1",
            },
        ],
        "assumption": [
            "MLWE",
        ],
        "primitive": [
            "PKE",
            "KEM",
        ],
    },
    {
        "name": "LAC",
        "params": [
            {
                "n": 512,
                "sd": 1/sqrt(2),
                "q": 251,
                "secret_distribution": "normal",
                "m": 2*512,
                "claimed": 128,
                "category": [
                    1,
                    2,
                ],
                "ring": "x^n+1",
            },
            {
                "n": 1024,
                "sd": 0.5,
                "q": 251,
                "secret_distribution": "normal",
                "m": 2*1024,
                "claimed": 192,
                "category": [
                    3,
                    4,
                ],
                "ring": "x^n+1",
            },
            {
                "n": 1024,
                "sd": 1/sqrt(2),
                "q": 251,
                "secret_distribution": "normal",
                "m": 2*1024,
                "claimed": 256,
                "category": [
                    5,
                ],
                "ring": "x^n+1",
            }
        ],
        "assumption": [
            "PLWE",
        ],
        "primitive": [
            "PKE",
            "KEM",
            "KE",
        ],
    },
    {
        "name": "LIMA-2p",
        "params": [
            {
                "n": 1024,
                "sd": sqrt(10),
                "q": 133121,
                "secret_distribution": "normal",
                "claimed": 208.8,
                "category": [
                    3,
                ],
                "ring": "x^n+1",
            },
            {
                "n": 2048,
                "sd": sqrt(10),
                "q": 184321,
                "secret_distribution": "normal",
                "claimed": 444.5,
                "category": [
                    4,
                ],
                "ring": "x^n+1",
            }
        ],
        "assumption": [
            "RLWE",
        ],
        "primitive": [
            "KEM",
            "PKE",
        ],
    },
    {
        "name": "LIMA‑sp",
        "params": [
            {
                "n": 1018,
                "sd": sqrt(10),
                "q": 12521473,
                "secret_distribution": "normal",
                "claimed": 139.2,
                "category": [
                    1,
                ],
                "ring": "\sum_{i=0}^n x^i",
            },
            {
                "n": 1306,
                "sd": sqrt(10),
                "q": 48181249,
                "secret_distribution": "normal",
                "claimed": 167.8,
                "category": [
                    2,
                ],
                "ring": "\sum_{i=0}^n x^i",
            },
            {
                "n": 1822,
                "sd": sqrt(10),
                "q": 44802049,
                "secret_distribution": "normal",
                "claimed": 247.9,
                "category": [
                    3,
                ],
                "ring": "\sum_{i=0}^n x^i",
            },
            {
                "n": 2062,
                "sd": sqrt(10),
                "q": 16900097,
                "secret_distribution": "normal",
                "claimed": 303.5,
                "category": [
                    4,
                ],
                "ring": "\sum_{i=0}^n x^i",
            }
        ],
        "assumption": [
            "RLWE",
        ],
        "primitive": [
            "KEM",
            "PKE",
        ],
    },
    {
        "name": "Lizard",
        "params": [
            {
                "n": 536,
                "sd": sqrt(4**2/ZZ(12)), # q/p = 4
                "q": 2048,
                "secret_distribution": ((-1,1), 140), # 792,
                "claimed": 130,
                "category": [
                    1,
                ],
            },
            {
                "n": 663,
                "sd": sqrt(4**2/ZZ(12)),
                "q": 1024,
                "secret_distribution": ((-1,1), 128), # 919,
                "claimed": 147,
                "category": [
                    1,
                ],
            },
            {
                "n": 816,
                "sd": sqrt(4**2/ZZ(12)),
                "q": 2048,
                "secret_distribution": ((-1,1), 200), # 1200,
                "claimed": 195,
                "category": [
                    3,
                ],
            },
            {
                "n": 952,
                "sd": sqrt(4**2/ZZ(12)),
                "q": 2048,
                "secret_distribution": ((-1,1), 200),
                "m": 1336,
                "claimed": 195,
                "category": [
                    3,
                ],
            },
            {
                "n": 1088,
                "sd": sqrt(4**2/ZZ(12)),
                "q": 4096,
                "secret_distribution": ((-1,1),200), # 1600,
                "claimed": 257,
                "category": [
                    5,
                ],
            },
            {
                "n": 1300,
                "sd": sqrt(4**2/ZZ(12)),
                "q": 2048,
                "secret_distribution": ((-1,1),200), # 1812,
                "claimed": 291,
                "category": [
                    5,
                ],
            },
        ],
        "assumption": [
            "LWE",
            "LWR",
        ],
        "primitive":[
            "PKE",
            "KEM",
        ],
    },
    {
        "name": "RLizard",
        "params": [
            {
                "n": 1024,
                "sd": sqrt(4**2/ZZ(12)),
                "q": 1024,
                "secret_distribution": ((-1,1), 128),
                "claimed": 147,
                "category": [
                    1,
                ],
                "ring": "x^n+1",
            },
            {
                "n": 1024,
                "sd": sqrt(4**2/ZZ(12)),
                "q": 2048,
                "secret_distribution": ((-1,1), 264),
                "claimed": 195,
                "category": [
                    3,
                ],
                "ring": "x^n+1",
            },
            {
                "n": 2048,
                "sd": sqrt(4**2/ZZ(12)),
                "q": 2048,
                "secret_distribution": ((-1,1), 164),
                "claimed": 291,
                "category": [
                    3,
                ],
                "ring": "x^n+1",
            },
            {
                "n": 2048,
                "sd": sqrt(4**2/ZZ(12)),
                "q": 4096,
                "secret_distribution": ((-1,1), 256),
                "claimed": 348,
                "category": [
                    5,
                ],
                "ring": "x^n+1",
            },
        ],
        "assumption": [
            "RLWE",
            "RLWR",
        ],
        "primitive": [
            "PKE",
            "KEM",
        ],
    },
    {
        "name": "LOTUS",
        "params": [
            {
                "n": 576,
                "sd": 3,
                "q": 8192,
                "secret_distribution": "normal",
                "claimed": 128,
                "category": [
                    1,
                    2,
                ],
            },
            {
                "n": 704,
                "sd": 3,
                "q": 8192,
                "secret_distribution": "normal",
                "claimed": 192,
                "category": [
                    3,
                    4,
                ],
            },
            {
                "n": 832,
                "sd": 3,
                "q": 8192,
                "secret_distribution": "normal",
                "claimed": 256,
                "category": [
                    5,
                ],
            },
        ],
        "assumption": [
            "LWE",
        ],
        "primitive": [
            "KEM",
            "PKE",
        ],
    },
    {
        "name": "uRound2.KEM",
        "params": [
            {
                "n": 500,
                "sd": sqrt(8**2/ZZ(12)), # |e_i| < q/(2p) unif, sd = sqrt((q/p)**2/ZZ(12)), q/p = 8
                "q": 2**14,
                "secret_distribution": ((-1,1), 74),
                "claimed": 74,
                "category": [
                    1,
                ],
            },
            {
                "n": 580,
                "sd": sqrt(16**2/ZZ(12)), # |e_i| < q/(2p) unif, sd = sqrt(((q/p+1)**2-1)/ZZ(12)), q/p = 16
                "q": 2**15,
                "secret_distribution": ((-1,1), 116),
                "claimed": 96,
                "category": [
                    2,
                ],
            },
            {
                "n": 630,
                "sd": sqrt(16**2/ZZ(12)), # |e_i| < q/(2p) unif, sd = sqrt(((q/p+1)**2-1)/ZZ(12)), q/p = 16
                "q": 2**15,
                "secret_distribution": ((-1,1), 126),
                "claimed": 106,
                "category": [
                    3,
                ],
            },
            {
                "n": 786,
                "sd": sqrt(16**2/ZZ(12)), # |e_i| < q/(2p) unif, sd = sqrt(((q/p+1)**2-1)/ZZ(12)), q/p = 16
                "q": 2**15,
                "secret_distribution": ((-1,1), 156),
                "claimed": 139,
                "category": [
                    4,
                ],
            },
            {
                "n": 786,
                "sd": sqrt(16**2/ZZ(12)), # |e_i| < q/(2p) unif, sd = sqrt(((q/p+1)**2-1)/ZZ(12)), q/p = 16
                "q": 2**15,
                "secret_distribution": ((-1,1), 156),
                "claimed": 138,
                "category": [
                    5,
                ],
            },
        ],
        "assumption": [
            "LWR",
        ],
        "primitive": [
            "KEM",
        ],
    },
    {
        "name": "uRound2.KEM", # Ring
        "params": [
            {
                "n": 418,
                "sd": sqrt(16**2/ZZ(12)),  # |e_i| < q/(2p) unif, sd = sqrt(((q/p+1)**2-1)/ZZ(12)), q/p = 16
                "q": 2**12,
                "secret_distribution": ((-1,1), 66),
                "claimed": 75,
                "category": [
                    1,
                ],
                "ring": "\sum_{i=0}^n x^i",
            },
            {
                "n": 522,
                "sd": sqrt(128**2/ZZ(12)), # |e_i| < q/(2p) unif, sd = sqrt(((q/p+1)**2-1)/ZZ(12)), q/p = 128
                "q": 32768,
                "secret_distribution": ((-1,1), 78),
                "claimed": 97,
                "category": [
                    2,
                ],
                "ring": "\sum_{i=0}^n x^i",
            },
            {
                "n": 540,
                "sd": sqrt(64**2/ZZ(12)), # |e_i| < q/(2p) unif, sd = sqrt(((q/p+1)**2-1)/ZZ(12)), q/p = 64
                "q": 16384,
                "secret_distribution": ((-1,1), 96),
                "claimed": 106,
                "category": [
                    3,
                ],
                "ring": "\sum_{i=0}^n x^i",
            },
            {
                "n": 700,
                "sd": sqrt(128**2/ZZ(12)), # |e_i| < q/(2p) unif, sd = sqrt(((q/p+1)**2-1)/ZZ(12)), q/p = 128
                "q": 32768,
                "secret_distribution": ((-1,1), 112),
                "claimed": 140,
                "category": [
                    4,
                ],
                "ring": "\sum_{i=0}^n x^i",
            },
            {
                "n": 676,
                "sd": sqrt(128**2/ZZ(12)), # |e_i| < q/(2p) unif, sd = sqrt(((q/p+1)**2-1)/ZZ(12)), q/p = 128
                "q": 32768,
                "secret_distribution": ((-1,1), 120),
                "claimed": 139,
                "category": [
                    5,
                ],
                "ring": "\sum_{i=0}^n x^i",
            },
        ],
        "assumption": [
            "RLWR",
        ],
        "primitive": [
            "KEM",
        ],
    },
    {
        "name": "uRound2.PKE",
        "params": [
            {
                "n": 500,
                "sd": sqrt(16**2/ZZ(12)), # |e_i| < q/(2p) unif, sd = sqrt(((q/p+1)**2-1)/ZZ(12)), q/p = 2**4
                "q": 32768,
                "secret_distribution": ((-1,1), 74),
                "claimed": 74,
                "category": [
                    1,
                ],
            },
            {
                "n": 585,
                "sd": sqrt(16**2/ZZ(12)), # |e_i| < q/(2p) unif, sd = sqrt(((q/p+1)**2-1)/ZZ(12)), q/p = 2**4
                "q": 32768,
                "secret_distribution": ((-1,1), 110),
                "claimed": 96,
                "category": [
                    2,
                ],
            },
            {
                "n": 643,
                "sd": sqrt(16**2/ZZ(12)), # |e_i| < q/(2p) unif, sd = sqrt(((q/p+1)**2-1)/ZZ(12)), q/p = 2**4
                "q": 32768,
                "secret_distribution": ((-1,1), 114),
                "claimed": 106,
                "category": [
                    3,
                ],
            },
            {
                "n": 835,
                "sd": sqrt(8**2/ZZ(12)), # |e_i| < q/(2p) unif, sd = sqrt(((q/p+1)**2-1)/ZZ(12)), q/p = 2**3
                "q": 32768,
                "secret_distribution": ((-1,1), 166),
                "claimed": 138,
                "category": [
                    4,
                ],
            },
            {
                "n": 835,
                "sd": sqrt(8**2/ZZ(12)), # |e_i| < q/(2p) unif, sd = sqrt(((q/p+1)**2-1)/ZZ(12)), q/p = 2**3
                "q": 32768,
                "secret_distribution": ((-1,1), 166),
                "claimed": 138,
                "category": [
                    5,
                ],
            },
        ],
        "assumption": [
            "LWR",
        ],
        "primitive": [
            "PKE",
        ],
    },
    {
        "name": "uRound2.PKE", # ring
        "params": [
            {
                "n": 420,
                "sd": sqrt(4**2/ZZ(12)), # |e_i| < q/(2p) unif, sd = sqrt(((q/p+1)**2-1)/ZZ(12)), q/p = 4
                "q": 1024,
                "secret_distribution": ((-1,1), 62),
                "claimed": 74,
                "category": [
                    1,
                ],
                "ring": "\sum_{i=0}^n x^i",
            },
            {
                "n": 540,
                "sd": sqrt(16**2/ZZ(12)), # |e_i| < q/(2p) unif, sd = sqrt(((q/p+1)**2-1)/ZZ(12)), q/p = 16
                "q": 8192,
                "secret_distribution": ((-1,1), 96),
                "claimed": 97,
                "category": [
                    2,
                ],
                "ring": "\sum_{i=0}^n x^i",
            },
            {
                "n": 586,
                "sd": sqrt(16**2/ZZ(12)), # |e_i| < q/(2p) unif, sd = sqrt(((q/p+1)**2-1)/ZZ(12)), q/p = 16
                "q": 8192,
                "secret_distribution": ((-1,1), 104),
                "claimed": 107,
                "category": [
                    3,
                ],
                "ring": "\sum_{i=0}^n x^i",
            },
            {
                "n": 708,
                "sd": sqrt(64**2/ZZ(12)), # |e_i| < q/(2p) unif, sd = sqrt(((q/p+1)**2-1)/ZZ(12)), q/p = 2**6
                "q": 32768,
                "secret_distribution": ((-1,1), 140),
                "claimed": 138,
                "category": [
                    4,
                    5,
                ],
                "ring": "\sum_{i=0}^n x^i",
            },
        ],
        "assumption": [
            "RLWR",
        ],
        "primitive": [
            "PKE",
        ],
    },
    {
        "name": "nRound2.KEM",
        "params": [
            {
                "n": 400,
                "sd": sqrt((3209/ZZ(2**8))**2/ZZ(12)), # |e_i| < q/(2p) unif, sd = sqrt(((q/p+1)**2-1)/ZZ(12)), p = 2**8
                "q": 3209,
                "secret_distribution": ((-1,1), 72),
                "claimed": 74,
                "category": [
                    1,
                ],
                "ring": "\sum_{i=0}^n x^i",
            },
            {
                "n": 486,
                "sd": sqrt(((1949/ZZ(2**8))**2)/ZZ(12)), # |e_i| < q/(2p) unif, sd = sqrt(((q/p+1)**2-1)/ZZ(12)), p = 2**8
                "q": 1949,
                "secret_distribution": ((-1,1), 96),
                "claimed": 97,
                "category": [
                    2,
                ],
                "ring": "\sum_{i=0}^n x^i",
            },
            {
                "n": 556,
                "sd": sqrt(((3343/ZZ(2**8))**2)/ZZ(12)), # |e_i| < q/(2p) unif, sd = sqrt(((q/p+1)**2-1)/ZZ(12)), p = 2**8
                "q": 3343,
                "secret_distribution": ((-1,1), 88),
                "claimed": 106,
                "category": [
                    3,
                ],
                "ring": "\sum_{i=0}^n x^i",
            },
            {
                "n": 658,
                "sd": sqrt(((1319/ZZ(2**8))**2)/ZZ(12)), # |e_i| < q/(2p) unif, sd = sqrt(((q/p+1)**2-1)/ZZ(12)), p = 2**8
                "q": 1319,
                "secret_distribution": ((-1,1), 130),
                "claimed": 139,
                "category": [
                    4,
                    5,
                ],
                "ring": "\sum_{i=0}^n x^i",
            },
        ],
        "assumption": [
            "RLWR",
        ],
        "primitive": [
            "KEM",
        ],
    },
    {
        "name": "nRound2.PKE",
        "params": [
            {
                "n": 442,
                "sd": sqrt(((2659/ZZ(2**9))**2)/ZZ(12)), # |e_i| < q/(2p) unif, sd = sqrt(((q/p+1)**2-1)/ZZ(12)), p= 2**9
                "q": 2659,
                "secret_distribution": ((-1,1), 74),
                "claimed": 74,
                "category": [
                    1,
                ],
                "ring": "\sum_{i=0}^n x^i",
            },
            {
                "n": 556,
                "sd": sqrt(((3343/ZZ(2**9))**2)/ZZ(12)), # |e_i| < q/(2p) unif, sd = sqrt(((q/p+1)**2-1)/ZZ(12)), p= 2**9
                "q": 3343,
                "secret_distribution": ((-1,1), 88),
                "claimed": 97,
                "category": [
                    2,
                ],
                "ring": "\sum_{i=0}^n x^i",
            },
            {
                "n": 576,
                "sd": sqrt(((2309/ZZ(2**9))**2)/ZZ(12)), # |e_i| < q/(2p) unif, sd = sqrt(((q/p+1)**2-1)/ZZ(12)), p= 2**9
                "q": 2309,
                "secret_distribution": ((-1,1), 108),
                "claimed": 106,
                "category": [
                    3,
                ],
                "ring": "\sum_{i=0}^n x^i",
            },
            {
                "n": 708,
                "sd": sqrt(((2837/ZZ(2**9))**2)/ZZ(12)), # |e_i| < q/(2p) unif, sd = sqrt(((q/p+1)**2-1)/ZZ(12)), p= 2**9
                "q": 2837,
                "secret_distribution": ((-1,1), 140),
                "claimed": 138,
                "category": [
                    4,
                    5,
                ],
                "ring": "\sum_{i=0}^n x^i",
            },
        ],
        "assumption": [
            "RLWR",
        ],
        "primitive": [
            "PKE",
        ],
    },
    {
        "name": "LightSaber",
        "params": [
            {
                "n": 2*256,
                "sd": sqrt(16/ZZ(3)), # binomial -> sqrt(5), not far from 3
                "q": 2**13,
                "k": 2,
                "secret_distribution": "normal",
                "m": 3*256,
                "claimed": 115,
                "category": [
                    1,
                ],
                "ring": "x^{n/k} + 1",
            },
        ],
        "assumption": [
            "MLWR",
        ],
        "primitive": [
            "PKE",
            "KEM"
        ],
    },
    {
        "name": "Saber",
        "params": [
            {
                "n": 3*256,
                "sd": sqrt(16/ZZ(3)),
                "q": 2**13,
                "k": 3,
                "secret_distribution": "normal",
                "m": 4*256,
                "claimed": 180,
                "category": [
                    3,
                ],
                "ring": "x^{n/k} + 1",
            },
        ],
        "assumption": [
            "MLWR",
        ],
        "primitive": [
            "PKE",
            "KEM"
        ],
    },
    {
        "name": "FireSaber",
        "params": [
            {
                "n": 4*256,
                "sd": sqrt(16/ZZ(3)),
                "q": 2**13,
                "k": 4,
                "secret_distribution": "normal",
                "m": 5*256,
                "claimed": 245,
                "category": [
                    5,
                ],
                "ring": "x^{n/k} + 1",
            },
        ],
        "assumption": [
            "MLWR",
        ],
        "primitive": [
            "PKE",
            "KEM"
        ],
    },
    {
        "name": "qTESLA",
        "params": [
            {
                "n": 1024,
                "sd": 10/sqrt(2*ln(2)),
                "q": 8058881,
                "secret_distribution": "normal",
                "claimed": 128,
                "category": [
                    1,
                ],
                "ring": "x^n + 1",
            },
            {
                "n": 2048,
                "sd": 10/sqrt(2*ln(2)),
                "q": 12681217,
                "secret_distribution": "normal",
                "claimed": 192,
                "category": [
                    3,
                ],
                "ring": "x^n + 1",
            },
            {
                "n": 2048,
                "sd": 10/sqrt(2*ln(2)),
                "q": 27627521,
                "secret_distribution": "normal",
                "claimed": 256,
                "category": [
                    5,
                ],
                "ring": "x^n + 1",
            },
        ],
        "assumption": [
            "RLWE",
        ],
        "primitive": [
            "DSA",
        ],
    },
    {
        "name": "Titanium.PKE",
        "params": [
            { # page 24, table 2.1, 128 bits of security
                "n": 1024,
                "sd": sqrt(2),
                "q": 86017,
                "secret_distribution": "normal", # 9*1024 ?
                "claimed": 128,
                "category": [
                    1,
                ],
                "ring": "x^n + \sum^{n-1}_{i=1} f_i x^i + f_0 \\text{ *}"
            },
            { # page 24, table 2.1, 128 bits of security
                "n": 1280,
                "sd": sqrt(2),
                "q": 301057,
                "secret_distribution": "normal", # 9*1280,
                "claimed": 160,
                "category": [
                    1,
                ],
                "ring": "x^n + \sum^{n-1}_{i=1} f_i x^i + f_0 \\text{ *}"
            },
            { # 192 bits of security
                "n": 1536,
                "sd": sqrt(2),
                "q": 737281,
                "secret_distribution": "normal", # 7*1536,
                "claimed": 192,
                "category": [
                    3,
                ],
                "ring": "x^n + \sum^{n-1}_{i=1} f_i x^i + f_0 \\text{ *}"
            },
            { # 256 bits of security
                "n": 2048,
                "sd": sqrt(2),
                "q": 1198081,
                "secret_distribution": "normal", # 7*2048,
                "claimed": 256,
                "category": [
                    5,
                ],
                "ring": "x^n + \sum^{n-1}_{i=1} f_i x^i + f_0 \\text{ *}"
            },
        ],
        "assumption": [
            "PLWE"
        ],
        "primitive": [
            "PKE"
        ],
    },
    {
        "name": "Titanium.KEM",
        "params": [
            { # page 27, table 2.6
                "n": 1024,
                "sd": sqrt(2),
                "q": 118273,
                "secret_distribution": "normal", # 10*1024,
                "claimed": 128,
                "category": [
                    1,
                ],
                "ring": "x^n + \sum^{n-1}_{i=1} f_i x^i + f_0 \\text{ *}"
            },
            {
                "n": 1280,
                "sd": sqrt(2),
                "q": 430081,
                "secret_distribution": "normal", # 10*1280,
                "claimed": 160,
                "category": [
                    1,
                ],
                "ring": "x^n + \sum^{n-1}_{i=1} f_i x^i + f_0 \\text{ *}"
            },
            {
                "n": 1536,
                "sd": sqrt(2),
                "q": 783361,
                "secret_distribution": "normal", # 8*1536,
                "claimed": 192,
                "category": [
                    3,
                ],
                "ring": "x^n + \sum^{n-1}_{i=1} f_i x^i + f_0 \\text{ *}"
            },
            {
                "n": 2048,
                "sd": sqrt(2),
                "q": 1198081,
                "secret_distribution": "normal", # 8*2048,
                "claimed": 256,
                "category": [
                    5,
                ],
                "ring": "x^n + \sum^{n-1}_{i=1} f_i x^i + f_0 \\text{ *}"
            },
        ],
        "assumption": [
            "PLWE",
        ],
        "primitive": [
            "KEM"
        ],
    },
]

NTRU_SCHEMES = [
    {
        "name": "NTRUEncrypt",
        "params": [
            {
                "n": 443,
                "sd": sqrt((143 + 144)/ZZ(443)),
                "q": 2048,
                "secret_distribution": ((-1,1), 143 + 144),
                "m": 443,
                "norm_f": sqrt(143 + 144),
                "norm_g": sqrt(143 + 144),
                "claimed": 84,
                "category": [
                    1,
                ],
                "ring": "x^n - 1",
            },
            {
                "n": 743,
                "sd": sqrt((247 + 248)/ZZ(743)),
                "q": 2048,
                "secret_distribution": ((-1,1), 247 + 248),
                "m": 743,
                "norm_f": sqrt(247 + 248),
                "norm_g": sqrt(247 + 248),
                "claimed": 159,
                "category": [
                    1,
                    2,
                    3,
                    4,
                    5,
                ],
                "ring": "x^n - 1",
            },
            {
                "n": 1024,
                "sd": 724,
                "q": 2**30+2**13+1,
                "secret_distribution": "normal",
                "m": 1024,
                "norm_f": sqrt(1024)*724,
                "norm_g": sqrt(1024)*724,
                "claimed": 198,
                "category": [
                    4,
                    5,
                ],
                "ring": "x^n - 1",
            }
        ],
        "assumption": [
            "NTRU",
        ],
        "primitive": [
            "KEM",
            "PKE",
        ],
    },
    {
        "name": "Falcon",
        "params": [
            {
                "n": 512,
                "sd": 1.17*sqrt((12289/ZZ(2))/ZZ(512)),
                "q": 12289,
                "secret_distribution": "normal",
                "m": 512,
                "norm_f": sqrt(12289/ZZ(2))*1.17,
                "norm_g": sqrt(12289/ZZ(2))*1.17,
                "claimed": 103,
                "category": [
                    1,
                ],
                "ring": "x^n + 1",
            },
            {
                "n": 768,
                "sd": 1.17*sqrt((18433/ZZ(2))/ZZ(768)),
                "q": 18433,
                "secret_distribution": "normal",
                "m": 768,
                "norm_f": sqrt(18433/ZZ(2))*1.17,
                "norm_g": sqrt(18433/ZZ(2))*1.17,
                "claimed": 172,
                "category": [
                    2,
                    3,
                ],
                "ring": "x^n - x^{n/2} + 1",
            },
            {
                "n": 1024,
                "sd": 1.17*sqrt((12289/ZZ(2))/ZZ(1024)),
                "q": 12289,
                "secret_distribution": "normal",
                "m": 1024,
                "norm_f": sqrt(12289/ZZ(2))*1.17,
                "norm_g": sqrt(12289/ZZ(2))*1.17,
                "claimed": 230,
                "category": [
                    4,
                    5,
                ],
                "ring": "x^n + 1",
            }
        ],
        "assumption": [
            "NTRU",
        ],
        "primitive": [
            "DSA",
        ],
    },
    {
        "name": "NTRU HRSS",
        "params": [
           {
               "n": 700,
               "sd": sqrt((700*10/ZZ(16))/ZZ(700)),
               "q": 8192,
               "secret_distribution": ((-1,1), floor(700*10/ZZ(16))),
               "m": 700,
               "norm_f": sqrt(700*10/ZZ(16)),
               "norm_g": sqrt(700*10/ZZ(16)),
               "claimed": 123,
               "category": [
                   1,
               ],
               "ring": "\sum_{i=0}^{n-1} x^i",
           }
        ],
        "assumption": [
            "NTRU",
        ],
        "primitive": [
            "KEM",
        ],
    },
    {
        "name": "NTRU Prime",
        "params": [
            {
                "n": 761,
                "sd": sqrt((761 * 2/ZZ(3))/ZZ(761)),
                "q": 4591,
                "secret_distribution": ((-1,1), 286),
                "m": 761,
                "norm_f": sqrt(286),
                "norm_g": sqrt(761 * 2/ZZ(3)),
                "claimed": 248,
                "category": [
                    5,
                ],
                "ring": "x^n - x - 1",
            },
            {
                "n": 761,
                "sd": sqrt((761 * 2/ZZ(3))/ZZ(761)),
                "q": 4591,
                "secret_distribution": ((-1,1), 250),
                "m": 761,
                "norm_f": sqrt(250),
                "norm_g": sqrt(761 * 2/ZZ(3)),
                "claimed": 225,
                "category": [
                    5,
                ],
                "ring": "x^n - x - 1",
            }
        ],
        "assumption": [
            "NTRU",
        ],
        "primitive": [
            "KEM",
        ],
    },
	{
        "name": "pqNTRUsign",
        "params": [
            {
                "n": 1024,
                "sd": sqrt(501/ZZ(1024)),
                "q": 2**16 + 1,
                "secret_distribution": ((-1,1), 501),
                "m": 1024,
                "norm_f": sqrt(250 + 251),
                "norm_g": sqrt(250 + 251),
                "claimed": 149,
                "category": [
                    1,
                    2,
                    3,
                    4,
                    5,
                ],
                "ring": "x^n - 1",
            }
        ],
        "assumption": [
            "NTRU",
        ],
        "primitive": [
            "DSA",
        ],
    },
]
