# -*- coding: utf-8 -*-
"""
Security cross-estimation for lattice based schemes proposed to NIST against the primal and dual attacks.
This script assumes that the LWE estimator commit 9302d42 is present in a subdirectory `estimator`.

NOTATION:

    LWE
    n       lwe secret dimension
    k       mlwe rank
    q       lwe modulo
    sd      lwe secret standard deviation (if normal form)
    m       number of lwe samples

AUTHOR:

    Rachel Player - 2017, 2018
    Fernando Virdia - 2017, 2018
    Thomas Wunderer - 2018

"""


from sage.all import *
import estimator as est
from schemes import LWE_SCHEMES, NTRU_SCHEMES
from cost_asymptotics import BKZ_COST_ASYMPTOTICS
from html import generate_json
from inspect import getsource
try:
    from config import NCPUS
except ImportError:
    NCPUS = 2
try:
    from config import SOBJPATH
except ImportError:
    SOBJPATH = "all_the_schemes.sobj"


def flatten(l):
    """ Flattens a list of lists into a list containing the elements of each
        sublist.

    :params l:      list of lists

    :return:        flattened list
    """
    return [item for sublist in l for item in sublist]


@parallel(ncpus=NCPUS)
def para_cost_scheme(scheme):
    """ Utility function for running LWE costing in parallel.

    :param scheme:      list containing an LWE scheme object
    """
    return cost_scheme(scheme[0])


def cost_scheme(scheme, debug=False):
    """ Costs LWE scheme by calling the [APS15] estimator.
        Costing is done against primal and dual attacks, and considers the distribution
        of the secret vector to apply scaling and dropping of columns.

        :params scheme:         LWE scheme object
        :params debug:          Boolean value, if set to True, catched exceptions are re-raised.

        :returns estimates:     list of estimated costs for the primal and dual attack
    """
    sname = scheme["name"]
    params = scheme["params"]

    # verbose output
    print "Costing lwe scheme: %s"%(sname)

    # loop parametrisations
    estimates = []
    for param in params:
        # cast everything to python type so we can json.dump it
        n = param["n"]
        sd = param["sd"]
        q = param["q"]
        secret_distribution = param["secret_distribution"]
        alpha = sqrt(2*pi) * sd / RR(q)
        key = "%s-%04d-%.2f-%d"%(sname,n,sd,q)
        primal_estimate = {
            "attack": "primal",
            "key": key,
            "scheme": {
                "name": sname,
                "primitive": scheme["primitive"],
                "assumption": scheme["assumption"],
            },
            "param": param,
            "cost": {},
        }
        dual_estimate = {
            "attack": "dual",
            "key": key,
            "scheme": {
                "name": sname,
                "primitive": scheme["primitive"],
                "assumption": scheme["assumption"],
            },
            "param": param,
            "cost": {},
        }

        is_ntru = "NTRU" in scheme["assumption"]
        samples = [n] if is_ntru else [n, 2*n]

        try:
            # loop cost models
            for cost_model in BKZ_COST_ASYMPTOTICS:
                cname = cost_model["name"]
                reduction_cost_model = cost_model["reduction_cost_model"]
                success_probability = cost_model["success_probability"]
                primal_results = {"n": {}, "2n": {}}
                if not is_ntru:
                    dual_results = {"n": {}, "2n": {}}

                for m in samples:
                    dropped = False
                    # Estimate standard attacks. The estimator will apply any possible scaling
                    cost_primal = est.primal_usvp(n, alpha, q, secret_distribution=secret_distribution,
                                                    m=m,  success_probability=success_probability,
                                                    reduction_cost_model=reduction_cost_model)
                    if not is_ntru:
                        cost_dual = est.dual_scale(n, alpha, q, secret_distribution=secret_distribution,
                                                        m=m, success_probability=success_probability,
                                                        reduction_cost_model=reduction_cost_model)

                    if est.SDis.is_bounded_uniform(secret_distribution):
                        a, b = est.SDis.bounds(secret_distribution)
                        if -a == b:
                            # Try guessing secret entries via drop_and_solve
                            primald = est.partial(est.drop_and_solve, est.primal_usvp, postprocess=False, decision=False)
                            cost_primal_dropped = primald(n, alpha, q, secret_distribution=secret_distribution,
                                                    m=m,  success_probability=success_probability,
                                                    reduction_cost_model=reduction_cost_model, rotations=is_ntru)
                            if not is_ntru:
                                duald = est.partial(est.drop_and_solve, est.dual_scale, postprocess=True)
                                cost_dual_dropped = duald(n, alpha, q, secret_distribution=secret_distribution,
                                                        m=m,  success_probability=success_probability,
                                                        reduction_cost_model=reduction_cost_model)

                            # Sometimes drop_and_solve results in a more costly attack
                            if cost_primal_dropped["rop"] < cost_primal["rop"]:
                                cost_primal = cost_primal_dropped
                                dropped = True
                            if not is_ntru:
                                if cost_dual_dropped["rop"] < cost_dual["rop"]:
                                    cost_dual = cost_dual_dropped
                                    dropped = True

                    # save results
                    primal_results["n" if m == n else "2n"] = {
                        "name": cname,
                        "dim":  int(cost_primal["d"]),
                        "beta": int(cost_primal["beta"]),
                        "rop":  int(ceil(log(cost_primal["rop"], 2))),
                        "drop": dropped,
                    }
                    if not is_ntru:
                        dual_results["n" if m == n else "2n"] = {
                            "name": cname,
                            "dim": int(cost_dual["d"]),
                            "beta": int(cost_dual["beta"]),
                            "rop": int(ceil(log(cost_dual["rop"], 2))),
                            "drop": dropped,
                        }

                primal_estimate["cost"][cname] = primal_results
                if not is_ntru:
                    dual_estimate["cost"][cname] = dual_results

        except Exception, e:
            primal_estimate["error"] = str(e)
            if not is_ntru:
                dual_estimate["error"] = str(e)
            if debug:
                raise

        estimates += [primal_estimate]
        if not is_ntru:
            estimates += [dual_estimate]
    return estimates


def main():
    """ Main function costing LWE and NTRU schemes.
        Runs each scheme costing in parallel.
        Results are saved as a Sage object and as an HTML table.

    :return estimates_list:     list containing scheme costs
    """

    lwe_estimates = list(para_cost_scheme([[s] for s in LWE_SCHEMES + NTRU_SCHEMES]))
    estimates_list = flatten([x[1] for x in lwe_estimates])

    # save estimates as sage object
    save(estimates_list, SOBJPATH)

    try:
        print "Generating html"
        generate_json(estimates_list)

    except Exception, e:
        print "Error generating html:", e

    print "Done."
    return estimates_list


def debug_call():
    """ Debug call to a single costing.
        It avoids the automatic exception handling done by @parallel.

    """
    cost_scheme(LWE_SCHEMES[0], debug=True)


""" Run main is executed as a script.
    Don't if attached/loaded/imported into sage/python.
"""
import __main__
if __name__ == "__main__" and hasattr(__main__, '__file__'):
    main()
    # debug_call()
