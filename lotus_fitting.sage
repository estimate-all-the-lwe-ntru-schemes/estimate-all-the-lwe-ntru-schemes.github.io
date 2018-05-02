# -*- coding: utf-8 -*-
"""

Curve fitting for LOTUS enumeration cost lower bound.

AUTHOR:

    Martin Albrecht - 2017
    Fernando Virdia - 2017, 2018
    
"""


# Volume of n-ball of radius 1
Vn = lambda n: pi**(ZZ(n)/2) / gamma(ZZ(n)/2+1)


def delta_0RR(k):
    """
        Returns root Hermite factor corresponding to block size [PhD:Chen13].

        .. [PhD:Chen13] Yuanmi Chen. Réduction de réseau et sécurité concrète du chiffrement
                        complètement homomorphe. PhD thesis, Paris 7, 2013.
    """
    k = RR(k)
    return RR((k/(2*pi*e) * (pi*k)**(1/k)))**(1/(2*(k-1)))


def LowerBoundCostLR(d, beta):
  """
      Returns the lower bound cost of lattice reduction for a lattice of dimension d using BKZ-beta. 
      By [PhD:Chen13] we recover the root Hermite factor for BKZ-beta, and then use the LOTUS lower
      bound for lattice reduction in dimension d and blocksize beta provided in equation (39) of [PHAM17]
      
      .. [PHAM17] Le  Trieu  Phong,  Takuya  Hayashi,  Yoshinori  Aono,  and  Shiho  Moriai.
      Lotus. Technical   report,   National   Institute   of   Standards and Technology, 2017.
      Available at https://csrc.nist.gov/projects/post-quantum-cryptography/round-1-submissions
  """
  delta = delta_0RR(beta)
  r = delta**(-4)
  return log(sum([r**(ZZ(k*(k-1))/4) * (pi**(-ZZ(k)/2)) * gamma(ZZ(k)/2) for k in range(1,d+1)])/ZZ(2),2).n()


def fitting():
  """
      Fit LowerBoundCostLR to a superexponential curve, as estimated for enumeration in [MW14].
      We attempt fitting up to different maximum dimensions to see the role played by the lattice dimension in the formula.

      .. [MW14] Micciancio, D., & Walter, M. (2014). Fast lattice point enumeration with minimal overhead.
  """

  # Using Bai and Galbraith's embedding and m = 2n samples,
  # one can construct lattices up to dim = 3n+1.
  # Max suggested n = 2062 (largest secret dimension in any NIST submission).
  l = {
    512: [],
    1024: [],
    2048: [],
    4096: [],
    6144: [],
  }

  for d in l:
      print "Computing data points up to dimension d: %04d"%d
      for beta in range(200, d, d/128):
          l[d].append((beta, LowerBoundCostLR(d, beta)))
  
  # setting up target curve
  c_1 = var('c_1', domain=RR)
  c_2 = var('c_2', domain=RR)
  c_3 = var('c_3', domain=RR)
  beta = var('beta', domain=RR)
  f = (c_1 * beta * log(beta, 2) + c_2*beta + c_3).function(beta)
  
  g = {}
  g["err"] = {}
  for d in l:
      g[d] = f.subs(find_fit(l[d], f, solution_dict=True))
      print "Fitted up to dimension %04d,"%d, g[d]
      g["err"][d] = [g[d](beta).n() - LowerBoundCostLR(d, beta) for beta in range(200,d)]
      max_err = max(map(abs, g["err"][d]))
      # max_err = max([abs(g[d](beta).n() - LowerBoundCostLR(d, beta)) for beta in [randint(200, d-1) for _ in range(200)]])
      print "Maximum log(error, 2): %f"%max_err
      # save(line(l[d]) + plot(g[d], 32, 1024, color="green"), "%d.png"%d)
  return g

""" 
Fitted up to dimension 0512, beta |--> -0.7601224342099866*beta + 0.12521943782285255*beta*log(beta)/log(2) + 2.5487390055186947
Maximum log(error, 2): 0.005164
Fitted up to dimension 1024, beta |--> -0.7566544389660474*beta + 0.1248726464590878*beta*log(beta)/log(2) + 2.3687074485590855
Maximum log(error, 2): 0.021761
Fitted up to dimension 2048, beta |--> -0.7550818937366788*beta + 0.12472525302110621*beta*log(beta)/log(2) + 2.254440896969337
Maximum log(error, 2): 0.046849
Fitted up to dimension 4096, beta |--> -0.7546002441518237*beta + 0.12468297258587618*beta*log(beta)/log(2) + 2.2042522365474535
Maximum log(error, 2): 0.065345
Fitted up to dimension 6144, beta |--> -0.7546116067361968*beta + 0.12468382131688087*beta*log(beta)/log(2) + 2.207675310818326
Maximum log(error, 2): 0.062897

We pick the one fitted to up to blocksize 2048.
""""
